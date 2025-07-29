import math, random, pygame

pygame.init()

class Player:
    def __init__(self, team=0):
        self.team = team  # Добавляем атрибут team
        self.x = 400 if team == 0 else 400
        self.y = 200 if team == 0 else 800
        self.current_speed_x = 0
        self.current_speed_y = 0
        self.speed = 3
        self.dashes = 5
        
    def draw(self, sc):
        color = 'blue' if self.team == 0 else 'red'  # Разные цвета для команд
        pygame.draw.circle(sc, color, (self.x, self.y), 15)
        
    def move(self, keys):
        self.current_speed_x = 0
        self.current_speed_y = 0
        if keys[pygame.K_w]:
            self.y -= self.speed
            self.current_speed_y = -self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
            self.current_speed_x = -self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
            self.current_speed_y = self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
            self.current_speed_x = self.speed

        if self.speed > 3: 
            self.speed -= 1