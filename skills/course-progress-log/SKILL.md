---
name: course-progress-log
description: "Use when the user pastes screenshots or page text of an online course's lesson list (LinkedIn Learning, freeCodeCamp or similar) and wants a progress log, or sends new ones to update one: chapters, episodes or steps, durations, totals, done ticks."
---

# Course progress log

One simple markdown file per course: chapters, episodes with durations, a Done tick per episode, totals per chapter and for the course. The script does all time arithmetic; never sum durations by hand.

## Steps

1. **Ask first, short and non-technical:** which chapters are missing from the screenshots (introduction, first lessons), where the file goes (default: the current working directory, `<course-slug>.md`), and the course URL if the user did not give it. If the user says not to ask, use those defaults and list what is missing. Duplicate screenshots count once. A screenshot cut off at the bottom may hide more episodes: say so in the report instead of guessing.
2. **Read every screenshot.** Say so if any text or time is unreadable; never guess a duration.
3. **Mark Done only from a green tick.** A half-filled circle, empty circle or highlighted "current" row is `false`. Say which rows you judged this way.
4. **Write `spec.json` in the scratchpad**, then run `python <skill folder>/scripts/build_log.py build spec.json <out>.md` using absolute paths. `done` is a JSON boolean; chapters are written with their names, in screenshot order.
5. **Check before reporting:** episode count equals the number of rows you read, every chapter you saw is present, and each tick matches the screenshots chapter by chapter. Report the course total, done time and remaining time from the totals line the script prints.

## Updating a log

New screenshots: edit the `[x]`/`[ ]` cells (or add rows) in the existing `.md`, then run `python <skill folder>/scripts/build_log.py recalc <file>.md` with absolute paths. It rewrites every chapter `Total | Done` line and the course totals, so never edit those by hand. Change only rows the screenshot shows differently; chapters not in it stay as they are. The file is the only source of truth; no JSON is kept.

## Steps mode (platforms that count steps, not minutes, such as freeCodeCamp)

Use it when the platform shows "N of M steps complete" and no durations. Never invent times. Add `"unit": "steps"` to the spec; each item has `type` (Theory, Workshop, Lab, Review, Quiz, Certification Project), `steps` and `passed` instead of `time` and `done`. Pasted page text beats screenshots here: it lists every step as Passed or Not Passed.

- **Counting rule:** a theory block counts one step per question listed, a workshop one per numbered step, a lab, review, quiz or certification project one. Confirm this by summing each chapter against the platform's own "M steps" figure before writing; if a chapter does not match, stop and ask.
- **Items outside the chapter counts** (certification projects between chapters, a final review) go in one last chapter. A non-counted exam goes in spec `notes`, printed as `Not counted in steps: ...`.
- **Done is derived** from `passed == steps`. To update, edit the Passed cell only, then run `recalc`; it rewrites ticks and totals. Partial progress is fine (`7` of `21`): the `Done` totals count every passed step, ticked or not, while a row is ticked only when all its steps are passed.
- Same `build` and `recalc` commands, same file placement. Totals line reads `Course total: N steps | Done: D | Remaining: R`.

## Video series and documentaries (no lesson list)

A multi-part video with no chapters can use the same file. Set `platform` (for example `YouTube`), make each part a chapter and cut each part into viewing segments of about 30 minutes named by their range (`0:30:00 to 1:00:00`), so partial progress shows. Take lengths from the platform, never by guess; tick a segment only when he says he watched that range. A range he gives ("watching 53:22 to the end") is a segment boundary: cut there and leave it unticked until he says it is finished. Plan it with `study-plan` like any course.

## Output shape (fixed)

Steps mode swaps the table for `| Done | Item | Type | Passed | Steps |` and the `Total | Done` lines count steps; everything else below holds. Title line; `Platform: URL` line (spec `platform` defaults to `LinkedIn Learning`); legend line; one bold totals line; then per chapter a `##` heading, a `Total | Done` line and a `| Done | Episode | Time |` table. Do not add columns, emoji or commentary.

## Spec shape

```json
{"title": "Course Name by Publisher", "url": "https://...",
 "chapters": [{"name": "Lesson 1: Basics",
   "episodes": [{"name": "Learning objectives", "time": "36s", "done": true}]}]}
```

Times exactly as shown on screen (`1h 5m 10s`, `3m 13s`, `39s`, `1m`). Keep episode names verbatim, including apostrophes.

## Common mistakes

- Off-by-one when setting `done` by chapter index (Introduction is index 0, so Lesson N is index N). Tick per episode from the screenshot instead.
- Counting a duplicated screenshot twice.
- Treating the lesson the user is on now as done.
