import pygame


pygame.init()

class Gate:
    def __init__(self, team):
        self.team = team
        self.x = 350
        self.y = 0
        self.w = 100
        self.h = 20
        
        if self.team == 0:
            self.x = 350
        if self.team == 1:
            self.x = 350
            self.y = 1000 - self.h
        
    def draw(self, sc):
        teams = ['blue', 'red']
        pygame.draw.rect(sc, teams[self.team], (self.x, self.y, self.w, self.h))
    
    def check_goal(self, ball):
        if ball.x >= self.x and ball.x <= self.x + self.w and ball.y >= self.y and ball.y <= self.y + self.h:
            return True
        else:
            return False