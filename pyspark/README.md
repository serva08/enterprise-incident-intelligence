# Databricks and PySpark Projects

This folder contains Databricks notebook source files exported as Python. Import a `.py` file into Databricks as a notebook to run cells marked with `# COMMAND ----------`. The workspace supplies the `spark` session and the `display()` helper.

## Notebook portfolio

| Notebook | Focus | Data requirements |
| --- | --- | --- |
| [`01_incident_data_preparation.py`](01_incident_data_preparation.py) | Synthetic incident DataFrame creation, filtering, grouping, trimming, and separating valid from invalid category values. | Creates six synthetic rows in the notebook; no source table is required. |
| [`03_supply_chain_orders.py`](03_supply_chain_orders.py) | Delivery duration and lateness features, overall metrics, and late-delivery percentage by purchase month. | Requires `raw_olist_orders` and `silver_delivery_performance` to exist in the active Databricks catalog and schema. |

## Key learning points

- DataFrame transformations describe a plan; actions such as `count()`, `show()`, `display()`, and `write()` trigger execution.
- Aggregate item- or order-level records before joining when necessary to avoid multiplying rows and distorting metrics.
- Keep the columns required by later transformations when using `select()`.
- Define the grain of each result before `groupBy()`. For a monthly rate, group by the month alone rather than by individual delivery attributes.
- Sort by a date or timestamp key for chronological order; formatted labels such as `"October 2026"` sort as text, not time.
- Validate nulls, blanks, duplicates, and date consistency before treating a dataset as a reliable input to analytics or AI.

## Data and scope notes

The incident-preparation notebook uses synthetic data. The supply-chain notebook reads tables already available in the user's Databricks environment and does not create or write those source tables. Confirm the provenance, permitted use, and schema of any tables provisioned in a workspace before running it. Neither notebook calls a paid AI API.

The notebooks are learning examples, not a packaged production pipeline: they do not include orchestration, incremental processing, automated data-quality reporting, or deployment configuration.
