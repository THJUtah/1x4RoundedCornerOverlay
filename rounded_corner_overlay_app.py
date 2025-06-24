def add_rounded_corner_mask(input_path, output_path):
    import fitz
    doc = fitz.open(input_path)
    if len(doc) != 1:
        raise ValueError("Only single-page PDFs are supported.")

    page = doc[0]
    w, h = page.rect.width, page.rect.height
    r = 0.125 * 72  # 0.125 inch radius in points

    # Helper to draw a filled white quarter arc mask using bezier curves
    def quarter_arc(center, start_angle_deg):
        # Approximating a quarter circle using 2 Bézier curves
        from math import cos, sin, pi

        path = page.new_shape()

        theta = start_angle_deg * pi / 180
        k = 0.5522847498  # Bézier constant to approximate a circle

        x, y = center

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

    # Draw four rounded corner cutouts
    quarter_arc((0, 0), 180)           # top-left
    quarter_arc((w, 0), 90)            # top-right
    quarter_arc((0, h), 270)           # bottom-left
    quarter_arc((w, h), 0)             # bottom-right

    doc.save(output_path)
