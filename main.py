import pygame, sys, random
from player import Player
from obstacle import Obstacle
from background import Background, Cloud
pygame.init()

screen_width = 1000
screen_height = 400
fps = 60

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Dinosaur Game')
clock = pygame.time.Clock()

font = pygame.font.Font('font/pixel.ttf', 30)
game_over_font = pygame.font.Font('font/pixel.ttf', 100)
hi = font.render('HI', False, 'black')
hi_rect = hi.get_rect(center=(830, 20))
game_over = False
game_over_msg = font.render('G     A     M     E            O     V     E     R', False, 'black')
game_over_rect = game_over_msg.get_rect(center=(500, 140))
restart_button = pygame.transform.rotozoom(pygame.image.load('graphics/restart_button.png'), 0, 0.75)
restart_button_rect = restart_button.get_rect(center=(500, 200))

background = pygame.sprite.Group()
background.add(Background(0))

cloud = pygame.sprite.Group()
cloud_interval = 3000

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacles = pygame.sprite.Group()
obstacle_interval = 1000

def main():
    global obstacle_interval, cloud_interval, game_over
    high_score = 0
    score = 0
    score_offset = 0
    prev_obstacle = 0
    prev_cloud = 0
    
    for i in range(random.randint(2, 3)):
        cloud.add(Cloud(2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
                mouse = pygame.mouse.get_pos()
                if restart_button_rect.collidepoint(mouse):
                    game_over = False
                    prev_obstacle = pygame.time.get_ticks()
                    score_offset = int(pygame.time.get_ticks()/80)

                    player.empty()
                    obstacles.empty()
                    cloud.empty()

                for _ in range(random.randint(2, 3)):
                    cloud.add(Cloud(2))
                player.add(Player())
                printHighscore(high_score)

        if not game_over:
            tick = pygame.time.get_ticks() - prev_obstacle
            if tick > obstacle_interval:
                prev_obstacle = pygame.time.get_ticks()
                obstacle_interval = random.randint(750, 1000)
                obstacles.add(Obstacle(random.choice(('small_obs', 'big_obs', 'big_obs','bird') if score > 200 else ('small_obs', 'big_obs', 'big_obs'))))
            tick = pygame.time.get_ticks() - prev_cloud
            if tick > cloud_interval:
                prev_cloud = pygame.time.get_ticks()
                cloud_interval = random.randint(4000, 8000)
                cloud.add(Cloud(1))

            score = int(pygame.time.get_ticks()/80) - score_offset if int(pygame.time.get_ticks()/80) - score_offset < 99999 else 99999
            score_str = str(score)
            for i in range(5 - len(score_str)):
                score_str = "0" + score_str
            score_msg = font.render(score_str, False, 'black')
            score_msg_rect = score_msg.get_rect(center=(950, 20))

            background.update()
            background.draw(screen)
            if len(background) == 1:
                background.add(Background(1000))
            printHighscore(high_score)
            screen.blit(hi, hi_rect)
            screen.blit(score_msg, score_msg_rect)

            cloud.update()
            cloud.draw(screen)

            if pygame.sprite.spritecollide(player.sprite, obstacles, False):
                game_over = True
                player.update(True)
            else:
                player.update(False)
            player.draw(screen)

            obstacles.update()
            obstacles.draw(screen)

            if game_over:
                high_score = score if score > high_score else high_score
                screen.blit(game_over_msg, game_over_rect)
                screen.blit(restart_button, restart_button_rect)

            pygame.display.update()
            clock.tick(fps)

def printHighscore(high_score):
    hi_sc = str(high_score)
    for i in range(5 - len(hi_sc)):
        hi_sc = "0" + hi_sc
    hi_msg = font.render(hi_sc, False, 'black')
    hi_msg_rect = hi_msg.get_rect(center=(880, 20))
    screen.blit(hi_msg, hi_msg_rect)

if __name__ == '__main__':
    main()