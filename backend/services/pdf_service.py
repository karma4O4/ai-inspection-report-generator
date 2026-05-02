import os
import io
import requests
from PIL import Image as PILImage
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically render page numbers "Page X of Y" 
    and custom headers/footers on every page.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#475569")) # Slate 600
        
        # Draw Running Header
        self.drawString(54, 750, "AI Professional Property Inspection Report")
        self.setStrokeColor(colors.HexColor("#cbd5e1")) # Slate 300
        self.setLineWidth(0.5)
        self.line(54, 742, 558, 742)
        
        # Draw Running Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 40, page_text)
        self.drawString(54, 40, "Confidential - Inspection Services")
        self.line(54, 52, 558, 52)
        
        self.restoreState()

class PDFService:
    @staticmethod
    def fetch_image_safely(image_url: str) -> io.BytesIO:
        """
        Safely reads local upload image or downloads remote URL image,
        resizes to proper scale to avoid PDF page overflows, and returns a file-like byte stream.
        """
        try:
            if image_url.startswith("http"):
                # Fetch remote
                r = requests.get(image_url, timeout=10)
                img_data = io.BytesIO(r.content)
            else:
                # Local static path or absolute path
                # Strip leading slash if present
                clean_path = image_url.lstrip("/")
                
                # Try finding relative path in backend dir
                possible_paths = [
                    image_url,
                    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), clean_path),
                    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static", "uploads", os.path.basename(image_url))
                ]
                
                img_data = None
                for p in possible_paths:
                    if os.path.exists(p) and os.path.isfile(p):
                        with open(p, "rb") as f:
                            img_data = io.BytesIO(f.read())
                        break
                
                if not img_data:
                    raise FileNotFoundError(f"Local file not found in paths: {possible_paths}")
            
            # Load with PIL to resize/validate format
            pil_img = PILImage.open(img_data)
            
            # Convert to RGB (in case of PNG alpha or weird colorspaces causing ReportLab crash)
            if pil_img.mode in ("RGBA", "P"):
                pil_img = pil_img.convert("RGB")
            
            # Compress and resize to maximum width of 450px to fit on PDF elegantly
            pil_img.thumbnail((450, 320))
            
            out_bytes = io.BytesIO()
            pil_img.save(out_bytes, format="JPEG", quality=85)
            out_bytes.seek(0)
            return out_bytes
            
        except Exception as e:
            print(f"Error fetching/formatting image {image_url}: {e}")
            # Return a blank white thumbnail placeholder image
            try:
                placeholder = PILImage.new("RGB", (300, 200), color="#e2e8f0")
                out_bytes = io.BytesIO()
                placeholder.save(out_bytes, format="JPEG")
                out_bytes.seek(0)
                return out_bytes
            except:
                return None

    @classmethod
    def generate_report_pdf(cls, report_data: dict, images: list) -> bytes:
        """
        Creates a beautifully designed property inspection report in PDF.
        Returns the PDF file contents as raw bytes.
        """
        pdf_buffer = io.BytesIO()
        
        # A4 margins (54pt = 0.75 in)
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=A4,
            leftMargin=54,
            rightMargin=54,
            topMargin=72,
            bottomMargin=72
        )
        
        styles = getSampleStyleSheet()
        
        # Custom Premium Styles (Deep Navy #1e3a8a, Charcoal #0f172a, Slate #475569)
        title_style = ParagraphStyle(
            name="ReportTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            textColor=colors.HexColor("#1e3a8a"),
            spaceAfter=15
        )
        
        meta_label_style = ParagraphStyle(
            name="MetaLabel",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=12,
            textColor=colors.HexColor("#475569")
        )
        
        meta_value_style = ParagraphStyle(
            name="MetaValue",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=12,
            textColor=colors.HexColor("#0f172a")
        )
        
        h1_style = ParagraphStyle(
            name="H1Style",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#1e3a8a"),
            spaceBefore=15,
            spaceAfter=8,
            keepWithNext=True
        )

        h2_style = ParagraphStyle(
            name="H2Style",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#1e3a8a"),
            spaceBefore=10,
            spaceAfter=4,
            keepWithNext=True
        )
        
        body_style = ParagraphStyle(
            name="BodyStyle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#334155")
        )
        
        desc_style = ParagraphStyle(
            name="DescriptionStyle",
            parent=styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor("#0f172a")
        )
        
        tag_style = ParagraphStyle(
            name="TagStyle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=11,
            textColor=colors.HexColor("#ffffff")
        )
        
        story = []
        
        # --- TITLE BLOCK & META ---
        story.append(Spacer(1, 10))
        story.append(Paragraph(report_data.get("report_title", "Inspection Report").upper(), title_style))
        story.append(Spacer(1, 10))
        
        # Metadata grid table
        meta_data = [
            [
                Paragraph("CLIENT NAME:", meta_label_style),
                Paragraph(report_data.get("client_name", "N/A"), meta_value_style),
                Paragraph("DATE OF INSPECTION:", meta_label_style),
                Paragraph(str(report_data.get("inspection_date", "N/A")), meta_value_style),
            ],
            [
                Paragraph("SITE LOCATION:", meta_label_style),
                Paragraph(report_data.get("site_name", "N/A"), meta_value_style),
                Paragraph("REPORT STATUS:", meta_label_style),
                Paragraph(report_data.get("status", "Draft").capitalize(), meta_value_style),
            ]
        ]
        
        meta_table = Table(meta_data, colWidths=[110, 140, 130, 120])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")), # Slate 50
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 20))
        
        # --- EXECUTIVE SUMMARY / CONCLUSION ---
        story.append(Paragraph("Executive Summary & Conclusions", h1_style))
        conclusion_text = report_data.get("conclusion") or "No conclusion has been compiled for this report yet."
        story.append(Paragraph(conclusion_text, body_style))
        story.append(Spacer(1, 25))
        
        # --- IMAGES AND DEFECT FINDINGS ---
        story.append(Paragraph("Detailed Photographic Findings", h1_style))
        
        if not images:
            story.append(Paragraph("No inspection images have been uploaded to this report yet.", body_style))
        else:
            for idx, img in enumerate(images, start=1):
                image_elements = []
                
                # Subheader for the photo
                cat_name = img.get("category") or "General Maintenance"
                image_elements.append(Paragraph(f"Item #{idx}: {cat_name}", h2_style))
                
                # Fetch image bytes safely
                img_bytes = cls.fetch_image_safely(img.get("image_url"))
                
                # Prepare visual details
                desc_text = img.get("edited_description") or img.get("ai_description") or "No inspection notes recorded."
                ocr_text = img.get("ocr_text")
                
                details_data = [
                    [Paragraph(f"<b>Category:</b> {cat_name}", body_style)],
                    [Spacer(1, 3)],
                    [Paragraph(f"<b>Inspector Findings & Analysis:</b><br/>{desc_text}", desc_style)]
                ]
                
                if ocr_text:
                    details_data.append([Spacer(1, 3)])
                    details_data.append([Paragraph(f"<b>Extracted Photo Text (OCR):</b> {ocr_text}", body_style)])
                
                # Photo Details block Table
                details_table = Table(details_data, colWidths=[240])
                details_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 5),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                    ('TOPPADDING', (0, 0), (-1, -1), 0),
                ]))
                
                # Side-by-side Table layout: [Image, Spacer, Details Table]
                if img_bytes:
                    try:
                        rep_img = Image(img_bytes, width=220, height=155)
                        rep_img.hAlign = 'LEFT'
                        
                        finding_row = [rep_img, Spacer(1, 10), details_table]
                        finding_table = Table([finding_row], colWidths=[220, 10, 240])
                        finding_table.setStyle(TableStyle([
                            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                            ('LEFTPADDING', (0, 0), (-1, -1), 0),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                        ]))
                        
                        image_elements.append(finding_table)
                    except Exception as ex:
                        print(f"Failed to load image in ReportLab flowable: {ex}")
                        image_elements.append(Paragraph("[Image failed to load in report]", body_style))
                else:
                    image_elements.append(details_table)
                
                image_elements.append(Spacer(1, 15))
                
                # Keep each image item details together on a page so it doesn't break mid-image
                story.append(KeepTogether(image_elements))
        
        # Build document
        doc.build(story, canvasmaker=NumberedCanvas)
        
        pdf_bytes = pdf_buffer.getvalue()
        pdf_buffer.close()
        return pdf_bytes
