import streamlit as st
import fitz  # PyMuPDF

doc = fitz.open("input_label.pdf")
page = doc[0]

# Define the page/label rectangle and the corner radius
page_rect = page.rect
corner_radius = 20  # example radius in points (adjust as needed)

# Create a new Shape for the overlay
shape = page.new_shape()

# Draw outer boundary (full page rectangle) and inner rounded rectangle
shape.draw_rect(page_rect)  # outer rectangle (covers full page)
shape.draw_rect(page_rect, radius=corner_radius)  # inner rounded-corner rect

# Finish the shape with white fill, using even-odd rule to hollow out the center
# (This fills outside the rounded rect)
shape.finish(fill=(1, 1, 1), even_odd=True)

# (Optional for debugging: add a visible border to the inner shape to verify curvature)
# shape.finish(color=(1, 0, 0), width=0.5, fill=(1, 1, 1), even_odd=True)

# Commit the overlay in the foreground
shape.commit(overlay=True)

doc.save("output_label_with_mask.pdf")
