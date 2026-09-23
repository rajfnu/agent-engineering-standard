# UX and frontend quality

Frontend is not disposable glue. A component tree with the same problems you would reject
in backend code — mixed responsibilities, duplicated state, leaked data shapes — is the
same defect, in the layer users actually touch.

## UX is not CSS

Answer these before writing a single style:

1. **Who is the user?** Their expertise, frequency of use, and stakes.
2. **What are they trying to do?** The job, not the screen.
3. **Where are they?** Entry point, device, interruption level, what they already know.
4. **What information do they need here?** Nothing more.
5. **What is the next obvious action?** There should be exactly one primary one.

If you cannot answer these, styling is premature.

## Review order

Work top-down. A beautiful button on the wrong screen is still wrong.

| Layer | Look for |
|---|---|
| Journey | dead ends, unnecessary steps, no way back, lost work on error |
| Information architecture | what belongs on this screen vs. one click away |
| Navigation | where am I, how do I get back, is state preserved |
| Terminology | product language matching user language, consistently |
| Progressive disclosure | defaults that work, advanced options out of the way |
| Forms | inline validation, preserved input on error, sensible tab order, real labels |
| Dialogs | only for genuine interruptions; destructive actions confirmed and reversible |
| Empty states | what this is, why it is empty, the one action to fill it |
| Errors | what happened, whether it is the user's fault, what to do now |
| Loading/progress | skeleton vs. spinner, optimistic updates, no layout shift |
| Accessibility | keyboard path, focus visibility and order, contrast, labels, live regions, motion preference |
| Visual | spacing, hierarchy, alignment, consistent tokens — **last** |

## Frontend code smells

- **Giant components** — a page component holding fetching, state, formatting, and markup.
- **Business logic in pages/routes** — rules that belong in the domain, living in JSX.
- **Duplicated state/API logic** — the same fetch-and-map in five components instead of
  one hook/service.
- **Backend shapes leaking into UI** — components destructuring the API response verbatim,
  so a backend rename breaks rendering. Map at the boundary to a view model.
- **Loading and error as afterthoughts** — only the success path implemented.
- **Inaccessible interactions** — click handlers on `div`s, focus traps, icon-only
  controls with no accessible name.
- **Weak component boundaries** — props objects with 20 fields, or components that reach
  into global state from anywhere.

## Accessibility floor

Not optional, and cheap when done as you go: every interactive element reachable and
operable by keyboard; visible focus; text contrast ≥ 4.5:1 (≥ 3:1 for large text and UI
boundaries); form controls with labels; images with meaningful or empty alt; heading
order that makes sense; live regions for async status; respect `prefers-reduced-motion`.

## Specialists

For deep visual design work, delegate to a dedicated design skill rather than
improvising — see the integrations table in the standard's `docs/integrations.md`.
