import html
import os
import re
import textwrap
import unicodedata
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "pdf" / "ai_enablement_prompt_pack.pdf"
MOODBOARD_EXAMPLE_IMAGE = ROOT / "tmp" / "pdfs" / "assets" / "chill_nest_moodboard_example.png"
COMPANION_SITE_URL = "https://oai-demo-eta.vercel.app/"
OPENAI_ACADEMY_URL = "https://academy.openai.com/"
CHATGPT_101_URL = "https://academy.openai.com/home/clubs/work-users-ynjqu/videos/chatgpt-101-a-guide-to-your-ai-superassistant-recording"
CHATGPT_OVERVIEW_URL = "https://chatgpt.com/overview/"
CHATGPT_URL = "https://chatgpt.com/"
SHEETS_APP_URL = "https://chatgpt.com/apps/spreadsheets/"
CODEX_URL = "https://chatgpt.com/codex"
PLUGIN_OVERVIEW_URL = "https://developers.openai.com/codex/plugins"
OPENAI_BUSINESS_URL = "https://openai.com/business/"
OPENAI_YOUTUBE_URL = "https://www.youtube.com/@OpenAI"
FINANCE_SETUP_DOWNLOAD_URL = (
    "https://oai-demo-eta.vercel.app/setup#:~:text=for%20the%20model.-,Download%20ZIP,-Tip%3A%20Review"
)
FINANCE_SOURCE_ZIP_URL = "https://oai-demo-eta.vercel.app/demo-files/chillnest_finance_source_pack.zip"
MARKETING_SOURCE_ZIP_URL = "https://oai-demo-eta.vercel.app/demo-files/chillnest_campaign_source_files.zip"

PAGE_W, PAGE_H = letter
BLUE = colors.HexColor("#2563EB")
CYAN = colors.HexColor("#22D3EE")
PURPLE = colors.HexColor("#C43FEA")
INK = colors.HexColor("#0F172A")
MUTED = colors.HexColor("#52637A")
LINE = colors.HexColor("#D9E2EC")
SOFT = colors.HexColor("#F7FAFC")
MINT = colors.HexColor("#ECFEFF")
PROMPT_BG = colors.HexColor("#F8FAFC")
HIGHLIGHT_BG = colors.HexColor("#FFF7ED")
HIGHLIGHT_LINE = colors.HexColor("#FDBA74")
LINK_BLUE = colors.HexColor("#0B63CE")


class Bookmark(Flowable):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.width = 0
        self.height = 0

    def draw(self):
        self.canv.bookmarkPage(self.name)


def normalize_text(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"<br\s*/?>", "\n", value, flags=re.I)
    value = re.sub(r"</p\s*>", "\n", value, flags=re.I)
    value = re.sub(r"</li\s*>", "\n", value, flags=re.I)
    value = re.sub(r"<[^>]+>", "", value)
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2192": "->",
        "\xa0": " ",
    }
    for before, after in replacements.items():
        value = value.replace(before, after)
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n\s+", "\n", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def clean_code(value: str) -> str:
    value = html.unescape(value or "")
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2192": "->",
        "\xa0": " ",
    }
    for before, after in replacements.items():
        value = value.replace(before, after)
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    return value.strip()


def wrap_code(value: str, width: int = 86) -> str:
    lines = []
    for line in clean_code(value).splitlines():
        if not line.strip():
            lines.append("")
            continue
        indent = len(line) - len(line.lstrip(" "))
        prefix = " " * indent
        wrapped = textwrap.wrap(
            line,
            width=width,
            subsequent_indent=prefix + "  ",
            break_long_words=False,
            break_on_hyphens=False,
        )
        lines.extend(wrapped or [""])
    return "\n".join(lines)


def first_match(pattern: str, text: str) -> str:
    match = re.search(pattern, text, flags=re.S | re.I)
    return match.group(1) if match else ""


def all_matches(pattern: str, text: str):
    return re.findall(pattern, text, flags=re.S | re.I)


def list_items(block: str):
    return [normalize_text(item) for item in all_matches(r"<li[^>]*>(.*?)</li>", block) if normalize_text(item)]


