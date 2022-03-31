# Libraries 
from glob import glob
import math
from pickle import TRUE
import random
from turtle import Screen
import pygame
from pygame import mixer
# Pygame Setup
pygame.init()

# Screen
screenW = 1300
screenH = 800
screen = pygame.display.set_mode((screenW, screenH))

# Init States
listOfZombies = []


# UI
pauseUpdate = False
font = pygame.font.Font("assets/fonts/Abel-Regular.ttf", 25)
class UI:
    def __init__(self):
        pass 
    def backgroundMusic(self):
        global isSoundMute
        if isSoundMute == False:
            mixer.music.load("assets/music/TWD.wav")
            mixer.music.play(-1)
        else:
            mixer.music.stop()
    def pauseGame(self):
        global pauseUpdate
        self.font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 60)
        self.pausedGame = self.font.render("Paused", True, (255, 255, 255))
        if pauseUpdate == True:
            pauseUpdate = False
        else:
            pauseUpdate = True        
        screen.blit(self.pausedGame, (((screenW / 2) - 180), ((screenH / 2) - 150)))
        pygame.display.update()
        # Space to play again
        self.font = pygame.font.Font("assets/fonts/Abel-Regular.ttf", 25)
        self.pToPlay = self.font.render("Press P To Play!", True, (255, 255, 255))
        screen.blit(self.pToPlay, (((screenW / 2) - 75), ((screenH / 2) + 10)))

    def displayGameOverText(self):
        # Game Over Text
        self.font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 70)
        self.gameOverText = self.font.render("Game Over", True, (255, 255, 255))
        screen.blit(self.gameOverText, (((screenW / 2) - 310), ((screenH / 2) - 170)))
        # Space to play again
        self.font = pygame.font.Font("assets/fonts/Abel-Regular.ttf", 25)
        self.spaceToPlay = self.font.render("Press Space To Play!", True, (255, 255, 255))
        screen.blit(self.spaceToPlay, (((screenW / 2) - 110), ((screenH / 2) + 30)))
        # Q to quit 
        self.font = pygame.font.Font("assets/fonts/Abel-Regular.ttf", 20)
        self.qToQuit = self.font.render("Press Q To Quit!", True, (255, 255, 255))
        screen.blit(self.qToQuit, (((screenW / 2) - 70), ((screenH / 2) + 260)))
        # M to mute
        self.font = pygame.font.Font("assets/fonts/Abel-Regular.ttf", 20)
        self.mToMute = self.font.render("Press M To Mute!", True, (255, 255, 255))
        screen.blit(self.mToMute, (((screenW / 2) - 75), ((screenH / 2) + 310)))
    def gameOver(self):
        global isGameOver
        isGameOver = True
    def startGame(self):
        global isGameStarting
        # Start Game Text
        screen.fill((100,100,100))
        screen.blit(background, (backgroundX, 0))
        self.font = pygame.font.Font("assets/fonts/PressStart2P-vaV7.ttf", 50)
        self.startGameText = self.font.render("I Am Ninja.", True, (255, 255, 255))
        screen.blit(self.startGameText, (((screenW / 2) - 250), ((screenH / 2) - 150)))
        # Space to play again
        self.font = pygame.font.Font("assets/fonts/Abel-Regular.ttf", 25)
        self.spaceToPlay = self.font.render("Press Space Key To Play!", True, (255, 255, 255))
        screen.blit(self.spaceToPlay, (((screenW / 2) - 115), ((screenH / 2) + 30)))
        #pygame.display.update()


