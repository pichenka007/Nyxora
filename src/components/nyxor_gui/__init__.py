from ..nyxor_utils import *
import pygame as pg
import pygame_gui as pgui
import time
import logging

log = logging.getLogger("main."+__name__.split(".")[-1])
log.setLevel(logging.DEBUG)

def init(win_w, win_h, sc_w, sc_h):

	log.info("init()")

	global manager
	manager = pgui.UIManager((win_w, win_h), theme_path="././assets/styles/style.json")

	for element in manager.get_root_container().elements:
		element.kill()

	sc_up_h = sc_h/5
	sc_left_w = sc_w/8


	MainContainer = pgui.elements.UIPanel(
		relative_rect=pg.Rect(0, 0, win_w, win_h),
		starting_height=1,
		container=None,
		parent_element=None,
		margins={'left': 0, 'right': 0, 'top': 0, 'bottom': 0},
		anchors={},
		object_id='MainContainer',
		manager=manager
	)

	UpContainer = pgui.elements.UIPanel(
		relative_rect=pg.Rect(0, 0, win_w, sc_up_h),
		starting_height=1,
		container=None,
		parent_element=None,
		margins={'left': 5, 'right': 5, 'top': 5, 'bottom': 5, "down": 5},
		anchors={},
		object_id='Container',
		manager=manager
	)

	DownContainer = pgui.elements.UIPanel(
		relative_rect=pg.Rect(0, sc_up_h-5, win_w, win_h-sc_up_h+5),
		starting_height=1,
		container=None,
		parent_element=None,
		margins={'left': 0, 'right': 0, 'top': 0, 'bottom': 0},
		anchors={},
		object_id='Container',
		manager=manager
	)

	LeftContainer = pgui.elements.UIPanel(
		relative_rect=pg.Rect(0, 0, sc_left_w+5, win_h-sc_up_h+5),
		starting_height=1,
		container=DownContainer,
		parent_element=DownContainer,
		margins={'left': 5, 'right': 5, 'top': 5, 'bottom': 5},
		anchors={},
		object_id='Container',
		manager=manager
	)

	RightContainer = pgui.elements.UIPanel(
		relative_rect=pg.Rect(sc_left_w, 0, win_w-sc_left_w, win_h-sc_up_h+5),
		starting_height=1,
		container=DownContainer,
		parent_element=DownContainer,
		margins={'left': 5, 'right': 5, 'top': 5, 'bottom': 5},
		anchors={},
		object_id='Container',
		manager=manager
	)

	DeltaContaner = UpContainer
	MainButton = pgui.elements.UIButton(
		relative_rect=pg.Rect(DeltaContaner.container_margins["left"],
		DeltaContaner.container_margins["top"],
		DeltaContaner.relative_rect.width-DeltaContaner.container_margins["right"]*2-DeltaContaner.container_margins["left"]*2,
		DeltaContaner.relative_rect.height-DeltaContaner.container_margins["bottom"]*2-DeltaContaner.container_margins["top"]*2),
		text="text",
		manager=manager,
		container=DeltaContaner,
		anchors={}
	)

	DeltaContaner = LeftContainer
	MainButton = pgui.elements.UIButton(
		relative_rect=pg.Rect(DeltaContaner.container_margins["left"],
		DeltaContaner.container_margins["top"],
		DeltaContaner.relative_rect.width-DeltaContaner.container_margins["right"]*2-DeltaContaner.container_margins["left"]*2,
		DeltaContaner.relative_rect.height-DeltaContaner.container_margins["bottom"]*2-DeltaContaner.container_margins["top"]*2),
		text="text",
		manager=manager,
		container=DeltaContaner,
		anchors={}
	)

	DeltaContaner = RightContainer
	MainButton = pgui.elements.UIButton(
		relative_rect=pg.Rect(DeltaContaner.container_margins["left"],
		DeltaContaner.container_margins["top"],
		DeltaContaner.relative_rect.width-DeltaContaner.container_margins["right"]*2-DeltaContaner.container_margins["left"]*2,
		DeltaContaner.relative_rect.height-DeltaContaner.container_margins["bottom"]*2-DeltaContaner.container_margins["top"]*2),
		text="text",
		manager=manager,
		container=DeltaContaner,
		anchors={}
	)

	#manager.set_visual_debug_mode(True)

def update(delta_time, sc):
	manager.update(delta_time)
	manager.draw_ui(sc)

