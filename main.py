import os
import io
import json
import cv2
import numpy as np
import requests



def text_reader(path):
    name  = "image.jpg"    #because detection.py is saving the image by name image.jpg
    image = cv2.imread(path)  #reading the image
    

    #converting the image to gray 
    gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    x,y = 0,0
    (w,h) = gray_image.shape
    
    roi = gray_image[y:y+w,x:x+h]  #extracting the region of interest
    
    #cv2.imshow('pic',image)
    #cv2.imshow("gray_image",gray_image)
   # cv2.imshow("img",roi)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
        

    ### implementing OCR
    url_api = "https://api.ocr.space/parse/image"   #api 

    _, compressedimage = cv2.imencode(".jpg",roi, [1, 90])   #compressing the region of interest(number plate)

    file_bytes = io.BytesIO(compressedimage)  

    result = requests.post(url_api,
                      files = {name: file_bytes},
                      data = {"apikey": "4dea1b139888957",
                              "language": "eng"})   #you have to enter your own API key from OCR space
    result = result.content.decode()                      
    result = json.loads(result)
    parsed_results = result.get("ParsedResults")[0]
    text_detected = parsed_results.get("ParsedText")

    return(text_detected)