# Player
class Player:
    def __init__(self):
        self.isMoving = False
        self.isDead = False
        self.attackSize = 0.2
        self.x = 0
        self.y = screenH - 200
        self.speed = 15
        self.xSpeed = self.speed
        self.ySpeed = self.speed
        self.animationIndex = 0
        self.playerIdleAnimation = [
            pygame.image.load("assets/characters/ninja/Idle__000.png"),
            pygame.image.load("assets/characters/ninja/Idle__001.png"),
            pygame.image.load("assets/characters/ninja/Idle__002.png"),
            pygame.image.load("assets/characters/ninja/Idle__003.png"),
            pygame.image.load("assets/characters/ninja/Idle__004.png"),
            pygame.image.load("assets/characters/ninja/Idle__005.png"),
            pygame.image.load("assets/characters/ninja/Idle__006.png"),
            pygame.image.load("assets/characters/ninja/Idle__007.png"),
            pygame.image.load("assets/characters/ninja/Idle__008.png"),
            pygame.image.load("assets/characters/ninja/Idle__009.png"),
        ]
        self.playerWalkAnimation = [
            pygame.image.load("assets/characters/ninja/Run__000.png"),
            pygame.image.load("assets/characters/ninja/Run__001.png"),
            pygame.image.load("assets/characters/ninja/Run__002.png"),
            pygame.image.load("assets/characters/ninja/Run__003.png"),
            pygame.image.load("assets/characters/ninja/Run__004.png"),
            pygame.image.load("assets/characters/ninja/Run__005.png"),
            pygame.image.load("assets/characters/ninja/Run__006.png"),
            pygame.image.load("assets/characters/ninja/Run__007.png"),
            pygame.image.load("assets/characters/ninja/Run__008.png"),
            pygame.image.load("assets/characters/ninja/Run__009.png"),
        ]
        self.playerAttackAnimation = [
            pygame.image.load("assets/characters/ninja/Attack__000.png"),
            pygame.image.load("assets/characters/ninja/Attack__001.png"),
            pygame.image.load("assets/characters/ninja/Attack__002.png"),
            pygame.image.load("assets/characters/ninja/Attack__003.png"),
            pygame.image.load("assets/characters/ninja/Attack__004.png"),
            pygame.image.load("assets/characters/ninja/Attack__005.png"),
            pygame.image.load("assets/characters/ninja/Attack__006.png"),
            pygame.image.load("assets/characters/ninja/Attack__007.png"),
            pygame.image.load("assets/characters/ninja/Attack__008.png"),
            pygame.image.load("assets/characters/ninja/Attack__009.png"),
        ]
        self.playerDeadAnimation = [
            pygame.image.load("assets/characters/ninja/Dead__000.png"),
            pygame.image.load("assets/characters/ninja/Dead__001.png"),
            pygame.image.load("assets/characters/ninja/Dead__002.png"),
            pygame.image.load("assets/characters/ninja/Dead__003.png"),
            pygame.image.load("assets/characters/ninja/Dead__004.png"),
            pygame.image.load("assets/characters/ninja/Dead__005.png"),
            pygame.image.load("assets/characters/ninja/Dead__006.png"),
            pygame.image.load("assets/characters/ninja/Dead__007.png"),
            pygame.image.load("assets/characters/ninja/Dead__008.png"),
            pygame.image.load("assets/characters/ninja/Dead__009.png"),
        ]
        #self.image = pygame.image.load(self.playerSprites[self.animationIndex])
        self.idleScale = (70, 150)
        self.runScale = (100, 150)
        self.attackScale = (150, 165)
        self.deadScale = (150, 165)
        self.currentScale = self.idleScale
        self.image = pygame.image.load("assets/characters/ninja/Idle__000.png")
        self.image = pygame.transform.scale(self.image, self.currentScale)
        self.currentAnimation = self.playerIdleAnimation
        self.flipImageHorizontal = False
        self.direction = 0
        self.isAttacking = False
        self.health = 10
        self.slashSound = mixer.Sound("assets/soundeffects/mixkit-metal-hit-woosh-1485.wav")
        self.slashSound.set_volume(0.4)
    def blit(self):
        screen.blit(self.image, (self.x, self.y))
    def moveIdle(self):
        self.isAttacking = False
        self.direction = 0
        self.currentAnimation = self.playerIdleAnimation
        self.currentScale = self.idleScale
        self.isMoving = False
    def moveLeft(self):
        self.direction = 1
        self.currentAnimation = self.playerWalkAnimation
        self.flipImageHorizontal = True
        self.currentScale = self.runScale
        self.isMoving = True
    def moveRight(self):
        self.direction = 2
        self.currentAnimation = self.playerWalkAnimation
        self.flipImageHorizontal = False
        self.currentScale = self.runScale
        self.isMoving = True
    def moveAttack(self):
        self.direction = 0
        self.isAttacking = True
        self.currentAnimation = self.playerAttackAnimation
        self.currentScale = self.attackScale
        self.slashSound.play()
        self.isMoving = False
    # Post Process
    def animate(self):
        self.image = self.currentAnimation[self.animationIndex]
        self.image = pygame.transform.scale(self.image, self.currentScale)
        self.image = pygame.transform.flip(self.image, self.flipImageHorizontal, False)
        if self.isMoving == True:
            WalkingAnimation(self.x, self.y, self.flipImageHorizontal)
        self.healthScore()
    # Box Constrains
    def windowConstraints(self):
        global background, backgroundX
        if self.x < 0:
            self.x = 0
            backgroundX += 20
            if backgroundX >= background.get_width():
                backgroundX = 0
        elif self.x > screenW - self.currentScale[0] - 70:
            self.x = screenW - self.currentScale[0] - 70
            backgroundX -= 20
            if backgroundX >= background.get_width():
                backgroundX = background.get_width()
    # Move
    def move(self):
        self.windowConstraints()
        if self.direction == 0:     # Idle
            self.x += 0
        elif self.direction == 1:   # Left
            self.x += -self.xSpeed
        elif self.direction == 2:   # Right
            self.x += self.xSpeed
    # Health
    def healthScore(self):
        self.font = pygame.font.Font("assets/fonts/Abel-Regular.ttf", 20)
        if self.health >= 80:
            healthColor = (0, 255, 255)
        elif self.health >= 50:
            healthColor = (0, 255, 0)
        elif self.health >= 20:
            healthColor = (255, 255, 0)
        elif self.health < 20:
            healthColor = (255, 0, 0)
        elif self.health <= 0:
            healthColor = (0, 0, 0)
        enemyHealth = self.font.render(str(self.health), True, healthColor)
        screen.blit(enemyHealth, (self.x + 30, self.y - 35))
        if self.health <= 0:
            self.isDead = True
            ui.gameOver()
    # Interaction
    def interaction(self, zombie):
        distance = math.sqrt( math.pow((zombie.x - self.x), 2) + math.pow((zombie.y - self.y), 2))
        if distance < 50:
            self.attackSize += 0.2         
            if int(self.attackSize) >= 1:
                self.health -= int(self.attackSize)
                self.attackSize = 0.01
            
    # Update
    def update(self, zombie):
        if self.health >= 1:
            self.interaction(zombie)
            self.move()
            self.animationIndex += 1
            if self.animationIndex > len(self.currentAnimation) - 1:
                self.animationIndex = 0
            self.animate()
        else:
            self.currentAnimation = self.playerDeadAnimation
            self.currentScale = self.deadScale
            self.image = self.playerDeadAnimation[len(self.playerDeadAnimation) - 1]
            self.image = pygame.transform.scale(self.image, self.deadScale)

