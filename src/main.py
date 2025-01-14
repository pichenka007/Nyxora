import pygame as pg
pg.init()
import pygame_gui
import pedalboard as pd
import scipy
import numpy
import time
import math
import sys
import win32gui
import win32con
import win32api
import logging
from logging.handlers import RotatingFileHandler


import components.nyxor_utils as utils
import components.nyxor_gui as gui


log = logging.getLogger("main")
log.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler = RotatingFileHandler('Nyxora.log', maxBytes=1048576, backupCount=5)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

log.addHandler(console_handler)
log.addHandler(file_handler)

log.info("Nyxora started")


def main():
	sc_info = pg.display.Info()
	sc_w = sc_info.current_w
	sc_h = sc_info.current_h

	log.info(f"SC size {sc_w}x{sc_h}")

	win_w = sc_w // 2
	win_h = sc_h // 2

	sc = pg.display.set_mode((win_w, win_h), pg.RESIZABLE|pg.SRCALPHA)

	log.info(f"window size {win_w}x{win_h}")

	pg.display.set_caption("Nyxora")
	hwnd = pg.display.get_wm_info()["window"]
	clock = pg.time.Clock()

	gui.init(win_w, win_h, sc_w, sc_h)

	#sc = pg.display.set_mode((win_w, win_h), pg.RESIZABLE|pg.SRCALPHA)
	#sc = pg.display.set_mode((win_w, win_h), pg.RESIZABLE|pg.SRCALPHA)
	#win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, sc_w//2-win_w//2, sc_h//2-win_h//2, win_w, win_h, win32con.SWP_SHOWWINDOW)

	#sprites = [pg.Surface((50, 50)) for _ in range(1000)]
	#for sprite in sprites:
	#	sprite.fill((255, 0, 0))

	start_time = time.time()
	frames = 0
	delta_time = time.time()

	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				utils.close(0)
			if event.type == pg.VIDEORESIZE:
				sc = pg.display.set_mode((max(event.w, 120), max(event.h, 100)), pg.RESIZABLE|pg.SRCALPHA)
				gui.init(max(event.w, 120), max(event.h, 100), sc_w, sc_h)
				gui.manager.set_window_resolution((max(event.w, 120), max(event.h, 100)))
			gui.manager.process_events(event)


		sc.fill((0, 0, 0))
		gui.update(time.time()-delta_time, sc)


		pg.display.flip()
		frames += 1

		clock.tick(FPS)
		delta_time = time.time()

	print(frames)



FPS = 60

if __name__ == "__main__":
	main()



