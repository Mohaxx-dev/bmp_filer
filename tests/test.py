import cv2
from bmpFiler import bmpFiler

if "__main__" == __name__:
    img = cv2.imread("kala.jpg")
    #TO BGRA
    img = np.insert(img, 3, 0, axis=2)
    bmpFiler.make_file(img, color_mode=bmpFiler.COLOR_MODE_BGRA, name="converted_file")