def extract_page(filename: str):
    raw = (ROOT / filename).read_text(encoding="utf-8")
    page = {
        "filename": filename,
        "title": normalize_text(first_match(r"<h1[^>]*>(.*?)</h1>", raw)),
        "lead": normalize_text(first_match(r'<p class="lesson-lead"[^>]*>(.*?)</p>', raw)),
        "inputs_outputs": [],
        "plugin_highlights": [],
        "requirements": [],
        "steps": [],
        "prompts": [],
        "callouts": [],
        "checks": [],
        "summary_title": "",
        "summary_text": "",
    }

    for card in all_matches(r'<article class="io-card"[^>]*>(.*?)</article>', raw):
        label = normalize_text(first_match(r"<span[^>]*>(.*?)</span>", card))
        items = list_items(card)
        if label and items:
            page["inputs_outputs"].append((label, items))

    for block in all_matches(r'<div[^>]*class="[^"]*\bplugin-highlight\b[^"]*"[^>]*>(.*?)</div>', raw):
        title = normalize_text(first_match(r"<h2[^>]*>(.*?)</h2>", block))
        rows = [
            normalize_text(item)
            for item in all_matches(r"<p[^>]*>(.*?)</p>", block)
            if normalize_text(item)
        ]
        link_match = re.search(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', block, flags=re.S | re.I)
        link_url = link_match.group(1) if link_match else ""
        link_label = normalize_text(link_match.group(2)) if link_match else ""
        if title or rows:
            page["plugin_highlights"].append(
                {"title": title or "Using a plugin", "rows": rows, "link_label": link_label, "link_url": link_url}
            )

    for label in all_matches(r'<label class="requirement-main"[^>]*>(.*?)</label>', raw):
        title = normalize_text(first_match(r"<strong[^>]*>(.*?)</strong>", label))
        desc = normalize_text(first_match(r"<small[^>]*>(.*?)</small>", label))
        items = list_items(label)
        if title:
            page["requirements"].append({"title": title, "desc": desc, "items": items})

    steps_html = first_match(r'<ol class="workflow-steps"[^>]*>(.*?)</ol>', raw)
    step_matches = re.findall(r"<li(?P<attrs>[^>]*)>(?P<body>.*?)</li>", steps_html, flags=re.S | re.I)
    for index, (attrs, step) in enumerate(step_matches, start=1):
        title = normalize_text(first_match(r"<h3[^>]*>(.*?)</h3>", step))
        desc = normalize_text(first_match(r"<p[^>]*>(.*?)</p>", step))
        prompts = []
        for pblock in all_matches(r'<article class="prompt-block[^"]*"[^>]*>(.*?)</article>', step):
            ptitle = normalize_text(first_match(r"<h3[^>]*>(.*?)</h3>", pblock))
            pre_match = re.search(
                r'<pre[^>]*id="([^"]+)"[^>]*>\s*<code>(.*?)</code>\s*</pre>',
                pblock,
                flags=re.S | re.I,
            )
            prompt_id = pre_match.group(1) if pre_match else ""
            pcode = clean_code(pre_match.group(2) if pre_match else first_match(r"<pre[^>]*>\s*<code>(.*?)</code>\s*</pre>", pblock))
            if ptitle and pcode:
                prompts.append({"title": ptitle, "text": pcode, "id": prompt_id})
                page["prompts"].append({"title": ptitle, "text": pcode, "id": prompt_id})
        if title:
            page["steps"].append(
                {
                    "number": index,
                    "title": title,
                    "desc": desc,
                    "prompts": prompts,
                    "highlight": "tool-highlight" in attrs,
                }
            )

    callout_matches = re.findall(
        r'<div(?P<attrs>[^>]*class="[^"]*\bcallout\b[^"]*"[^>]*)>(?P<body>.*?)</div>',
        raw,
        flags=re.S | re.I,
    )
    for attrs, callout in callout_matches:
        text = normalize_text(callout)
        if text:
            page["callouts"].append({"text": text, "highlight": "ownership-reminder" in attrs})

    page["checks"] = [
        normalize_text(item)
        for item in all_matches(r'<label class="check-row"[^>]*>.*?<span[^>]*>(.*?)</span>.*?</label>', raw)
        if normalize_text(item)
    ]

    summary = first_match(r'<div[^>]*class="[^"]*\bworkflow-summary\b[^"]*"[^>]*>(.*?)</div>', raw)
    if summary:
        page["summary_title"] = normalize_text(first_match(r"<h2[^>]*>(.*?)</h2>", summary))
        summary_paragraphs = [
            normalize_text(item)
            for item in all_matches(r"<p[^>]*>(.*?)</p>", summary)
            if normalize_text(item).lower() != "workflow"
        ]
        page["summary_text"] = summary_paragraphs[-1] if summary_paragraphs else ""

    return page


PAGES = [
    ("Finance", "Requirements", "setup.html"),
    ("Finance", "Workflow 1", "story.html"),
    ("Finance", "Workflow 2", "model.html"),
    ("Finance", "Workflow 3", "validate.html"),
    ("Finance", "Workflow 4", "dashboard.html"),
    ("Marketing", "Requirements", "marketing-setup.html"),
    ("Marketing", "Workflow 1", "marketing-brief.html"),
    ("Marketing", "Workflow 2", "marketing-creative.html"),
    ("Marketing", "Workflow 3", "marketing-handoff.html"),
    ("Marketing", "Workflow 4", "marketing-assets.html"),
    ("Marketing", "Workflow 5", "marketing-landing.html"),
]


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="CoverTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=34,
        leading=38,
        textColor=INK,
        spaceAfter=12,
    )
)
styles.add(
    ParagraphStyle(
        name="Deck",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=13,
        leading=18,
        textColor=MUTED,
        spaceAfter=14,
    )
)
styles.add(
    ParagraphStyle(
        name="SectionTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=29,
        textColor=INK,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="WorkflowTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=INK,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="H3Custom",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15,
        textColor=INK,
        spaceBefore=8,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.3,
        leading=13,
        textColor=INK,
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="Muted",
        parent=styles["BodyCustom"],
        textColor=MUTED,
    )
)
styles.add(
    ParagraphStyle(
        name="Kicker",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=BLUE,
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="PromptTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=13,
        textColor=INK,
    )
)
styles.add(
    ParagraphStyle(
        name="PromptCode",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7.4,
        leading=9.6,
        textColor=colors.HexColor("#111827"),
        leftIndent=0,
        firstLineIndent=0,
    )
)
styles.add(
    ParagraphStyle(
        name="Center",
        parent=styles["BodyCustom"],
        alignment=TA_CENTER,
    )
)
styles.add(
    ParagraphStyle(
        name="LinkBody",
        parent=styles["BodyCustom"],
        textColor=LINK_BLUE,
    )
)


