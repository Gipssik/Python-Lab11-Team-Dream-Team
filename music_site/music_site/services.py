import os
import secrets

from . import app
from PIL import Image


def save_image(form_image):
    random_hex = secrets.token_hex(32)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/img', image_fn)
    output_size = (100, 100)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(image_path)
    return image_fn


def save_audio(audio):
    random_hex = secrets.token_hex(32)
    _, f_ext = os.path.splitext(audio.filename)
    audio_fn = random_hex + f_ext
    audio_path = os.path.join(app.root_path, 'static/songs', audio_fn)

    if not os.path.exists(os.path.join(app.root_path, 'static/songs')):
        try:
            original_umask = os.umask(0)
            os.makedirs(audio_path, 0o0777)
        finally:
            os.umask(original_umask)

    with open(audio_path, 'wb') as file:
        file.write(audio.read())

    return audio_fn
