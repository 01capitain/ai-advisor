#!/usr/bin/env python3
"""Build the self-contained advisory-board.html presentation layer.

Reads (from the SKILL dir):  advisor .md files, portraits, advisor-style.json
Reads (from the REPO dir):   conversations/*.md
Writes (to the REPO dir):    advisory-board.html

The HTML is a single self-contained file (portraits embedded as base64). Three
views — History / Conversation / Advisors — with hash routing and flip cards.

Usage:
  advisory_build.py [--skill-dir DIR] [--repo DIR] [--conversations DIR] [--out FILE]
"""
import argparse, base64, json, os, re, sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")
try:
    import markdown
except ImportError:
    sys.exit("markdown required: pip install markdown")

def wsl_url(abspath, distro=None):
    """Render a local absolute path as a WSL UNC file URL:
    file://wsl.localhost/<distro><abspath>  (falls back to plain file:// off-WSL)."""
    distro = distro or os.environ.get("WSL_DISTRO_NAME")
    p = abspath.replace(os.sep, "/")
    if distro:
        return f"file://wsl.localhost/{distro}{p}"
    return "file://" + p

_MD = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
def md2html(text: str) -> str:
    _MD.reset()
    return _MD.convert((text or "").strip())

PALETTE = ["#0EA5E9", "#8B5CF6", "#3B82F6", "#EF4444", "#F59E0B", "#06B6D4",
           "#A855F7", "#22C55E", "#F97316", "#10B981", "#EAB308", "#EC4899",
           "#14B8A6", "#6366F1", "#D946EF", "#84CC16"]

# ---------- advisor parsing -------------------------------------------------

def _section(text, heading):
    """Return the body under a `## heading` or `### heading` up to the next
    same-or-higher-level heading."""
    m = re.search(rf"^#{{2,3}}\s+{re.escape(heading)}\s*$", text, re.M)
    if not m:
        return ""
    start = m.end()
    nxt = re.search(r"^#{1,3}\s+", text[start:], re.M)
    end = start + nxt.start() if nxt else len(text)
    return text[start:end].strip()

def _field(text, label):
    m = re.search(rf"^\*\*{re.escape(label)}:\*\*\s*(.+)$", text, re.M)
    return m.group(1).strip() if m else ""

def parse_advisor(path):
    text = open(path, encoding="utf-8").read()
    slug = os.path.splitext(os.path.basename(path))[0]
    ident = _section(text, "Identity")
    questions = []
    q = _section(text, "Signature questions")
    for line in q.splitlines():
        m = re.match(r"^\s*\d+\.\s+(.*)$", line)
        if m:
            questions.append(m.group(1).strip())
    return {
        "slug": slug,
        "name": _field(ident, "Real-life figure") or slug,
        "role": _field(ident, "Advisor role") or "",
        "position": _section(text, "Position"),
        "stance": _section(text, "Default stance"),
        "when": _section(text, "Use this advisor when"),
        "questions": questions,
    }

def load_advisors(skill_dir):
    adv_dir = os.path.join(skill_dir, "references", "advisors")
    port_dir = os.path.join(skill_dir, "assets", "portraits")
    style_path = os.path.join(skill_dir, "assets", "advisor-style.json")
    style = json.load(open(style_path)) if os.path.exists(style_path) else {}

    advisors = []
    for fn in sorted(os.listdir(adv_dir)):
        if not fn.endswith(".md"):
            continue
        advisors.append(parse_advisor(os.path.join(adv_dir, fn)))

    # self-heal accents: assign a deterministic palette color to any advisor
    # missing an entry, and persist it back to advisor-style.json.
    changed = False
    used = {v.get("accent") for v in style.values() if isinstance(v, dict)}
    for i, a in enumerate(advisors):
        entry = style.get(a["slug"])
        if not (isinstance(entry, dict) and entry.get("accent")):
            color = next((c for c in PALETTE[i:] + PALETTE if c not in used), PALETTE[i % len(PALETTE)])
            used.add(color)
            style.setdefault(a["slug"], {})["accent"] = color
            changed = True
            print(f"  + assigned accent {color} to new advisor '{a['slug']}'")
    if changed:
        json.dump(style, open(style_path, "w"), indent=2)
        print(f"  updated {style_path}")

    for a in advisors:
        a["accent"] = style.get(a["slug"], {}).get("accent", "#64748B")
        p = os.path.join(port_dir, f"{a['slug']}.png")
        if os.path.exists(p):
            b = base64.b64encode(open(p, "rb").read()).decode("ascii")
            a["portrait"] = f"data:image/png;base64,{b}"
        else:
            a["portrait"] = ""
        # pre-render long fields to HTML
        a["position_html"] = md2html(a["position"])
        a["stance_html"] = md2html(a["stance"])
        a["when_html"] = md2html(a["when"])
    return advisors