def p(text, style="BodyCustom"):
    return Paragraph(normalize_text(text), styles[style])


class MarkupText(str):
    pass


def xml_text(text: str) -> str:
    return html.escape(normalize_text(text), quote=False)


def link(label: str, url: str) -> str:
    return f'<a href="{html.escape(url, quote=True)}" color="#0B63CE">{xml_text(label)}</a>'


def linked_row(text: str, label: str, url: str) -> MarkupText:
    return MarkupText(f"{xml_text(text)} {link(label, url)}")


def link_row(label: str, url: str) -> MarkupText:
    return MarkupText(link(label, url))


def paragraph_source(item) -> str:
    if isinstance(item, MarkupText):
        return str(item)
    return xml_text(item)


def bullets(items, level=0):
    rows = [
        [Paragraph(f"- {paragraph_source(item)}", styles["BodyCustom"])]
        for item in items
        if paragraph_source(item)
    ]
    if not rows:
        rows = [[Paragraph("", styles["BodyCustom"])]]
    table = Table(rows)
    table.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ]
        )
    )
    return table


def small_table(title, rows, background=MINT, box_color=colors.HexColor("#A5F3FC")):
    data = [[Paragraph(title, styles["PromptTitle"])]]
    data.append([bullets(rows)])
    table = Table(data, colWidths=[7.0 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), background),
                ("BOX", (0, 0), (-1, -1), 0.7, box_color),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return table


