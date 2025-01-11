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

log = logging.getLogger("main."+__name__.split(".")[-1])
log.setLevel(logging.DEBUG)

def close(code=0, trace=None):
	if not trace:
		log.info(f"Program successfully terminated with code: {code}")
	else:
		log.info(f"Error: Program terminated with error code: {code}")
		log.info(f"Trace Back: {trace}")
		input("Enter to close")
	sys.exit()