# ---------- conversation parsing -------------------------------------------

def split_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm = yaml.safe_load(text[3:end]) or {}
            return fm, text[end + 4:]
    return {}, text

TURN_RE = re.compile(r"^##\s+Turn\s+(\d+)\s*[—-]\s*(.*?)\s*$", re.M)

def parse_turn_sections(block):
    """Split a turn body into labelled `### ` sections."""
    parts = re.split(r"^###\s+(.*?)\s*$", block, flags=re.M)
    # parts[0] = preamble (ignored); then (label, body) pairs
    out = []
    for i in range(1, len(parts), 2):
        out.append((parts[i].strip(), parts[i + 1].strip()))
    return out

def parse_conversation(path, name_to_slug, slug_to_adv):
    text = open(path, encoding="utf-8").read()
    fm, body = split_frontmatter(text)
    if fm.get("date") is not None:
        fm["date"] = str(fm["date"])
    slug = os.path.splitext(os.path.basename(path))[0]

    matches = list(TURN_RE.finditer(body))
    turns = []
    for idx, m in enumerate(matches):
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        raw_title = m.group(2)
        # optional trailing " · YYYY-MM-DD"
        tdate = fm.get("date", "")
        dm = re.search(r"·\s*(\d{4}-\d{2}-\d{2})\s*$", raw_title)
        if dm:
            tdate = dm.group(1)
            raw_title = raw_title[:dm.start()].rstrip(" ·")
        turn = {"num": int(m.group(1)), "title": raw_title, "date": tdate,
                "user": "", "calibration": "", "briefing": "",
                "advisor_prompt": "", "exec": "", "advisors": []}
        for label, content in parse_turn_sections(body[start:end]):
            low = label.lower()
            if low == "user":
                turn["user"] = md2html(content)
            elif low in ("dana · calibration", "dana: calibration"):
                turn["calibration"] = md2html(content)
            elif low in ("dana · briefing", "dana: briefing"):
                turn["briefing"] = md2html(content)
            elif low in ("dana · advisor prompt", "dana: advisor prompt"):
                turn["advisor_prompt"] = md2html(content)
            elif low in ("dana · executive summary", "dana: executive summary"):
                turn["exec"] = md2html(content)
            elif low.startswith("advisor · ") or low.startswith("advisor: "):
                aname = label.split("·", 1)[-1].split(":", 1)[-1].strip()
                aslug = name_to_slug.get(aname.lower())
                adv = slug_to_adv.get(aslug, {})
                summary, resp_body = "", content
                sm = re.match(r"^\*\*Summary:\*\*\s*(.+?)(?:\n\n|\Z)", content, re.S)
                if sm:
                    summary = sm.group(1).strip()
                    resp_body = content[sm.end():].strip()
                turn["advisors"].append({
                    "name": aname,
                    "slug": aslug or "",
                    "role": adv.get("role", ""),
                    "summary": md2html(summary),
                    "response": md2html(resp_body),
                })
        turns.append(turn)

    last_user_date = turns[-1]["date"] if turns else fm.get("date", "")
    return {
        "slug": slug,
        "title": fm.get("title", slug),
        "date": fm.get("date", ""),
        "last_user_date": last_user_date,
        "session_id": fm.get("session_id", ""),
        "advisors_involved": fm.get("advisors_involved", []),
        "turn_count": len(turns),
        "turns": turns,
    }

def load_conversations(conv_dir, advisors):
    if not os.path.isdir(conv_dir):
        return []
    name_to_slug = {a["name"].lower(): a["slug"] for a in advisors}
    slug_to_adv = {a["slug"]: a for a in advisors}
    convs = []
    for fn in sorted(os.listdir(conv_dir)):
        if fn.endswith(".md"):
            convs.append(parse_conversation(os.path.join(conv_dir, fn),
                                            name_to_slug, slug_to_adv))
    convs.sort(key=lambda c: c["last_user_date"], reverse=True)
    return convs

