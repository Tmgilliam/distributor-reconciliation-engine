# Distributor Sales Reconciliation Engine

A small Python and SQL portfolio prototype for cleaning distributor transaction data, flagging exceptions, and estimating unresolved reporting exposure before ERP reporting.

## Business problem

External distributor files often contain missing customer identifiers and inconsistent reference data. Those exceptions can make channel reporting incomplete or difficult to reconcile. This prototype provides a basic ingestion and customer-ID reconciliation path, plus a documented governance plan for follow-up.

## Current workflow

1. **Ingest and standardize:** Python reads a distributor CSV, normalizes customer names and addresses, and preserves transaction amounts.
2. **Flag missing IDs:** Rows without a `customer_id` are marked for review.
3. **Classify returns:** Negative `sales_amount` values are labeled `Return/Credit`; positive values are labeled `Sale`.
4. **Reconcile in SQL:** The query compares staged customer IDs with an ERP customer master and classifies missing IDs, unmapped IDs, and confirmed matches.
5. **Aggregate diagnostics:** SQL reports record counts, gross-value exposure, and share of transaction records by reconciliation status.

## Supplied baseline audit

The case-study material reports the following results from a sample run:

- **Transactions:** 25 records totaling $17,820.00 in gross value.
- **Confirmed match rate:** 64.0% by record count (reported matched value: $12,170.00).
- **Unresolved sales value:** $5,650.00, or 31.7% of gross value, across 9 exceptions.
- **Reported exception drivers:** missing customer IDs ($2,850.00; 44.4% of exception records), unmapped product SKUs ($1,900.00; 33.3%), and account name/address variants ($900.00; 22.2%).

Unresolved value is reporting uncertainty, not proven lost revenue. These figures are supplied case-study results; the input CSV and ERP reference data are not included, so the baseline cannot be reproduced from this repository alone.

## Run the Python step

Requires Python 3.11 or newer.

```bash
python -m pip install -r requirements.txt
```

Place a fictionalized input file named `distributor_sales_2026_Q2.csv` beside `main.py`. It must include these columns:

`transaction_id`, `distributor_id`, `customer_id`, `customer_name`, `customer_address`, `sales_amount`, `transaction_type`

Then run:

```bash
python main.py
```

The script writes `stg_distributor_sales.csv` in the current directory.

## Run the SQL step

Load the generated staging file into a table named `stg_distributor_sales` and provide an `erp_customer_master` table containing `customer_id`. Run `main.sql` in a compatible SQL database. Adjust table-loading syntax for your database as needed.

The query uses `SUM(ABS(sales_amount))` for gross-value exposure, so credits and returns contribute their absolute value to the exposure metric rather than reducing it.

## Scope and limitations

This repository contains a proof-of-concept Python cleansing and missing-ID flagging step and a customer-ID SQL cross-reference. It does not currently implement SKU mapping, fuzzy name/address matching, a persistent alias table, an interactive BI dashboard, or a live ERP integration. The dashboard and continuous-improvement plan are documented separately from the running code.

Use fictionalized data only. Do not commit customer, distributor, financial, or other confidential records.

## Governance plan

See [Data-Governance-Improvement-Plan.md](Data-Governance-Improvement-Plan.md) for the exception-resolution workflow, distributor submission controls, return/credit handling, and review cadence.

## Technology

- Python (Pandas, NumPy)
- SQL (customer-master cross-reference and diagnostic aggregation)
- BI dashboarding (blueprint only; not implemented in this prototype)