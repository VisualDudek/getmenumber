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
    img = img.resize((150, 52), PIL.Image.LANCZOS) # ratio 0,35
    img = img.getchannel('R')
    img = img.point(lambda x: 0 if x < 140 else 255) 
    # img.show()

    return pytesseract.image_to_string(img, lang='eng', \
        config='--psm 6 --oem 3')

if __name__ == "__main__":

    # Example urls for testing

    urls = [
        ('https://pbs.twimg.com/media/ETYlu89WsAYZrwr?format=jpg&name=4096x4096', '9515'),
        ('https://pbs.twimg.com/media/ETTee-AXYAMo_mc?format=jpg&name=4096x4096', '7899'),
        ('https://pbs.twimg.com/media/ETJLirdWAAENj2v?format=jpg&name=4096x4096', '5493'),
        ('https://pbs.twimg.com/media/ETEd72dWkAE8Cy1?format=jpg&name=4096x4096', '4414'),
        ('https://pbs.twimg.com/media/ES-ctkBWkAAUPku?format=jpg&name=4096x4096', '2889'),
        ('https://pbs.twimg.com/media/ES5xff1WsAEzLW4?format=jpg&name=4096x4096', '2234'),
        ('https://pbs.twimg.com/media/ES0QpA0XsAAaKg8?format=jpg&name=4096x4096', '2024'),
        ('https://pbs.twimg.com/media/ESu9JMAXsAA8bgB?format=jpg&name=4096x4096', '1630'),
        ('https://pbs.twimg.com/media/ESrKYwGXkAQF1zc?format=jpg&name=4096x4096', '1384'),
        ('https://pbs.twimg.com/media/ESliwtcWkAEUAeJ?format=jpg&name=4096x4096', '1154'),
        ('https://pbs.twimg.com/media/ESbCKZWXsAAKfYB?format=jpg&name=4096x4096', '855'),
    ]

    for url, test_no in urls:

        res = number(url)
        print(res, test_no, test_no == res)
    
    