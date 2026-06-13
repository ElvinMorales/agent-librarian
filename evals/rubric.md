# MVP Evaluation Rubric

## Classification

- Common filenames map to a generic artifact class and stable taxonomy bucket.
- Protocol or framework information appears only as an optional hint.

## Extraction

- Frontmatter and supported headings populate normalized entry fields.
- Missing metadata remains visible rather than being invented.

## Warnings

- Incomplete fixtures receive the expected discoverability warnings.
- Possible disclosure indicators require human review.

## Overlap

- The two synthetic summary skills produce an overlap candidate.
- Every candidate requires human review and no source files are changed.

## Safety

- Scanned content is never executed.
- No external service is called.
- Generated files are written only under the selected output directory.
