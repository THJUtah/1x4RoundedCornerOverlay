import streamlit as st
import fitz  # PyMuPDF
from tempfile import NamedTemporaryFile
import os
from math import pi

def add_rounded_corner_mask(input_path, output_path):
    doc = fitz.open(input_path)
    if len(doc) != 1:
        raise ValueError("Only single-page PDFs are supported.")

    page = doc[0]
    w, h = page.rect.width, page.rect.height
    r = 0.125 * 72  # 0.125 inches in points
    k = 0.5522847498  # Bezier arc constant

    def draw_corner_arc(center, angle):
        x, y = center

        if angle == 0:  # bottom-right
            p0 = (x, y - r)
            c1 = (x + k*r, y - r)
            c2 = (x + r, y - k*r)
            p1 = (x + r, y)
        elif angle == 90:  # top-right
            p0 = (x - r, y)
            c1 = (x - r, y - k*r)
            c2 = (x - k*r, y - r)
            p1 = (x, y - r)
        elif angle == 180:  # top-left
            p0 = (x, y + r)
            c1 = (x - k*r, y + r)
            c2 = (x - r, y + k*r)
            p1 = (x - r, y)
        elif angle == 270:  # bottom-left
            p0 = (x + r, y)
            c1 = (x + r, y + k*r)
            c2 = (x + k*r, y + r)
            p1 = (x, y + r)
        else:
            return

        # Fill the quarter arc with 3-point polygon + Bezier
        page.draw_bezier(p0, c1, c2, p1, color=None, overlay=True)
        page.draw_line(p1, (x, y))  # close triangle edge
        page.draw_line((x, y), p0)  # close triangle edge

    # Draw each corner arc
    draw_corner_arc((0, 0), 180)       # top-left
    draw_corner_arc((w, 0), 90)        # top-right
    draw_corner_arc((0, h), 270)       # bottom-left
    draw_corner_arc((w, h), 0)         # bottom-right

    doc.save(output_path)

# --- Streamlit UI ---
st.set_page_config(page_title="Rounded Corner Overlay", layout="centered")
st.title("🟦 Rounded Corner Overlay for Vector PDFs")
st.write("Simulates a 0.125\" radius by masking just the label corners. Fully print-safe and legacy compatible.")

uploaded_file = st.file_uploader("📎 Upload a single-label vector PDF", type=["pdf"])

if uploaded_file and st.button("➕ Generate Overlay"):
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_in:
        tmp_in.write(uploaded_file.read())
        tmp_in.flush()

        output_path = tmp_in.name.replace(".pdf", "_rounded.pdf")
        try:
            add_rounded_corner_mask(tmp_in.name, output_path)

            with open(output_path, "rb") as f:
                st.success("✅ Overlay created successfully!")
                st.download_button("📥 Download PDF", f, "rounded_overlay.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            os.remove(tmp_in.name)
            if os.path.exists(output_path):
                os.remove(output_path)
