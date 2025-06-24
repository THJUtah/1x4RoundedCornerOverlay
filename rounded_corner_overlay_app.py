import streamlit as st
import fitz  # PyMuPDF
from tempfile import NamedTemporaryFile
import os
from math import pi

def add_rounded_corner_mask(input_path, output_path):
    import fitz
    from math import pi

    src = fitz.open(input_path)
    if len(src) != 1:
        raise ValueError("Only single-page PDFs are supported.")

    page0 = src[0]
    w, h = page0.rect.width, page0.rect.height
    r = 0.125 * 72  # 0.125 inches in points
    k = 0.5522847498  # Bézier arc approximation constant

    # Create new PDF with original page inserted
    doc = fitz.open()
    page = doc.new_page(width=w, height=h)
    page.show_pdf_page(page.rect, src, 0)  # place original content on base layer

    def draw_corner_arc(x, y, angle):
        if angle == 0:  # bottom-right
            p0 = (x, y - r)
            c1 = (x + k * r, y - r)
            c2 = (x + r, y - k * r)
            p1 = (x + r, y)
        elif angle == 90:  # top-right
            p0 = (x - r, y)
            c1 = (x - r, y - k * r)
            c2 = (x - k * r, y - r)
            p1 = (x, y - r)
        elif angle == 180:  # top-left
            p0 = (x, y + r)
            c1 = (x - k * r, y + r)
            c2 = (x - r, y + k * r)
            p1 = (x - r, y)
        elif angle == 270:  # bottom-left
            p0 = (x + r, y)
            c1 = (x + r, y + k * r)
            c2 = (x + k * r, y + r)
            p1 = (x, y + r)
        else:
            return

        # Draw filled Bezier arc
        page.draw_bezier(p0, c1, c2, p1, color=None, fill=(1, 1, 1), overlay=True)
        # Close triangle to center
        page.draw_polyline([p1, (x, y), p0], color=None, fill=(1, 1, 1), closePath=True, overlay=True)

    # Draw all 4 corners
    draw_corner_arc(0, 0, 180)     # top-left
    draw_corner_arc(w, 0, 90)      # top-right
    draw_corner_arc(0, h, 270)     # bottom-left
    draw_corner_arc(w, h, 0)       # bottom-right

    doc.save(output_path)

# --- Streamlit UI ---
st.set_page_config(page_title="Rounded Corner Overlay", layout="centered")
st.title("🟦 Rounded Corner Overlay for Vector PDFs")
st.write("Adds white rounded corners (0.125\") on top of your uploaded label. For use with matrix-removed labels.")

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
