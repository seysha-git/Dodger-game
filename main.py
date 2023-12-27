import pygame as pg 
import random as rd
import os
import time
pg.font.init()

WIN_HEIGHT,WIN_WIDTH = 800,900
MAIN_WIDTH, MAIN_HEIGHT = 45,35
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

SCORE_FONT = pg.font.SysFont("comicsans", 30)
TOP_SCORE_FONT = pg.font.SysFont("comicsans", 30)
FINISHED_FONT = pg.font.SysFont("comicsans",100)

pg.display.set_caption("Dodger game")

INTRO_FONT = pg.font.SysFont("comicsans", 30)
HEALTH_FONT = pg.font.SysFont("comicsans", 30)

ENEMY_VEL = 8
HIT_POST = pg.USEREVENT
WIN = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
MAIN_IMAGE = pg.transform.scale(pg.image.load(os.path.join("Assets", "geometry_dash_player.png")), (MAIN_WIDTH, MAIN_HEIGHT))
MAIN_VEL = 9
clock = pg.time.Clock()
FPS = 60

def draw_window(win, main,enemies, score, top_score, health):
    win.fill(BLACK)
    score_label = SCORE_FONT.render(f"Score: {score}", 1, WHITE)
    win.blit(score_label, (30, 50))
    top_score_label = TOP_SCORE_FONT.render(f"Top Score: {top_score}", 1, WHITE)
    win.blit(top_score_label, (30, 80))
    health_label = HEALTH_FONT.render(f"Health: {health}", 1, WHITE)
    win.blit(health_label, (30, 120))
    for enemy in enemies:
        pg.draw.rect(win, GREEN, enemy)
    win.blit(MAIN_IMAGE,(main.x, main.y))
    pg.display.update()


def handle_mouvement_main(main):
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        main.y -= MAIN_VEL
    if keys[pg.K_s] and main.y + main.height + MAIN_VEL < WIN_HEIGHT:
        main.y += MAIN_VEL 
    if keys[pg.K_a] and main.x + MAIN_VEL > 0+50:
        main.x -= MAIN_VEL
    if keys[pg.K_d] and main.x + main.width + MAIN_VEL < WIN_WIDTH:
        main.x += MAIN_VEL

def handle_mouvement_enemy(enemies, main):
    level = 1
    for enemy in enemies:
        enemy.y += ENEMY_VEL
        if enemy.y + enemy.height + ENEMY_VEL > WIN_HEIGHT:
            enemies.remove(enemy)
        if enemy.colliderect(main):
            pg.event.post(pg.event.Event(HIT_POST))

def main(win):
    run = True
    score = 0
    top_score = 0
    level = 0 
    health = 3
    enemies = []
    start_time = pg.time.get_ticks()
    main_char = pg.Rect(WIN_WIDTH//2 - MAIN_WIDTH//2, WIN_HEIGHT-MAIN_HEIGHT*1.5, MAIN_WIDTH, MAIN_HEIGHT)
    while run:
        if len(enemies) == 0:
            level += 1
            enemies = [pg.Rect(rd.randint(0,WIN_WIDTH-100),rd.randint(-500,-50), rd.randint(50,220), rd.randint(50,250)) for i in range(3*level)]
            for i in range(len(enemies) - 1):
                for j in range(i + 1, len(enemies)):
                    if enemies[i].colliderect(enemies[j]):
                        enemies[i].width, enemies[i].height = enemies[i].width *0.4, enemies[i].height *0.4
                        enemies[i].y -= 200  # Move the first colliding enemy up by 200 pixels
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        if event.type == HIT_POST:
            health -= 1
        if health <= 0:
            health = 3
            finished_label = FINISHED_FONT.render("You lost",1,WHITE)
            win.blit(finished_label, (300, 300))
            pg.display.update()
            pg.time.delay(2000)
            if score > top_score:
                top_score = score
            enemies = [pg.Rect(rd.randint(0,WIN_WIDTH-100),rd.randint(-300,-50), 50, 50) for i in range(3*level)]
            main_char.x = WIN_WIDTH//2 - MAIN_WIDTH//2
            main_char.y = WIN_HEIGHT-MAIN_HEIGHT*1.5
            score = 0
            level = 1
            
        handle_mouvement_main(main_char)
        handle_mouvement_enemy(enemies, main_char)
        draw_window(win, main_char, enemies, score, top_score, health)
        elapsed_time = (pg.time.get_ticks() - start_time) // 1000  # Convert milliseconds to seconds
        score = elapsed_time  # Use seconds as the score
    pg.quit()
    

"""
#def main_menu(win):
    run = True
    while run:
        win.fill(GREEN)
        intro_label = INTRO_FONT.render("\nPress mouse down to commence or \n QPress Quit to exit",1,WHITE)
        win.blit(intro_label,(WIN_WIDTH // 2 - intro_label.get_width()//2, WIN_HEIGHT//2))
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                main(win)
"""


if __name__ == "__main__":
    main(WIN)


