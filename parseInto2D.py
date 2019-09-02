import numpy as np
from PIL import Image

# CHANGE ME



# DON'T CHANGE ME
data = np.loadtxt(open("./psdem.csv", "rb"), skiprows=550, max_rows=3950, delimiter=",", dtype=np.int16)

# Gen a whole pile of things
data = np.interp(data, (5, 55), (0, 255))

img = Image.fromarray( data )       # Create a PIL image
img = img.convert("RGBA")
pixdata = img.load()

width, height = img.size
for y in range(height):
    for x in range(width):
        if pixdata[x, y] == (0, 0, 0, 255):
            pixdata[x, y] = (255, 255, 255, 0)

img.save("psdem.png", "PNG")

# Create a 1024x1024x3 array of 8 bit unsigned integers
#data = np.loadtxt(open("./psdem.asc", "rb"), delimiter=" ", dtype=np.int16, usecols=range(12500, 16006))