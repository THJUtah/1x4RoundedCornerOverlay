import streamlit as st
import fitz  # PyMuPDF
import io

st.title("Rounded-Corner Overlay Tool for Label PDFs")

uploaded_file = st.file_uploader("Upload a vector-based PDF (single label)", type=["pdf"])

if uploaded_file:
    # Constants
    FIXED_RADIUS_INCHES = 0.125
    POINTS_PER_INCH = 72
    fixed_radius_pts = FIXED_RADIUS_INCHES * POINTS_PER_INCH

    # Load PDF
    input_pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    page = input_pdf[0]
    page_rect = page.rect

    # Convert to fraction for draw_rect()
    radius_frac = fixed_radius_pts / min(page_rect.width, page_rect.height)
    radius_frac = min(radius_frac, 0.5 - 0.001)

    # Create overlay shape
    shape = page.new_shape()

    # Outer full-page rect
    shape.draw_rect(page_rect)

    # Slightly smaller inner rect to prevent antialiasing edge
    inset = 0.5  # pt
    inner_rect = fitz.Rect(
        page_rect.x0 + inset,
        page_rect.y0 + inset,
        page_rect.x1 - inset,
        page_rect.y1 - inset
    )
    shape.draw_rect(inner_rect, radius=radius_frac)

    # Fill with white, no stroke
    shape.finish(fill=(1, 1, 1), even_odd=True, stroke_opacity=0)
    shape.commit(overlay=True)

    # Save to buffer
    output_buffer = io.BytesIO()
    input_pdf.save(output_buffer)
    input_pdf.close()

    # Download
    st.success("Overlay applied successfully!")
    st.download_button(
        label="Download PDF with Rounded-Corner Mask",
        data=output_buffer.getvalue(),
        file_name="rounded_corner_label.pdf",
        mime="application/pdf"
    )