def companion_page_url(filename: str) -> str:
    stem = Path(filename).stem
    if stem == "index":
        return COMPANION_SITE_URL
    return f"{COMPANION_SITE_URL.rstrip('/')}/{stem}"


def prompt_copy_url(filename: str, prompt):
    prompt_id = prompt.get("id")
    if not prompt_id:
        return ""
    return f"{companion_page_url(filename)}#{prompt_id}"


def prompt_box(title, text, copy_url=""):
    pre = Preformatted(wrap_code(text), styles["PromptCode"])
    header = [Paragraph(title, styles["PromptTitle"])]
    if copy_url:
        header.append(Paragraph(link("Copy prompt on website", copy_url), styles["LinkBody"]))
    else:
        header.append(Paragraph("", styles["LinkBody"]))
    table = Table(
        [header, [pre, ""]],
        colWidths=[4.85 * inch, 2.15 * inch],
        repeatRows=0,
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.white),
                ("BACKGROUND", (0, 1), (-1, 1), PROMPT_BG),
                ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#7DD3FC")),
                ("LINEBELOW", (0, 0), (-1, 0), 0.4, LINE),
                ("SPAN", (0, 1), (1, 1)),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return table


def step_block(step, filename=""):
    body = [
        Paragraph(f"Step {step['number']}: {step['title']}", styles["H3Custom"]),
    ]
    if step["desc"]:
        body.append(p(step["desc"], "Muted"))
    links = step_resource_links(filename, step)
    if links:
        body.append(Spacer(1, 3))
        body.append(bullets(links))
    for prompt in step["prompts"]:
        body.append(Spacer(1, 4))
        body.append(prompt_box(prompt["title"], prompt["text"], prompt_copy_url(filename, prompt)))
    table = Table([[body]], colWidths=[7.0 * inch])
    background = HIGHLIGHT_BG if step.get("highlight") else colors.white
    box_color = HIGHLIGHT_LINE if step.get("highlight") else LINE
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), background),
                ("BOX", (0, 0), (-1, -1), 0.7 if step.get("highlight") else 0.5, box_color),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def draw_gradient(canvas, x, y, width, height, left=BLUE, mid=CYAN, right=PURPLE, steps=80):
    def interp(c1, c2, t):
        return colors.Color(
            c1.red + (c2.red - c1.red) * t,
            c1.green + (c2.green - c1.green) * t,
            c1.blue + (c2.blue - c1.blue) * t,
        )

    for i in range(steps):
        t = i / max(steps - 1, 1)
        if t < 0.5:
            c = interp(left, mid, t / 0.5)
        else:
            c = interp(mid, right, (t - 0.5) / 0.5)
        canvas.setFillColor(c)
        canvas.rect(x + width * i / steps, y, width / steps + 1, height, stroke=0, fill=1)


def scaled_image(path: Path, max_width: float, max_height: float):
    reader = ImageReader(str(path))
    width, height = reader.getSize()
    scale = min(max_width / width, max_height / height)
    image = Image(str(path), width=width * scale, height=height * scale)
    image.hAlign = "CENTER"
    return image


def page_header(canvas, doc):
    canvas.saveState()
    draw_gradient(canvas, 0, PAGE_H - 64, PAGE_W, 64)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 13)
    canvas.drawString(42, PAGE_H - 31, "AI Enablement Prompt Pack")
    canvas.setFont("Helvetica", 8.5)
    canvas.drawString(42, PAGE_H - 47, "ChatGPT for Finance + Codex for Marketing")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(PAGE_W - 42, 28, f"Page {doc.page}")
    canvas.restoreState()


def cover_page(canvas, doc):
    canvas.saveState()
    draw_gradient(canvas, 0, PAGE_H - 155, PAGE_W, 155)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 24)
    canvas.drawString(42, PAGE_H - 72, "Hands-on AI Enablement")
    canvas.setFont("Helvetica", 12)
    canvas.drawString(42, PAGE_H - 96, "Prompt pack + workflow instructions")
    canvas.restoreState()


