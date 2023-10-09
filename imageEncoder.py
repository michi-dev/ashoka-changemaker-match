import base64
from PIL import Image

def encodeImage(image_path): 
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')
        return f'''data:image/png;base64,{base64_image}'''

