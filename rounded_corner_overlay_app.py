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
    r = 0.125 * 72  # 0.125 inch corner radius in points

    # Draw quarter arc in a corner using Bezier approximation
    def quarter_arc(center, start_angle_deg):
        k = 0.5522847498  # constant for circular arc approximation

        x, y = center
        path = page.new_shape()

        if start_angle_deg == 0:  # bottom-right
            p0 = (x, y - r)
            p1 = (x + k*r, y - r)
            p2 = (x + r, y - k*r)
            p3 = (x + r, y)
        elif start_angle_deg == 90:  # top-right
            p0 = (x - r, y)
            p1 = (x - r, y - k*r)
            p2 = (x - k*r, y - r)
            p3 = (x, y - r)
        elif start_angle_deg == 180:  # top-left
            p0 = (x, y + r)
            p1 = (x - k*r, y + r)
            p2 = (x - r, y + k*r)
            p3 = (x - r, y)
        elif start_angle_deg == 270:  # bottom-left
            p0 = (x + r, y)
            p1 = (x + r, y + k*r)
            p2 = (x + k*r, y + r)
            p3 = (x, y + r)
        else:
            return

        path.move_to(x, y)
        path.line_to(*p0)
        path.curve_to(p1, p2, p3)
        path.close_path()
        path.finish(color=None, fill=(1, 1, 1), overlay=True)
        path.commit()

    # Draw masks in all 4 corners
    quarter_arc((0, 0), 180)       # top-left
    quarter_arc((w, 0), 90)        # top-right
    quarter_arc((0, h), 270)       # bottom-left
    quarter_arc((w, h), 0)         # bottom-right

    doc.save(output_path)

# --- Streamlit UI ---
st.set_page_config(page_title="Rounded Corner Overlay", layout="centered")
st.title("🟦 Rounded Corner Overlay for Vector PDFs")
st.write("Adds a white corner mask with 0.125\" rounded radius for label printing. Vector-safe, legacy-compatible.")

uploaded_file = st.file_uploader("📎 Upload a single-label vector PDF", type=["pdf"])

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
