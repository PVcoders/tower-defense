import pygame
import data
import copy
from os import system, path

win = pygame.display.set_mode((800, 800))
turret = pygame.image.load(path.join("assets", "turret.png"))
turret = pygame.transform.scale(turret, (60, 60))
enemy = pygame.image.load(path.join("assets", "test-enemy.png"))
enemy = pygame.transform.scale(enemy, (20, 20))
turretBuilder = copy.copy(turret)
turretBuilder.set_alpha(80)
pygame.display.set_caption("tower defense")
pathList = []
towers = []
enemies = []

def loadPath():
    global pathList
    for i in data.coords:
        system("cls")
        pathRect = pygame.Rect(i[0], i[1], i[2], i[3])
        pathList.append(pathRect)
        print(pathList)

class Tower:
    def __init__(self, rect, type = ""):
        self.towerRect = rect
        self.type = type

    def tr(self):
        return self.towerRect

class Enemy:
    def __init__(self, rect, speed, hp = 1):
        self.enemyRect = rect
        self.hp = hp
        self.speed = speed
        self.pathNum = 0
        self.moves = 0
    def er(self):
        return self.enemyRect

def main():
    global towers
    global enemies
    loadPath()
    clock = pygame.time.Clock() 
    running = True
    turretBox = pygame.Rect(0, 0, 60, 60)
    placing = False
    while running:

        # high priority
        turretBox.x, turretBox.y = pygame.mouse.get_pos()
        turretBox.x -= turretBox.width / 2
        turretBox.y -= turretBox.height / 2

        # misc

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    placing = not placing
                if event.key == pygame.K_F11:
                    enemies.append(Enemy(pygame.Rect(data.spawn[0], data.spawn[1], 10, 10), 2))
                    print(enemies)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if placing:
                    colliding = False
                    for i in pathList:
                        if pygame.Rect.colliderect(i, turretBox):
                            colliding = True
                    for i in towers:
                        if pygame.Rect.colliderect(i.tr(), turretBox):
                            colliding = True
                    if turretBox.x + turretBox.width > 800 or turretBox.y + turretBox.height > 800 or turretBox.x < 0 or turretBox.y < 0: # checks if box is in area completely
                        colliding = True
                    if not colliding:
                        towers.append(Tower(copy.copy(turretBox)))
                        print(towers)
        
        # keys
        keys = pygame.key.get_pressed()
        # drawing
        clock.tick(60)
        win.fill((50, 160, 50))

        for i in pathList:
            pygame.draw.rect(win, (150, 75, 0), i)

        for i in towers:
            win.blit(turret, (i.tr().x, i.tr().y))
        
        for i in enemies:
            i.moves += 1
            if i.er().x < data.moveTo[i.pathNum][0]:
                if i.er().x + i.speed > data.moveTo[i.pathNum][0]:
                    i.er().x = data.moveTo[i.pathNum][0]
                else:
                    i.er().x += i.speed
            elif i.er().x > data.moveTo[i.pathNum][0]:
                if i.er().x - i.speed < data.moveTo[i.pathNum][0]:
                    i.er().x = data.moveTo[i.pathNum][0]
                else:
                    i.er().x -= i.speed
            if i.er().y < data.moveTo[i.pathNum][1]:
                if i.er().y + i.speed > data.moveTo[i.pathNum][1]:
                    i.er().y = data.moveTo[i.pathNum][1]
                else:
                    i.er().y += i.speed
            elif i.er().y > data.moveTo[i.pathNum][1]:
                if i.er().y - i.speed < data.moveTo[i.pathNum][1]:
                    i.er().y = data.moveTo[i.pathNum][1]
                else:
                    i.er().y -= i.speed
            elif i.er().x == data.moveTo[i.pathNum][0]:
                i.pathNum += 1
                print("Im there")
            if i.pathNum == len(data.moveTo):
                print("Leak")
                enemies.remove(i)
            win.blit(enemy, (i.er().x, i.er().y))
        if placing:
            win.blit(turretBuilder, (turretBox.x, turretBox.y))
        
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()

