import pygame
import os

import time

pygame.init()

WIDTH = 1000
HEIGHT = 600

# Colors

LIGHT_GREEN = (127, 223, 170)
LIGHT_ORANGE = (245, 157, 84)
LIGHT_YELLOW = (218, 247, 166)


# fonts subject to change
smallFont = pygame.font.Font("PressStart2P.ttf", 15)
mediumFont = pygame.font.Font("PressStart2P.ttf", 24)
largeFont = pygame.font.Font("PressStart2P.ttf", 32)
moveFont = pygame.font.Font("PressStart2P.ttf", 48)

upgrade_cost_font = pygame.font.Font("PressStart2P.ttf", 10)
upgrade_times_bought_font = pygame.font.Font("PressStart2P.ttf", 20)

pygame.display.set_caption("VandyCoin Clicker")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Load Images
coin_image = pygame.transform.scale(pygame.image.load(os.path.join("icons", "VandyCoin.png")), (300, 300))

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("icons", "background.jpg")), (WIDTH, HEIGHT))

PRIZE = pygame.transform.scale(pygame.image.load(os.path.join("icons", "Prize.png")), (250, 250))

'''Buildings'''
# follow the format below
# NAME = pygame.transform.scale(pygame.image.load(os.path.join("icons", FILENAME.extension)), (300, 64))
cursor_img = pygame.transform.scale(pygame.image.load(os.path.join("icons", "Cursor.png")), (300, 88))
purse_img = pygame.transform.scale(pygame.image.load(os.path.join("icons", "Purse.png")), (300, 88))


# set up coin class
class MainCoin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 300
        self.height = 300

        self.animation_state = 0

    def draw(self):
        if self.animation_state > 0:
            coin_shrink = pygame.transform.scale(coin_image, (int(0.9*self.width), int(0.9*self.height)))
            screen.blit(coin_shrink, coin_shrink.get_rect(center=(int(self.x + self.width/2),
                                                                  int(self.y + self.height/2))))
            self.animation_state -= 1
        else:
            screen.blit(coin_image, coin_image.get_rect(center=(int(self.x + self.width/2),
                                                                int(self.y + self.height/2))))

    def collide_point(self, mouse_pos):
        return pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(mouse_pos)


# set up coin and coin per second display
class CoinDisplay:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100

    def draw(self):

        coins_label = mediumFont.render(f"Coins: {int(user.coins)}", 1, (255, 255, 255))
        coins_per_second = mediumFont.render(f"Rate = {round(user.coins_per_second, 1)} per Tick", 1, LIGHT_GREEN)

        screen.blit(coins_label, (coins_label.get_rect(center=(int(self.x + self.width/2),
                                                               int(self.y + self.height/2)))))
        screen.blit(coins_per_second, (coins_per_second.get_rect(center=(int(WIDTH - self.x + self.width/2) - 240,
                                                                         int((self.y + self.height/2))))))


# Upgrades Class
class Upgrades:
    def __init__(self, name, x, y, image, base_cost, cost_scaling, coins_per_second):
        self.name = name
        self.x = x
        self.y = y
        self.width = 300
        self.height = 88

        self.image = image
        # self.icon = icon
        self.base_cost = base_cost
        self.cost_scaling = cost_scaling
        self.coins_per_second = coins_per_second

        self.times_bought = 0
        self.created = 0

    def collide_point(self, mouse_pos):
        return pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(mouse_pos)

    def get_total_cost(self):
        return int(self.base_cost * self.cost_scaling**self.times_bought)

    def draw(self, solid):

        icon = self.image.convert()
        cost = upgrade_cost_font.render(f"{self.get_total_cost()} Coins", 1, LIGHT_ORANGE)
        times_bought = upgrade_times_bought_font.render(f"{self.times_bought} Times", 1, LIGHT_ORANGE)
        if not solid:
            icon.set_alpha(100)
        else:
            icon.set_alpha(255)

        screen.blit(icon, (self.x, self.y))
        screen.blit(cost, (self.x + 150, self.y + self.height-30))
        screen.blit(times_bought, (self.x + self.width - 40, self.y + 15))


# initialize the player
class Player:
    def __init__(self):
        self.coins = 0
        self.click_multiplier = 1
        self.coins_per_second = 0

    def update_total_cps(self, upgrades_list):
        self.coins_per_second = 0
        for upgrade in upgrades_list:
            self.coins_per_second += upgrade.coins_per_second * upgrade.times_bought


