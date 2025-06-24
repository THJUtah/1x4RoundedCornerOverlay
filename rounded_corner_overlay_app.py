import streamlit as st
import fitz  # PyMuPDF
import io

# Convert inches to PDF points (1 in = 72 pts)
def inches_to_points(inches):
    return inches * 72

st.title("Rounded-Corner Overlay for Label PDFs")

uploaded_file = st.file_uploader("Upload a vector-based single-page PDF", type=["pdf"])

# Default radius: 0.125 in (1/8")
corner_radius_in = st.number_input("Corner Radius (inches)", min_value=0.01, value=0.125, step=0.01)

if uploaded_file:
    # Convert radius to points
    corner_radius_pt = inches_to_points(corner_radius_in)

    # Load uploaded PDF
    input_pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    # Work on first page only (single label)
    page = input_pdf[0]
    page_rect = page.rect

    # Create overlay shape
    shape = page.new_shape()

    # Outer rect (full page)
    shape.draw_rect(page_rect)

    # Inner rounded rect (label area to preserve)
    shape.draw_rect(page_rect, radius=corner_radius_pt)

    # Fill white using even-odd fill rule (masks only the corners)
    shape.finish(fill=(1, 1, 1), even_odd=True)

    # Apply overlay
    shape.commit(overlay=True)

    # Save to memory buffer
    output_buffer = io.BytesIO()
    input_pdf.save(output_buffer)
    input_pdf.close()

    # Show download button
    st.success("Rounded-corner overlay applied!")
    st.download_button(
        label="Download Modified PDF",
        data=output_buffer.getvalue(),
        file_name="rounded_overlay_label.pdf",
        mime="application/pdf"
    )
