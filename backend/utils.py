from fpdf import FPDF
from pathlib import Path
import io
import pandas as pd
from datetime import datetime

class PDF(FPDF):
    def header(self):
        # Title Header
        self.set_font("DejaVu", "B", 16)
        self.cell(0, 10, "Sams Coffee Orders Report", ln=True, align="C")
        self.set_font("DejaVu", "", 11)
        self.cell(0, 8, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")
        self.ln(5)
        # Divider line
        self.set_draw_color(180, 180, 180)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(8)

    def footer(self):
        # Footer with page number
        self.set_y(-15)
        self.set_font("DejaVu", "", 9)
        self.set_text_color(120)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def df_to_pdf(df: pd.DataFrame):
    pdf = PDF()

    # Load font before adding any page
    font_path = Path(__file__).parent.parent / "dejavu-sans" / "DejaVuSans.ttf"
    if not font_path.exists():
        raise FileNotFoundError(f"Font not found at: {font_path.resolve()}")

    # Now safe to add a page
    pdf.add_font("DejaVu", "", str(font_path), uni=True)
    pdf.add_font("DejaVu", "B", str(font_path), uni=True)
    pdf.set_font("DejaVu", "", 11)
    pdf.add_page()

    # Format date columns (remove time)
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime('%Y-%m-%d')

    # Convert 'Items' lists into readable strings
    if "Items" in df.columns:
        df["Items"] = df["Items"].apply(lambda items: ", ".join(items) if isinstance(items, list) else str(items))

    # Auto-adjust column widths (max width 40)
    col_widths = []
    for col in df.columns:
        max_len = max(df[col].astype(str).map(len).max(), len(col))
        col_widths.append(min(max_len * 3.5, 40))

    # Table header
    pdf.set_fill_color(210, 210, 210)
    pdf.set_text_color(0)
    pdf.set_font("DejaVu", "B", 11)
    for i, col in enumerate(df.columns):
        pdf.cell(col_widths[i], 10, col, border=1, align="C", fill=True)
    pdf.ln()

    # Table rows with alternating fills
    pdf.set_font("DejaVu", "", 10)
    fill = False
    for _, row in df.iterrows():
        pdf.set_fill_color(245, 245, 245) if fill else pdf.set_fill_color(255, 255, 255)
        for i, value in enumerate(row):
            pdf.cell(col_widths[i], 8, str(value), border=1, align="C", fill=True)
        pdf.ln()
        fill = not fill

    # Convert PDF to BytesIO
    pdf_bytes = pdf.output(dest="S")
    if isinstance(pdf_bytes, str):
        pdf_bytes = pdf_bytes.encode("latin1")

    pdf_output = io.BytesIO(pdf_bytes)
    pdf_output.seek(0)
    return pdf_output