def add_moodboard_example(story):
    if not MOODBOARD_EXAMPLE_IMAGE.exists():
        return
    story.append(Paragraph("MARKETING", styles["Kicker"]))
    story.append(Paragraph("Example output: visual mood board", styles["WorkflowTitle"]))
    story.append(
        Paragraph(
            "This is one example of what the mood-board output can look like. Each user's output will look different based on the files, prompt, plugin response, and choices made while reviewing.",
            styles["Deck"],
        )
    )
    story.append(Spacer(1, 10))
    story.append(scaled_image(MOODBOARD_EXAMPLE_IMAGE, 4.15 * inch, 6.9 * inch))
    story.append(PageBreak())


def add_learn_more(story):
    resources = [
        linked_row(
            "OpenAI Academy - Guided courses, events, and practical learning for work:",
            "OpenAI Academy",
            OPENAI_ACADEMY_URL,
        ),
        linked_row(
            "ChatGPT - Product overview and examples of what ChatGPT can help with:",
            "ChatGPT overview",
            CHATGPT_OVERVIEW_URL,
        ),
        linked_row(
            "Codex - Learn more about using Codex as an AI teammate for work:",
            "Codex",
            CODEX_URL,
        ),
        linked_row(
            "Codex plugins - Understand how plugins extend Codex with workflows, skills, integrations, and MCP servers:",
            "Codex plugins docs",
            PLUGIN_OVERVIEW_URL,
        ),
        linked_row(
            "OpenAI for Business - Explore OpenAI products and examples for teams and organizations:",
            "OpenAI for Business",
            OPENAI_BUSINESS_URL,
        ),
        linked_row(
            "OpenAI YouTube - Watch official demos, talks, launch videos, and product walkthroughs:",
            "OpenAI YouTube channel",
            OPENAI_YOUTUBE_URL,
        ),
    ]
    story.append(Paragraph("LEARN MORE", styles["Kicker"]))
    story.append(Paragraph("Keep learning with OpenAI", styles["WorkflowTitle"]))
    story.append(
        Paragraph(
            "Use these official OpenAI resources after the demo to keep practicing, explore product updates, and find more examples for your team.",
            styles["Deck"],
        )
    )
    story.append(Spacer(1, 10))
    story.append(
        small_table(
            "Official resources",
            resources,
            background=colors.HexColor("#F8FAFC"),
            box_color=colors.HexColor("#93C5FD"),
        )
    )
    story.append(Spacer(1, 12))
    story.append(
        small_table(
            "Suggested next step",
            [
                "Pick one workflow from this pack, rerun it with your own safe sample files, and iterate until the output is useful enough for a real review conversation."
            ],
            background=MINT,
            box_color=colors.HexColor("#A5F3FC"),
        )
    )
    story.append(PageBreak())


def add_overview(story):
    story.append(Spacer(1, 160))
    story.append(Paragraph("AI Enablement Prompt Pack", styles["CoverTitle"]))
    story.append(
        Paragraph(
            "Reusable prompts and workflow steps for the ChatGPT for Finance and Codex for Marketing demos.",
            styles["Deck"],
        )
    )
    story.append(Spacer(1, 12))
    story.append(
        small_table(
            "How to use this pack",
            [
                linked_row(
                    "Use this PDF as a prompt pack, or follow along through the companion website:",
                    "Open the website.",
                    COMPANION_SITE_URL,
                ),
                "Choose a demo: ChatGPT for Finance or Codex for Marketing.",
                "Confirm the requirements and download the source files from the companion website.",
                "Your screen might look different than the facilitator's screen because of your settings or your organization's admin preferences. Don't worry - follow along, and ask if you have questions.",
                "Follow each workflow in order. Copy the prompts, then iterate based on the output.",
                "Review generated artifacts. Subject matter expertise and approval always matter.",
                "Have fun and learn. This is meant to be an interactive, conversational demo.",
            ],
        )
    )
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            f'Learn more about ChatGPT: <a href="{CHATGPT_OVERVIEW_URL}" color="#0B63CE">{CHATGPT_OVERVIEW_URL}</a>',
            styles["BodyCustom"],
        )
    )
    story.append(Spacer(1, 12))
    story.append(Paragraph("Contents", styles["H3Custom"]))
    story.append(
        Paragraph(
            '- <a href="#finance_start" color="#0B63CE">ChatGPT for Finance</a>: requirements, finance story, lightweight DCF, assumption validation, dashboard, and ownership reminder.',
            styles["BodyCustom"],
        )
    )
    story.append(
        Paragraph(
            '- <a href="#marketing_start" color="#0B63CE">Codex for Marketing</a>: requirements, campaign brief, visual mood board, production handoff, channel assets, landing page.',
            styles["BodyCustom"],
        )
    )
    story.append(PageBreak())


