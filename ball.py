import pygame, math, random

def go_to_0(number, speed):
    if number < 0:
        return number + speed
    elif number > 0:
        return number - speed
    else:
        return 0
    
pygame.init()

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.ball_weight = 0.09
        
    def draw(self, sc):
        pygame.draw.circle(sc, 'yellow', (self.x, self.y), 10)
        pygame.draw.circle(sc, 'black', (self.x, self.y), 10, 2)
    def reset(self, x=None, y=None):
        self.x = x if x is not None else 400
        self.y = y if y is not None else 500
        self.vx = 0
        self.vy = 0
    def move(self, players):
        if self.x <= 0 and self.vx <= 0: self.vx *= -1
        if self.x >= 800 and self.vx >= 0: self.vx *= -1

        if self.y <= 0 and self.vy <= 0: self.vy *= -1
        if self.y >= 1000 and self.vy >= 0: self.vy *= -1
        
        for player in players:
            dist = math.hypot(self.x - player.x, self.y - player.y)
            if dist <= 25:
                self.vx = player.current_speed_x + (1 if player.current_speed_x > 0 else -1)
                self.vy = player.current_speed_y + (1 if player.current_speed_y > 0 else -1)
        
        self.vx = go_to_0(self.vx, self.ball_weight)
        self.vy = go_to_0(self.vy, self.ball_weight)
        
        self.x += self.vx
        self.y += self.vy