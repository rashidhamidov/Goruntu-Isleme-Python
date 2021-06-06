#@programming_fever
import cv2
import imutils
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img = cv2.imread('bekleme/8.png',cv2.IMREAD_COLOR)

img = cv2.resize(img, (150, 70))
def temizleme(resim,bottomx,bottomy):
    resim[0:bottomx, 0:31] = 255
    resim[0:21, 0:bottomy] = 255
    resim[45:bottomx, 0:bottomy] = 255
    resim[0:bottomx, 53:80] = 255
    resim[0:bottomx, 101:128] = 255
    resim[0:bottomx, 150:177] = 255
    resim[0:bottomx, 199:226] = 255
    resim[0:bottomx, 248:bottomy] = 255


def kesinlestir_1(resim,bottomx,bottomy,topx,topy):
    i = 0
    j = 0
    while (i < (bottomx - topx)):
        while (j < (bottomy - topy)):
            if(resim[i,j] >=30 and resim[i,j]<=50):
                resim[i, j] -= 20
            j += 1
        i += 1
        j = 0

def kesinlestirme(resim,bottomx,bottomy,topx,topy):
    i = 0
    j = 0
    while (i < (bottomx - topx)):
        while (j < (bottomy - topy)):
            if (resim[i, j] < 100):
                resim[i, j] = 0
            else:
                resim[i, j] = 255
            j += 1
        i += 1
        j = 0


def preproces(img):
    if img is not None:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        canny=cv2.Canny(gray,80,180)
        image=cv2.GaussianBlur(gray,(5,5),0)
        #image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 5)
        cv2.imshow('',img)

        (x, y) = 70,150
        (topx, topy) = (0,0)
        (bottomx, bottomy) = (np.max(x), np.max(y))
        image = image[topx:bottomx, topy:bottomy]
        kesinlestir_1(image,bottomx,bottomy,topx,topy)
        kesinlestirme(image,bottomx,bottomy,topx,topy)
        #Cropped=cv2.Canny(Cropped,80,150)
        Cropped = cv2.threshold(image, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        #Cropped = cv2.Canny(Cropped, 10, 60, 65)

        text = pytesseract.image_to_string(Cropped)




        cv2.imshow('Sayac Endeks',Cropped)
        print(text)
preproces(img)
cv2.waitKey(0)
cv2.destroyAllWindows()