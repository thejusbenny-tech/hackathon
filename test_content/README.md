# Test Content

## Generate Documents

```bash
cd test_content
pip install reportlab python-pptx
python generate_docs.py
```

Outputs 12 files into `./documents/`:
- 4 Case Studies (PDF)
- 4 Proposals (PDF)
- 2 Whitepapers (PDF)
- 2 Pitch Decks (PPTX)

Upload all files to the shared Google Drive folder and share it with Person 1's service account email.

## Test Files

| File | Purpose |
|---|---|
| `golden_qa.json` | 13 Q&A pairs for accuracy testing (incl. multi-turn chain) |
| `guardrail_tests.json` | 9 input guardrail tests + 4 output guardrail tests + multi-turn chain |

## Demo Script — Multi-Turn Chain

Run in the same session (do NOT click New Chat between turns):

1. `"What experience do we have in manufacturing?"` — broad overview
2. `"Narrow that to 2023 only"` — year filter, should drop 2021/2022 docs
3. `"What about specifically in South India?"` — regional filter on top of year

Expected final answer: Tamil Nadu Cluster + Chennai Predictive Maintenance + Coimbatore Mid-Market (all 2023, all South India).
