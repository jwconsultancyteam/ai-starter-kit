# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this directory is

This directory holds data, not code. It contains one file, `shipments-export-sample.csv`. There is no build, lint, or test tooling, no README, and it is not a git repository. Any analysis scripts written here will be the first code in the directory.

## `shipments-export-sample.csv`

This is a sample export of freight shipments. It has a header row and 198 data rows, with no quoting and no embedded commas.

| column | notes |
|---|---|
| `date` | ISO `YYYY-MM-DD`, from 2026-08-24 to 2026-10-16. Weekdays only, so weekends are missing rather than zero. Several rows per day. |
| `shipment_id` | `SHP-26001` to `SHP-26198`, sequential and in date order. |
| `client` | Seven placeholder clients, each name ending in ` (example)`: Alpha Retail, Beta Foods, Gamma Tools, Delta Home, Epsilon Garden, Zeta Sports, Eta Office. |
| `route` | `ORIGIN-DEST` country codes. Only four values appear: `BE-NL`, `NL-BE`, `BE-FR`, `BE-BE` (domestic). |
| `pallets` | Integer, 1 to 22. |
| `weight_kg` | Integer. Roughly 380 to 520 kg per pallet. |
| `status` | Every row is `delivered` in this sample. Don't assume no other statuses exist in real exports. |

Things to keep in mind when analysing this file:
- The data is anonymised sample data (note the ` (example)` suffix). Don't present findings from it as real client figures.
- Because weekends are absent, use business days, not calendar days, when computing daily averages or plotting time series. Otherwise you'll get false zero days.
- Beta Foods ships much larger loads (often 15+ pallets) than Eta Office (1 to 5 pallets). Per-client volume comparisons should use pallets or weight, not shipment counts.
