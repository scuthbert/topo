import numpy as np
from PIL import Image
from itertools import chain

# CHANGE ME
top_row = 550
bottom_row = 4500

slices = chain(range(-900, -200, 100), range(-200, 100, 20), range(100, 300, 100), range(300, 1000, 150), range(1000, 2000, 500))

# DON'T CHANGE ME
raw_data = np.loadtxt(open("./psdem.csv", "rb"), skiprows=top_row, max_rows=bottom_row-top_row, delimiter=",", dtype=np.int16)

previous = -1000
for i in slices:
    data = np.interp(raw_data, (previous, i), (0, 255))

    img = Image.fromarray( data )       # Create a PIL image
    img = img.convert("RGBA")
    pixdata = img.load()

    width, height = img.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == (0, 0, 0, 255):
                pixdata[x, y] = (255, 255, 255, 0)

    img.save("./export/" + str(previous) + "to" + str(i) + ".png", "PNG")
    previous = i