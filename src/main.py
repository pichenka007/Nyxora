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
from logging import basicConfig, INFO, debug, info, warning, error, critical

from components.utils import *
from components.gui import *

basicConfig(level=INFO, filename="Nyxora.log",filemode="w", format="%(asctime)s %(levelname)s %(message)s")
info("lol")
FPS = 60

if __name__ == "__main__":

	pg.init()

	sc_info = pg.display.Info()
	sc_w = sc_info.current_w
	sc_h = sc_info.current_h

	info(f"SC size {sc_w}x{sc_h}")

	win_w = sc_w // 2
	win_h = sc_h // 2

	sc = pg.display.set_mode((win_w, win_h), pg.RESIZABLE)
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