import pygame, sys, random, neat, os
from player import Player
from obstacle import Obstacle
from background import Background, Cloud
pygame.init()

screen_width = 1000
screen_height = 400
fps = 60

LOCAL_DIR = os.path.dirname(__file__)
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         os.path.join(LOCAL_DIR, 'config.txt'))

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('NEAT Dinosaur Game')
clock = pygame.time.Clock()

font = pygame.font.Font('font/pixel.ttf', 30)
game_over_font = pygame.font.Font('font/pixel.ttf', 100)
hi = font.render('HI', False, 'black')
hi_rect = hi.get_rect(center=(830, 20))

generations = 0
def main(genomes, config):
    global generations
    generations += 1
    high_score = 0
    score = 0
    score_offset = 0
    prev_obstacle = 0
    prev_cloud = 0
    
    background = pygame.sprite.Group()
    background.add(Background(0))

    cloud = pygame.sprite.Group()
    cloud_interval = 3000

    obstacles = pygame.sprite.Group()
    obstacle_interval = 1000

    for i in range(random.randint(2, 3)):
        cloud.add(Cloud(2))

    networks = []
    players = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append([network, genome])
        player = pygame.sprite.GroupSingle()
        player.add(Player())
        players.append(player)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        obstacles_present = False
        for obstacle in obstacles:
            if obstacle.rect.right >= 50:
                obstacles_present = True
                closest_obstacle_x = obstacle.rect.x
                closest_obstacle_y = obstacle.rect.y
                obstacle_type = obstacle.type
                if obstacle_type == "bird":
                    obstacle_is_bird = 1
                else:
                    obstacle_is_bird = 0
                break

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

        for index, [network, genome] in enumerate(networks):
            player = players[index]
            if not player.sprite.is_dead:
                if pygame.sprite.spritecollide(player.sprite, obstacles, False):
                    player.sprite.is_dead = True
                if obstacles_present:
                    output = network.activate((closest_obstacle_x , closest_obstacle_y, obstacle_is_bird, player.sprite.rect.bottom))
                else:
                    output = network.activate((0, 0, 0, 0))
                decision = output.index(max(output))
                player.update(decision)
                genome.fitness += 1
            
                player.draw(screen)

        generation_dead = True
        alive_player = 0
        for player in players:
            if not player.sprite.is_dead:
                generation_dead = False
                alive_player += 1
                
        if generation_dead:
            cloud.empty()
            background.empty()
            obstacles.empty()
            return

        obstacles.update()
        obstacles.draw(screen)

        gen_label = font.render(f"Generation: {generations}", False, "black")
        gen_label_rect = gen_label.get_rect(topleft=(20, 20))
        alive_label = font.render(f"Alive: {alive_player}", False, "black")
        alive_label_rect = alive_label.get_rect(topleft=(20, 50))
        screen.blit(gen_label, gen_label_rect)
        screen.blit(alive_label, alive_label_rect)

        pygame.display.update()
        clock.tick(fps)

def printHighscore(high_score):
    hi_sc = str(high_score)
    for i in range(5 - len(hi_sc)):
        hi_sc = "0" + hi_sc
    hi_msg = font.render(hi_sc, False, 'black')
    hi_msg_rect = hi_msg.get_rect(center=(880, 20))
    screen.blit(hi_msg, hi_msg_rect)

if __name__ == "__main__":
    p = neat.Population(config)
    p.run(main)