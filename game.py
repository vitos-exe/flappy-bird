import pygame as pg
from classes import Bird, tube_pair_factory
from time import sleep
from collections import deque

#constants
ANIMATION = 1001
TUBE_SPAWN = 1002
WHITE = (255,255,255)

#initializing pygame window, setting timers for custom events
pg.init()
surface = pg.display.set_mode((800, 600))
pg.display.set_caption("Flappy bird")
pg.time.set_timer(pg.event.Event(ANIMATION),100)
pg.time.set_timer(pg.event.Event(TUBE_SPAWN),2000)

#loading and processing all necessary sprites
background = pg.image.load("Assets/background.png").convert()
ending_surface = pg.image.load("Assets/ending.png").convert()
bird_states = [
    pg.image.load("Assets/wings_up.png").convert(),
    pg.image.load("Assets/bird.png").convert(),
    pg.image.load("Assets/wings_down.png").convert()
]
tubes = [
    pg.image.load("Assets/top_tube.png").convert(),
    pg.image.load("Assets/bottom_tube.png").convert()
]
for el in bird_states + tubes + [ending_surface]:
    el.set_colorkey(WHITE)
f = pg.font.Font(None,100)

#creating working objects
passing_lines = deque()
bird = Bird(bird_states)
upper_tubes = pg.sprite.Group()
bottom_tubes = pg.sprite.Group()

running = True

#starting game cycle
while running:

    #checking events
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            running = False
        #if arrow up was pressed bird jumps
        elif ev.type == pg.KEYDOWN and ev.key == pg.K_UP:
            bird.jump()
        #spawns a pair of tubes every 2 seconds
        elif ev.type == TUBE_SPAWN:
            tube_pair = tube_pair_factory(tubes)
            upper_tubes.add(tube_pair[0])
            bottom_tubes.add(tube_pair[1])
            passing_lines.append(880)
        #changes the state of bird
        elif ev.type == ANIMATION:
            bird.change_state()

    #updating all sprites
    for el in (bird, upper_tubes, bottom_tubes):
        el.update()

    #checking collisions 
    if any([pg.sprite.spritecollideany(bird, g) for g in (upper_tubes, bottom_tubes)]):
        pg.event.post(pg.event.Event(pg.QUIT))

    #checking if the bird crossed a passing line so as to increase counter
    passing_lines = deque([l - 2 for l in passing_lines])
    if passing_lines and passing_lines[0] == 100:
        bird.counter += 1
        passing_lines.popleft()

    #drawing all spirites on the display
    surface.blit(background,(0,0))
    surface.blit(bird.image,bird.rect)
    upper_tubes.draw(surface)
    bottom_tubes.draw(surface)
    surface.blit(f.render(str(bird.counter),True , WHITE), (0,0))

    #updating display, making delay for stable framerate
    pg.display.update()
    pg.time.delay(17)

#drawing the ending scene, waiting 3 seconds until quiting the game
surface.blit(ending_surface,ending_surface.get_rect(center = (400, 250)))
pg.display.update()
sleep(3)
quit()