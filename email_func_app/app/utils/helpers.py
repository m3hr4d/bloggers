"""Helper utilities."""
import os
import secrets
from PIL import Image
from flask import current_app

def save_image(form_image, upload_folder):
    """Save uploaded image with a secure filename."""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(current_app.root_path, 'static', upload_folder, image_fn)

    # Resize image
    output_size = (500, 500)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(image_path)

    return image_fn

def allowed_file(filename):
    """Check if file extension is allowed."""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_filename(original_filename):
    """Generate a secure filename."""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(original_filename)
    return random_hex + f_ext
