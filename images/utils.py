from PIL import Image as PILImage
import os
from io import BytesIO
from images.models import Thumbnail


def create_thumbnails(image_obj, image_file):

    thumbnail_sizes = [100, 200, 300]  # Rozmiary miniatur do utworzenia

    with PILImage.open(image_file) as im:
        original_width, original_height = im.size
        for height in thumbnail_sizes:
            image_name, image_extension = os.path.splitext(image_file.name)
            image_extension = image_extension.lower()
            if image_extension == '.jpg':
                image_extension = '.jpeg'
            thumbnail_name = f"{image_name}_thumbnail_{height}{image_extension}"
            aspect_ratio = original_width / original_height
            new_width = int(aspect_ratio * height)
            im.thumbnail((new_width, height))
            buffer = BytesIO()
            if image_extension == '.jpeg':
                im.save(buffer, format='JPEG', quality=85)
            else:
                im.save(buffer, image_extension.replace('.', ''))
            thumbnail_obj = Thumbnail.objects.create(name=thumbnail_name, image=image_obj)
            thumbnail_obj.thumbnail.save(thumbnail_name, buffer)