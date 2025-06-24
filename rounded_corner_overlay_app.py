import streamlit as st
import fitz  # PyMuPDF
from tempfile import NamedTemporaryFile
import os

DPI = 72  # PDF point resolution

def add_rounded_corner_mask(input_path, output_path, radius_pts, padding_pts):
    doc = fitz.open(input_path)
    if len(doc) != 1:
        raise ValueError("Only single-page PDFs are supported.")

    page = doc[0]
    page_width, page_height = page.rect.width, page.rect.height

    # Define the rectangle with optional padding
    rect = fitz.Rect(
        padding_pts,
        padding_pts,
        page_width - padding_pts,
        page_height - padding_pts
    )

    # Draw white rounded rectangle
    shape = page.new_shape()
    shape.draw_rect(rect, round=radius_pts)
    shape.finish(color=None, fill=(1, 1, 1), overlay=True)
    shape.commit()

    doc.save(output_path)

# --- Streamlit UI ---
st.set_page_config(page_title="Rounded Corner Mask", layout="centered")
st.title("🟦 Rounded Corner Mask Overlay for Vector PDFs")
st.write("This tool adds a white rounded rectangle overlay to simulate label corner cuts.")

uploaded_file = st.file_uploader("Upload a vector-based single-page PDF", type=["pdf"])

radius_in = st.number_input("Corner Radius (inches)", min_value=0.01, value=0.125, step=0.01)
padding_in = st.number_input("Padding (inches)", min_value=0.0, value=0.0, step=0.01)

if uploaded_file and st.button("Generate Rounded Corner PDF"):
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_in:
        tmp_in.write(uploaded_file.read())
        tmp_in.flush()

        output_path = tmp_in.name.replace(".pdf", "_rounded.pdf")
        try:
            add_rounded_corner_mask(
                tmp_in.name,
                output_path,
                radius_pts=radius_in * DPI,
                padding_pts=padding_in * DPI
            )

            with open(output_path, "rb") as f:
                st.success("✅ Overlay created successfully!")
                st.download_button(
                    label="Download PDF with Rounded Corners",
                    data=f,
                    file_name="rounded_overlay.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            os.remove(tmp_in.name)
            if os.path.exists(output_path):
                os.remove(output_path)
