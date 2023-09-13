"""
Project Name : Flappy bird game using A.I.
Objective : To develop an A.I. which is able to play Flappy Bird.
Language used : Python
Modules used : Pygame,Random,OS,Neat
Developed by: 
Saharsh Raj
Aashish 
Kshitiz Sharma

"""

#Importing modules:

import pygame
import random
import os
import neat

#Initialing Font:
pygame.font.init()
gen = 0

#Importing mixer for sound:
pygame.mixer.init()
from pygame import mixer

#Setting up Window:
WIN_HEIGHT = 1080
WIN_WIDTH = 1920
FLOOR = 900
STAT_FONT = pygame.font.SysFont("timesnewroman", 50)
END_FONT = pygame.font.SysFont("timesnewroman", 70)
DRAW_LINES = False

#Initialising Window
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

#Importing images/icons:
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")).convert_alpha())
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (1920, 1080))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")).convert_alpha())
BIRD_IMGS = [(pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png")).convert_alpha())),(pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png")).convert_alpha())), (pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")).convert_alpha()))]

#Adding music:
mixer.music.load("bgm.wav")
mixer.music.play(-1)

#Creating classes:

#1-> Class Bird
class Bird:

    #Animating Flappy Bird:

    MAX_ROTATION = 25
    IMGS = BIRD_IMGS
    ROT_VEL = 20
    ANIMATION_TIME = 1


    #Initialising Bird:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    #Jump Function:

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    #Move Function:

    def move(self):
        
        self.tick_count += 1
        displacement = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2  
        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16
        if displacement < 0:
            displacement -= 2
        self.y = self.y + displacement
        if displacement < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # tilt down
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    
    #Placing the bird on screen (Drawing):

    def draw(self, win):
        self.img_count += 1

        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)
    
    #Getting Pixels used by bird (mask):

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    
#2=> Class Pipe:
    
class Pipe:
    
    GAP = 200
    VEL = 10

    #Initialising Pipe
    def __init__(self, x):

        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False

        self.set_height()

    #Setting Height:

    def set_height(self):

        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    #Adds motion to pipe:

    def move(self):
        self.x -= self.VEL

    #Place Pipes on screen (Draw):

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    #Collision Logic:

    def collide(self, bird, win):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            return True
        return False
    
#3-> Class Base:

class Base:
    VEL = 10
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    #Initialising object Base:

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    #Adds motion to base:

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    #Places the base on screen (Draw):

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

#Function Declarations:

#Function to tilt the bird:

def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    surf.blit(rotated_image, new_rect.topleft)

#Draw Function:

def draw_window(win, birds, pipes, base, score, gen, pipe_ind):
    if gen == 0:
        gen = 1
    win.blit(BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    for bird in birds:
        if DRAW_LINES:
            try:
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].height), 5)
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom), 5)
            except:
                pass
        bird.draw(win)

    #Show score:

    score_label = STAT_FONT.render("Score: " + str(round(score)),1,(255,255,255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    #Show generations:

    score_label = STAT_FONT.render("Gens: " + str(gen-1),1,(255,255,255))
    win.blit(score_label, (10, 10))

    #Show Birds alive:

    score_label = STAT_FONT.render("Alive: " + str(len(birds)),1,(255,255,255))
    win.blit(score_label, (10, 50))

    pygame.display.update()

#A.I. Implementation, Main game loop:

def eval_genomes(genomes, config):
    global WIN, gen
    win = WIN
    gen += 1

    nets = []
    birds = []
    ge = []
    
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230,350))
        ge.append(genome)

    base = Base(FLOOR)
    pipes = [Pipe(1920)]
    score = 0

    clock = pygame.time.Clock()

    run = True
    while run and len(birds) > 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1

        for x, bird in enumerate(birds):
            ge[x].fitness += 0.1
            bird.move()

            output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                birdjump = mixer.Sound("jump.wav")
                birdjump.set_volume(0.08)
                birdjump.play()
                bird.jump()

        base.move()
        birdpop = mixer.Sound("scream.wav")

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()

            for bird in birds:
                if pipe.collide(bird, win):
                    ge[birds.index(bird)].fitness -= 1
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))
                    birdpop.play()

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x+1000:
                pipe.passed = True
                add_pipe = True
            
            if  pipe.passed and pipe.x < bird.x:
                score += 0.02941176470

        if add_pipe:
            # score += 1
            for genome in ge:
                genome.fitness += 5
            pipes.append(Pipe(WIN_WIDTH))

        for r in rem:
            pipes.remove(r)

        for bird in birds:
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))
                birdpop.play()
                

        draw_window(WIN, birds, pipes, base, score, gen, pipe_ind)

#Runs Neat's algo to train AI bird:

def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet, neat.DefaultStagnation,config_file)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(eval_genomes, 50)
    print('\nBest genome:\n{!s}'.format(winner))

#Determine's path to configuration file, added to prevent errors regarding current directory.

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)

#End