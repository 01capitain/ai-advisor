#!/usr/bin/env python3
"""Stop hook: deterministically remind Claude (quietly, via systemMessage) that
the board `save` capability exists, so the offer to persist a conversation is
never forgotten at wind-down.

- Loop-safe: exits immediately when stop_hook_active is set.
- Repo-gated: only fires when ./conversations/ exists (the opt-in marker).
- Non-blocking: always exits 0; systemMessage is Claude-facing, not user spam.
"""
import sys, json, os

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("stop_hook_active"):
        return 0
    cwd = data.get("cwd") or os.getcwd()
    if not os.path.isdir(os.path.join(cwd, "conversations")):
        return 0
    msg = ("Advisory board: this repo persists board conversations. If a board "
           "consultation happened this session and has not yet been saved, offer "
           "the user `/ai-advisory-board save` before wrapping up. Do not repeat "
           "the offer if it was already declined or the conversation is already saved.")
    print(json.dumps({"systemMessage": msg}))
    return 0

if __name__ == "__main__":
    sys.exit(main())
