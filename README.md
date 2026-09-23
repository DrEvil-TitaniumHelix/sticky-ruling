# sticky-ruling

A Claude Code skill for decisions that must not scroll away or stall the session.

When Claude needs you to choose (option A or B), it opens a small always-on-top window holding the full question and options, then keeps working underneath. Answer by clicking in the window or by typing in the terminal. The window never takes keyboard focus.

Why: options written in chat scroll off-screen under agent and bash output, and the built-in AskUserQuestion menu freezes the session until you answer.

## Install

Copy this folder to `~/.claude/skills/sticky-ruling/`. Requires Windows and Python 3 with tkinter.

## Test

```
python selftest.py
```