walkAnimationIndex = 0
def WalkingAnimation(x, y, flipImageHorizontal):
    global walkAnimationIndex
    playerWalkDustAnimation = [
        pygame.image.load("assets/vfx/dustCloud/1.png"),
        pygame.image.load("assets/vfx/dustCloud/2.png"),
        pygame.image.load("assets/vfx/dustCloud/3.png"),
        pygame.image.load("assets/vfx/dustCloud/4.png"),
        pygame.image.load("assets/vfx/dustCloud/5.png"),
        pygame.image.load("assets/vfx/dustCloud/6.png"),
        pygame.image.load("assets/vfx/dustCloud/7.png"),
        pygame.image.load("assets/vfx/dustCloud/8.png"),
    ]
    walkAnimationIndex += 1
    if walkAnimationIndex > (len(playerWalkDustAnimation) - 1):
        walkAnimationIndex = 0
    image = playerWalkDustAnimation[walkAnimationIndex].convert_alpha()
    image.set_alpha(80)
    image = pygame.transform.scale(image, (50, 50))
    image = pygame.transform.flip(image, flipImageHorizontal, False)
    if flipImageHorizontal == True:
        x += 80
    else:      
        x -= 15
    screen.blit(image, (x, y + 100))



# Zombie
class Zombie:
    def __init__(self):
        self.health = 80
        self.x = random.randint(0, screenW - 220)
        self.y = screenH - 220
        self.speed = 6
        self.xSpeed = self.speed
        self.ySpeed = self.speed
        self.animationIndex = 0
        global listOfZombies
        if random.randint(0,1) < 1:
            self.zombieIdleAnimation = [
                pygame.image.load("assets/characters/zombies/male/Idle (1).png"),
                pygame.image.load("assets/characters/zombies/male/Idle (2).png"),
                pygame.image.load("assets/characters/zombies/male/Idle (3).png"),
                pygame.image.load("assets/characters/zombies/male/Idle (4).png"),
                pygame.image.load("assets/characters/zombies/male/Idle (5).png"),
                pygame.image.load("assets/characters/zombies/male/Idle (6).png"),
                pygame.image.load("assets/characters/zombies/male/Idle (7).png"),
                pygame.image.load("assets/characters/zombies/male/Idle (8).png"),
                pygame.image.load("assets/characters/zombies/male/Idle (9).png"),
                pygame.image.load("assets/characters/zombies/male/Idle (10).png"),
                pygame.image.load("assets/characters/zombies/male/Idle (11).png"),
                pygame.image.load("assets/characters/zombies/male/Idle (12).png"),
                pygame.image.load("assets/characters/zombies/male/Idle (13).png"),
                pygame.image.load("assets/characters/zombies/male/Idle (14).png"),
                pygame.image.load("assets/characters/zombies/male/Idle (15).png"),
            ]
            self.zombieWalkAnimation = [
                pygame.image.load("assets/characters/zombies/male/Walk (1).png"),
                pygame.image.load("assets/characters/zombies/male/Walk (2).png"),
                pygame.image.load("assets/characters/zombies/male/Walk (3).png"),
                pygame.image.load("assets/characters/zombies/male/Walk (4).png"),
                pygame.image.load("assets/characters/zombies/male/Walk (5).png"),
                pygame.image.load("assets/characters/zombies/male/Walk (6).png"),
                pygame.image.load("assets/characters/zombies/male/Walk (7).png"),
                pygame.image.load("assets/characters/zombies/male/Walk (8).png"),
                pygame.image.load("assets/characters/zombies/male/Walk (9).png"),
                pygame.image.load("assets/characters/zombies/male/Walk (10).png"),
            ]
            self.zombieAttackAnimation = [
                pygame.image.load("assets/characters/zombies/male/Attack (1).png"),
                pygame.image.load("assets/characters/zombies/male/Attack (2).png"),
                pygame.image.load("assets/characters/zombies/male/Attack (3).png"),
                pygame.image.load("assets/characters/zombies/male/Attack (4).png"),
                pygame.image.load("assets/characters/zombies/male/Attack (5).png"),
                pygame.image.load("assets/characters/zombies/male/Attack (6).png"),
                pygame.image.load("assets/characters/zombies/male/Attack (7).png"),
                pygame.image.load("assets/characters/zombies/male/Attack (8).png"),
            ]
            self.zombieDeadAnimation = [
                pygame.image.load("assets/characters/zombies/male/Dead (1).png"),
                pygame.image.load("assets/characters/zombies/male/Dead (2).png"),
                pygame.image.load("assets/characters/zombies/male/Dead (3).png"),
                pygame.image.load("assets/characters/zombies/male/Dead (4).png"),
                pygame.image.load("assets/characters/zombies/male/Dead (5).png"),
                pygame.image.load("assets/characters/zombies/male/Dead (6).png"),
                pygame.image.load("assets/characters/zombies/male/Dead (7).png"),
                pygame.image.load("assets/characters/zombies/male/Dead (8).png"),
                pygame.image.load("assets/characters/zombies/male/Dead (9).png"),
                pygame.image.load("assets/characters/zombies/male/Dead (10).png"),
                pygame.image.load("assets/characters/zombies/male/Dead (11).png"),
                pygame.image.load("assets/characters/zombies/male/Dead (12).png"),
            ]
        else:
            self.zombieIdleAnimation = [
                pygame.image.load("assets/characters/zombies/female/Idle (1).png"),
                pygame.image.load("assets/characters/zombies/female/Idle (2).png"),
                pygame.image.load("assets/characters/zombies/female/Idle (3).png"),
                pygame.image.load("assets/characters/zombies/female/Idle (4).png"),
                pygame.image.load("assets/characters/zombies/female/Idle (5).png"),
                pygame.image.load("assets/characters/zombies/female/Idle (6).png"),
                pygame.image.load("assets/characters/zombies/female/Idle (7).png"),
                pygame.image.load("assets/characters/zombies/female/Idle (8).png"),
                pygame.image.load("assets/characters/zombies/female/Idle (9).png"),
                pygame.image.load("assets/characters/zombies/female/Idle (10).png"),
                pygame.image.load("assets/characters/zombies/female/Idle (11).png"),
                pygame.image.load("assets/characters/zombies/female/Idle (12).png"),
                pygame.image.load("assets/characters/zombies/female/Idle (13).png"),
                pygame.image.load("assets/characters/zombies/female/Idle (14).png"),
                pygame.image.load("assets/characters/zombies/female/Idle (15).png"),
            ]
            self.zombieWalkAnimation = [
                pygame.image.load("assets/characters/zombies/female/Walk (1).png"),
                pygame.image.load("assets/characters/zombies/female/Walk (2).png"),
                pygame.image.load("assets/characters/zombies/female/Walk (3).png"),
                pygame.image.load("assets/characters/zombies/female/Walk (4).png"),
                pygame.image.load("assets/characters/zombies/female/Walk (5).png"),
                pygame.image.load("assets/characters/zombies/female/Walk (6).png"),
                pygame.image.load("assets/characters/zombies/female/Walk (7).png"),
                pygame.image.load("assets/characters/zombies/female/Walk (8).png"),
                pygame.image.load("assets/characters/zombies/female/Walk (9).png"),
                pygame.image.load("assets/characters/zombies/female/Walk (10).png"),
            ]
            self.zombieAttackAnimation = [
                pygame.image.load("assets/characters/zombies/female/Attack (1).png"),
                pygame.image.load("assets/characters/zombies/female/Attack (2).png"),
                pygame.image.load("assets/characters/zombies/female/Attack (3).png"),
                pygame.image.load("assets/characters/zombies/female/Attack (4).png"),
                pygame.image.load("assets/characters/zombies/female/Attack (5).png"),
                pygame.image.load("assets/characters/zombies/female/Attack (6).png"),
                pygame.image.load("assets/characters/zombies/female/Attack (7).png"),
                pygame.image.load("assets/characters/zombies/female/Attack (8).png"),
            ]
            self.zombieDeadAnimation = [
                pygame.image.load("assets/characters/zombies/female/Dead (1).png"),
                pygame.image.load("assets/characters/zombies/female/Dead (2).png"),
                pygame.image.load("assets/characters/zombies/female/Dead (3).png"),
                pygame.image.load("assets/characters/zombies/female/Dead (4).png"),
                pygame.image.load("assets/characters/zombies/female/Dead (5).png"),
                pygame.image.load("assets/characters/zombies/female/Dead (6).png"),
                pygame.image.load("assets/characters/zombies/female/Dead (7).png"),
                pygame.image.load("assets/characters/zombies/female/Dead (8).png"),
                pygame.image.load("assets/characters/zombies/female/Dead (9).png"),
                pygame.image.load("assets/characters/zombies/female/Dead (10).png"),
                pygame.image.load("assets/characters/zombies/female/Dead (11).png"),
                pygame.image.load("assets/characters/zombies/female/Dead (12).png"),
            ]

        #self.image = pygame.image.load(self.playerSprites[self.animationIndex])
        self.idleScale = (110, 175)
        self.runScale = (120, 175)
        self.attackScale = (150, 165)
        self.deadScale = (160, 170)
        self.currentScale = self.idleScale
        self.image = pygame.image.load("assets/characters/zombies/male/Idle (1).png")
        self.image = pygame.transform.scale(self.image, self.currentScale)
        self.currentAnimation = self.zombieIdleAnimation
        self.flipImageHorizontal = False
        self.direction = 0
        self.font = pygame.font.Font("assets/fonts/Abel-Regular.ttf", 20)
        self.isDead = False
        self.bodyCutSound = mixer.Sound("assets/soundeffects/mixkit-gore-video-game-blood-splash-263.wav")
        self.bodyCutSound.set_volume(0.1)
    def blit(self):
        screen.blit(self.image, (self.x, self.y))
    def moveIdle(self):
        self.direction = 0
        self.currentAnimation = self.zombieIdleAnimation
        self.currentScale = self.idleScale
    def moveLeft(self):
        self.direction = 1
        self.currentAnimation = self.zombieWalkAnimation
        self.flipImageHorizontal = True
        self.currentScale = self.runScale
    def moveRight(self):
        self.direction = 2
        self.currentAnimation = self.zombieWalkAnimation
        self.flipImageHorizontal = False
        self.currentScale = self.runScale
    def moveAttack(self):
        self.direction = 0
        self.currentAnimation = self.zombieAttackAnimation
        self.currentScale = self.attackScale
    # Post Process
    def animate(self):
        self.image = self.currentAnimation[self.animationIndex]
        self.image = pygame.transform.scale(self.image, self.currentScale)
        self.image = pygame.transform.flip(self.image, self.flipImageHorizontal, False)
        self.healthScore()
    # Box Constrains
    def windowConstraints(self):
        if self.x < 0:
            self.x = 0
        elif self.x > screenW - self.currentScale[0]:
            self.x = screenW - self.currentScale[0]
    # Move
    def move(self):
        self.windowConstraints()
        if self.direction == 0:     # Idle
            self.x += 0
        elif self.direction == 1:   # Left
            self.x += -self.xSpeed
        elif self.direction == 2:   # Right
            self.x += self.xSpeed
    # Health
    def healthScore(self):
        self.font = pygame.font.Font("assets/fonts/Abel-Regular.ttf", 20)
        if self.health >= 80:
            healthColor = (0, 255, 0)
        elif self.health >= 50:
            healthColor = (0, 200, 0)
        elif self.health >= 20:
            healthColor = (255, 255, 0)
        elif self.health < 20:
            healthColor = (255, 0, 0)
        elif self.health <= 0:
            healthColor = (0, 0, 0)
        enemyHealth = self.font.render(str(self.health), True, healthColor)
        screen.blit(enemyHealth, (self.x + 50, self.y - 15))
    # Interact
    def interact(self, playerX, playerY, isPlayerAttacking):
        distance = math.sqrt( math.pow((playerX - self.x), 2) + math.pow((playerY - self.y), 2) )        
        if distance < 80:
            self.currentAnimation = self.zombieAttackAnimation
        else:
            self.currentAnimation = self.zombieIdleAnimation
        if distance > 80:
            if playerX > self.x:
                self.moveRight()
            elif playerX < self.x:
                self.moveLeft()
            else:
                self.moveIdle()
        if isPlayerAttacking == True:
            if distance < 140:
                global attackSize
                self.bodyCutSound.play()
                self.health -= attackSize
                self.currentAnimation = self.zombieAttackAnimation
        
            
    # Update
    def update(self, playerX, playerY, isPlayerAttacking):
        if self.health >= 1:
            self.interact(playerX, playerY, isPlayerAttacking)
            self.move()
            self.animationIndex += 1
            if self.animationIndex > len(self.currentAnimation) - 1:
                self.animationIndex = 0
            self.animate()
        else:
            if self.isDead == False:
                global listOfZombies, numOfKills, delayTime
                newNumOfZombies = random.randint(1, 3)
                delayTime -= 1
                if delayTime <= 1:
                    delayTime = 5
                numOfKills += 1
                #zombie = Zombie()            
                #listOfZombies.append(zombie)
                #while len(listOfZombies) > 10:
                #    del listOfZombies[0]
                zombie = Zombie()
                listOfZombies.append(zombie)
                global attackSize, player
                randomRoll = random.randint(0, 3)
                if randomRoll == 0:                    
                    attackSize += random.randint(1, 3)
                    if attackSize >= 6:
                        attackSize = 6
                if randomRoll == 1:                    
                    player.health += random.randint(5, 10)
                    if player.health >= 100:
                        player.health = 100
                if randomRoll == 2:                    
                    player.speed += random.randint(5, 10)
                    if player.speed >= 20:
                        player.speed = 20
                if randomRoll == 3:                    
                    zombie.speed += random.randint(5, 10)
                    if zombie.speed >= 20:
                        zombie.speed = 20
                self.y += 20  
            self.currentAnimation = self.zombieDeadAnimation
            self.image = self.zombieDeadAnimation[len(self.zombieDeadAnimation) - 1]
            self.currentScale = self.deadScale
            self.image = pygame.transform.scale(self.image, self.currentScale)
            self.image = pygame.transform.flip(self.image, self.flipImageHorizontal, False)
            self.isDead = True
            #gom.update()
        

