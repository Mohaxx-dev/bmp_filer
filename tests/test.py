import cv2
import numpy as np
import bmpFiler.bmpFiler as bf

if "__main__" == __name__:
    img = cv2.imread("kala.jpg")
    #TO BGRA
    img = np.insert(img, 3, 255, 2)
    bf.make_file(img, color_mode=bf.COLOR_MODE_BGRA, name="converted_file")