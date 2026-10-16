import imghdr
def is_png(data: bytes) -> bool:
    return imghdr.what(None, h=data) == "png"
