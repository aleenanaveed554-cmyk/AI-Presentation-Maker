from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE


def get_theme_colors(theme):

    themes = {
        "Modern Dark": {
            "background": RGBColor(10, 15, 35),
            "accent": RGBColor(124, 58, 237),
            "title": RGBColor(255, 255, 255),
            "text": RGBColor(220, 225, 240)
        },

        "Professional Blue": {
            "background": RGBColor(15, 35, 70),
            "accent": RGBColor(37, 99, 235),
            "title": RGBColor(255, 255, 255),
            "text": RGBColor(220, 230, 245)
        },

        "Purple Gradient": {
            "background": RGBColor(35, 20, 60),
            "accent": RGBColor(168, 85, 247),
            "title": RGBColor(255, 255, 255),
            "text": RGBColor(235, 225, 250)
        },

        "Minimal White": {
            "background": RGBColor(248, 250, 252),
            "accent": RGBColor(79, 70, 229),
            "title": RGBColor(15, 23, 42),
            "text": RGBColor(51, 65, 85)
        },

        "Academic": {
            "background": RGBColor(20, 35, 30),
            "accent": RGBColor(34, 197, 94),
            "title": RGBColor(255, 255, 255),
            "text": RGBColor(220, 235, 225)
        },

        "Technology": {
            "background": RGBColor(5, 25, 35),
            "accent": RGBColor(6, 182, 212),
            "title": RGBColor(255, 255, 255),
            "text": RGBColor(215, 240, 245)
        }
    }

    return themes.get(theme, themes["Modern Dark"])


def add_background(slide, color):

    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        0,
        0,
        Inches(13.333),
        Inches(7.5)
    )

    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()

    # Send background behind everything
    slide.shapes._spTree.remove(shape._element)
    slide.shapes._spTree.insert(2, shape._element)


def add_accent(slide, color):

    accent = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0),
        Inches(0),
        Inches(0.18),
        Inches(7.5)
    )

    accent.fill.solid()
    accent.fill.fore_color.rgb = color
    accent.line.fill.background()


def add_text(
    slide,
    text,
    left,
    top,
    width,
    height,
    font_size,
    color,
    bold=False
):

    textbox = slide.shapes.add_textbox(
        Inches(left),
        Inches(top),
        Inches(width),
        Inches(height)
    )

    tf = textbox.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]

    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.name = "Aptos"
    p.font.color.rgb = color

    return textbox


def create_pptx(slides, topic, theme):

    prs = Presentation()

    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    colors = get_theme_colors(theme)

    # -------------------------
    # Title slide
    # -------------------------

    slide = prs.slides.add_slide(
        prs.slide_layouts[6]
    )

    add_background(
        slide,
        colors["background"]
    )

    add_accent(
        slide,
        colors["accent"]
    )

    add_text(
        slide,
        "AI PRESENTATION",
        1.0,
        1.5,
        8,
        0.5,
        18,
        colors["accent"],
        True
    )

    add_text(
        slide,
        topic,
        1.0,
        2.2,
        11,
        1.5,
        40,
        colors["title"],
        True
    )

    add_text(
        slide,
        "Generated with AI Presentation Maker",
        1.0,
        4.1,
        8,
        0.5,
        17,
        colors["text"]
    )

    add_text(
        slide,
        f"Theme: {theme}",
        1.0,
        5.0,
        6,
        0.5,
        14,
        colors["text"]
    )

    # -------------------------
    # Content slides
    # -------------------------

    for index, item in enumerate(slides):

        slide = prs.slides.add_slide(
            prs.slide_layouts[6]
        )

        add_background(
            slide,
            colors["background"]
        )

        add_accent(
            slide,
            colors["accent"]
        )

        add_text(
            slide,
            f"0{index + 1}" if index < 9 else str(index + 1),
            0.7,
            0.55,
            1,
            0.4,
            14,
            colors["accent"],
            True
        )

        add_text(
            slide,
            item.get("title", ""),
            1.4,
            0.55,
            10.5,
            0.8,
            30,
            colors["title"],
            True
        )

        points = item.get("points", [])

        y_position = 1.7

        for point in points:

            # Bullet circle
            circle = slide.shapes.add_shape(
                MSO_SHAPE.OVAL,
                Inches(1.4),
                Inches(y_position + 0.08),
                Inches(0.14),
                Inches(0.14)
            )

            circle.fill.solid()
            circle.fill.fore_color.rgb = colors["accent"]
            circle.line.fill.background()

            add_text(
                slide,
                point,
                1.75,
                y_position,
                10.2,
                0.65,
                18,
                colors["text"]
            )

            y_position += 1.0

        # Footer
        add_text(
            slide,
            f"AI Presentation Maker  •  {index + 1}",
            1.4,
            7.0,
            8,
            0.3,
            10,
            colors["text"]
        )

    # -------------------------
    # Save to memory
    # -------------------------

    output = BytesIO()

    prs.save(output)

    output.seek(0)

    return output.getvalue()