# initialize the prize
class Prize:
    def __init__(self, x, y, image, cost):
        self.x = x
        self.y = y
        self.cost = cost
        self.width = 300
        self.height = 300
        self.image = image

    def collide_point(self, mouse_pos):
        return pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(mouse_pos)

    def get_total_cost(self):
        return self.cost

    def draw(self, solid):

        icon = self.image.convert()
        cost = upgrade_cost_font.render(f"{self.get_total_cost()} Coins", 1, LIGHT_ORANGE)
        final_prize = largeFont.render("LIMITED", 1, LIGHT_ORANGE)
        final_prize2 = largeFont.render("EDITION", 1, LIGHT_ORANGE)

        if not solid:
            icon.set_alpha(100)
            screen.blit(final_prize, (self.x + 10, self.y + 10))
            screen.blit(final_prize2, (self.x + 10, self.y + 60))
        else:
            icon.set_alpha(255)

        screen.blit(icon, (self.x, self.y))
        screen.blit(cost, (self.x + 150, self.y + self.height-30))


coin = MainCoin(100, 100)
coin_display = CoinDisplay(100, 0)
user = Player()
prize = Prize(700, HEIGHT - 500, PRIZE, 10)

# constructing upgrades class
base_y = HEIGHT
cursor = Upgrades('Cursor', 700, base_y - 88*2, cursor_img, base_cost=10, cost_scaling=1.15, coins_per_second=0.1)
purse = Upgrades('Purse', 700, base_y - 88, purse_img, base_cost=100, cost_scaling=1.15, coins_per_second=1)

list_of_upgrades = [cursor, purse]


def endgame():

    screen.blit(BACKGROUND, (0, 0))
    congrats = moveFont.render("Congratulation!", 1, (255, 255, 255))
    congrats2 = moveFont.render("You have Bought the", 1, (255, 255, 255))
    congrats3 = largeFont.render("Limited Edition VH Sticker!!", 1, (255, 255, 255))
    screen.blit(congrats, (int((WIDTH/2) - 400), int(HEIGHT/2 - 150)))
    screen.blit(congrats2, (int((WIDTH/2) - 460), int(HEIGHT/2)))
    screen.blit(congrats3, (int((WIDTH/2) - 430), int((HEIGHT/2) + 150)))
    pygame.display.update()


# main loop
def main():
    # set up run boolean to see if loop is running
    run = True
    fps = 60
    # coins = 0
    # coins_per_second = 0
    clock = pygame.time.Clock()
    channel_a = pygame.mixer.Channel(0)
    channel_b = pygame.mixer.Channel(1)
    bg_sound = pygame.mixer.Sound(os.path.join('audio', 'bgmusic.wav'))
    channel_a.set_volume(0.2)
    channel_a.play(bg_sound, -1)

    def redraw_window():
        # Draw background
        screen.blit(BACKGROUND, (0, 0))
        # Draw coin
        coin.draw()
        coin_display.draw()
        if user.coins >= prize.get_total_cost():
            prize.draw(solid=True)
        else:
            prize.draw(solid=False)
        for upgrades in list_of_upgrades:
            if user.coins >= upgrades.get_total_cost():
                upgrades.draw(solid=True)
            else:
                upgrades.draw(solid=False)

            user.coins += upgrades.times_bought * upgrades.coins_per_second * 0.1
            upgrades.created += upgrades.times_bought * upgrades.coins_per_second * .01

        pygame.display.update()

    while run:
        # makes sure game run consistent with FPS
        clock.tick(fps)
        redraw_window()
        #

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if coin.collide_point(mouse_pos):
                    user.coins += 1
                    coin.animation_state = 1
                    click_sound = pygame.mixer.Sound(os.path.join('audio', 'switch21.wav'))
                    channel_b.play(click_sound)

                for upgrade in list_of_upgrades:
                    if upgrade.collide_point(mouse_pos) and user.coins >= upgrade.get_total_cost():
                        user.coins -= upgrade.get_total_cost()
                        upgrade.times_bought += 1
                        user.update_total_cps(list_of_upgrades)

                if prize.collide_point(mouse_pos):
                    if user.coins >= prize.get_total_cost():
                        user.coins -= prize.get_total_cost()
                        endgame()
                        time.sleep(20)
                        run = False

            if event.type == pygame.QUIT:
                run = False


main()
