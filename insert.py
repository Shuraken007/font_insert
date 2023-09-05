#!python3
# -*- coding: utf-8 -*-
# for linux: 
# sudo apt-get install python3-fontforge
# for venv: pyvenv.cfg -> include-system-site-packages = true

import fontforge
import psMat

def scale(glyph, scalex, scaley):
    glyph.transform(psMat.scale(scalex, scaley))

def adjust_glyph_scale(font):
    for glyph in font.selection.byGlyphs:
        if glyph.width > 550:
            scalex = 550/glyph.width
            scaley = 1
            scale(glyph, scalex, scaley)
            glyph.right_side_bearing = 550
            glyph.width = 550

def generate_font(font, name):
    font.selection.all()
    font.fontname = name
    font.fullname = name
    font.generate(name + '.otf')

i_to = fontforge.open('input/to.otf')
i_from = fontforge.open('input/from.otf')

i_from.selection.select(("ranges", None), ord("А"), ord("я"))
i_from.copy()
i_to.selection.select(("ranges", None), ord("А"), ord("я"))
i_to.paste()
adjust_glyph_scale(i_to)

generate_font(i_to, 'Merged')
