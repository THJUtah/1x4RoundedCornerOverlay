import streamlit as st
import fitz  # PyMuPDF
from tempfile import NamedTemporaryFile
import os
from math import pi

def add_rounded_corner_mask(input_path, output_path):
    import fitz
    from math import pi

    doc = fitz.open(input_path)
    if len(doc) != 1:
        raise ValueError("Only single-page PDFs are supported.")

    page = doc[0]
    w, h = page.rect.width, page.rect.height
    r = 0.125 * 72  # radius in points

    # Constant to approximate a circle with Bézier curves
    k = 0.5522847498

    # --- Draw quarter arc shapes manually using Bezier paths ---
    def draw_quarter_corner(x, y, angle):
        # Creates a 90-degree arc from the corner inward
        if angle == 0:  # bottom-right
            start = (x, y - r)
            c1 = (x + k*r, y - r)
            c2 = (x + r, y - k*r)
            end = (x + r, y)
        elif angle == 90:  # top-right
            start = (x - r, y)
            c1 = (x - r, y - k*r)
            c2 = (x - k*r, y - r)
            end = (x, y - r)
        elif angle == 180:  # top-left
            start = (x, y + r)
            c1 = (x - k*r, y + r)
            c2 = (x - r, y + k*r)
            end = (x - r, y)
        elif angle == 270:  # bottom-left
            start = (x + r, y)
            c1 = (x + r, y + k*r)
            c2 = (x + k*r, y + r)
            end = (x, y + r)
        else:
            return

        # Draw triangle corner + arc
        page.draw_line((x, y), start, color=None, fill=(1, 1, 1), overlay=True)
        page.draw_bezier(start, c1, c2, end, color=None, fill=(1, 1, 1), overlay=True)
        page.draw_line(end, (x, y), color=None, fill=(1, 1, 1), overlay=True)

    draw_quarter_corner(0, 0, 180)     # top-left
    draw_quarter_corner(w, 0, 90)      # top-right
    draw_quarter_corner(0, h, 270)     # bottom-left
    draw_quarter_corner(w, h, 0)       # bottom-right

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
