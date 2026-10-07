"""Replaceable export adapters: paper, answer key, or worked solutions.
No private source metadata is included. Advanced TeX remains a future adapter;
current exporters use the authored prose explanation and symbol-safe fonts.
"""
import base64, os
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape
from docx import Document
from docx.oxml import parse_xml
from docx.shared import Inches, Pt, RGBColor
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .mathtext import inline_to_unicode, latex_to_omml, latex_to_unicode, split_inline

ASSETS=Path(__file__).resolve().parents[2]/"frontend"/"public"/"brand"

def add_text(doc,text,style=None):
    """A paragraph whose $…$ segments become real, editable Word equations."""
    p=doc.add_paragraph(style=style)
    for is_math,chunk in split_inline(text or ""):
        if is_math: p._p.append(parse_xml(latex_to_omml(chunk)))
        else: p.add_run(chunk)
    return p

def add_formula(doc,latex):
    p=doc.add_paragraph()
    p._p.append(parse_xml(latex_to_omml(latex)))
    return p

def image_bytes(c):
    return BytesIO(base64.b64decode(c["asset"].split(",",1)[1])) if c.get("asset") else None

def credit(q):
    if q.source.get('kind') not in ('textbook-excerpt','adapted-textbook'):return None
    prefix='Adapted from' if q.source['kind']=='adapted-textbook' else 'From'
    return f"{prefix} LearningExpress, 501 Challenging Logic and Reasoning Problems, 2nd ed., question {q.source['question_number']}."

def render_export(questions,format,kind,title):
    output=BytesIO()
    if format=="docx":
        doc=Document()
        normal=doc.styles["Normal"]; normal.font.name="Arial"; normal.font.size=Pt(11)
        normal.paragraph_format.space_after=Pt(8)
        if (ASSETS/"me-logo.png").exists(): doc.add_picture(str(ASSETS/"me-logo.png"),width=Inches(.6))
        doc.add_heading(title,0)
        doc.add_paragraph("Logic practice • Multiple choice • Select one answer per question")
        doc.sections[0].footer.paragraphs[0].text="Mechanical Engineering @ RUPP · Theory → Practice → Reflection → Improvement"
        for i,q in enumerate(questions,1):
            c=q.content
            doc.add_heading(f"{i}. {q.difficulty}",2)
            add_text(doc,c["stem"])
            if credit(q):doc.add_paragraph(credit(q))
            if kind!="key":
                if image_bytes(c): doc.add_picture(image_bytes(c),width=Inches(4.5))
                if c.get("diagram"):
                    labels=c["diagram"]["labels"]
                    table=doc.add_table(rows=1,cols=len(labels)); table.style="Table Grid"
                    for cell,label in zip(table.rows[0].cells,labels): cell.text=str(label)
                for o in c["options"]: add_text(doc,f"{o['id']}. {o['text']}")
            if kind in ("key","solutions"): doc.add_paragraph(f"Answer: {c['correct']}")
            if kind=="solutions":
                add_text(doc,c["explanation"])
                if c.get("math"): add_formula(doc,c["math"])
                for o in c["options"]:
                    if o["id"]!=c["correct"]: add_text(doc,f"{o['id']}: {o['rationale']}")
        doc.save(output)
        return output.getvalue(),"application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    font="Helvetica"
    for path in [os.getenv("EXPORT_FONT",""),"C:/Windows/Fonts/arial.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if path and Path(path).exists():
            pdfmetrics.registerFont(TTFont("ExportSans",path)); font="ExportSans"; break
    styles=getSampleStyleSheet()
    body=ParagraphStyle("Body",fontName=font,fontSize=10.5,leading=16,spaceAfter=8)
    head=ParagraphStyle("Head",parent=body,fontSize=19,leading=25,textColor=colors.HexColor("#0B2D4D"),spaceAfter=14)
    small=ParagraphStyle("Small",parent=body,fontSize=8,leading=12)
    story=[]
    if (ASSETS/"me-logo.png").exists():
        logo=Image(str(ASSETS/"me-logo.png"),width=42,height=42,kind="proportional"); logo.hAlign="LEFT"; story.append(logo)
    story.extend([Paragraph(escape(title),head),Paragraph("Logic practice · Select one answer per question",body),Spacer(1,12)])
    for i,q in enumerate(questions,1):
        c=q.content
        story.append(Paragraph(escape(inline_to_unicode(f"{i}. {c['stem']}")),body))
        if credit(q):story.append(Paragraph(escape(credit(q)),small))
        if kind!="key":
            raw=image_bytes(c)
            if raw:
                im=Image(raw); ratio=min(430/im.imageWidth,230/im.imageHeight); im.drawWidth=im.imageWidth*ratio; im.drawHeight=im.imageHeight*ratio; story.append(im)
            if c.get("diagram"):
                labels=c["diagram"]["labels"]
                table=Table([[Paragraph(escape(str(x)),small) for x in labels]],colWidths=[430/len(labels)]*len(labels))
                table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#EAF2F8")),("BOX",(0,0),(-1,-1),.5,colors.HexColor("#0B2D4D")),("INNERGRID",(0,0),(-1,-1),.5,colors.HexColor("#D9DEE3")),("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)])); story.append(table); story.append(Spacer(1,8))
            for o in c["options"]: story.append(Paragraph(escape(inline_to_unicode(f"{o['id']}. {o['text']}")),body))
        if kind in ("key","solutions"): story.append(Paragraph(escape(f"Answer: {c['correct']}"),body))
        if kind=="solutions":
            story.append(Paragraph(escape(inline_to_unicode(c["explanation"])),body))
            if c.get("math"): story.append(Paragraph(escape(latex_to_unicode(c["math"])),body))
            for o in c["options"]:
                if o["id"]!=c["correct"]: story.append(Paragraph(escape(inline_to_unicode(f"{o['id']}: {o['rationale']}")),small))
        story.append(Spacer(1,16))
    def footer(canvas,doc):
        canvas.setFont(font,8); canvas.setFillColor(colors.HexColor("#0B2D4D"))
        canvas.drawString(48,30,"Mechanical Engineering @ RUPP · Logic practice")
        canvas.drawRightString(547,30,str(doc.page))
    SimpleDocTemplate(output,rightMargin=48,leftMargin=48,topMargin=42,bottomMargin=48).build(story,onFirstPage=footer,onLaterPages=footer)
    return output.getvalue(),"application/pdf"
