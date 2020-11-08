"""Overlay unique QR codes on PNG poster and export to multi-page PDF"""
import copy
import json
import math
from PIL import Image
import qrcode
import random

BASE_36_CHARACTERS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# USER INPUT
# QR code placement
X_COORDINATE = int(input('QR distance from left (pixels): '))
Y_COORDINATE = int(input('QR distance from top (pixels): '))
SIZE = int(input('QR size (pixels): '))
# File paths
INPUT_FILE_PATH = input('Relative file path to poster PNG: ')
# QR code URL data
POSTER_TYPE = input('Destination URL ID (e.g. "0"): ')
assert len(POSTER_TYPE) == 1 and POSTER_TYPE in BASE_36_CHARACTERS
NUMBER_OF_POSTERS = int(input('Number of posters: '))

BASE_POSTER = Image.open(INPUT_FILE_PATH).convert('RGB')

# TODO: Import used links from posters that have already been generated
print('WARNING: Potential link conflicts with existing posters')
USED_LINK_IDS = []
POSTER_IMAGES = []
while len(USED_LINK_IDS) < NUMBER_OF_POSTERS:
    link_id = POSTER_TYPE + '/'
    for n in range(5):
        link_id += random.choice(BASE_36_CHARACTERS)
    if link_id in USED_LINK_IDS:
        continue

    USED_LINK_IDS.append(link_id)
    QR_DATA = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=30,
        border=0,
    )
    QR_DATA.add_data('HTTPS://L.VALUEOURMINDS.COM/' + link_id)
    QR_DATA.make(fit=True)
    QR_CODE_IMAGE = QR_DATA.make_image().resize((SIZE, SIZE))
    POSTER_IMAGE = copy.deepcopy(BASE_POSTER)
    POSTER_IMAGE.paste(QR_CODE_IMAGE, box=(X_COORDINATE, Y_COORDINATE))
    POSTER_IMAGES.append(POSTER_IMAGE)

# Export a maximum of 50 pages per PDF for easier printing
for n in range(math.ceil(NUMBER_OF_POSTERS/50)):
    first_poster_index = 0 + 50*n
    last_poster_index = 49 + 50*n
    if last_poster_index > NUMBER_OF_POSTERS-1:
        last_poster_index = NUMBER_OF_POSTERS-1
    file_name = f'output-{n+1}.pdf'
    POSTER_IMAGES[first_poster_index].save(file_name, 'PDF', resolution=100.0, save_all=True, append_images=POSTER_IMAGES[first_poster_index+1:last_poster_index+1])
    print(f'PDF exported to {file_name}')

with open('output-poster-ids.json', 'w') as file:
    json.dump(USED_LINK_IDS, file)
print('Poster IDs exported to output-poster-ids.json')