def add_journey_intro(story, name, subtitle, anchor=None):
    if anchor:
        story.append(Bookmark(anchor))
    draw = Table(
        [[Paragraph(name, styles["SectionTitle"]), Paragraph(subtitle, styles["Deck"])]],
        colWidths=[2.4 * inch, 4.6 * inch],
    )
    draw.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), MINT),
                ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#A5F3FC")),
                ("LEFTPADDING", (0, 0), (-1, -1), 16),
                ("RIGHTPADDING", (0, 0), (-1, -1), 16),
                ("TOPPADDING", (0, 0), (-1, -1), 18),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.append(draw)
    story.append(Spacer(1, 14))


def requirement_resource_links(filename: str, title: str):
    resources = []
    key = (filename, title)
    if key == ("setup.html", "ChatGPT"):
        resources.extend(
            [
                link_row("Open ChatGPT", CHATGPT_URL),
                link_row("Pre-review: ChatGPT 101", CHATGPT_101_URL),
                link_row("Learn more about ChatGPT", CHATGPT_OVERVIEW_URL),
            ]
        )
    elif key == ("setup.html", "ChatGPT for Excel or Google Sheets"):
        resources.append(link_row("Install ChatGPT for Excel or Google Sheets", SHEETS_APP_URL))
    elif key == ("setup.html", "Download ChillNest files"):
        resources.extend(
            [
                link_row("Download finance source ZIP", FINANCE_SOURCE_ZIP_URL),
                link_row("Open finance requirements page", FINANCE_SETUP_DOWNLOAD_URL),
            ]
        )
    elif key == ("marketing-setup.html", "Codex"):
        resources.append(link_row("Download Codex or learn more", CODEX_URL))
    elif key == ("marketing-setup.html", "Download Campaign Source Files"):
        resources.append(link_row("Download marketing source ZIP", MARKETING_SOURCE_ZIP_URL))
    return resources


def callout_resource_links(filename: str, callout: str):
    if filename == "marketing-creative.html" and "Learn more about plugins" in callout:
        return [link_row("Learn more about Codex plugins", PLUGIN_OVERVIEW_URL)]
    return []


def step_resource_links(filename: str, step):
    if filename == "validate.html" and step.get("highlight"):
        return [link_row("Learn how to download and install ChatGPT for Excel or Google Sheets", SHEETS_APP_URL)]
    return []


