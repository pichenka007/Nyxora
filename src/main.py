import pygame as pg
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

from components import *

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

log.info("log started")

FPS = 60

if __name__ == "__main__":

	pg.init()

	sc_info = pg.display.Info()
	sc_w = sc_info.current_w
	sc_h = sc_info.current_h
	log.error("pzdc")
	log.info(f"SC size {sc_w}x{sc_h}")

	win_w = sc_w // 2
	win_h = sc_h // 2

	sc = pg.display.set_mode((win_w, win_h), pg.RESIZABLE)
	log.info(f"window size {win_w}x{win_h}")
	pg.display.set_caption("Nyxora")
	hwnd = pg.display.get_wm_info()["window"]
	clock = pg.time.Clock()


	sprites = [pg.Surface((50, 50)) for _ in range(1000)]
	for sprite in sprites:
		sprite.fill((255, 0, 0))

	start_time = time.time()
	frames = 0

	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				close(0)

		sc.fill((0, 0, 0))
		for i, sprite in enumerate(sprites):
			sc.blit(sprite, (i % 20 * 60+time.time()%10, i // 20 * 60))

		pg.display.flip()
		frames += 1
		

		clock.tick(FPS)


	print(frames)