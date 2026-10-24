"""
FALCON: 100% Final Implementation Report PDF Generator
Strictly adheres to the formatting, geometry, typography, and page structure
of the benchmark project progress report (8-page US Letter, Times New Roman,
dark-green table styling, standalone cover page, and dot-leader TOC).
"""

import os
import re
import gc
import pymupdf
import markdown_it

def build_pdf():
    falcon_dir = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.join(falcon_dir, "FALCON_100_Percent_Implementation_Report.md")
    output_pdf = os.path.join(falcon_dir, "FALCON_100_Percent_Implementation_Report.pdf")
    temp_body_pdf = os.path.join(falcon_dir, "_temp_body.pdf")

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Extract body starting from Section 1
    sec1_match = re.search(r"## 1\. Executive Summary", md_text)
    if not sec1_match:
        raise ValueError("Could not find '## 1. Executive Summary' in markdown")
    body_md = md_text[sec1_match.start():]

    # Convert markdown to HTML using commonmark + tables
    md = markdown_it.MarkdownIt("commonmark").enable("table")
    raw_body_html = md.render(body_md)

    # Convert equation blockquotes into styled equation containers (neutral styling, no green borders)
    cleaned_html = re.sub(
        r'<blockquote>\s*<p>(<strong>Equation\s+8\.[0-9].*?)</p>\s*</blockquote>',
        r'<div class="equation-container">\1</div>',
        raw_body_html,
        flags=re.DOTALL
    )

    # Insert page break before Section 3 so Table 1 starts cleanly at the top of its page
    cleaned_html = re.sub(
        r'<h2>3\.\s*Overall Project Implementation Snapshot</h2>',
        r'<div style="page-break-before: always;"></div><h2>3. Overall Project Implementation Snapshot</h2>',
        cleaned_html
    )

    # Style HTML matching the example report's exact typography
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        @page {{
            size: letter;
            margin: 72pt;
        }}
        body {{
            font-family: "Nimbus Roman", "Times New Roman", serif;
            font-size: 11pt;
            line-height: 1.35;
            color: #000000;
        }}
        h2 {{
            font-size: 16pt;
            font-weight: bold;
            color: #000000;
            margin-top: 18pt;
            margin-bottom: 8pt;
            page-break-after: avoid;
        }}
        h3 {{
            font-size: 13pt;
            font-weight: bold;
            color: #000000;
            margin-top: 14pt;
            margin-bottom: 6pt;
            page-break-after: avoid;
        }}
        h4 {{
            font-size: 11pt;
            font-weight: bold;
            color: #000000;
            margin-top: 10pt;
            margin-bottom: 4pt;
            page-break-after: avoid;
        }}
        p {{
            margin-top: 0;
            margin-bottom: 8pt;
            text-align: justify;
        }}
        ul, ol {{
            margin-top: 0;
            margin-bottom: 8pt;
            padding-left: 20pt;
        }}
        li {{
            margin-bottom: 3pt;
            text-align: justify;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 8pt;
            margin-bottom: 12pt;
            font-size: 10pt;
            page-break-inside: avoid;
        }}
        th, td {{
            border: 0.5pt solid #c0c0c0;
            padding: 4.5pt 6.5pt;
            text-align: left;
        }}
        th {{
            color: #ffffff;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f7faf7;
        }}
        .equation-container {{
            background-color: #fcfcfc;
            border: 0.5pt solid #d8d8d8;
            padding: 6pt 10pt;
            margin: 8pt 0 10pt 0;
            font-size: 10.5pt;
            page-break-inside: avoid;
        }}
        code {{
            font-family: "Courier New", Courier, monospace;
            font-size: 9.5pt;
            background-color: #f3f4f6;
            padding: 1pt 3pt;
        }}
        pre {{
            background-color: #fbfbfb;
            border: 0.5pt solid #d0d0d0;
            padding: 6pt 8pt;
            font-family: "Courier New", Courier, monospace;
            font-size: 8.5pt;
            line-height: 1.25;
            margin-top: 6pt;
            margin-bottom: 10pt;
            page-break-inside: avoid;
        }}
        hr {{
            border: none;
            border-top: 0.5pt solid #d0d0d0;
            margin: 14pt 0;
        }}
        a {{
            color: #000000;
            text-decoration: none;
        }}
    </style>
    </head>
    <body>
    {cleaned_html}
    </body>
    </html>
    """

    # Render Body
    story = pymupdf.Story(html=styled_html)
    writer = pymupdf.DocumentWriter(temp_body_pdf)
    mediabox = pymupdf.Rect(0, 0, 612, 792)
    content_rect = pymupdf.Rect(72, 72, 540, 720)
    story.write(writer, rectfn=lambda n, f: (mediabox, content_rect, None))
    writer.close()

    body_doc = pymupdf.open(temp_body_pdf)
    num_body_pages = len(body_doc)

    # Master Table of Contents schema
    toc_schema = [
        (1, "1. Executive Summary", "1. Executive Summary"),
        (1, "2. Introduction", "2. Introduction"),
        (2, "2.1 Background and Motivation", "2.1 Background and Motivation"),
        (2, "2.2 Objectives", "2.2 Objectives"),
        (2, "2.3 Scope of This Final Report", "2.3 Scope of This Final Report"),
        (1, "3. Overall Project Implementation Snapshot", "3. Overall Project Implementation Snapshot"),
        (1, "4. Scientific Grounding, Literature & Patent Landscape", "4. Scientific Grounding"),
        (2, "4.1 Key Findings from Academic Literature", "4.1 Key Findings from Academic Literature"),
        (2, "4.2 Patent Landscape & Novelty Gaps", "4.2 Patent Landscape & Novelty Gaps"),
        (2, "4.3 Patented Novelty Claims", "4.3 Patented Novelty Claims"),
        (1, "5. Multi-Guild Dataset & Ecological Taxonomy", "5. Multi-Guild Dataset & Ecological Taxonomy"),
        (2, "5.1 Invertebrate Image Corpus", "5.1 Invertebrate Image Corpus"),
        (2, "5.2 Functional Ecological Guild Mapping", "5.2 Functional Ecological Guild Mapping"),
        (1, "6. Deep Learning Detector Architecture & Performance Evaluation", "6. Deep Learning Detector Architecture"),
        (2, "6.1 YOLOv8 & YOLOv11n Baseline Implementations", "6.1 YOLOv8 & YOLOv11n Baseline Implementations"),
        (2, "6.2 Per-Class Performance Metrics", "6.2 Per-Class Performance Metrics"),
        (2, "6.3 Morphological Confusion Analysis", "6.3 Morphological Confusion Analysis"),
        (1, "7. Platform & Hardware System Design", "7. Platform & Hardware System Design"),
        (2, "7.1 UAV Airframe & Payload Bay CAD", "7.1 UAV Airframe & Payload Bay CAD"),
        (2, "7.2 End-to-End Autonomous Data Pipeline", "7.2 End-to-End Autonomous Data Pipeline"),
        (2, "7.3 Guild Isolation Testing Module", "7.3 Guild Isolation Testing Module"),
        (1, "8. Mathematical Biodiversity Engine & Green Credit Formulation", "8. Mathematical Biodiversity Engine"),
        (2, "8.1 Shannon-Wiener Faunal Diversity Index", "8.1 Shannon-Wiener Faunal Diversity Index"),
        (2, "8.2 Simpson's Diversity Index", "8.2 Simpson's Diversity Index"),
        (2, "8.3 Pollinator-to-Pest Ratio", "8.3 Pollinator-to-Pest Ratio"),
        (2, "8.4 Soil Bioturbation Proxy Score", "8.4 Soil Bioturbation Proxy Score"),
        (2, "8.5 Composite Ecological Quality Score & Net Uplift", "8.5 Composite Ecological Quality Score"),
        (2, "8.6 Standardized Green Credit Units & Accreditation Tiers", "8.6 Standardized Green Credit Units"),
        (1, "9. Cryptographic Verification & Tamper-Evident Audit Ledger", "9. Cryptographic Verification"),
        (2, "9.1 Sequential SHA-256 Chained Block Architecture", "9.1 Sequential SHA-256 Chained Block Architecture"),
        (2, "9.2 Cryptographic Anti-Tamper Security Validation", "9.2 Cryptographic Anti-Tamper Security Validation"),
        (2, "9.3 Audit Certificate & GeoJSON Vector Exports", "9.3 Audit Certificate & GeoJSON Vector Exports"),
        (1, "10. System Validation, Simulation Flight Trials & Experimental Results", "10. System Validation"),
        (2, "10.1 Automated Self-Test & Unit Verification", "10.1 Automated Self-Test & Unit Verification"),
        (2, "10.2 Autonomous Transect Simulation Flight Trial", "10.2 Autonomous Transect Simulation Flight Trial"),
        (2, "10.3 Real-Time Ecological & Green Credit HUD Streaming", "10.3 Real-Time Ecological & Green Credit HUD Streaming"),
        (1, "11. Regulatory, Compliance & Environmental Market Impact", "11. Regulatory, Compliance & Environmental Market Impact"),
        (1, "12. Conclusion", "12. Conclusion"),
        (1, "13. References", "13. References"),
    ]

    # Detect exact page numbers from heading text in body pages
    actual_toc = []
    for level, title, pattern in toc_schema:
        assigned_page = None
        for p_idx, page in enumerate(body_doc):
            blocks = page.get_text("dict")["blocks"]
            matched = False
            for b in blocks:
                if "lines" in b:
                    for l in b["lines"]:
                        for s in l["spans"]:
                            if s["size"] >= 12.0 and pattern in s["text"]:
                                assigned_page = p_idx + 3  # Page 1 = Cover, Page 2 = TOC, Body 0 = Page 3
                                matched = True
                                break
                        if matched:
                            break
                if matched:
                    break
            if assigned_page is not None:
                break
        
        # Fallback if not detected by font size
        if assigned_page is None:
            for p_idx, page in enumerate(body_doc):
                if pattern in page.get_text("text"):
                    assigned_page = p_idx + 3
                    break
        
        if assigned_page is None:
            assigned_page = 3
            
        actual_toc.append((level, title, assigned_page))

    # Apply precise dark forest green table header backgrounds on pages where tables actually exist
    for p_idx, page in enumerate(body_doc):
        blocks = page.get_text("blocks")
        for b in blocks:
            txt = b[4].strip()
            if (
                txt.startswith("Work Package")
                or txt.startswith("Ecological\nGuild")
                or txt.startswith("Ecological Guild")
                or txt.startswith("Quality Score (Q)")
            ):
                rect = pymupdf.Rect(72.0, b[1] - 4.5, 540.0, b[3] + 4.5)
                page.draw_rect(rect, fill=(0.18039, 0.32549, 0.22353), overlay=False)

    # Assemble Final Document
    final_doc = pymupdf.open()

    # --- PAGE 1: COVER PAGE (Standalone, Exact Layout) ---
    p1 = final_doc.new_page(width=612, height=792)
    def center_text(page, y, text, font, size):
        w = pymupdf.get_text_length(text, fontname=font, fontsize=size)
        x = (612.0 - w) / 2.0
        page.insert_text(pymupdf.Point(x, y), text, fontname=font, fontsize=size)

    center_text(p1, 184.4, "PROJECT COMPLETION REPORT", "times-bold", 20.0)
    center_text(p1, 222.6, "FALCON: Autonomous Aerial Biodiversity &", "times-bold", 22.0)
    center_text(p1, 246.6, "Nature-Credit Auditing System", "times-bold", 22.0)
    center_text(p1, 276.0, "A Deep-Learning-Powered System for Aerial Micro-Fauna Auditing,", "times-italic", 15.0)
    center_text(p1, 295.0, "Ecological Indexing, and Verifiable Green Credit Issuance", "times-italic", 15.0)
    center_text(p1, 345.0, "Overall Project Completion", "times-bold", 11.0)
    center_text(p1, 372.0, "100%", "times-bold", 24.0)
    center_text(p1, 470.0, "Repository:", "times-bold", 10.0)
    center_text(p1, 486.0, "https://github.com/ashcodes28/FALCON", "times-roman", 10.0)
    center_text(p1, 512.0, "Date of Submission", "times-bold", 10.0)
    center_text(p1, 528.0, "24 October 2026", "times-roman", 10.0)

    # --- PAGE 2: TABLE OF CONTENTS (Standalone, Dot Leaders) ---
    p2 = final_doc.new_page(width=612, height=792)
    p2.insert_text(pymupdf.Point(72.0, 95.0), "Table of Contents", fontname="times-roman", fontsize=16.0)

    y_cursor = 118.0
    line_step = 14.5
    font = "times-roman"
    size = 10.0
    right_edge = 540.0

    def draw_toc_row(page, y, level, title, page_num):
        x_left = 72.0 if level == 1 else 82.0
        title_str = title + " "
        page_str = str(page_num)
        page_w = pymupdf.get_text_length(page_str, fontname=font, fontsize=size)
        
        # Insert title
        page.insert_text(pymupdf.Point(x_left, y), title_str, fontname=font, fontsize=size)
        title_w = pymupdf.get_text_length(title_str, fontname=font, fontsize=size)
        
        # Calculate dot leader string
        dots_x = x_left + title_w
        avail_dots_w = (right_edge - page_w - 4.0) - dots_x
        if avail_dots_w > 0:
            dots = ""
            while pymupdf.get_text_length(dots + ".", fontname=font, fontsize=size) <= avail_dots_w:
                dots += "."
            page.insert_text(pymupdf.Point(dots_x, y), dots, fontname=font, fontsize=size)
            
        # Right-aligned page number
        page.insert_text(pymupdf.Point(right_edge - page_w, y), page_str, fontname=font, fontsize=size)

    # First entry: Table of Contents itself
    draw_toc_row(p2, y_cursor, 1, "Table of Contents", 2)
    y_cursor += line_step

    for level, title, page_num in actual_toc:
        draw_toc_row(p2, y_cursor, level, title, page_num)
        y_cursor += line_step

    # --- INSERT BODY PAGES ---
    for page in body_doc:
        final_doc.insert_pdf(body_doc, from_page=page.number, to_page=page.number)

    final_doc.save(output_pdf)
    final_doc.close()
    body_doc.close()
    del final_doc, body_doc
    gc.collect()

    if os.path.exists(temp_body_pdf):
        try:
            os.remove(temp_body_pdf)
        except Exception:
            pass

    print(f"Report successfully compiled: {output_pdf}")

if __name__ == "__main__":
    build_pdf()
