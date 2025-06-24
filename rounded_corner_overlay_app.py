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

    # Draw 4 corner white circles to fake rounded mask cutouts
    # Top-left
    page.draw_circle(center=(x0 + r, y0 + r), radius=r, color=None, fill=(1, 1, 1), overlay=True)
    # Top-right
    page.draw_circle(center=(x1 - r, y0 + r), radius=r, color=None, fill=(1, 1, 1), overlay=True)
    # Bottom-left
    page.draw_circle(center=(x0 + r, y1 - r), radius=r, color=None, fill=(1, 1, 1), overlay=True)
    # Bottom-right
    page.draw_circle(center=(x1 - r, y1 - r), radius=r, color=None, fill=(1, 1, 1), overlay=True)

    # Draw white rectangles over the straight sides and center
    page.draw_rect(fitz.Rect(x0 + r, y0, x1 - r, y1), color=None, fill=(1, 1, 1), overlay=True)  # center
    page.draw_rect(fitz.Rect(x0, y0 + r, x1, y1 - r), color=None, fill=(1, 1, 1), overlay=True)  # vertical sides

    doc.save(output_path)
