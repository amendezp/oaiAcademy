# ChatGPT for Finance Lab

An audience-facing static lab site for Finance teams learning how to use ChatGPT and ChatGPT for Excel or Google Sheets.

Learners move through a guided journey:

1. Requirements: download files and prepare tools.
2. Story: explain raw country and regional performance data in ChatGPT.
3. Model: create a DCF model live in ChatGPT for Excel or Google Sheets.
4. Validate: refresh assumptions with research or approved connectors.
5. Dashboard: create a leadership-ready dashboard and briefing.
6. Review: check accuracy, assumptions, and human judgment before sharing.

## Files

- `index.html` - two-journey landing page
- `setup.html` - Finance requirements checklist
- `story.html` - raw-data story workflow
- `model.html` - model creation workflow
- `validate.html` - assumption validation workflow
- `dashboard.html` - dashboard creation workflow
- `review.html` - final review checklist
- `marketing.html` - Codex for Marketing journey preview
- `styles.css` - visual styling
- `script.js` - copy-prompt behavior
- `demo-files/chillnest_country_performance.csv` - synthetic country-level finance data
- `demo-files/chillnest_monthly_region_performance.csv` - synthetic monthly regional trend and free cash flow data
- `demo-files/chillnest_operating_notes.txt` - synthetic operating context
- `demo-files/chillnest_company_profile.txt` - one-page company context for upload
- `demo-files/chillnest_company_profile.pdf` - one-page company context for reading
- `demo-files/chillnest_historical_pl.csv` - historical P&L
- `demo-files/chillnest_historical_balance_sheet.csv` - historical balance sheet
- `demo-files/chillnest_historical_cash_flow.csv` - historical cash flow statement
- `demo-files/chillnest_finance_source_pack.zip` - bundled Finance journey source files

## Deploy To Vercel

This is a dependency-free static site. In Vercel, import the repo and leave the build command blank. The output directory is the repository root.

For local preview, open `index.html` in a browser.
