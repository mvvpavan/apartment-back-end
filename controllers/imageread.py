import cv2
import pytesseract
img=cv2.imread("telugu.jpeg")
text=pytesseract.image_to_string(img)
print(text)
#from PIL import Image
#from tesseract import image_to_string
#print image_to_string(Image.open('Breaking_News.png'))
#print image_to_string(Image.open('Breaking_News.png'), lang='eng')

#sudo apt-get update
#sudo apt-get install tesseract-ocr
#sudo apt-get install libtesseract-dev

#pip install tesseract
#pip install tesseract-ocr

#pip install pytesseract and pip install tesseract