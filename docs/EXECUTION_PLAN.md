# Execution Plan

## v0.1.0 — Model A Web MVP

### Completed

- [x] Project setup
- [x] Virtual environment
- [x] Dataset investigation
- [x] V2 data cleaning/audit
- [x] Final feature selection
- [x] Preprocessing pipeline
- [x] Random Forest training
- [x] Model evaluation
- [x] Model artifact saving
- [x] Preprocessor artifact saving
- [x] Reload/prediction verification
- [x] Django integration
- [x] Responsive frontend
- [x] Custom Other/Unknown inputs
- [x] Seller Type UI field
- [x] Git LFS configuration
- [x] v0.1.0 release

## v0.2.0 — Model B

### Goal

Build a second valuation path that combines the existing Model A ML estimate with current Indian used-car market evidence.

Model B is designed as an AI-assisted market research pipeline rather than a model that blindly asks an LLM to invent a price.

### Current Architecture

```text
                         User Input
                             │
                  ┌──────────┴──────────┐
                  ↓                     ↓
             Model A ML            Model B Pipeline
                  │                     │
                  │              Gemini AI analysis
                  │                     │
                  │              Current-market search
                  │                     │
                  │                  Tavily
                  │                     │
                  │              Structured evidence
                  │                     │
                  │              Python validation /
                  │               statistical logic
                  │                     │
                  └──────────┬──────────┘
                             ↓
                     Separate results
                             ↓
                   Model A | Model B
{ _ble_edit_exec_gexec__save_lastarg "$@"; } 4>&1 5>&2 &>/dev/null
