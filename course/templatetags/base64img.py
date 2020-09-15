import base64

def get_image_file_as_base64_data():
    with open(FILEPATH, 'r') as image_file:
        return base64.b64encode(image_file.read())