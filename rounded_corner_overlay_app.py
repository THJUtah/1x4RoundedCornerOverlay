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
