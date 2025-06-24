import streamlit as st
import fitz  # PyMuPDF
from tempfile import NamedTemporaryFile
import os

def add_rounded_corner_mask(input_path, output_path):
    doc = fitz.open(input_path)
    if len(doc) != 1:
        raise ValueError("Only single-page PDFs are supported.")

    page = doc[0]
    page_width, page_height = page.rect.width, page.rect.height

    r = 0.125 * 72  # 0.125 inch corner radius
    pad = 0.0

    x0 = pad
    y0 = pad
    x1 = page_width - pad
    y1 = page_height - pad

    # Draw 4 white circles to mask the corners
    page.draw_circle(center=(x0 + r, y0 + r), radius=r, color=None, fill=(1, 1, 1), overlay=True)  # top-left
    page.draw_circle(center=(x1 - r, y0 + r), radius=r, color=None, fill=(1, 1, 1), overlay=True)  # top-right
    page.draw_circle(center=(x0 + r, y1 - r), radius=r, color=None, fill=(1, 1, 1), overlay=True)  # bottom-left
    page.draw_circle(center=(x1 - r, y1 - r), radius=r, color=None, fill=(1, 1, 1), overlay=True)  # bottom-right

    # Draw center and side rectangles to complete the mask
    page.draw_rect(fitz.Rect(x0 + r, y0, x1 - r, y1), color=None, fill=(1, 1, 1), overlay=True)  # horizontal center
    page.draw_rect(fitz.Rect(x0, y0 + r, x1, y1 - r), color=None, fill=(1, 1, 1), overlay=True)  # vertical sides

    doc.save(output_path)

# --- Streamlit UI ---
st.set_page_config(page_title="Rounded Corner Overlay", layout="centered")
st.title("🟦 Rounded Corner Overlay for Vector PDFs")
st.write("Adds a white mask with 0.125\" simulated rounded corners (legacy-compatible).")

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
