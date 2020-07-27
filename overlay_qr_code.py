"""Overlay unique QR codes on PNG poster and export to multi-page PDF"""
import copy
from PIL import Image
import qrcode

# USER INPUT
# QR code placement
X_COORDINATE = int(input('QR distance from left (pixels): '))
Y_COORDINATE = int(input('QR distance from top (pixels): '))
SIZE = int(input('QR size (pixels): '))
# File paths
INPUT_FILE_PATH = input('Relative file path to poster PNG: ')
OUTPUT_FILE_PATH = input('Relative output file path for PDF: ')
# QR code URL data
POSTER_TYPE = input('Type identifier for poster (e.g. "a"): ')
LINK_ID_START = int(input('First poster number: '))
LINK_ID_END = int(input('Last poster number: '))

BASE_POSTER = Image.open(INPUT_FILE_PATH).convert('RGB')

POSTER_IMAGES = []
for poster_number in range(LINK_ID_START, LINK_ID_END+1):
    QR_DATA = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=30,
        border=0,
    )
    QR_DATA.add_data('https://link.valueourminds.com/poster/' + POSTER_TYPE + str(poster_number))
    QR_DATA.make(fit=True)
    QR_CODE_IMAGE = QR_DATA.make_image().resize((SIZE, SIZE))
    POSTER_IMAGE = copy.deepcopy(BASE_POSTER)
    POSTER_IMAGE.paste(QR_CODE_IMAGE, box=(X_COORDINATE, Y_COORDINATE))
    POSTER_IMAGES.append(POSTER_IMAGE)

POSTER_IMAGES[0].save(OUTPUT_FILE_PATH, 'PDF', resolution=100.0, save_all=True, append_images=POSTER_IMAGES[1:])
print('PDF exported to ' + OUTPUT_FILE_PATH)
