# Hardening the Logic bank — audit of the 36 unproven questions

> Historical record, kept because its findings still hold. The question counts
> here (89, 87, 53 provable) are the Logic-only bank as it stood on 2026-10-02,
> before Mathematics was added. The bank is now 168 questions, of which 132 are
> machine-provable; the 36 `editorial` ones discussed below are unchanged and
> still await a teacher's reading. The test count has since grown from 25 to 39.

Date: 2026-10-02. Scope: the questions whose answers carry **no machine proof**
(`validation.method == "editorial"`) — 12 `arguments`, 12 `relationships`,
12 `verbal`, four skills × three each, all auto-approved by the demo seed.

## 1. Headline

**Every one of the 36 answer keys was correct.** I worked through each question
independently and reached the keyed answer every time. No student would have
been marked wrong for a right answer.

**But six defect classes were found in the surrounding material** — stems,
distractors, explanations and error tags. These matter: a student who reads an
explanation that misstates the premises, or meets an option about a person who
does not exist in the question, loses trust in the whole set.

## 2. Defects found, with root causes

| # | Defect | Affected | Root cause |
|---|---|---|---|
| 1 | Options named a person who never appears in the stem ("Rithy must be an inspector" in a question about Dara) | 3 (`necessary-condition`) | One `wrong` list shared by three depths in `generator.py`; depth 1 introduces only one name but inherited distractors naming a second |
| 2 | Options relied on premises the stem never introduced — "permit", "inspector" | 6 (`necessary-condition`, `must-be-true`) | Same shared list. Depth 1 has no inspectors and no permits; depth 2 has inspectors but no permits |
| 3 | A rationale asserted "The premises explicitly allow trained inspectors" in a question with no inspectors | 3 | Same shared list |
| 4 | Stem named **two different machines**, and the worked explanation ("Training and a permit are both necessary") was **false** | 2 (`multi-condition-judgment`) | `stem.replace('the cutter', ...)` did not match "Every **cutter operator** also has a permit", so only part of the stem was substituted |
| 5 | "a ammeter", "a anemometer", "A anemometer measures air speed" | up to 4 templates | Hard-coded `a` article in four places |
| 6 | Every analogy distractor tagged `reversed-relationship` when it is a wrong-quantity choice | 3 questions, 9–12 options | Single hard-coded tag. This corrupts the "Patterns to revisit" analytics, which aggregate by tag — it would report a misconception students did not have |

A seventh, milder item: the classification stem asked "Which **item** belongs to
the same category…" while every option is a **category**.

## 3. What was changed

All fixes are in `backend/app/generator.py`, at the template level, so the
defects cannot reappear on regeneration:

- Added an `article()` helper; applied at the four sites that hard-coded `a`.
- Split the shared `verbal` distractor list into **three depth-specific lists**,
  so an option may only rely on premises its own stem introduces. Depth 1 now
  draws on training/operator only; depth 2 adds inspectors; depth 3 adds permits.
- Substituted the machine name consistently (`'cutter' → equipment`), so a stem
  names one machine and the depth-3 explanation is true.
- Retagged analogy distractors `reversed-relationship` → `wrong-quantity`.
- Reworded the classification stem to "Which category do X and Y both belong to?"

## 4. Verification

- **Generator sweep:** 320 freshly generated questions (both domains, all four
  levels, 4- and 5-option), checked for every defect class above —
  **0 problems**.
- **Live bank repaired:** all 36 rows regenerated in place with the fixed
  templates. Ids preserved so attempts, audit rows and exports stay intact;
  version bumped; each repair recorded in the audit trail as `template_repair`.
- **Re-audit of all 89 questions:** **0 defects.**
- **Answer re-verification:** 89/89 pass, 0 recomputation failures, 0
  disagreements with stored validation.
- `pytest -q` **25 passed**; Playwright **6 passed** (the textbook test now runs
  rather than skipping, since the checked selection is imported).

## 5. What is still open — read this part

**The 36 are still `editorial`.** Their wording is now sound, but that is a
quality improvement, **not** a proof. The split is unchanged: 53 machine-provable,
36 resting on authored reasoning. Hardening did not make them verifiable.

**Near-duplicate questions, deliberately not changed.** Five stems are each
shared by two approved questions — 10 of 87:

```
x2  Which category do an ammeter and an anemometer both belong to?
x2  Complete the functional analogy: balance is to mass as clock is to _____.
x2  For this exercise, preventive maintenance of a cutter means ...
x2  In a fictional workshop, every person operating the lathe ...
x2  At a fictional Battambang repair center, output increased ...
```

The seed signature is `(stem, option count)`, so the same stem seeds twice — once
with 4 options, once with 5. A 14-question mock exam draws by question id, which
does not stop both twins appearing in one paper. Three ways to fix it:

1. **De-duplicate by stem when assembling a practice set or exam** (recommended —
   fixes the student-facing symptom whatever the bank contains).
2. Make the seed signature stem-only (simple, but shrinks the bank below 84).
3. Add template variety so collisions are rarer (largest change).

I did not implement any of them: all three touch exam assembly or bank size,
which affects the capacity guarantees and the counts verified against the
reference preview. It is your call.

## 6. Recommended next step

Nine of the 36 — `necessary-condition`, `must-be-true` and
`multi-condition-judgment` — are **formal conditional logic**: universal
conditionals plus a fact about one person, asking what must follow. That is
mechanically checkable the same way the `ordering` family already is, by
enumerating the models consistent with the premises and confirming exactly one
option holds in all of them.

Building that validator would move **9 questions from "trust the author" to
"proved"**, and every future question in those families with it — which is the
direct answer to not having time to review. The remaining 27 (analogy,
classification, essential-part, and the four argument skills) rest on meaning,
not form, and will always need a teacher's eye.
