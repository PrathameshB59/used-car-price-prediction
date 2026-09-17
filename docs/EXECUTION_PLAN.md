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
                   Model A | Model B\
```


## Frontend Integration Status — 2026-09-15

- [x] Separate Results dashboard page
- [x] Local prediction history using browser `localStorage`
- [x] ML Price Estimate frontend naming
- [x] Market AI Estimate frontend naming
- [x] Prediction loading, result, and error states
- [x] Results page navigation
- [x] Separate How It Works page
- [x] Topbar-only application navigation

### Current Frontend Flow

Prediction Form
      ↓
Loading State
      ↓
Prediction Result
      ↓
ML Price Estimate + Market AI Estimate
      ↓
Local Prediction History
      ↓
Results Dashboard

## Frontend UI Milestone — 2026-09-16

### Completed

- [x] Separate Results dashboard
- [x] Local prediction history with browser `localStorage`
- [x] Separate How It Works page
- [x] Topbar-only navigation
- [x] ML Price Estimate terminology
- [x] Market AI Estimate terminology
- [x] Connected Model A visual pipeline
- [x] Connected Model B visual pipeline
- [x] Light/dark theme toggle
- [x] Persistent theme preference
- [x] Blue-gray light-mode visual system
- [x] Semantic colors for major How It Works sections
- [x] Before/after Git checkpoints
- [x] UI milestone pushed to `feature/ui-redesign`

### Architecture Boundary

The frontend work changes presentation and browser-side state only.

```text
Frontend
   ↓
Form / UI state / theme / local history
   ↓
Django
   ↓
Model A + Model B
