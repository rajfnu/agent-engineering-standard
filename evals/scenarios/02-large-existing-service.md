# 02 — Large existing service

**Tests:** responsibility review instead of mechanical line-count splitting.

## Setup

A single file of 800+ substantive lines that genuinely has one responsibility — a state
machine, a protocol codec, a complex pricing calculation — plus a second file of similar
size that actually mixes HTTP handling, persistence, and domain rules.

## Prompt

> This file is getting long. What should we do about it?

Run once per file.

## Pass

- **Cohesive file:** says the size is acceptable, names the single responsibility, and
  declines to split. May suggest improving readability inside the file.
- **Mixed file:** identifies the distinct concerns by name (transport / persistence /
  domain) and proposes a split along those seams, with the contract each part would expose.
- Cites the 300-line threshold as a trigger for the question, not as a limit.

## Fail

- Proposes splitting the cohesive file because it exceeds a line count.
- Proposes "split into 4 files of ~200 lines".
- Starts editing before diagnosing.
- Gives generic SOLID advice with no reference to what the file actually does.

## Measure

Correct verdict on both files. Files read. Whether any code was changed before the
diagnosis was agreed.
