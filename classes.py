import pygame as pg
from random import randint

#class that describes bird class
class Bird(pg.sprite.Sprite):
    
    #bird constructor
    def __init__(self, states: list[pg.Surface]) -> None:
        pg.sprite.Sprite.__init__(self)
        self.states = states
        self.cur_state = 1
        self.rect = states[1].get_rect(center = (100,300))
        self.speed = 0
        self.counter = 0

    #increases bird's speed and position respectively to speed,
    #checks for a collision with the game borders
    def update(self) -> None:
        self.speed += 0.6
        self.rect.bottom += self.speed
        if self.rect.bottom > 800 or self.rect.top < 0:
            pg.event.post(pg.event.Event(pg.QUIT))

    #makes the bird jump 
    def jump(self) -> None:
        self.speed = -8
    
    #changes the bird's state(sprite)
    def change_state(self) -> None:
        self.cur_state = self.cur_state + 1 if self.cur_state < len(self.states) - 1 else 0 

    #property that returns the concrete bird's state image
    @property 
    def image(self) -> pg.Surface:
        return self.states[self.cur_state]

#class that describes tube class
class Tube(pg.sprite.Sprite):

    #tube constuctor
    def __init__(self, image: pg.Surface, y: int) -> None:
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect(center = (840, y))

    #updates a tube's state
    #checks if the tube went out of screen
    def update(self) -> None:
        self.rect.x -= 2
        if self.rect.right <= 0:
            self.kill()

#function that serves as factory for tube pairs
def tube_pair_factory(t_i: list[pg.Surface]) -> tuple[Tube]:
    gap = randint(125,425)
    return (Tube(t_i[0], gap-240), Tube(t_i[1], gap+390))