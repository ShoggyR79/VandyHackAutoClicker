import pygame
import os
import time

WIDTH = 750
HEIGHT = 750

pygame.display.set_caption("VandyCoin Clicker")

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
# Load Images
COIN = pygame.image.load(os.path.join("icons", "vandy_coin.png"))

BACKGROUND = pygame.image.load(os.path.join("icons", "background.jpg"))