# ---------- render ----------------------------------------------------------

def render(advisors, conversations):
    data = json.dumps({"advisors": advisors, "conversations": conversations},
                      ensure_ascii=False)
    data = data.replace("</", "<\\/")  # never break the inline <script>
    return HTML_TEMPLATE.replace("/*__DATA__*/", data)

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Advisory Board</title>
<style>
:root{--bg:#071017;--panel:#0d1724;--panel2:#111c2b;--ink:#f1f5f9;--muted:#9aa7bd;--line:rgba(255,255,255,.12);--accent:#0EA5E9;}
*{box-sizing:border-box;}
body{margin:0;min-height:100vh;color:var(--ink);font:16px/1.65 Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
 background:radial-gradient(1100px 600px at 75% -8%,rgba(14,165,233,.14),transparent 55%),linear-gradient(180deg,#071017,#0b1220);}
a{color:inherit;}
.topbar{position:sticky;top:0;z-index:30;backdrop-filter:blur(10px);background:rgba(7,16,23,.82);border-bottom:1px solid var(--line);}
.topbar-inner{max-width:1180px;margin:0 auto;padding:14px 22px;display:flex;align-items:center;gap:20px;flex-wrap:wrap;}
.brand{font-weight:800;letter-spacing:-.02em;font-size:1.05rem;}
.brand span{color:var(--muted);font-weight:600;}
.tabs{display:flex;gap:8px;margin-left:auto;}
.tabs button{border:1px solid var(--line);background:rgba(255,255,255,.05);color:var(--ink);border-radius:999px;padding:8px 16px;cursor:pointer;font-size:.92rem;font-weight:600;transition:.15s;}
.tabs button:hover{background:rgba(255,255,255,.1);}
.tabs button.active{background:var(--accent);border-color:var(--accent);color:#04121b;}
main{max-width:1180px;margin:0 auto;padding:30px 22px 90px;}
.view{display:none;animation:fade .3s ease;}
.view.active{display:block;}
@keyframes fade{from{opacity:0;transform:translateY(6px);}to{opacity:1;transform:none;}}
h1.page{font-size:clamp(1.6rem,4vw,2.6rem);letter-spacing:-.04em;margin:.2em 0 .1em;}
.sub{color:var(--muted);margin:0 0 26px;}

/* history */
.hist-list{display:grid;gap:14px;}
.hist-card{display:flex;gap:18px;align-items:center;border:1px solid var(--line);background:var(--panel);border-radius:16px;padding:18px 20px;cursor:pointer;transition:.18s;}
.hist-card:hover{transform:translateY(-2px);border-color:rgba(255,255,255,.25);box-shadow:0 14px 40px rgba(0,0,0,.4);}
.hist-card .meta{flex:1;}
.hist-card h3{margin:0 0 6px;font-size:1.2rem;letter-spacing:-.02em;}
.hist-card .line{color:var(--muted);font-size:.9rem;}
.hist-avatars{display:flex;}
.hist-avatars img{width:38px;height:38px;border-radius:50%;object-fit:cover;border:2px solid var(--panel);margin-left:-10px;}
.pill{display:inline-block;background:rgba(255,255,255,.08);border:1px solid var(--line);border-radius:999px;padding:2px 10px;font-size:.78rem;color:var(--muted);}

/* conversation */
.conv-head{display:flex;align-items:flex-start;gap:16px;flex-wrap:wrap;margin-bottom:8px;}
.conv-head h1{margin:0;}
.turnav{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0 26px;}
.turnav button{border:1px solid var(--line);background:rgba(255,255,255,.05);color:var(--ink);border-radius:10px;padding:7px 14px;cursor:pointer;font-weight:600;font-size:.9rem;}
.turnav button.active{background:var(--accent);border-color:var(--accent);color:#04121b;}
.turn{display:none;}
.turn.active{display:block;}
.block{border:1px solid var(--line);border-radius:16px;padding:20px 24px;margin:0 0 18px;background:var(--panel);}
.block .label{font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;font-weight:800;margin:0 0 10px;}
.block.user{border-left:4px solid #64748b;}
.block.user .label{color:#94a3b8;}
.block.dana{border-left:4px solid var(--accent);}
.block.dana .label{color:var(--accent);}
.block.prompt{background:var(--panel2);border-style:dashed;}
.block.exec{border-left:4px solid #22c55e;}
.block.exec .label{color:#22c55e;}
.block :is(p,ul,ol,table):first-child{margin-top:0;}
.block :is(p,ul,ol,table):last-child{margin-bottom:0;}
.sectiontitle{font-size:.78rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);font-weight:800;margin:30px 0 14px;border-bottom:1px solid var(--line);padding-bottom:8px;}

/* Dana message row: portrait on the left, collapsible body */
.msg{display:flex;gap:16px;align-items:flex-start;margin:0 0 16px;cursor:pointer;}
.msg .dana-portrait{flex:none;object-fit:cover;border:1px solid color-mix(in srgb,var(--accent) 50%,var(--line));}
.msg .dana-portrait.full{width:132px;height:188px;border-radius:16px;box-shadow:0 12px 36px rgba(0,0,0,.42);}
.msg .dana-portrait.head{width:56px;height:56px;border-radius:50%;}
.msg .bubble{flex:1;border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:16px;padding:16px 22px;background:var(--panel);min-width:0;transition:box-shadow .25s,border-color .25s;}
.msg.prompt .bubble{background:var(--panel2);border-style:dashed;}
.msg .label{font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;font-weight:800;margin:0;color:var(--accent);}
.msg .bubble .full{margin-top:12px;}
.msg .bubble .full :is(p,ul,ol,table,blockquote):first-child{margin-top:0;}
.msg .bubble .full :is(p,ul,ol,table,blockquote):last-child{margin-bottom:0;}
.msg .bubble .sub + .sub{margin-top:18px;border-top:1px solid var(--line);padding-top:14px;}
.msg .bubble .sublabel{display:block;font-size:.66rem;letter-spacing:.14em;text-transform:uppercase;font-weight:800;color:var(--muted);margin:0 0 8px;}
.msg .bubble .more{margin:9px 0 0;font-size:.72rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--accent);opacity:.8;}
.msg:not(.active) .bubble .full{display:none;}
.msg:not(.active):hover .bubble{border-color:color-mix(in srgb,var(--accent) 50%,var(--line));}
.msg.active .bubble{box-shadow:0 12px 40px color-mix(in srgb,var(--accent) 14%,transparent);}
.msg.active .bubble .more{display:none;}

/* advisor in conversation: inactive = profile card only; active = advice + card */
.advisors{display:flex;flex-wrap:wrap;gap:16px;margin:0 0 6px;align-items:flex-start;}
.adv{cursor:pointer;}
.adv .resp{display:none;}
.adv .card{transition:filter .3s;}
.card.static{width:200px;height:300px;flex:0 0 200px;}
.adv:not(.active){width:200px;}
.adv:not(.active) .card{filter:grayscale(.8) brightness(.82) opacity(.7);}
.adv:not(.active):hover .card{filter:grayscale(.25) brightness(.96) opacity(1);}
.adv.active{width:100%;display:flex;gap:22px;align-items:flex-start;}
.adv.active .resp{display:block;flex:1;min-width:0;order:1;border:1px solid color-mix(in srgb,var(--accent) 55%,var(--line));border-left:4px solid var(--accent);border-radius:16px;padding:18px 22px;background:var(--panel);box-shadow:0 12px 40px color-mix(in srgb,var(--accent) 14%,transparent);}
.adv.active .card{order:2;filter:none;}
.adv .resp .who{font-weight:800;letter-spacing:-.01em;margin:0 0 2px;}
.adv .resp .role{font-size:.85rem;font-weight:700;margin:0 0 12px;color:var(--accent);}
.adv .resp .full :is(p,ul,ol):first-child{margin-top:0;}
.adv .resp .full :is(p,ul,ol):last-child{margin-bottom:0;}

/* flip card */
.card{flex:0 0 240px;width:240px;height:360px;perspective:1300px;cursor:pointer;}
.card.gallery{flex:none;}
.card-inner{position:relative;width:100%;height:100%;transform-style:preserve-3d;transition:transform .6s cubic-bezier(.2,.8,.2,1);}
.card.flipped .card-inner{transform:rotateY(180deg);}
.face{position:absolute;inset:0;border-radius:20px;overflow:hidden;backface-visibility:hidden;border:1px solid color-mix(in srgb,var(--cardaccent) 60%,transparent);
 background:linear-gradient(180deg,color-mix(in srgb,var(--cardaccent) 20%,transparent),transparent 46%),rgba(9,15,26,.92);
 box-shadow:0 16px 48px rgba(0,0,0,.45),0 0 30px color-mix(in srgb,var(--cardaccent) 20%,transparent);display:flex;flex-direction:column;}
.face.back{transform:rotateY(180deg);padding:18px;overflow-y:auto;}
.face.front{padding:0;}
.portrait{position:absolute;inset:0;background:#111827;}
.portrait img{width:100%;height:100%;object-fit:cover;display:block;}
.front-copy{position:absolute;left:0;right:0;bottom:0;padding:20px 16px 16px;
 background:linear-gradient(to top,rgba(4,9,16,.97) 6%,rgba(4,9,16,.80) 46%,rgba(4,9,16,0) 100%);}
.eyebrow{margin:0 0 6px;color:var(--cardaccent);text-transform:uppercase;letter-spacing:.13em;font-size:.66rem;font-weight:800;}
.face h2{margin:0;font-size:1.4rem;line-height:1.05;letter-spacing:-.03em;}
.face .crole{margin:8px 0 0;color:var(--cardaccent);font-weight:800;font-size:.92rem;}
.face .cpos{margin:7px 0 0;color:#cbd5e1;font-size:.84rem;line-height:1.4;}
.face.back h2{font-size:1.2rem;}
.face.back .qlabel{margin-top:12px;}
.face.back .stance{color:#dbeafe;font-size:.9rem;line-height:1.5;margin:6px 0 0;}
.face.back ol{margin:6px 0 0;padding-left:18px;display:grid;gap:7px;}
.face.back li{font-size:.85rem;line-height:1.3;font-weight:600;}
/* gallery grid */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:22px;justify-items:center;}
.toolbar{display:flex;gap:10px;margin:0 0 22px;}
.toolbar button{border:1px solid var(--line);background:rgba(255,255,255,.06);color:var(--ink);border-radius:999px;padding:8px 16px;cursor:pointer;font-weight:600;}

.empty{color:var(--muted);text-align:center;padding:60px 0;}
@media(max-width:680px){.adv-row{flex-direction:column;}.card{width:100%;flex-basis:auto;}}
</style>
</head>
<body>
<header class="topbar"><div class="topbar-inner">
  <div class="brand">AI Advisory Board <span>· presentation</span></div>
  <nav class="tabs">
    <button data-go="#/history">History</button>
    <button data-go="#/advisors">Advisors</button>
  </nav>
</div></header>
<main>
  <section id="view-history" class="view"></section>
  <section id="view-conversation" class="view"></section>
  <section id="view-advisors" class="view"></section>
</main>
<script>
const DATA = /*__DATA__*/;
const advBySlug = Object.fromEntries(DATA.advisors.map(a=>[a.slug,a]));
const convBySlug = Object.fromEntries(DATA.conversations.map(c=>[c.slug,c]));
const $ = (s,r=document)=>r.querySelector(s);
const el = (tag,cls,html)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(html!=null)e.innerHTML=html;return e;};
const esc = s => (s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

function frontFaceHTML(adv){
  return `<section class="face front">
      <div class="portrait">${adv.portrait?`<img src="${adv.portrait}" alt="${esc(adv.name)}">`:''}</div>
      <div class="front-copy">
        <h2>${esc(adv.name)}</h2>
        <p class="crole">${esc(adv.role)}</p>
        <div class="cpos">${adv.position_html||''}</div>
      </div>
    </section>`;
}
// flip card — portrait ⇄ background. Used only in the Advisors gallery.
function flipCard(adv){
  const c = el('article','card gallery');
  c.style.setProperty('--cardaccent', adv.accent||'#64748B');
  const qs = (adv.questions||[]).map(q=>`<li>${esc(q)}</li>`).join('');
  c.innerHTML = `<div class="card-inner">
    ${frontFaceHTML(adv)}
    <section class="face back">
      <p class="eyebrow">Default stance</p>
      <h2>${esc(adv.name)}</h2>
      <div class="stance">${adv.stance_html||''}</div>
      <p class="eyebrow qlabel">When to ask</p>
      <div class="stance">${adv.when_html||''}</div>
      ${qs?`<p class="eyebrow qlabel">Signature questions</p><ol>${qs}</ol>`:''}
    </section>
  </div>`;
  c.addEventListener('click',()=>c.classList.toggle('flipped'));
  return c;
}
// static profile card — front only, no flip. Used inside a conversation.
function profileCard(adv){
  const c = el('article','card static');
  c.style.setProperty('--cardaccent', adv.accent||'#64748B');
  c.innerHTML = `<div class="card-inner">${frontFaceHTML(adv)}</div>`;
  return c;
}

function renderHistory(){
  const v = $('#view-history'); v.innerHTML='';
  v.append(el('h1','page','Conversation history'));
  v.append(el('p','sub','Board conversations conducted in the terminal, saved to this repository.'));
  if(!DATA.conversations.length){ v.append(el('div','empty','No saved conversations yet. Run the <code>save</code> command after a board session.')); return; }
  const list = el('div','hist-list');
  for(const c of DATA.conversations){
    const card = el('div','hist-card');
    const avatars = (c.advisors_involved||[]).map(s=>advBySlug[s]).filter(a=>a&&a.portrait)
      .map(a=>`<img src="${a.portrait}" title="${esc(a.name)}" alt="">`).join('');
    card.innerHTML = `<div class="meta">
        <h3>${esc(c.title)}</h3>
        <div class="line"><span class="pill">${c.turn_count} turn${c.turn_count===1?'':'s'}</span> &nbsp; last message ${esc(c.last_user_date||c.date||'')}</div>
      </div>
      <div class="hist-avatars">${avatars}</div>`;
    card.addEventListener('click',()=>location.hash='#/c/'+c.slug);
    list.append(card);
  }
  v.append(list);
}

function renderConversation(slug, turnNo){
  const v = $('#view-conversation'); v.innerHTML='';
  const c = convBySlug[slug];
  if(!c){ v.append(el('div','empty','Conversation not found.')); return; }
  const head = el('div','conv-head');
  head.innerHTML = `<h1 class="page">${esc(c.title)}</h1>`;
  v.append(head);
  v.append(el('p','sub',`Started ${esc(c.date||'')} · ${c.turn_count} turn${c.turn_count===1?'':'s'}`));

  const nav = el('div','turnav');
  c.turns.forEach(t=>{
    const b = el('button',null,`Turn ${t.num}`);
    b.addEventListener('click',()=>location.hash=`#/c/${slug}/t/${t.num}`);
    b.dataset.turn=t.num;
    nav.append(b);
  });
  v.append(nav);

  const dana = advBySlug['dana-perino'];
  // Dana message: collapsible. size = 'full' (calibration/briefing/exec) or 'head' (internal prompt).
  const danaMsg = (cls,label,html,size,active)=>{
    const m = el('div','msg dana '+cls+(active?' active':''));
    if(dana) m.style.setProperty('--accent', dana.accent||'#0EA5E9');
    const img = dana&&dana.portrait ? `<img class="dana-portrait ${size}" src="${dana.portrait}" alt="Dana Perino">` : '';
    m.innerHTML = `${img}<div class="bubble"><p class="label">${esc(label)}</p>`+
      `<div class="full">${html}</div><div class="more">Click to expand ▾</div></div>`;
    m.addEventListener('click', ()=>m.classList.toggle('active'));
    return m;
  };
  for(const t of c.turns){
    const turn = el('div','turn'); turn.id='turn-'+t.num; turn.dataset.turn=t.num;
    if(t.user) turn.append(el('div','block user',`<p class="label">User question</p>${t.user}`));
    if(t.calibration || t.briefing){
      const body = `${t.calibration?`<div class="sub"><span class="sublabel">Calibration</span>${t.calibration}</div>`:''}`+
        `${t.briefing?`<div class="sub"><span class="sublabel">Briefing</span>${t.briefing}</div>`:''}`;
      turn.append(danaMsg('calbrief','Dana · Calibration & Briefing',body,'full',false));
    }
    if(t.advisor_prompt) turn.append(danaMsg('prompt','Dana · Prompt forwarded to advisors',t.advisor_prompt,'head',false));
    if(t.advisors.length){
      turn.append(el('div','sectiontitle','Advisor responses — click a card to expand'));
      const wrap = el('div','advisors');
      for(const a of t.advisors){
        const adv = advBySlug[a.slug];
        const item = el('div','adv');
        item.style.setProperty('--accent', (adv&&adv.accent)||'#0EA5E9');
        const resp = el('div','resp');
        resp.innerHTML = `<p class="who">${esc(a.name)}</p><p class="role">${esc(a.role)}</p>`+
          `<div class="full">${a.response}</div>`;
        if(adv) item.append(profileCard(adv));
        item.append(resp);
        item.addEventListener('click', ()=>item.classList.toggle('active'));
        wrap.append(item);
      }
      turn.append(wrap);
    }
    // Executive summary is the only thing active at the start.
    if(t.exec) turn.append(danaMsg('exec','Dana · Executive summary',t.exec,'full',true));
    v.append(turn);
  }
  // activate the requested turn (default last)
  const turns = c.turns.map(t=>t.num);
  const target = turnNo && turns.includes(+turnNo) ? +turnNo : turns[turns.length-1];
  v.querySelectorAll('.turn').forEach(d=>d.classList.toggle('active', +d.dataset.turn===target));
  nav.querySelectorAll('button').forEach(b=>b.classList.toggle('active', +b.dataset.turn===target));
  window.scrollTo({top:0,behavior:'smooth'});
}

function renderAdvisors(){
  const v = $('#view-advisors'); v.innerHTML='';
  v.append(el('h1','page','The board'));
  v.append(el('p','sub','All available advisors. Click a card to flip between portrait and background.'));
  const tb = el('div','toolbar');
  const front = el('button',null,'Show all portraits');
  const back = el('button',null,'Show all backgrounds');
  tb.append(front,back); v.append(tb);
  const grid = el('div','grid');
  for(const a of DATA.advisors) grid.append(flipCard(a));
  v.append(grid);
  front.addEventListener('click',()=>grid.querySelectorAll('.card').forEach(c=>c.classList.remove('flipped')));
  back.addEventListener('click',()=>grid.querySelectorAll('.card').forEach(c=>c.classList.add('flipped')));
}

function route(){
  const h = location.hash || '#/history';
  const show = id => document.querySelectorAll('.view').forEach(s=>s.classList.toggle('active',s.id===id));
  document.querySelectorAll('.tabs button').forEach(b=>b.classList.toggle('active',b.dataset.go && h.startsWith(b.dataset.go)));
  let m;
  if((m=h.match(/^#\/c\/([^/]+)(?:\/t\/(\d+))?/))){ show('view-conversation'); renderConversation(decodeURIComponent(m[1]), m[2]); }
  else if(h.startsWith('#/advisors')){ show('view-advisors'); renderAdvisors(); }
  else { show('view-history'); renderHistory(); }
}
document.querySelectorAll('.tabs button').forEach(b=>b.addEventListener('click',()=>location.hash=b.dataset.go));
window.addEventListener('hashchange',route);
route();
</script>
</body>
</html>
"""

# ---------- main ------------------------------------------------------------

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    default_skill = os.path.normpath(os.path.join(here, ".."))
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill-dir", default=default_skill)
    ap.add_argument("--repo", default=os.getcwd())
    ap.add_argument("--conversations", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--distro", default=None, help="WSL distro for file:// URL (default: $WSL_DISTRO_NAME)")
    ap.add_argument("--open-slug", default=None, help="conversation slug to deep-link in the printed URL")
    args = ap.parse_args()

    conv_dir = args.conversations or os.path.join(args.repo, "conversations")
    out = args.out or os.path.join(args.repo, "advisory-board.html")

    print(f"skill-dir:     {args.skill_dir}")
    print(f"conversations: {conv_dir}")
    advisors = load_advisors(args.skill_dir)
    print(f"  parsed {len(advisors)} advisors")
    conversations = load_conversations(conv_dir, advisors)
    print(f"  parsed {len(conversations)} conversations")
    html = render(advisors, conversations)
    open(out, "w", encoding="utf-8").write(html)
    print(f"wrote {out} ({os.path.getsize(out)//1024} KB)")

    # printed open link (WSL UNC form), deep-linked to a conversation if possible
    out_abs = os.path.abspath(out)
    anchor = ""
    target = next((c for c in conversations if c["slug"] == args.open_slug), None) \
        if args.open_slug else (conversations[0] if conversations else None)
    if target:
        last = target["turns"][-1]["num"] if target["turns"] else 1
        anchor = f"#/c/{target['slug']}/t/{last}"
    print("open:", wsl_url(out_abs, args.distro) + anchor)

if __name__ == "__main__":
    main()