def add_page(story, journey, label, page):
    story.append(Paragraph(journey.upper(), styles["Kicker"]))
    story.append(Paragraph(f"{label}: {page['title']}", styles["WorkflowTitle"]))
    if page["lead"]:
        story.append(Paragraph(page["lead"], styles["Deck"]))

    is_requirements_page = page["filename"] in {"setup.html", "marketing-setup.html"}
    summary_rendered = False
    if is_requirements_page and page["summary_title"]:
        story.append(
            KeepTogether(
                [
                    Spacer(1, 4),
                    small_table(page["summary_title"], [page["summary_text"]]),
                    Spacer(1, 7),
                ]
            )
        )
        summary_rendered = True

    if page["inputs_outputs"]:
        cols = []
        for label_text, items in page["inputs_outputs"]:
            cols.append([Paragraph(label_text, styles["PromptTitle"]), bullets(items)])
        if len(cols) == 2:
            table = Table([cols], colWidths=[3.42 * inch, 3.42 * inch])
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                        ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                        ("LEFTPADDING", (0, 0), (-1, -1), 10),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ]
                )
            )
            story.append(table)
            story.append(Spacer(1, 9))

    if page["plugin_highlights"]:
        for item in page["plugin_highlights"]:
            rows = list(item["rows"])
            if item.get("link_label") and item.get("link_url"):
                rows.append(link_row(item["link_label"], item["link_url"]))
            story.append(
                small_table(
                    item["title"],
                    rows,
                    background=colors.HexColor("#FAF5FF"),
                    box_color=colors.HexColor("#C084FC"),
                )
            )
            story.append(Spacer(1, 9))

    if page["requirements"]:
        story.append(Paragraph("Requirements", styles["H3Custom"]))
        for req in page["requirements"]:
            lines = []
            if req["desc"]:
                lines.append(req["desc"])
            lines.extend(req["items"])
            lines.extend(requirement_resource_links(page["filename"], req["title"]))
            story.append(small_table(req["title"], lines))
            story.append(Spacer(1, 5))

    if page["steps"]:
        story.append(Paragraph("Workflow Steps", styles["H3Custom"]))
        for step in page["steps"]:
            story.append(step_block(step, page["filename"]))
            story.append(Spacer(1, 7))

    if page["summary_title"] and not summary_rendered:
        story.append(
            KeepTogether(
                [
                    Spacer(1, 4),
                    small_table(page["summary_title"], [page["summary_text"]]),
                    Spacer(1, 7),
                ]
            )
        )

    if page["checks"]:
        story.append(Paragraph("Before moving on", styles["H3Custom"]))
        story.append(bullets(page["checks"]))

    if page["callouts"]:
        section_title = "Setup Notes" if is_requirements_page else "Review Notes"
        review_bits = [Paragraph(section_title, styles["H3Custom"])]
        for callout in page["callouts"]:
            callout_text = callout["text"] if isinstance(callout, dict) else callout
            callout_highlight = bool(callout.get("highlight")) if isinstance(callout, dict) else False
            title = "Ownership and accountability" if callout_highlight else ("Note" if is_requirements_page else "Review")
            background = HIGHLIGHT_BG if callout_highlight else MINT
            box_color = HIGHLIGHT_LINE if callout_highlight else colors.HexColor("#A5F3FC")
            review_bits.append(
                small_table(
                    title,
                    [callout_text, *callout_resource_links(page["filename"], callout_text)],
                    background=background,
                    box_color=box_color,
                )
            )
            review_bits.append(Spacer(1, 5))
        story.append(KeepTogether(review_bits))

    story.append(PageBreak())


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=42,
        rightMargin=42,
        topMargin=84,
        bottomMargin=44,
        title="AI Enablement Prompt Pack",
        author="OpenAI Academy Demo",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates(
        [
            PageTemplate(id="cover", frames=[frame], onPage=cover_page, autoNextPageTemplate="main"),
            PageTemplate(id="main", frames=[frame], onPage=page_header),
        ]
    )

    story = []
    add_overview(story)

    add_journey_intro(
        story,
        "ChatGPT for Finance",
        "A short finance demo that starts with raw files, builds a lightweight model, validates assumptions, and prepares a dashboard.",
        anchor="finance_start",
    )
    for journey, label, filename in PAGES[:5]:
        add_page(story, journey, label, extract_page(filename))

    add_journey_intro(
        story,
        "Codex for Marketing",
        "A customer-facing marketing demo that turns messy campaign context into a brief, mood board, handoff, assets, and landing page.",
        anchor="marketing_start",
    )
    for journey, label, filename in PAGES[5:]:
        add_page(story, journey, label, extract_page(filename))
        if filename == "marketing-creative.html":
            add_moodboard_example(story)

    add_learn_more(story)

    if story and isinstance(story[-1], PageBreak):
        story.pop()
    doc.build(story)
    print(OUT)


if __name__ == "__main__":
    build()
