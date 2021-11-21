import os
import secrets
from . import app
from PIL import Image


def save_image(form_image):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/img', image_fn)
    output_size = (100, 100)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(image_path)
    return image_fn
