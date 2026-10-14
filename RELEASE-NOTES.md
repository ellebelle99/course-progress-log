# Release notes

## v1.1.0 (14-10-2026)

Steps mode for platforms that count steps, not minutes (freeCodeCamp and similar).

- A steps log lists each block with its type, steps passed and total steps; totals and ticks are derived from the Passed cells
- Partial progress inside a block is kept (7 of 21 steps)
- Accepts pasted page text as well as screenshots
- Time mode is unchanged: existing logs recalculate byte for byte

## v1.0.0 (14-10-2026)

First public release.

- Builds a course progress log from lesson-list screenshots: chapters, episodes, durations, done ticks, totals
- Updates an existing log from new screenshots and recalculates every total
- Install with `npx skills add ellebelle99/course-progress-log -g`
