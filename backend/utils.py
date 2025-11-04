from fpdf import FPDF
from pathlib import Path
import io

def df_to_pdf(df):
    pdf = FPDF()
    pdf.add_page()

    # Find the font relative to this file
    font_path = Path(__file__).parent.parent / "dejavu-sans" / "DejaVuSans.ttf"

    if not font_path.exists():
        raise FileNotFoundError(f"Font not found at: {font_path.resolve()}")

    pdf.add_font("DejaVu", "", str(font_path), uni=True)
    pdf.set_font("DejaVu", "", 12)

    # Title
    pdf.cell(0, 10, "Filtered Orders Report", ln=True, align="C")
    pdf.ln(5)

    # Table
    col_width = pdf.w / len(df.columns) - 5
    for col in df.columns:
        pdf.cell(col_width, 10, str(col), border=1)
    pdf.ln()
    for _, row in df.iterrows():
        for value in row:
            pdf.cell(col_width, 10, str(value), border=1)
        pdf.ln()

    # Save to BytesIO
    pdf_bytes = pdf.output(dest="S")
    if isinstance(pdf_bytes, str):
        pdf_bytes = pdf_bytes.encode("latin1")

    pdf_output = io.BytesIO(pdf_bytes)
    pdf_output.seek(0)
    return pdf_output

