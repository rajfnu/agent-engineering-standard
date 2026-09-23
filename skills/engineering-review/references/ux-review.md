# UX review

Run this only when the change touches user-facing frontend. Work top-down and stop when
the change's scope is covered — a CSS-token change does not need a journey review, but it
does need the accessibility floor.

## 1. Journey

- Can the user complete the job the change is part of, start to finish?
- Is there a step that exists only because the implementation is shaped that way?
- What happens on failure mid-flow — is entered work preserved?
- Is there a way back, and does back restore state?

## 2. Information architecture and navigation

- Is everything on this screen needed *here*, or is it here because it was easy to add?
- Does the user know where they are and how they got here?
- Is the primary action singular and obvious?

## 3. Content

- Does the wording match the words the user uses, or the words the database uses?
- Is terminology consistent with the rest of the product?
- Do error messages say what happened, whose fault it is, and what to do next?

## 4. States

Every async surface needs all four. Missing states are the most common real defect in
frontend diffs.

| State | Check |
|---|---|
| Loading | skeleton over spinner where layout is known; no layout shift |
| Empty | explains what this is, why it is empty, and the one action to fill it |
| Error | actionable, specific, recoverable; retry where retry makes sense |
| Partial/stale | is stale data labelled, or silently presented as current |

## 5. Accessibility floor

Non-negotiable, and cheap in-flight:

- every interactive element reachable and operable by keyboard;
- visible focus, in a sensible order; no focus traps;
- accessible names on icon-only controls;
- labels tied to form controls; errors associated with their field;
- text contrast ≥ 4.5:1, large text and UI boundaries ≥ 3:1;
- meaningful heading order; landmarks present;
- async status announced via a live region;
- `prefers-reduced-motion` respected.

## 6. Frontend code quality

- Is a page/route component doing fetching, state, formatting, and markup at once?
- Are business rules living in components instead of the domain?
- Is the same fetch-and-map duplicated across components instead of one hook/service?
- Do components consume the API response shape verbatim, so a backend rename breaks
  rendering? Map to a view model at the boundary.
- Are component props honest and bounded, or a 20-field bag?

## 7. Visuals — last

Spacing rhythm, hierarchy, alignment, consistent design tokens rather than one-off values,
dark mode if the product has it, and behaviour at the narrowest supported viewport.

For substantial visual design work, delegate to a dedicated design skill (see the
standard's `docs/integrations.md`) rather than improvising a design system in a review.
