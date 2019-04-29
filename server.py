from flask import Flask, request, send_file
from PIL import Image
from io import BytesIO
import requests
import random

app = Flask(__name__)


@app.route('/mozaika')
def mozaika():
    arg_losowo = request.args.get('losowo')
    arg_rozdzielczosc = request.args.get('rozdzielczosc')
    arg_zdjecia = request.args.get('zdjecia')

    url_list = arg_zdjecia.split(',')
    img_list = []
    for x in url_list:
        img_list.append(convert_url(x))

    if (arg_losowo != None and arg_losowo == "1"):
        random.shuffle(img_list)

    if (arg_rozdzielczosc != None):
        rozdzielczosc = arg_rozdzielczosc.split('x')
        try:
            mozaika = Image.new('RGB', (int(rozdzielczosc[0]), int(rozdzielczosc[1])))
        except ValueError:
            print('Invalid value of "rozdzielczosc" argument!')
            return None
    else:
        mozaika = Image.new('RGB', (2048, 2048))

    merge_mozaika(mozaika, img_list)
    mozaika.save('mozaika.jpg')
    return send_file('mozaika.jpg', mimetype='image/jpg')


def convert_url(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))


def merge_mozaika(mozaika, img_list):
    X, Y = mozaika.size
    rows=[]

    if (mozaika.size[0] < mozaika.size[1]):  # pionowy kształt
        if (len(img_list) == 1):
            rows.append([img_list[0]])
        elif (len(img_list) == 2):
            rows.append([img_list[0]])
            rows.append([img_list[1]])
        elif (len(img_list) == 3):
            rows.append([img_list[0]])
            rows.append([img_list[1]])
            rows.append([img_list[2]])
        elif (len(img_list) == 4):
            rows.append([img_list[0], img_list[1]])
            rows.append([img_list[2], img_list[3]])
        elif (len(img_list) == 5):
            rows.append([img_list[0], img_list[1]])
            rows.append([img_list[2], img_list[3]])
            rows.append([img_list[4]])
        elif (len(img_list) == 6):
            rows.append([img_list[0], img_list[1]])
            rows.append([img_list[2], img_list[3]])
            rows.append([img_list[4], img_list[5]])
        elif (len(img_list) == 7):
            rows.append([img_list[0], img_list[1]])
            rows.append([img_list[2], img_list[3]])
            rows.append([img_list[4], img_list[5]])
            rows.append([img_list[6]])
        elif (len(img_list) == 8):
            rows.append([img_list[0], img_list[1]])
            rows.append([img_list[2], img_list[3]])
            rows.append([img_list[4], img_list[5]])
            rows.append([img_list[6], img_list[7]])
    elif (X - Y < 0.1 * X and X - Y < 0.1 * Y):  # kwadratowy kształt
        if (len(img_list) == 1):
            rows.append([img_list[0]])
        elif (len(img_list) == 2):
            rows.append([img_list[0], img_list[1]])
        elif (len(img_list) == 3):
            rows.append([img_list[0], img_list[1], img_list[2]])
        elif (len(img_list) == 4):
            rows.append([img_list[0], img_list[1]])
            rows.append([img_list[2], img_list[3]])
        elif (len(img_list) == 5):
            rows.append([img_list[0], img_list[1]])
            rows.append([img_list[2], img_list[3], img_list[4]])
        elif (len(img_list) == 6):
            rows.append([img_list[0], img_list[1], img_list[2]])
            rows.append([img_list[3], img_list[4], img_list[5]])
        elif (len(img_list) == 7):
            rows.append([img_list[0], img_list[1], img_list[2]])
            rows.append([img_list[3], img_list[4], img_list[5]])
            rows.append([img_list[6]])
        elif (len(img_list) == 8):
            rows.append([img_list[0], img_list[1], img_list[2]])
            rows.append([img_list[3], img_list[4], img_list[5]])
            rows.append([img_list[6], img_list[7]])
    else:  # poziomy kształt
        if (len(img_list) == 1):
            rows.append([img_list[0]])
        elif (len(img_list) == 2):
            rows.append([img_list[0], img_list[1]])
        elif (len(img_list) == 3):
            rows.append([img_list[0], img_list[1], img_list[2]])
        elif (len(img_list) == 4):
            rows.append([img_list[0], img_list[1]])
            rows.append([img_list[2], img_list[3]])
        elif (len(img_list) == 5):
            rows.append([img_list[0], img_list[1]])
            rows.append([img_list[2], img_list[3], img_list[4]])
        elif (len(img_list) == 6):
            rows.append([img_list[0], img_list[1], img_list[2]])
            rows.append([img_list[3], img_list[4], img_list[5]])
        elif (len(img_list) == 7):
            rows.append([img_list[0], img_list[1], img_list[2]])
            rows.append([img_list[3], img_list[4], img_list[5], img_list[6]])
        elif (len(img_list) == 8):
            rows.append([img_list[0], img_list[1], img_list[2], img_list[3]])
            rows.append([img_list[3], img_list[4], img_list[5], img_list[7]])

    it_row = 0
    it_col = 0
    for r in rows:
        for i in r:
            i = i.resize((int(X / len(r)), int(Y / len(rows))), Image.ANTIALIAS)
            mozaika.paste(i, (int(X / len(r)) * it_col, int(Y / len(rows) * it_row)))
            it_col += 1
        it_col *= 0
        it_row += 1


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(80),
        threaded=True,
        debug=False
    )
