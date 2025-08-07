import os
import re
import uuid
from weasyprint import HTML
import html as html_escape

def generate_roadmap_pdf(text: str) -> str:
    os.makedirs("generated_roadmaps", exist_ok=True)
    filename = f"roadmap_{uuid.uuid4().hex}.pdf"
    pdf_path = os.path.join("generated_roadmaps", filename)

    def markdown_to_html(text):
        lines = text.split("\n")
        html_lines = []
        in_list = False

        def convert_inline_formatting(line):
            line = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", line)
            line = re.sub(r"\*(.*?)\*", r"<b>\1</b>", line)  # Treat "*" as bold
            return line

        for line in lines:
            stripped = line.strip()
            if not stripped:
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                html_lines.append("<br>")
                continue

            # Handle [label](url) format links
            def replace_links(match):
                label, url = match.groups()
                return f'<a href="{url}" target="_blank">{label}</a>'

            line = re.sub(r'\[(.*?)\]\((https?://[^\s]+)\)', replace_links, stripped)
            line = html_escape.escape(line, quote=False)
            line = line.replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")
            line = line.replace("&lt;i&gt;", "<i>").replace("&lt;/i&gt;", "</i>")
            line = line.replace("&lt;a ", "<a ").replace("&lt;/a&gt;", "</a>").replace("&gt;", ">")

            line = convert_inline_formatting(line)

            # Headings
            if line.lower().startswith("phase") or line.endswith(":"):
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                html_lines.append(f"<h3>{line}</h3>")
                html_lines.append('<hr style="border: none; border-top: 1px solid #ddd; margin: 12px 0;">')

            # Project / Build highlight (standalone block)
            elif any(line[1:].strip().lower().startswith(prefix) for prefix in ["project:", "build:"]) and (line.startswith("-") or line.startswith("*")):
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                html_lines.append(f'<div class="project-box">{line[1:].strip()}</div>')

            # Bullet points
            elif line.startswith("-") or line.startswith("*"):
                if not in_list:
                    html_lines.append("<ul>")
                    in_list = True
                html_lines.append(f"<li>{line[1:].strip()}</li>")

            # Paragraphs
            else:
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                html_lines.append(f"<p>{line}</p>")

        if in_list:
            html_lines.append("</ul>")

        return "\n".join(html_lines)

    html_body = markdown_to_html(text)

    html_template = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                padding: 40px;
                background-color: #ffedd8;
                color: #333;
                line-height: 1.6;
                font-size: 15px;
            }}
            h2 {{
                text-align: center;
                color: #000000;
                margin-bottom: 30px;
            }}
            h3 {{
                color: #1a73e8;
                margin-top: 24px;
                margin-bottom: 8px;
                text-transform: uppercase;
            }}
            hr {{
                border: none;
                border-top: 1px solid #ddd;
                margin: 12px 0;
            }}
            ul {{
                padding-left: 20px;
                margin-top: 0;
                margin-bottom: 16px;
            }}
            li {{
                margin-bottom: 6px;
            }}
            a {{
                color: #1a0dab;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            b {{
                font-weight: bold;
            }}
            .project-box {{
                background-color: #fff8dc;
                padding: 8px 14px;
                border-radius: 6px;
                border: 1px solid #ddd;
                margin-top: 10px;
                margin-bottom: 10px;
                display: block;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
            }}
        </style>
    </head>
    <body>
        <h2>🎯 Personalized Learning Roadmap</h2>
        {html_body}
    </body>
    </html>
    """

    HTML(string=html_template).write_pdf(pdf_path)
    return pdf_path