class GameObjectManager():
    def __init__(self):
        pass
    def update(self):
        global pauseUpdate
        pauseUpdate = True
    def cleanZombies(self):
        global listOfZombies, pauseUpdate
        if len(listOfZombies) > 5:
            listOfZombies.reverse()
            listOfZombies.pop()
        pauseUpdate = False

def muteSound(state):
    if state == True:
        mixer.Sound.stop()

class rainDrop:
    def __init__(self) -> None:
        self.x = random.randint(0, screenW)
        self.y = 0
        self.w = random.randint(0, 3)
        self.h = random.randint(0, 4)
class Weather():
    def __init__(self) -> None:
        pass
    def rainOrSnow(self):
        global ros, rainSnowSpeed
        if ros == 0:
            self.color = (0, 0, 255)
        else:
            self.color = (255, 255, 255)
        rain = rainDrop()
        listOfRainDrops.append(rain)
        for i in range(0, len(listOfRainDrops) - 1):
            listOfRainDrops[i].y += rainSnowSpeed
            if listOfRainDrops[i].y >= screenH - 46:
                listOfRainDrops[i].y = screenH - 46
            #listOfRainDrops[i] += 2
            pygame.draw.rect(screen, self.color, (listOfRainDrops[i].x, listOfRainDrops[i].y, listOfRainDrops[i].w ,listOfRainDrops[i].h), 2)

