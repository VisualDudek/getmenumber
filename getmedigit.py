import requests
import PIL
from PIL import Image, ImageFilter
from PIL import ImageOps
from io import BytesIO
import pytesseract


def number(url):

    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    border = (0, 550, 2260, 1350) # left, up, right, bottom
    img = img.crop(border)
    img = img.resize((300, 105), PIL.Image.LANCZOS) # ratio 0,35
    img = img.convert('L')
    img = img.filter(ImageFilter.MedianFilter()) 
    img = img.point(lambda x: 0 if x < 140 else 255) 
    # img.show()

    return pytesseract.image_to_string(img, lang='eng', \
        config='--psm 6 --oem 3')

if __name__ == "__main__":

    # Example urls for testing

    urls = [
        ('https://pbs.twimg.com/media/ETTee-AXYAMo_mc?format=jpg&name=4096x4096', '7899'),
        ('https://pbs.twimg.com/media/ETJLirdWAAENj2v?format=jpg&name=4096x4096', '5493'),
        ('https://pbs.twimg.com/media/ES-ctkBWkAAUPku?format=jpg&name=4096x4096', '2889')
    ]

    for url, test_no in urls:

        res = number(url)
        print(res, test_no, test_no == res)
    
    