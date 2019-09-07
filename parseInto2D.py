import numpy as np
from PIL import Image
from itertools import chain
from subprocess import run
from multiprocessing import Process



# DON'T CHANGE ME
def gen_for_slice(bottom, top):
    data = np.interp(raw_data, (bottom, top), (0, 255))
    img = Image.fromarray( data )
    img = img.convert("RGBA")
    pixdata = img.load()

    width, height = img.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == (0, 0, 0, 255):
                pixdata[x, y] = (0, 0, 0, 0)

    filename = "./export/" + str(bottom) + ".png"
    filenameBW = "./export/BW" + str(bottom) + ".bmp"

    img.save(filename, "PNG")

    for y in range(height):
        for x in range(width):
            if pixdata[x, y] != (0, 0, 0, 0):
                pixdata[x, y] = (255, 255, 255, 255)

    img.save(filenameBW, "BMP")

    cmd = "potrace " + filenameBW + " -s -t 100"
    run(cmd, shell=True, check=True)

    #Change it so that the svg line is hairline black on white w/sed
    #Call it good?


if __name__ == '__main__':
    # CHANGE ME
    top_row = 550
    bottom_row = 4500

    slices = chain(range(-900, -200, 100), range(-200, 100, 20), range(100, 300, 100), range(300, 1000, 150), range(1000, 2000, 500))
    begin = -1000

    raw_data = np.loadtxt(open("./psdem.csv", "rb"), skiprows=top_row, max_rows=bottom_row-top_row, delimiter=",", dtype=np.int16)

    for i in slices:
        p = Process(target=gen_for_slice, args=(begin,i,))
        p.start()
        begin = i
