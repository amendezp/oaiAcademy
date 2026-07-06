# ChatGPT for Finance Lab

An audience-facing static lab site for Finance teams learning how to use ChatGPT and ChatGPT for Excel or Google Sheets.

Learners move through a guided journey:

1. Setup: download files and prepare tools.
2. Story: explain raw country and regional performance data in ChatGPT.
3. Model: create a forecast model live in ChatGPT for Excel or Google Sheets.
4. Validate: refresh assumptions with research or approved connectors and apply Finance house style.
5. Dashboard: create a leadership-ready dashboard and briefing.
6. Review: check accuracy, assumptions, and human judgment before sharing.

## Files

- `index.html` - learner-facing lab site
- `setup.html` - setup checklist
- `story.html` - raw-data story workflow
- `model.html` - model creation workflow
- `validate.html` - assumption validation and Finance house style workflow
- `dashboard.html` - dashboard creation workflow
- `review.html` - final review checklist
- `styles.css` - visual styling
- `script.js` - copy-prompt behavior
- `demo-files/chillnest_country_performance.csv` - synthetic country-level finance data
- `demo-files/chillnest_monthly_region_performance.csv` - synthetic monthly regional trend and free cash flow data
- `demo-files/chillnest_operating_notes.txt` - synthetic operating context

## Deploy To Vercel

This is a dependency-free static site. In Vercel, import the repo and leave the build command blank. The output directory is the repository root.

For local preview, open `index.html` in a browser.
