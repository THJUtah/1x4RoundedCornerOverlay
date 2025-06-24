import streamlit as st
import fitz  # PyMuPDF
import io

st.title("Rounded-Corner Overlay Tool for Label PDFs")

uploaded_file = st.file_uploader("Upload a vector-based PDF (single label)", type=["pdf"])

if uploaded_file:
    FIXED_RADIUS_INCHES = 0.125  # 1/8 inch
    POINTS_PER_INCH = 72
    fixed_radius_pts = FIXED_RADIUS_INCHES * POINTS_PER_INCH

    # Open PDF
    input_pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    page = input_pdf[0]
    page_rect = page.rect
    width = page_rect.width
    height = page_rect.height

    # Compute safe fractional radius for PyMuPDF
    min_side = min(width, height)
    radius_frac = fixed_radius_pts / min_side
    radius_frac = min(radius_frac, 0.5 - 0.001)  # must be <= 0.5

    # Create the white mask overlay using even-odd fill
    shape = page.new_shape()
    shape.draw_rect(page_rect)  # Outer full-page rectangle
    shape.draw_rect(page_rect, radius=radius_frac)  # Inner rounded rectangle
    shape.finish(fill=(1, 1, 1), even_odd=True, stroke_opacity=0)
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
