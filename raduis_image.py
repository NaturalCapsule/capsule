import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk


import cairo

# def create_circular_pixbuf(pixbuf):
#     width, height = pixbuf.get_width(), pixbuf.get_height()
#     radius = min(width, height) // 2

#     surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
#     ctx = cairo.Context(surface)

#     ctx.set_source_rgba(0, 0, 0, 0)
#     ctx.set_operator(cairo.Operator.SOURCE)
#     ctx.paint()

#     ctx.set_operator(cairo.Operator.OVER)
#     ctx.arc(width // 2, height // 2, radius, 0, 2 * 3.1416)
#     ctx.clip()

#     gdk_cairo = Gdk.cairo_surface_create_from_pixbuf(pixbuf, 0, None)
#     ctx.set_source_surface(gdk_cairo, 0, 0)
#     ctx.paint()

#     return Gdk.pixbuf_get_from_surface(surface, 0, 0, width, height)

def create_radius_pixbuf(pixbuf):
    width, height = pixbuf.get_width(), pixbuf.get_height()

    corner_radius = 30

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)

    ctx.set_source_rgba(0, 0, 0, 0)
    ctx.set_operator(cairo.Operator.SOURCE)
    ctx.paint()

    ctx.set_operator(cairo.Operator.OVER)
    ctx.move_to(corner_radius, 0)
    ctx.line_to(width - corner_radius, 0)
    ctx.arc(width - corner_radius, corner_radius, corner_radius, 3 * 3.1416 / 2, 2 * 3.1416)
    ctx.line_to(width, height - corner_radius)
    ctx.arc(width - corner_radius, height - corner_radius, corner_radius, 0, 3.1416 / 2)
    ctx.line_to(corner_radius, height)
    ctx.arc(corner_radius, height - corner_radius, corner_radius, 3.1416 / 2, 3.1416)
    ctx.line_to(0, corner_radius)
    ctx.arc(corner_radius, corner_radius, corner_radius, 3.1416, 3 * 3.1416 / 2)
    ctx.close_path()

    bite_radius = corner_radius // 2  
    bite_angle_start = 1.5 
    bite_angle_end = 2.0   

    ctx.arc(corner_radius, corner_radius, bite_radius, bite_angle_start * 3.1416, bite_angle_end * 3.1416)
    ctx.line_to(corner_radius, corner_radius)

    ctx.clip()

    gdk_cairo = Gdk.cairo_surface_create_from_pixbuf(pixbuf, 0, None)
    ctx.set_source_surface(gdk_cairo, 0, 0)

    ctx.paint()

    return Gdk.pixbuf_get_from_surface(surface, 0, 0, width, height)