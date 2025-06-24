import streamlit as st
import fitz  # PyMuPDF
from tempfile import NamedTemporaryFile
import os

def draw_rounded_rect(page, x0, y0, x1, y1, r, color=(1, 1, 1)):
    # Draws a white rounded rectangle using only legacy-safe methods
    # Top edge
    page.draw_line((x0 + r, y0), (x1 - r, y0), color=None, fill=color, overlay=True)
    # Top-right corner
    page.draw_bezier((x1 - r, y0), (x1, y0), (x1, y0 + r), color=None, fill=color, overlay=True)
    # Right edge
    page.draw_line((x1, y0 + r), (x1, y1 - r), color=None, fill=color, overlay=True)
    # Bottom-right corner
    page.draw_bezier((x1, y1 - r), (x1, y1), (x1 - r, y1), color=None, fill=color, overlay=True)
    # Bottom edge
    page.draw_line((x1 - r, y1), (x0 + r, y1), color=None, fill=color, overlay=True)
    # Bottom-left corner
    page.draw_bezier((x0 + r, y1), (x0, y1), (x0, y1 - r), color=None, fill=color, overlay=True)
    # Left edge
    page.draw_line((x0, y1 - r), (x0, y0 + r), color=None, fill=color, overlay=True)
    # Top-left corner
    page.draw_bezier((x0, y0 + r), (x0, y0), (x0 + r, y0), color=None, fill=color, overlay=True)

def add_rounded_corner_mask(input_path, output_path):
    doc = fitz.open(input_path)
    if len(doc) != 1:
        raise ValueError("Only single-page PDFs are supported.")
    
    page = doc[0]
    page_width, page_height = page.rect.width, page.rect.height

    r = 0.125 * 72  # radius in points (0.125 inches)
    pad = 0.0       # no padding

    x0 = pad
    y0 = pad
    x1 = page_width - pad
    y1 = page_height - pad

    draw_rounded_rect(page, x0, y0, x1, y1, r)
    doc.save(output_path)

# --- Streamlit UI ---
st.set_page_config(page_title="Rounded Corner Overlay", layout="centered")
st.title("🟦 Rounded Corner Overlay for Vector PDFs")
st.write("This tool adds a white overlay with 0.125\" rounded corners for label printing.")

uploaded_file = st.file_uploader("📎 Upload your single-label vector PDF", type=["pdf"])

if uploaded_file and st.button("➕ Generate Overlay"):
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_in:
        tmp_in.write(uploaded_file.read())
        tmp_in.flush()

        output_path = tmp_in.name.replace(".pdf", "_rounded.pdf")
        try:
            add_rounded_corner_mask(tmp_in.name, output_path)

            with open(output_path, "rb") as f:
                st.success("✅ Rounded overlay created successfully!")
                st.download_button("📥 Download PDF", f, "rounded_overlay.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            os.remove(tmp_in.name)
            if os.path.exists(output_path):
                os.remove(output_path)
