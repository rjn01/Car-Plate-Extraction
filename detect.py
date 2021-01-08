import os
import cv2
import numpy as np


#load yolo 
def object(user_image):

	model_weight = "lapi.weights"
	model_cfg = "darknet-yolov3.cfg"
	net = cv2.dnn.readNet(model_weight,model_cfg)
	
	classes=['Plate','NO_Plate']


	layers_name = net.getLayerNames()
	output_layers = [layers_name[i[0] - 1] for i in net.getUnconnectedOutLayers()]

	#loading image
	img = cv2.imread(user_image)
		
	height,width,channels = img.shape
	
	
	#detecting image
	blob = cv2.dnn.blobFromImage(img,0.00392,(416,416),(0,0,0),True,crop=False)

	net.setInput(blob)
	outs = net.forward(output_layers)

	

	#showing info on screen
	class_ids=[]
	confidences=[]
	boxes=[]

	for out in outs:
		for detection in out:
			scores = detection[5:]
			class_id = np.argmax(scores)
			confidence = scores[class_id]
			
			
			
			if confidence>0.3:
				#object detected
				center_x = int(detection[0]*width)
				center_y = int(detection[1]*height)
				w = int(detection[2]*width)
				h = int(detection[3]*height)
				x = int(center_x - w/2)
				y = int(center_y - h/2)

				boxes.append([x,y,w,h])
				confidences.append(float(confidence))
				class_ids.append(class_id)
	
	
	
	indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
	#this line will remove the bounding boxes which are around same object


	font = cv2.FONT_HERSHEY_SIMPLEX 
	for i in range(len(boxes)):
		if i in indexes:   #show the boxes only if it is present in indexes
			x,y,w,h = boxes[i]
			label = str(classes[class_ids[i]])
			
			roi = img[y:y+h,x:x+w]		
			cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),1)
			
			
			path = os.path.join('../Car-Plate-Extraction/static',"image.jpg")
			cv2.imwrite(path,roi)
			
			return(path)
		
