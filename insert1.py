#!python3
# -*- coding: utf-8 -*-
# for linux: 
# sudo apt-get install python3-fontforge
# for venv: pyvenv.cfg -> include-system-site-packages = true

import fontforge
import psMat

def scale(glyph, scalex, scaley):
    glyph.transform(psMat.scale(scalex, scaley))

def adjust_glyph_scale(source_font, template_font, scaley, is_italic):
    # for attr in ['ascent', 'descent',
    #             'hhea_ascent', 'hhea_ascent_add',
    #             'hhea_linegap',
    #             'hhea_descent', 'hhea_descent_add',
    #             'os2_winascent', 'os2_winascent_add',
    #             'os2_windescent', 'os2_windescent_add',
    #             'os2_typoascent', 'os2_typoascent_add',
    #             'os2_typodescent', 'os2_typodescent_add',
    #             ]:
    #     setattr(source_font, attr, getattr(template_font, attr))    
    for glyph in source_font.selection.byGlyphs:
        _scaley = scaley
        if not is_italic:
            # custom fix for specific cases
            # fontforge not copy some glyphs, instead combine them from existing symbols
            # as example cyryllic Ы = b + I, real width = 550*2, but fontforge set it to 550*4
            if chr(glyph.unicode) == 'й': 
                glyph.right_side_bearing = 550
                glyph.width = 550
                continue
            if chr(glyph.unicode) == 'Ы':
                glyph.width = 1100
                _scaley = 1

        if (glyph.width - 550 > 10e-5):
            scalex = 550/glyph.width
            scale(glyph, scalex, _scaley)
            glyph.right_side_bearing = 550
            glyph.width = 550

def generate_merged_font(font, name):
    font.selection.all()
    font.fontname += name
    font.fullname += name
    font.generate('output/' + font.fontname + '.otf')

def merge(i_from, i_to, is_italic):
    scaley = i_to.capHeight / i_from.capHeight
    i_from.selection.select(("ranges", None), ord("А"), ord("я"))
    i_from.copy()
    i_to.selection.select(("ranges", None), ord("А"), ord("я"))
    i_to.paste()
    print(i_to.fontname)
    adjust_glyph_scale(i_to, i_from, scaley, is_italic)
    generate_merged_font(i_to, 'Merged')

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
    f.selection.all()
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

comic = fontforge.open('input/comic_i.ttf')
comic_nerd = fontforge.open('input/comic_nerd.otf')
merge(comic, comic_nerd, 1)

comic_i = fontforge.open('input/comic_i.ttf')
comic_nerd_i = generate_italic('input/comic_nerd.otf', 'Italic', 'ComicShannsMono Nerd Font Italic', 'ComicShannsMonoNF-italic', 'italic')
merge(comic_i, comic_nerd_i, 1)

comic_b = fontforge.open('input/comicbi.ttf')
comic_nerd_b = fontforge.open('input/comic_nerd_b.otf')
merge(comic_b, comic_nerd_b, 1)

comic_bi = fontforge.open('input/comicbi.ttf')
comic_nerd_bi = generate_italic('input/comic_nerd_b.otf', 'Bold Italic', 'ComicShannsMono Nerd Font Bold Italic', 'ComicShannsMonoNF-BoldItalic', 'bolditalic')
merge(comic_bi, comic_nerd_bi, 1)


