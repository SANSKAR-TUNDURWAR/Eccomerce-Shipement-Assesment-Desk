# 📦 AI-Powered Incident & Damage Triage Console (Exception Desk)

An automated logistics exception management system powered by **LangChain**, **Groq LLMs**, and **Gradio**. This pipeline classifies unstructured customer incident reports, calculates policy-based compensations (delayed, damaged, lost), drafts personalized customer responses, escalates unresolvable issues to management, and tracks real-time triage metrics.

---

## 🚀 Key Features

- **LLM-Powered Classification:** Uses Groq-hosted LLMs to classify unstructured claim text into standard logistics categories: `delayed`, `damaged`, `lost`, or `unknown`.
- **Deterministic Compensation Rules:**
  - **Delayed:** Computes compensation based on per-day delay calculations ($10.00/day).
  - **Damaged:** Applies severity multipliers to the base shipment price.
  - **Lost:** Calculates payouts based on an insurance coverage percentage (80% default).
- **Automated Customer Communication:** Dynamically generates empathetic, customer-ready resolution emails referencing tracking IDs and exact compensation amounts.
- **Managerial Escalation Pipeline:** Flags ambiguous or unknown issues, auto-drafting an internal operational memo for management review.
- **Interactive Web Interface:** A Gradio-based control center to submit claims, view real-time pipeline decisions, inspect triage logs, and generate aggregated operational summaries.

---

## 📁 Repository Structure

```text
├── app.py          # Gradio web application UI and event handlers
├── pipeline.py     # Core business logic, routing, and tool orchestration
├── chains.py       # LangChain prompt templates, LLM configuration, and output parsers
├── tools.py        # Deterministic compensation calculators
├── session.py      # TriageSession state tracker and daily metric aggregator
├── requirements.txt# Python project dependencies
├── .env.example    # Environment variable template
└── README.md       # Project documentation
```

## Project Flow 
```
                        [ Customer Damage Report ]
                                    │
                                    ▼
                         [ Classify Chain (LLM) ]
                                    │
             ┌──────────────────────┼──────────────────────┐
             ▼                      ▼                      ▼
        [ Delayed ]            [ Damaged ]              [ Lost ]
   (Daily Rate Calc)       (Severity Multiplier)   (Insurance Payout)
             │                      │                      │
             └──────────────────────┼──────────────────────┘
                                    │
                                    ▼
                      [ Draft Customer Email (LLM) ]
                                    │
                         [ Update Session & Logs ]

```

(Note: Reports classified as unknown trigger the Escalate Chain to notify operations management.)