# Game Loop
attackSize = 2
ros = random.randint(0, 1)
rainSnowSpeed = random.randint(2, 6)
rain = rainDrop()
listOfRainDrops = [rain]
isSoundMute = False
isGameRunning = True
delayTime = 20
ui = UI()
weather = Weather()
ui.backgroundMusic()
gom = GameObjectManager()
player = Player()
numOfKills = 0
background = pygame.image.load("assets/backgrounds/2.jpg")
background = pygame.transform.scale(background, ((background.get_width() - 4200), screenH))
backgroundX = 0
isGameOver = False
pauseUpdate = False
isGameStarting = True
def gameInit():
    global isGameRunning, delayTime, player,numOfKills, listOfZombies, backgroundX, isGameOver, pauseUpdate, isGameStarting, isSoundMute, listOfRainDrops, ros, rainSnowSpeed
    ros = random.randint(0, 1)
    rainSnowSpeed = random.randint(2, 6)
    rain = rainDrop()
    listOfRainDrops = [rain]
    isGameRunning = True
    isGameStarting = False
    delayTime = 20
    player = Player()
    numOfKills = 0
    zombie = Zombie()
    listOfZombies = []  
    listOfZombies.append(zombie)    
    screen.fill((0,0,0))
    background = pygame.image.load("assets/backgrounds/2.jpg")
    background = pygame.transform.scale(background, ((background.get_width() - 5800), screenH))
    backgroundX = 0
    isGameOver = False
    pauseUpdate = False


