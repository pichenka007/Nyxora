from ..nyxor_utils import *
from .ui_dynamic_container import UIDynamicContainer
import pygame as pg
import pygame_gui as pgui
import time
import logging

log = logging.getLogger('main.'+__name__.split('.')[-1])
log.setLevel(logging.DEBUG)

def init(win_w, win_h, sc_w, sc_h):

	log.info('init()')

	global manager
	manager = pgui.UIManager((win_w, win_h), theme_path='././assets/styles/style.json')

	for element in manager.get_root_container().elements:
		element.kill()

	sc_up_h = '20sh'
	sc_left_h = '20sh'

	MainContainer = UIDynamicContainer(
		dynamic_rect=[0, '100%'],
		starting_height=1,
		container=None,
		parent_element=None,
		margins={'left': 0, 'right': 0, 'top': 0, 'bottom': 0},
		anchors={},
		object_id='MainContainer',
		manager=manager
	)
	UpContainer = UIDynamicContainer(
		dynamic_rect=[0, 0, '100%', sc_up_h],
		container=MainContainer,
		margins={'left': 2, 'right': 2, 'top': 2, 'bottom': 1},
		object_id='UpContainer',
		manager=manager
	)
	LeftContainer = UIDynamicContainer(
		dynamic_rect=['0', sc_up_h, sc_left_h, f'100%-{sc_up_h}'],
		container=MainContainer,
		margins={'left': 2, 'right': 1, 'top': 1, 'bottom': 2},
		object_id='LeftContainer',
		manager=manager
	)
	DownContainer = UIDynamicContainer(
		dynamic_rect=[sc_left_h, sc_up_h, f'100%-{sc_left_h}', f'100%-{sc_up_h}'],
		container=MainContainer,
		margins={'left': 1, 'right': 2, 'top': 1, 'bottom': 2},
		object_id='DownContainer',
		manager=manager
	)
	#RightContainer = pgui.elements.UIDynamicContainer(
	#	dynamic_rect=['25sh', '0', '100%-25sh', '100%'],
	#	starting_height=1,
	#	container=DownContainer,
	#	parent_element=None,
	#	margins=['0px'],
	#	anchors={},
	#	object_id='Container',
	#	manager=manager
	#)
	#UpLeftContainer = pgui.elements.UIDynamicContainer(
	#	dynamic_rect=['0', '0', '100h', '100h'],
	#	starting_height=1,
	#	container=UpContainer,
	#	parent_element=None,
	#	margins=['4px'],
	#	anchors={},
	#	object_id='Container',
	#	manager=manager
	#)
	DeltaContaner = UpContainer
	MainButton = pgui.elements.UIButton(
		pg.Rect(0,
		0,
		DeltaContaner.get_container().get_size()[0],
		DeltaContaner.get_container().get_size()[1]),
		text='text',
		manager=manager,
		container=DeltaContaner,
		anchors={'left': 'left', 'right': 'right', 'top': 'top', 'bottom': 'bottom'}
	)
	#DeltaContaner = DownContainer
	#MainButton = pgui.elements.UIButton(
	#	relative_rect=pg.Rect(0,
	#	0,
	#	DeltaContaner.relative_rect.width,
	#	DeltaContaner.relative_rect.height),
	#	text='text',
	#	manager=manager,
	#	container=DeltaContaner,
	#	anchors={}
	#)
	#DeltaContaner = UpLeftContainer
	#MainButton = pgui.elements.UIButton(
	#	relative_rect=pg.Rect(0,
	#	0,
	#	DeltaContaner.get_container().get_size()[0],
	#	DeltaContaner.get_container().get_size()[1]),
	#	text='text',
	#	manager=manager,
	#	container=DeltaContaner,
	#	anchors={}
	#)
	#DeltaContaner = UpContainer
	#manager.set_visual_debug_mode(True)

def update(delta_time, sc):
	manager.update(delta_time)
	manager.draw_ui(sc)

