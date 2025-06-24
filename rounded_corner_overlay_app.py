import streamlit as st
import fitz  # PyMuPDF

# File upload
st.title("Rounded-Corner PDF Overlay")
pdf_file = st.file_uploader("Upload a PDF label", type=["pdf"])
if pdf_file is not None:
    # Open the PDF in PyMuPDF
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    # Input corner radius as percentage of smaller page side (0 to 0.5)
    radius_frac = st.number_input("Corner radius (as fraction of page size)", 
                                  min_value=0.0, max_value=0.5, value=0.1, step=0.05)
    # Iterate over pages and add white rounded rectangle overlay
    for page in doc:
        page_rect = page.rect               # get page dimensions:contentReference[oaicite:10]{index=10}
        shape = page.new_shape()            # create drawing canvas:contentReference[oaicite:11]{index=11}
        # Draw a rectangle covering the page, with rounded corners
        shape.draw_rect(page_rect, radius=radius_frac)   # vector path:contentReference[oaicite:12]{index=12}
        # Finish the path with white fill and no stroke (mask shape)
        shape.finish(fill=(1, 1, 1), color=(1, 1, 1), stroke_opacity=0)  #:contentReference[oaicite:13]{index=13}:contentReference[oaicite:14]{index=14}
        # Commit the shape as an overlay on top of existing content
        shape.commit(overlay=True)          # place in foreground:contentReference[oaicite:15]{index=15}
    # Prepare download
    output_pdf_bytes = doc.write()  # get modified PDF content in memory
    st.download_button("Download PDF with Rounded Overlay", 
                       data=output_pdf_bytes, file_name="rounded_overlay.pdf", 
                       mime="application/pdf")
