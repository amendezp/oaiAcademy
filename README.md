# AI Enablement Journeys

An audience-facing static lab site for teams learning through two paths: ChatGPT for Finance and Codex for Marketing.

Learners move through guided journeys.

The ChatGPT for Finance journey follows an analysis and modeling arc:

1. Requirements: download files and prepare tools.
2. Story: explain raw country and regional performance data in ChatGPT.
3. Model: create a DCF model live in ChatGPT using the remaining historical files.
4. Validate: refresh assumptions with research or approved connectors.
5. Dashboard: create a dashboard and close with ownership, accountability, and iteration reminders.

The Codex for Marketing journey follows a campaign-production arc:

1. Requirements: download Chill Nest marketing source files and prepare Codex.
2. Brief: turn the messy campaign pile into a sharp campaign brief.
3. Creative: turn the brief into creative worlds and moodboard direction.
4. Handoff: turn the chosen creative world into a production handoff.
5. Assets: draft channel assets for search, display, Meta, TikTok, email, and landing page.
6. Landing page: create a promotion landing page preview from the campaign kit.

## Files

- `index.html` - two-journey landing page
- `finance.html` - ChatGPT for Finance workflow overview
- `setup.html` - Finance requirements checklist
- `story.html` - raw-data story workflow
- `model.html` - model creation workflow
- `validate.html` - assumption validation workflow
- `dashboard.html` - dashboard creation workflow
- `marketing.html` - Codex for Marketing workflow overview
- `marketing-setup.html` - Marketing requirements checklist and campaign source-file download
- `marketing-brief.html` - marketing brief workflow
- `marketing-creative.html` - creative direction and moodboard workflow
- `marketing-handoff.html` - production handoff workflow
- `marketing-assets.html` - channel assets workflow
- `marketing-landing.html` - promotion landing page workflow
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
- `demo-files/chillnest_finance_source_pack.zip` - bundled ChatGPT for Finance source files
- `demo-files/chillnest_campaign_source_files.zip` - bundled Codex for Marketing campaign source files

## Deploy To Vercel

This is a dependency-free static site. In Vercel, import the repo and leave the build command blank. The output directory is the repository root.

For local preview, open `index.html` in a browser.
