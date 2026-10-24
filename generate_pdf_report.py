"""
Compiles FALCON_100_Percent_Implementation_Report.md into a formatted PDF
matching the styling and structure of the project progress report.
"""

import re
import pymupdf
import markdown_it

def build_pdf():
    # Read Markdown source
    with open("FALCON_100_Percent_Implementation_Report.md", "r", encoding="utf-8") as f:
        md_text = f.read()

    # Convert Markdown to HTML
    md = markdown_it.MarkdownIt("commonmark").enable("table")
    raw_html = md.render(md_text)

    # Clean and style HTML
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        @page {{
            size: letter;
            margin: 54pt;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            font-size: 10pt;
            line-height: 1.55;
            color: #1a1a1a;
        }}
        h1 {{
            font-size: 18pt;
            font-weight: 700;
            color: #111827;
            border-bottom: 1.5pt solid #e5e7eb;
            padding-bottom: 4pt;
            margin-top: 22pt;
            margin-bottom: 10pt;
            page-break-after: avoid;
        }}
        h2 {{
            font-size: 14pt;
            font-weight: 600;
            color: #1f2937;
            margin-top: 18pt;
            margin-bottom: 8pt;
            page-break-after: avoid;
        }}
        h3 {{
            font-size: 11pt;
            font-weight: 600;
            color: #374151;
            margin-top: 12pt;
            margin-bottom: 6pt;
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
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10pt;
            margin-bottom: 14pt;
            font-size: 9pt;
            page-break-inside: avoid;
        }}
        th, td {{
            border: 0.5pt solid #d1d5db;
            padding: 5pt 7pt;
            text-align: left;
        }}
        th {{
            background-color: #f3f4f6;
            font-weight: 600;
            color: #111827;
        }}
        tr:nth-child(even) {{
            background-color: #f9fafb;
        }}
        code {{
            font-family: "Courier New", Courier, monospace;
            font-size: 8.5pt;
            background-color: #f3f4f6;
            padding: 1pt 3pt;
            border-radius: 2pt;
        }}
        pre {{
            background-color: #f8fafc;
            border: 0.5pt solid #e2e8f0;
            border-left: 3pt solid #10b981;
            padding: 8pt;
            font-family: "Courier New", Courier, monospace;
            font-size: 8pt;
            line-height: 1.4;
            overflow-x: auto;
            margin-top: 6pt;
            margin-bottom: 10pt;
            page-break-inside: avoid;
        }}
        blockquote {{
            border-left: 3pt solid #3b82f6;
            margin: 8pt 0;
            padding-left: 10pt;
            color: #4b5563;
            font-style: italic;
        }}
        hr {{
            border: none;
            border-top: 0.5pt solid #e5e7eb;
            margin: 16pt 0;
        }}
        a {{
            color: #2563eb;
            text-decoration: none;
        }}
    </style>
    </head>
    <body>
    {raw_html}
    </body>
    </html>
    """

    temp_pdf = "_temp_report.pdf"
    output_pdf = "FALCON_100_Percent_Implementation_Report.pdf"
    
    # Story layout
    story = pymupdf.Story(html=styled_html)
    writer = pymupdf.DocumentWriter(temp_pdf)
    
    # Standard Letter: 612 x 792 pt, 54 pt margins
    mediabox = pymupdf.Rect(0, 0, 612, 792)
    content_rect = pymupdf.Rect(54, 54, 558, 738)
    
    story.write(writer, rectfn=lambda n, f: (mediabox, content_rect, None))
    writer.close()
    
    # Post-process with PyMuPDF to add header & footer page numbering
    doc = pymupdf.open(temp_pdf)
    total_pages = len(doc)
    
    for i, page in enumerate(doc):
        # Header (pages after page 1)
        if i > 0:
            page.insert_text(
                pymupdf.Point(54, 38),
                "FALCON: 100% Final Implementation Report | ashcodes28/FALCON",
                fontsize=8,
                color=(0.4, 0.4, 0.4),
            )
            page.draw_line(
                pymupdf.Point(54, 42),
                pymupdf.Point(558, 42),
                color=(0.8, 0.8, 0.8),
                width=0.5,
            )
        
        # Footer
        footer_text = f"Page {i + 1} of {total_pages}"
        page.draw_line(
            pymupdf.Point(54, 750),
            pymupdf.Point(558, 750),
            color=(0.8, 0.8, 0.8),
            width=0.5,
        )
        page.insert_text(
            pymupdf.Point(280, 764),
            footer_text,
            fontsize=8,
            color=(0.4, 0.4, 0.4),
        )

    doc.save(output_pdf)
    doc.close()
    del doc
    
    import gc, os
    gc.collect()
    if os.path.exists(temp_pdf):
        try:
            os.remove(temp_pdf)
        except Exception:
            pass
        
    print(f"[FALCON] PDF successfully compiled: {output_pdf} ({total_pages} pages)")

if __name__ == "__main__":
    build_pdf()
