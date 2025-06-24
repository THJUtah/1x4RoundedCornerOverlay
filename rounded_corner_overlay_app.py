import streamlit as st
import fitz  # PyMuPDF
import io

# === Constants ===
FIXED_RADIUS_INCHES = 0.125  # 1/8 inch
POINTS_PER_INCH = 72
FIXED_RADIUS_PTS = FIXED_RADIUS_INCHES * POINTS_PER_INCH

st.title("Rounded-Corner Overlay Tool for Label PDFs")

uploaded_file = st.file_uploader("Upload a vector-based PDF (single label)", type=["pdf"])

if uploaded_file:
    # Open PDF
    input_pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    page = input_pdf[0]
    page_rect = page.rect

    # Clamp radius to avoid overflow errors
    max_radius = min(page_rect.width, page_rect.height) / 2.0
    corner_radius_pt = min(FIXED_RADIUS_PTS, max_radius - 0.1)

    # Create the white mask overlay using even-odd fill
    shape = page.new_shape()
    shape.draw_rect(page_rect)  # Outer full-page rectangle
    shape.draw_rect(page_rect, radius=corner_radius_pt)  # Inner rounded rectangle
    shape.finish(fill=(1, 1, 1), even_odd=True)  # Fill outside rounded rectangle
    shape.commit(overlay=True)

    # Save to buffer
    output_buffer = io.BytesIO()
    input_pdf.save(output_buffer)
    input_pdf.close()

    # Download button
    st.success("Overlay applied successfully!")
    st.download_button(
        label="Download PDF with Rounded-Corner Mask",
        data=output_buffer.getvalue(),
        file_name="rounded_corner_label.pdf",
        mime="application/pdf"
    )
