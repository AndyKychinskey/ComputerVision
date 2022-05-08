import os
import cv2
import json
import numpy as np
import pyautogui as pyagui

class JSON_Object(object):
	"""
	Class to parse JSON object and get parsed data back
	"""
	def __init__(self, path_to_file):
		with open(path_to_file, mode='r', encoding='utf-8') as file:
			self.__json_data = json.load(file)

	def get_object(self):
		return self.__json_data


class Validation_Point(object):
	"""
	Class to load image and get image back
	"""
	def __init__(self, category, gui_object_name, parsed_json):
		try:
			path_to_img = parsed_json.get(category).get(gui_object_name)
			if os.path.exists(path_to_img):
				self.__data = cv2.imread(path_to_img, 0)
			else:
				raise Exception(f"unvalid path: {path_to_img}")
		except Exception as ex:
			print(ex)

	def get_object(self):
		return self.__data


class GUI_Object(Validation_Point):
	"""
	Class inherited from GUI_Object
	"""
	def __init__(self, category, gui_object_name, parsed_json, validation_point=None, comment_to_validation_point='', wait_in_cycle=False):
		super().__init__(category, gui_object_name, parsed_json)
		self.is_validation_point = False
		self.is_wait_in_cycle = wait_in_cycle
		if validation_point:
			self.is_validation_point = True
			self.__validation_point = validation_point
		self.__comment_to_validation_point = comment_to_validation_point

	def get_validation_object(self):
		return self.__validation_point

	def comment_to_validation_point(self):
		return self.__comment_to_validation_point


class GUI_Object_Handler(object):
	__cwd = os.getcwd()
	def __init__(self, threshold_to_find_elem=0.9):
		self.__threshold = threshold_to_find_elem
		print(self.__cwd)

	def get_threshold(self):
		return self.__threshold

	@classmethod
	def get_template_location_on_screen(cls, template_to_match, threshold=0.9):
		pyagui.sleep(0.5)
		pyagui.screenshot(imageFilename='screen.png')
		img_rgb = cv2.imread(os.path.join(cls.__cwd, 'screen.png'))
		img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
		pyagui.sleep(0.2)
		res = cv2.matchTemplate(img_gray, template_to_match.get_object(), cv2.TM_CCOEFF_NORMED)
		loc = np.where(res >= threshold)
		return loc

	@classmethod
	def check_result_with_template(cls, template_to_match, threshold=0.9):
		try:
		    if cls.get_template_location_on_screen(template_to_match, threshold)[0][0]:
		        return True
		except IndexError:
		    return False

	@classmethod
	def locate_template_on_screen(cls, template_to_locate, threshold=0.9, need_to_click=False, need_to_move_to=False):
		try:
		    loc = cls.get_template_location_on_screen(template_to_locate, threshold)
		    if loc[0][0]:
		    	w, h = template_to_locate.get_object().shape[::-1]
		    	if need_to_click:
		    		pyagui.click(loc[1][0] + w/2, loc[0][0] + h/2)
		    	elif need_to_move_to:
		    		pyagui.moveTo(loc[1][0] + w*0.6, loc[0][0] + h*0.6, 0.5)
		    	return loc
		except IndexError:
		    return False
