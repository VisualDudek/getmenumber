import requests
import PIL
from PIL import Image, ImageFilter
from PIL import ImageOps
from io import BytesIO
import pytesseract

# MZImageReader

class BaniaOCRException(Exception):
    pass

class NegatywneOCRException(Exception):
    pass

class ConsistencyException(Exception):
    pass

def number(url):

    response = requests.get(url)
    img_original = Image.open(BytesIO(response.content))

    # left, up, right, bottom
    borders = [
        (0, 550, 2260, 1350),
        (2300, 400, 2900, 680),
    ]

    img = img_original.crop(borders[0])
    img = img.resize((150, 52), PIL.Image.LANCZOS) # ratio 0,35
    img = img.filter(ImageFilter.MaxFilter(3))
    img = img.filter(ImageFilter.MinFilter(3))
    img = img.getchannel('R')
    img_badania = img.point(lambda x: 0 if x < 140 else 255) 
    # img_badania.show()

    # Negatywne
    img = img_original.crop(borders[1])
    img = img.resize((150, 70), PIL.Image.LANCZOS)
    img = img.filter(ImageFilter.MaxFilter(3))
    img = img.filter(ImageFilter.MinFilter(3))
    img = img.point(lambda x: 0 if x < 200 else 255) 
    img_negatywne = img.getchannel('R')
    # img_negatywne.show()

    res_badania = pytesseract.image_to_string(img_badania, lang='eng', config='--psm 6 --oem 3')

    try:
        res_badania = int(res_badania)
    except ValueError:
        # raise BaniaOCRException(f'OCR return non digit while processing BADANIA: {res_badania}')
        return None, None

    res_negatywne = pytesseract.image_to_string(img_negatywne, lang='eng', config='--psm 6 --oem 3')

    try:
        res_negatywne = int(res_negatywne)
    except ValueError:
        # raise NegatywneOCRException(f'OCR return non digit while processing NEGATYWNE: {res_negatywne}')
        return None, None

    return (res_badania, res_negatywne)

if __name__ == "__main__":

    # Example urls for testing

    urls = [
        ('https://pbs.twimg.com/media/ETdtVtJWAAEn_o_?format=jpg&name=4096x4096', '11196', '10891'),
        ('https://pbs.twimg.com/media/ETYlu89WsAYZrwr?format=jpg&name=4096x4096', '9515', '9269'),
        ('https://pbs.twimg.com/media/ETTee-AXYAMo_mc?format=jpg&name=4096x4096', '7899', '7694'),
        ('https://pbs.twimg.com/media/ETJLirdWAAENj2v?format=jpg&name=4096x4096', '5493', '5382'),
        ('https://pbs.twimg.com/media/ETEd72dWkAE8Cy1?format=jpg&name=4096x4096', '4414', '0000'),
        ('https://pbs.twimg.com/media/ES-ctkBWkAAUPku?format=jpg&name=4096x4096', '2889', '2831'),
        ('https://pbs.twimg.com/media/ES5xff1WsAEzLW4?format=jpg&name=4096x4096', '2234', '2187'),
        ('https://pbs.twimg.com/media/ES0QpA0XsAAaKg8?format=jpg&name=4096x4096', '2024', '1999'),
        ('https://pbs.twimg.com/media/ESu9JMAXsAA8bgB?format=jpg&name=4096x4096', '1630', '1613'),
        ('https://pbs.twimg.com/media/ESrKYwGXkAQF1zc?format=jpg&name=4096x4096', '1384', '1368'),
        ('https://pbs.twimg.com/media/ESliwtcWkAEUAeJ?format=jpg&name=4096x4096', '1154', '1146'),
        ('https://pbs.twimg.com/media/ESbCKZWXsAAKfYB?format=jpg&name=4096x4096', '855', '854'),
    ]

    for url, badania, negatywne in urls:

        badania, negatywne = int(badania), int(negatywne)
        res = number(url)
        print(f'BadaniaOCR: {res[0]}, {badania}; NegatywneOCR: {res[1]}, {negatywne} \
            CHECK: {res[0] == badania} AND {res[1] == negatywne}')
    
    