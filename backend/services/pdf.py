import markdown2
from weasyprint import HTML



html = """
# Top title (ATX)

Subtitle (setext)
-----------------

### An even lower heading (ATX)

**Text in bold**

_Text in italics_

~~Strikethrough~~

[This is a link](https://github.com/PyFPDF/fpdf2)

<https://py-pdf.github.io/fpdf2/>

This is an unordered list:
* an item
* another item

This is an ordered list:
1. first item
2. second item
3. third item with an unordered sublist:
    * an item
    * another item

Inline `code span`

A table:

| Foo | Bar | Baz |
| ---:|:---:|:--- |
| Foo | Bar | Baz |

Actual HTML:

<dl>
  <dt>Term1</dt><dd>Definition1</dd>
  <dt>Term2</dt><dd>Definition2</dd>
</dl>

Some horizontal thematic breaks:

***
---
___

![Alternate description](https://py-pdf.github.io/fpdf2/fpdf2-logo.png)
"""



def markdown_to_pdf(markdown_text: str) -> bytes:
    html_body = markdown2.markdown(markdown_text,extras=["fenced-code-blocks", "tables", "strike"])

    styled_html = f"""
    <html>
    <head>
        <style>
            @page {{
                size: A4;
                margin: 2.5cm;
            }}

            body {{
                font-family: "Helvetica", "Arial", sans-serif;
                font-size: 12pt;
                line-height: 1.7;
                color: #222;
            }}

            p {{
                margin: 0 0 12px 0;
            }}

            h1, h2, h3, h4 {{
                margin-top: 24px;
                margin-bottom: 12px;
                page-break-after: avoid;
            }}

            h1 {{ font-size: 24pt; }}
            h2 {{ font-size: 18pt; }}
            h3 {{ font-size: 14pt; }}

            ul, ol {{
                margin-left: 20px;
                margin-bottom: 12px;
            }}

            li {{
                margin-bottom: 6px;
            }}

            code {{
                background: #f4f4f4;
                padding: 2px 4px;
                font-family: monospace;
                font-size: 10pt;
            }}

            pre {{
                background: #f4f4f4;
                padding: 10px;
                overflow-wrap: break-word;
                page-break-inside: avoid;
            }}

            blockquote {{
                border-left: 4px solid #ccc;
                padding-left: 12px;
                color: #555;
                margin: 12px 0;
            }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """

    return HTML(string=styled_html).write_pdf()



# markdown_to_pdf(html)