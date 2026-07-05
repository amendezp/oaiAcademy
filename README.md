# ChatGPT for Finance Enablement Lab

A static companion site for a 10-minute Finance department enablement demo.

The demo flow:

1. Tell the story of raw country performance data in ChatGPT.
2. Create a forecast model live in ChatGPT for Excel or Google Sheets.
3. Validate assumptions and refresh the same model in-place with research or approved connectors.
4. Create a leadership-ready dashboard and briefing.

## Files

- `index.html` - companion site
- `styles.css` - visual styling
- `script.js` - copy-prompt behavior
- `demo-files/chillnest_country_performance.csv` - synthetic finance data
- `demo-files/chillnest_operating_notes.md` - synthetic operating context

## Deploy To Vercel

This is a dependency-free static site. In Vercel, import the repo and leave the build command blank. The output directory is the repository root.

For local preview, open `index.html` in a browser.
