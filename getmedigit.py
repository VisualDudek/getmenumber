import requests
from PIL import Image
from PIL import ImageOps
from io import BytesIO
import pytesseract


def number(url):

    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    border = (0, 550, 2260, 1350) # left, up, right, bottom
    cropped = img.crop(border)

    return pytesseract.image_to_string(cropped, lang='eng', \
        config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789')

if __name__ == "__main__":

    # Example urls for testing
    # url = 'https://pbs.twimg.com/media/ETTee-AXYAMo_mc?format=jpg&name=4096x4096'
    # url = 'https://pbs.twimg.com/media/ETJLirdWAAENj2v?format=jpg&name=4096x4096'
    url = 'https://pbs.twimg.com/media/ES-ctkBWkAAUPku?format=jpg&name=4096x4096'

    print(number(url))
    
    