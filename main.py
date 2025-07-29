import pygame, time, math
from player import Player
from ball import Ball
from gates import Gate
from neiro_main import AIPlayer

FPS = 60
pygame.init()
w, h = 800, 1000
sc = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

# Создаем игроков
players = []
players.append(Player())  # Игрок управляемый человеком
players.append(AIPlayer(team=0))  # AI союзник
players.append(AIPlayer(team=1))  # AI противник 1
players.append(AIPlayer(team=1))  # AI противник 2

ball = Ball(400, 500)
gates = [Gate(0), Gate(1)]
goal0, goal1 = False, False
tick = 0
score = [0, 0]  # Счет команд
font = pygame.font.SysFont(None, 36)

def reset_positions():
    ball.reset()
    players[0].x, players[0].y = 400, 500  # Человек в центре
    players[1].x, players[1].y = 200, 200  # Союзник
    players[2].x, players[2].y = 200, 800  # Противник 1
    players[3].x, players[3].y = 600, 800  # Противник 2

while True:
    sc.fill('white')
    clock.tick(FPS)

    for ev in pygame.event.get():
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                if players[0].dashes >= 1:
                    players[0].speed = 9
                    players[0].dashes -= 1
        if ev.type == pygame.QUIT:
            exit(0)

    # Управление человеком
    keys = pygame.key.get_pressed()
    players[0].move(keys)
    
    # Управление AI
    for player in players[1:]:
        if isinstance(player, AIPlayer):
            player.move(ball, players, gates)
    
    # Отрисовка
    for player in players:
        player.draw(sc)
    
    for gate in gates:
        gate.draw(sc)
    
    # Проверка голов
    goal0, goal1 = gates[0].check_goal(ball), gates[1].check_goal(ball)
    if goal0:
        score[1] += 1
        reset_positions()
        # Награда для AI команды 1
        for player in players[2:]:
            player.give_reward(10)  # Большая награда за гол
            player.goals_scored += 1
        # Штраф для AI команды 0
        players[1].give_reward(-5)
        players[1].goals_conceded += 1
    elif goal1:
        score[0] += 1
        reset_positions()
        # Награда для AI команды 0
        players[1].give_reward(10)
        players[1].goals_scored += 1
        # Штраф для AI команды 1
        for player in players[2:]:
            player.give_reward(-5)
            player.goals_conceded += 1
    
    # Малые награды за приближение к мячу и воротам
    for player in players[1:]:
        if isinstance(player, AIPlayer):
            # Награда за приближение к мячу
            dist_to_ball = math.hypot(player.x - ball.x, player.y - ball.y)
            player.give_reward(0.1 * (100 - dist_to_ball) / 100)
            
            # Награда за движение к воротам противника, когда у них мяч
            if (ball.vx**2 + ball.vy**2 < 1 and 
                ((player.team == 0 and ball.y > 500) or 
                 (player.team == 1 and ball.y < 500))):
                target_gate = gates[1 - player.team]
                dist_to_gate = math.hypot(player.x - target_gate.x, player.y - target_gate.y)
                player.give_reward(0.05 * (500 - dist_to_gate) / 500)
    
    ball.draw(sc)
    ball.move(players)
    
    # Восстановление рывков
    if tick % 350 == 0:
        for player in players:
            player.dashes = min(player.dashes + 1, 5)
    
    # Обучение AI
    if tick % 100 == 0:
        for player in players[1:]:
            if isinstance(player, AIPlayer):
                player.learn()
    
    # Отображение счета
    score_text = font.render(f"{score[0]} - {score[1]}", True, 'black')
    sc.blit(score_text, (w//2 - score_text.get_width()//2, 20))
    
    tick += 1
    pygame.display.update()