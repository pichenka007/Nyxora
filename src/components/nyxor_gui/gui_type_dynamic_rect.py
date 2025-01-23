from typing import List, Optional, Dict

import pygame
from pygame_gui.core import UIElement, UIContainer

class DynamicRect():
	'''
	A type from UIDynamicContainer
	'{x}'   >> '{x}'
	'{x}px' >> '{x}'
	'{x}%'  >> '{x}/100*{width/height into context}'
	'{x}w'  >> '{x}/100*{width}'
	'{x}h'  >> '{x}/100*{height}'
	'{x}sc' >> '{x}/100*{screen width/height into context}'
	'{x}sw' >> '{x}/100*{screen width}'
	'{x}sh' >> '{x}/100*{screen height}'
	:param dynamics:    dynamics size [x, y, width, height]
	:param element: link to self UIDynamicContainer
	:param margins: dynamics margins [left, right, top, bottom]
	'''
	def __init__(self,
				 dynamics: List[str|int]|Dict[str, str|int],
				 element: UIContainer,
				 margins: Optional[List[str|int]|Dict[str, str|int]] = None
				 ):
		self.element = element

		if dynamics is None:
			self.dynamics = {'x':      '0',
							 'y':      '0',
							 'width':  '100%',
							 'height': '100%'}
		elif type(dynamics) == list:
			if len(dynamics) == 2:
				self.dynamics = {'x':      str(dynamics[0]),
								 'y':      str(dynamics[0]),
								 'width':  str(dynamics[1]),
								 'height': str(dynamics[1])}
			else:
				self.dynamics = {'x':      str(dynamics[0]),
								 'y':      str(dynamics[1]),
								 'width':  str(dynamics[2]),
								 'height': str(dynamics[3])}
		elif type(dynamics) == dict:
			self.dynamics = {}
			try:    self.dynamics['x']      = dynamics['x']
			except: self.dynamics['x']      = '0'
			try:    self.dynamics['y']      = dynamics['y']
			except: self.dynamics['y']      = '0'
			try:    self.dynamics['width']  = dynamics['width']
			except: self.dynamics['width']  = '0'
			try:    self.dynamics['height'] = dynamics['height']
			except: self.dynamics['height'] = '0'
		if margins is None:
			self.margins = {'left':   '0',
							'right':  '0',
							'top':    '0',
							'bottom': '0'}
		elif type(margins) == list:
			if len(margins) == 1:
				self.margins = {'left':   str(margins[0]),
								'right':  str(margins[0]),
								'top':    str(margins[0]),
								'bottom': str(margins[0])}	
			elif len(margins) == 2:
				self.margins = {'left':   str(margins[0]),
								'right':  str(margins[0]),
								'top':    str(margins[1]),
								'bottom': str(margins[1])}
			else:
				self.margins = {'left':   str(margins[0]),
								'right':  str(margins[1]),
								'top':    str(margins[2]),
								'bottom': str(margins[3])}		
		elif type(margins) == dict:
			self.margins = {}
			try:    self.margins['left']   = str(margins['left'])
			except: self.margins['left']   = '0'
			try:    self.margins['right']  = str(margins['right'])
			except: self.margins['right']  = '0'
			try:    self.margins['top']    = str(margins['top'])
			except: self.margins['top']    = '0'
			try:    self.margins['bottom'] = str(margins['bottom'])
			except: self.margins['bottom'] = '0'


		self.rect = self.get_rect()




	def calc_dynamic_string(self, dynamic_string, context='h'):
		'''
		calculate dynamic string
		:param dynamic_string: dynamic string
		:param context:        'h' or 'v' (horizontal(-) or vertical(|))
		'''
		pixel = 1
		procent_context = self.element.container_size[int(context == 'v')]
		width           = self.element.container_size[0]
		height          = self.element.container_size[1]
		window_context  = self.element.window_size[int(context == 'v')]
		window_width    = self.element.window_size[0]
		window_height   = self.element.window_size[1]
		screen_context  = self.element.screen_size[int(context == 'v')]
		screen_width    = self.element.screen_size[0]
		screen_height   = self.element.screen_size[1]

		dynamic_string = dynamic_string.replace('px', f'*{pixel}')
		dynamic_string = dynamic_string.replace('%', f'/100*{procent_context}')
		dynamic_string = dynamic_string.replace('wc', f'/100*{window_context}')
		dynamic_string = dynamic_string.replace('ww', f'/100*{window_width}')
		dynamic_string = dynamic_string.replace('wh', f'/100*{window_height}')
		dynamic_string = dynamic_string.replace('sc', f'/100*{screen_context}')
		dynamic_string = dynamic_string.replace('sw', f'/100*{screen_width}')
		dynamic_string = dynamic_string.replace('sh', f'/100*{screen_height}')
		dynamic_string = dynamic_string.replace('w', f'/100*{width}')
		dynamic_string = dynamic_string.replace('h', f'/100*{height}')

		'''
		I know it's not good to use eval.
		I just don't want to add an extra 100kb of memory to the library.
		+ I read that the gui want to port to android and unnecessary bilio libraries are not necessary.
		'''
		return eval(dynamic_string)


	def get_rect(self):
		'''
		return rect
		'''
		rect = [0, 0, 0, 0]
		rect[0] = self.calc_dynamic_string(self.dynamics['x'])+self.calc_dynamic_string(self.margins['left'])
		rect[1] = self.calc_dynamic_string(self.dynamics['y'], 'v')+ self.calc_dynamic_string(self.margins['top'], 'v')
		rect[2] = self.calc_dynamic_string(self.dynamics['width'])-(self.calc_dynamic_string(self.margins['left'])+
										   self.calc_dynamic_string(self.margins['right']))
		rect[3] = self.calc_dynamic_string(self.dynamics['height'], 'v')-(self.calc_dynamic_string(self.margins['top'], 'v')+
										   self.calc_dynamic_string(self.margins['bottom'], 'v'))
		self.rect = pygame.Rect(*rect)
		return self.rect


	def set_dynamics(self, dynamics:List[str]|Dict[str, str]):
		'''
		set dynamics
		'{x}'   >> '{x}'
		'{x}px' >> '{x}'
		'{x}%'  >> '{x}/100*{width/height into context}'
		'{x}w'  >> '{x}/100*{width}'
		'{x}h'  >> '{x}/100*{height}'
		'{x}sc' >> '{x}/100*{screen width/height into context}'
		'{x}sw' >> '{x}/100*{screen width}'
		'{x}sh' >> '{x}/100*{screen height}'
		:param dynamics: dynamics size [x, y, width, height]
		'''
		if dynamics is None:
			self.dynamics = {'x':      '0',
							 'y':      '0',
							 'width':  '100%',
							 'height': '100%'}
		elif type(dynamics) == list:
			if len(dynamics) == 2:
				self.dynamics = {'x':      str(dynamics[0]),
								 'y':      str(dynamics[0]),
								 'width':  str(dynamics[1]),
								 'height': str(dynamics[1])}
			else:
				self.dynamics = {'x':      str(dynamics[0]),
								 'y':      str(dynamics[1]),
								 'width':  str(dynamics[2]),
								 'height': str(dynamics[3])}
		elif type(dynamics) == dict:
			self.dynamics = {}
			try:    self.dynamics['x']      = dynamics['x']
			except: self.dynamics['x']      = '0'
			try:    self.dynamics['y']      = dynamics['y']
			except: self.dynamics['y']      = '0'
			try:    self.dynamics['width']  = dynamics['width']
			except: self.dynamics['width']  = '0'
			try:    self.dynamics['height'] = dynamics['height']
			except: self.dynamics['height'] = '0'

		self.rect = self.get_rect()


	def set_margins(self, margins:Optional[List[str|int]|Dict[str, str|int]] = None):
		'''
		set margins
		:param margins: dynamics margins [left, right, top, bottom]
		'''
		if margins is None:
			self.margins = {'left':   '0',
							'right':  '0',
							'top':    '0',
							'bottom': '0'}
		elif type(margins) == list:
			if len(margins) == 1:
				self.margins = {'left':   str(margins[0]),
								'right':  str(margins[0]),
								'top':    str(margins[0]),
								'bottom': str(margins[0])}	
			elif len(margins) == 2:
				self.margins = {'left':   str(margins[0]),
								'right':  str(margins[0]),
								'top':    str(margins[1]),
								'bottom': str(margins[1])}
			else:
				self.margins = {'left':   str(margins[0]),
								'right':  str(margins[1]),
								'top':    str(margins[2]),
								'bottom': str(margins[3])}		
		elif type(margins) == dict:
			self.margins = {}
			try:    self.margins['left']   = str(margins['left'])
			except: self.margins['left']   = '0'
			try:    self.margins['right']  = str(margins['right'])
			except: self.margins['right']  = '0'
			try:    self.margins['top']    = str(margins['top'])
			except: self.margins['top']    = '0'
			try:    self.margins['bottom'] = str(margins['bottom'])
			except: self.margins['bottom'] = '0'

		self.rect = self.get_rect()
		