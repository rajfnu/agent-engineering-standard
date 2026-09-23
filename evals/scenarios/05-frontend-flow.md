# 05 — Frontend flow

**Tests:** UX reasoning before cosmetic styling.

## Setup

A multi-step form or checkout flow with real problems: no loading state, a generic error
banner, entered data lost on failure, an icon-only submit button, and unremarkable styling.

## Prompt

> Can you improve this signup flow?

## Pass

- Asks or reasons about who the user is and what they are trying to do before touching CSS.
- Identifies the lost-data-on-error problem as the most serious issue.
- Covers loading, empty, and error states.
- Flags the icon-only control's missing accessible name and the keyboard path.
- Addresses visuals last, if at all.

## Fail

- Opens with colours, spacing, or a component library recommendation.
- Rewrites styling without changing any behaviour.
- Ignores accessibility.
- Treats "improve" as "restyle".

## Measure

Order of concerns addressed (journey → states → a11y → visuals). Whether the data-loss bug
was found. Whether any real UX defect was fixed versus only cosmetics changed.
