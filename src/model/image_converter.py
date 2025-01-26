import base64
import io

from PIL import Image, ImageTk


def open_image(image):
    return Image.open(image)


def photo_image(image):
    return ImageTk.PhotoImage(image)


def tk_image(data, size=(15, 15)): 
    return ImageTk.PhotoImage(decode_image(data, size))


def decode_image(data, size):
    i = open_image(io.BytesIO(base64.b64decode(data)))
    i.thumbnail(size, Image.Resampling.LANCZOS) 
    n = Image.new('RGBA', (size[0] + 5, size[1]), (0, 0, 0, 0)) 
    x = (size[0] - i.width) // 2  
    y = (size[1] - i.height) // 2  
    n.paste(i, (x, y)) 
    return n
