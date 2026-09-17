# CRM ↔ Accounting Sync Platform

A public-safe integration demo for synchronizing CRM deals with accounting invoices, payments, customer records, and exception handling.

## What it demonstrates

- event-driven CRM → accounting sync
- customer and invoice creation rules
- duplicate detection
- conflict handling
- failed-sync retry queues
- audit log visibility
- reconciliation between commercial and finance systems

All entities and transactions are synthetic; no live CRM or accounting tenant is connected.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

`Python` `Streamlit` `APIs` `Webhooks` `CRM` `QuickBooks/Xero Patterns` `RevOps` `Finance Automation`
