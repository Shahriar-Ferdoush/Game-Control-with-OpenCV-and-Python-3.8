# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 22:44:37 2020

@author: Shahriar Ferdoush
"""

import cv2
import datetime
import numpy as np
from pynput.mouse import Controller, Button

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 400)
cap.set(10, 125)

m = Controller()

last_click = datetime.datetime.now()

while True:
	_, frame = cap.read()
	frame = cv2.flip(frame, 1)

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	lower_orange = np.array([157, 86, 57])
	upper_orange = np.array([179, 221, 255])
	mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)

	lower_green = np.array([60, 156, 25])
	upper_green = np.array([80, 255, 121])
	mask_green = cv2.inRange(hsv, lower_green, upper_green)

	contoursOrange, _ = cv2.findContours(mask_orange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for c in contoursOrange :
		if cv2.contourArea(c) <= 50 :
			continue
		x, y, _, _ = cv2.boundingRect(c)
		m.position = x*1920/640, y*1120/400
		cv2.drawContours(frame, contoursOrange, -1, (0, 255, 0), 3)

	contoursGreen, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for c in contoursGreen :
		if cv2.contourArea(c) <= 50 :
			continue
		now = datetime.datetime.now()
		diff = now - last_click
		if diff.total_seconds() > 0.5 :
			last_click = datetime.datetime.now()
			cv2.drawContours(frame, contoursGreen, -1, (0, 255, 0), 3)
			x, y = m.position
			m.click(Button.left, 1)
	
	cv2.imshow("Webcam", frame)
	
	key = cv2.waitKey(1)
	if key == 27:
		break

cap.release()
cv2.destroyAllWindows()