# course-progress-log

Turns screenshots of an online course's lesson list into one markdown progress log.

You see every chapter, episode, duration, done tick and total at a glance, and can update it with a new screenshot.

Claude reads the screenshots, builds a spec and runs a bundled script, so all time sums are exact.


## Why this skill

Course platforms show progress per lesson, never for the whole course.

A fixed output shape keeps every course log comparable.

The script, not the model, does the arithmetic.


## Install

    npx skills add ellebelle99/course-progress-log -g

The `-g` installs it for every project.

Installing this way lets `npx skills update` keep the skill current for you.

No Node? Copy `skills/course-progress-log/` into `.claude/skills/`.
Copied skills are not tracked, so `npx skills update` will not update them.


## Requirements

- Python 3 (runs the bundled script).


## Use

Paste screenshots of the course's lesson list and ask for a progress log.

Claude asks which chapters are missing and where the file goes, then writes `<course-slug>.md`.

Paste new screenshots later to update the ticks and totals.


## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

A sample log is in [examples/example-log.md](examples/example-log.md).



If you like the skill, a star is appreciated.

Watching the repo is an easy way to keep an eye on changes.


## License

MIT, see [LICENSE](LICENSE).
