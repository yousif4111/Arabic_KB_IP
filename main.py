import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller


cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=0.8)

keys=[["ض","ص","ث","ق","ف","غ","ع","ه","خ","ح","ج","د","ذ"],
	  ["ش","س","ي","ب","ل","ا","ت","ن","م","ك","ط"],
	  ["ئ","ء","ؤ","ر","لا","ى","ة","و","ز","ظ"]]

finalText=""

keyboard=Controller()
def drawALL(img, buttonList):
	for button in buttonList:
		x,y=button.pos
		w,h=button.size
		cv2.rectangle(img, button.pos, (x+w,y+h), (255, 0, 255), cv2.FILLED)
		fontpath = "./arial.ttf"
		font = ImageFont.truetype(fontpath, 32)
		img_pil = Image.fromarray(img)
		draw = ImageDraw.Draw(img_pil)
		draw.text((x + 21, y + 22.5), button.text, font=font,stroke_width=1)
		img = np.array(img_pil)
	return img

class Button():
	def __init__(self,pos,text,size=[65,65]):
		self.pos = pos
		self.size = size
		self.text =text



buttonList=[]
for i in range(len(keys)):
	for j, key in enumerate(keys[i]):
		buttonList.append(Button([90 * j + 5, 100 * i + 5], key))
while True:
	success, img = cap.read()
	img = detector.findHands(img)
	lmList, bboxInfo = detector.findPosition(img)

	img=drawALL(img, buttonList)
	if lmList:
		for button in buttonList:
			x, y = button.pos
			w, h = button.size

			if x<lmList[8][0]<x+w and y<lmList[8][1]<y+h:
				cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
				fontpath = "./arial.ttf"
				font = ImageFont.truetype(fontpath, 32)
				img_pil = Image.fromarray(img)
				draw = ImageDraw.Draw(img_pil)
				draw.text((x + 21, y + 22.5), button.text, font=font, stroke_width=1)
				img = np.array(img_pil)


				l,_,_=detector.findDistance(8,12,img, draw=False)
				print(l)

				if l<60:
					keyboard.press(button.text)
					cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
					fontpath = "./arial.ttf"
					font = ImageFont.truetype(fontpath, 32)
					img_pil = Image.fromarray(img)
					draw = ImageDraw.Draw(img_pil)
					draw.text((x + 21, y + 22.5), button.text, font=font, stroke_width=1)
					img = np.array(img_pil)
					finalText += button.text
					sleep(0.2)


	cv2.imshow("Image", img)
	cv2.waitKey(1)

