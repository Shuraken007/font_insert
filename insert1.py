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
    scaley = 1
    for glyph in font.selection.byGlyphs:
        if glyph.width > 550:
            scalex = 550/glyph.width
            scale(glyph, scalex, scaley)
            glyph.right_side_bearing = 550
            glyph.width = 550

def generate_merged_font(font, name):
    # font.selection.all()
    font.fontname += name
    font.fullname += name
    font.generate('output/' + font.fontname + '.otf')

def merge(font):
    font.selection.select(("ranges", None), ord("А"), ord("я"))
    font.paste()
    print(font.fontname)
    generate_merged_font(font, 'Merged')

_weightToStyleMap = {
    # fsSelection: Set bit 6 ("REGULAR").
    'normal': (0x40, 0),

    # fsSelection: Set bit 6 ("REGULAR").
    'medium': (0x40, 0),

    # fsSelection: Set bits 0 ("ITALIC") and 9 ("OBLIQUE").
    # macStyle: Set bit 1 (which presumably also means "ITALIC").
    'italic': (0x201, 0x2),

    # fsSelection: Set bit 5 ("BOLD").
    # macStyle: Set bit 0 (which presumably also means "BOLD").
    'bold': (0x20, 0x1),

    # fsSelection: Set bits 0 ("ITALIC"), 9 ("OBLIQUE") and 5 ("BOLD").
    # macStyle: Set bits 1 (italic) and 0 (bold).
    'bolditalic': (0x221, 0x3),
}

def generate_italic(path, subfamily, fullname, postscriptname, os2_weight):
    f = fontforge.open(path)
    # f.selection.all()
    f.italicangle = -12
    f.italicize(italic_angle = -12)

    f.sfnt_names = (
        ('English (US)', 'SubFamily', subfamily),
        ('English (US)', 'Fullname', fullname),
        ('English (US)', 'PostScriptName', postscriptname),
        ('English (US)', 'UniqueID', fullname),
    ) + f.sfnt_names

    styleMap, macStyle = _weightToStyleMap[os2_weight]

    f.os2_stylemap |= styleMap
    f.macstyle |= macStyle

    f.fontname = fullname
    f.fullname = fullname    

    return f

macStyle = 0b11 # 0b01 - Bold; 0b10 - Italic

ms_sans = fontforge.open('input/from.otf')
ms_sans.selection.select(("ranges", None), ord("А"), ord("я"))
adjust_glyph_scale(ms_sans)
ms_sans.copy()

comic_nerd = fontforge.open('input/comic_nerd.otf')
merge(comic_nerd)

comic_i = fontforge.open('input/comic_i.ttf')
comic_nerd_i = generate_italic('input/comic_nerd.otf', 'Italic', 'ComicShannsMono Nerd Font Italic', 'ComicShannsMonoNF-italic', 'italic')
merge(comic_nerd_i)

comic_b = fontforge.open('input/comicbi.ttf')
comic_nerd_b = fontforge.open('input/comic_nerd_b.otf')
merge(comic_nerd_b)

comic_bi = fontforge.open('input/comicbi.ttf')
comic_nerd_bi = generate_italic('input/comic_nerd_b.otf', 'Bold Italic', 'ComicShannsMono Nerd Font Bold Italic', 'ComicShannsMonoNF-BoldItalic', 'bolditalic')
merge(comic_nerd_bi)


