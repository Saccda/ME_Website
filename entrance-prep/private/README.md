# Private reference location

Store licensed textbooks outside the public web root, build context, and version control. This directory is ignored except for this note. The app never serves this directory and never loads textbook questions for generation.

## `exam_bank.json`

The examination panel's own 100-question physics bank, read by `backend/tools/import_exam_bank.py`. It belongs here rather than in the repository for a different reason from the textbooks: the GitHub repository is public, and these are the questions the real paper draws on, so committing them would publish the examination. Carry the file to the lab by hand and leave it in this directory. Nothing in the app reads it at runtime — only the import tool does, and only when run deliberately.

The provided reference was recovered from the previous chat's temporary attachment because `/mnt/data/501 Challenging Logic and Reasonig Problems.pdf` does not exist on this Windows host. Keep a durable private copy yourself; temporary chat attachment paths are not a deployment dependency.

The internal reference is LearningExpress, LLC, *501 Challenging Logic and Reasoning Problems*, 2nd edition, copyright 2005, ISBN 1-57685-534-1. Domain mapping follows Introduction, printed page viii (PDF page 8). Generated content is original. The private selection payload contains three explicitly selected excerpts checked before import and excluded from the portable archive. The four-level rubric is locally defined and needs teacher calibration against the actual entrance exam.
