#!/usr/bin/env python3
"""Idempotently insert a `## Position` section (real-world credential) into each
advisor .md file, placed just before `## Short bio`. Safe to re-run."""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ADVISORS = os.path.normpath(os.path.join(HERE, "..", "references", "advisors"))

POSITIONS = {
    "dana-perino": "Former White House Press Secretary; co-host of *The Five* and *America's Newsroom* on Fox News.",
    "laszlo-bock": "Former SVP of People Operations at Google; co-founder and CEO of Humu.",
    "marty-cagan": "Founder and partner of Silicon Valley Product Group; author of *Inspired*, *Empowered*, and *Transformed*.",
    "mark-cuban": "Entrepreneur and investor; former majority owner of the Dallas Mavericks; founder of Cost Plus Drugs.",
    "horst-schulze": "Co-founder and former President & COO of The Ritz-Carlton Hotel Company; founder of the Capella Hotel Group.",
    "dj-patil": "Former U.S. Chief Data Scientist (White House OSTP); former Head of Data Products at LinkedIn.",
    "steve-jobs": "Co-founder and former CEO of Apple; founder of NeXT and chairman of Pixar.",
    "martin-fowler": "Chief Scientist at Thoughtworks; author of *Refactoring* and *Patterns of Enterprise Application Architecture*.",
    "eric-evans": "Author of *Domain-Driven Design*; founder of Domain Language, Inc.",
    "indra-nooyi": "Former Chairman and CEO of PepsiCo.",
    "lebron-james": "NBA player for the Los Angeles Lakers; founder of the LeBron James Family Foundation and the SpringHill Company.",
    "whitney-wolfe-herd": "Founder and former CEO of Bumble; co-founder of Tinder.",
    "reid-hoffman": "Co-founder of LinkedIn; partner at Greylock; co-founder of Inflection AI.",
}

def main():
    changed, skipped, missing = [], [], []
    for slug, pos in POSITIONS.items():
        path = os.path.join(ADVISORS, f"{slug}.md")
        if not os.path.exists(path):
            missing.append(slug); continue
        text = open(path, encoding="utf-8").read()
        if re.search(r"^## Position\b", text, re.M):
            skipped.append(slug); continue
        block = f"## Position\n\n{pos}\n\n"
        if "## Short bio" in text:
            text = text.replace("## Short bio", block + "## Short bio", 1)
        else:  # fallback: append at end
            text = text.rstrip() + "\n\n" + block
        open(path, "w", encoding="utf-8").write(text)
        changed.append(slug)
    print(f"changed: {changed}")
    print(f"skipped (already had Position): {skipped}")
    if missing: print(f"MISSING files: {missing}")

if __name__ == "__main__":
    main()