# Game Loop
while isGameRunning:
    if isGameStarting == True:
        ui.startGame()
        #ui.backgroundMusic()
    if pauseUpdate == False and isGameStarting == False:
        # Blits
        screen.fill((100,100,100))
        # Scene
        screen.blit(background, (backgroundX, 0))

        # Characters
        if player.isDead == False:
            for zombies in listOfZombies:
                zombies.blit()
            player.blit()
        # Score
        playerKills = font.render("Kills " + str(numOfKills), True, (255, 255, 255))
        screen.blit(playerKills, (10, 5))
        playerPower = font.render("Power " + str(attackSize), True, (255, 255, 255))
        screen.blit(playerPower, (10, 35))

    # Events
    for event in pygame.event.get():
        # Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.moveLeft()
            if event.key == pygame.K_RIGHT:
                player.moveRight()
            if event.key == pygame.K_q:
                pygame.quit()
            if event.key == pygame.K_SPACE:
                pauseUpdate == False
                if isGameStarting == True:
                    gameInit()                    
                if isGameOver == True:
                    gameInit()
                else: 
                    player.moveAttack()        
                isGameStarting == False    
            if event.key == pygame.K_p:
                ui.pauseGame()
            if event.key == pygame.K_m:
                if isSoundMute == True:
                    isSoundMute = False
                    ui.backgroundMusic()
                elif isSoundMute == False:
                    isSoundMute = True
                    ui.backgroundMusic()

        if event.type == pygame.KEYUP:
                player.moveIdle() 
        
        # Exit
        if event.type == pygame.QUIT:
            isGameRunning = False

    # Updates
    pygame.time.delay(delayTime)
    if pauseUpdate == False:
        if player.isDead == False:
            for zombies in listOfZombies:
                zombies.update(player.x, player.y, player.isAttacking)
                if zombies.isDead == False:
                    player.update(zombies)
    if isGameOver == True:
        ui.displayGameOverText()
    weather.rainOrSnow()

    pygame.display.update()
pygame.quit()




