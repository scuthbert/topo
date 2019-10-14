import numpy as np
from PIL import Image
from itertools import chain
from subprocess import run
from multiprocessing import Process

# DON'T CHANGE ME
def gen_for_slice(bottom, top, index, passed_data):
    data = np.interp(passed_data, (bottom, top), (0, 255))
    img = Image.fromarray( data )
    img = img.convert("RGBA")
    pixdata = img.load()

    width, height = img.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == (0, 0, 0, 255):
                pixdata[x, y] = (0, 0, 0, 0)

    filename = "./export/" + str(index) + ".png"
    filenameBW = "./export/BW" + str(index) + ".bmp"
    filenameBWSVG = "./export/BW" + str(index) + ".svg"

    img.save(filename, "PNG")

    for y in range(height):
        for x in range(width):
            if pixdata[x, y] != (0, 0, 0, 0):
                pixdata[x, y] = (255, 255, 255, 255)

    img.save(filenameBW, "BMP")

    cmd = "potrace " + filenameBW + " -s -t 100 --color \"#ffffff\""
    run(cmd, shell=True, check=True)

    replace = "sed -i -e s/stroke\=\\\"none\\\"/stroke\=\\\"#000000\\\"\ stroke\-width\=\\\"5\.00\\\"/g " + filenameBWSVG
    run(replace, shell=True, check=True)


if __name__ == '__main__':
    # CHANGE ME
    top_row = 550
    bottom_row = 4500

    slices = chain(range(-200, 200, 50), range(200, 1100, 150), range(1100, 2600, 500))
    begin = -250

    raw_data = np.loadtxt(open("./psdem.csv", "rb"), skiprows=top_row, max_rows=bottom_row-top_row, delimiter=",", dtype=np.int16)

    new_raw = np.rot90(raw_data)

    for (index, top) in enumerate(slices):
        gen_for_slice(begin, top, index, new_raw)
        begin = top
