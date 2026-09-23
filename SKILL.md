---
name: sticky-ruling
description: Post a decision the user must make (A/B, pick-one, approve/skip) as an always-on-top window that keeps the full context on screen while you keep working. Use when the user or CLAUDE.md asks for sticky rulings, or says "sticky ruling". Replaces AskUserQuestion, which freezes the session.
---

# Sticky ruling

Chat-text options scroll away under agent and bash output, and AskUserQuestion blocks the whole session until answered. A sticky ruling does neither: a small topmost window holds the full question while you keep working. The window never takes keyboard focus, so it can't disrupt typing or dictation.

## Post a ruling

Bash tool, `run_in_background: true`:

```
python "~/.claude/skills/sticky-ruling/ruling.py" "Item 12 of 35" "<question + all the context needed to decide>" "A: <option + trade-off>" "B: <option + trade-off>"
```

- The window alone must carry everything needed to decide. Assume the chat has scrolled away.
- Put a short unique label first ("Item 12 of 35"). The user refers to rulings by it.
- Note the background task ID next to the label.

## Keep working

Continue with everything that doesn't depend on the ruling. Never idle waiting, never ask "still awaiting your ruling".

## Receive the answer, either way

- **Clicked in the window:** the background task finishes with `RULING <label>: <answer>` and you are notified, even if idle.
- **Typed in the terminal** ("ruling 12: B"): act on it, then stop that ruling's background task (TaskStop with its ID) so the window closes.

Answers clicked in the window are logged to `~/.claude/rulings/rulings.log`.

## Notes

- Several open rulings stack as separate windows.
- The window's X only minimizes it. A ruling never disappears unanswered.
- Windows only (tkinter + user32). Self-test: `python selftest.py`.
