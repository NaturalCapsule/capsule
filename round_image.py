import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk


import cairo

def create_circular_pixbuf(pixbuf):
    width, height = pixbuf.get_width(), pixbuf.get_height()
    radius = min(width, height) // 2

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)

    ctx.set_source_rgba(0, 0, 0, 0)
    ctx.set_operator(cairo.Operator.SOURCE)
    ctx.paint()

    ctx.set_operator(cairo.Operator.OVER)
    ctx.arc(width // 2, height // 2, radius, 0, 2 * 3.1416)
    ctx.clip()

    gdk_cairo = Gdk.cairo_surface_create_from_pixbuf(pixbuf, 0, None)
    ctx.set_source_surface(gdk_cairo, 0, 0)
    ctx.paint()

    return Gdk.pixbuf_get_from_surface(surface, 0, 0, width, height)