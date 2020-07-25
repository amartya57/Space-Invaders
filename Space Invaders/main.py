#author - @amartya057

import pygame
import random
import math
import numpy as np
from pygame import mixer
import io

#innitializing pygame
pygame.init()

#creating the game screen
screen=pygame.display.set_mode((626,626))

#Adding background image
background=pygame.image.load("background.png")

#Adding Background music
mixer.music.load("background.wav")
mixer.music.play(-1)

#Title and icon added
pygame.display.set_caption("Corona Shooter")
icon=pygame.image.load("alien.png")
pygame.display.set_icon(icon)

#High Score
f=io.open("HighScore.txt","r")
high_score_value=f.read(4)
high_output=io.open("HighScore.txt","w")
font_high=pygame.font.Font("freesansbold.ttf", 40)
highX=10
highY=70
#print(high_score_value)

def show_high(x,y):
	high_score=font.render("HIGH SCORE : " + str(high_score_value), True, (255,255,0))
	screen.blit(high_score, (x,y))

#Scoring
score_value=0
font=pygame.font.Font("freesansbold.ttf", 40)
textX=10
textY=10

def show_score(x,y):
	score=font.render("SCORE : " + str(score_value), True, (255,255,0))
	screen.blit(score, (x,y))

#Game_Over
over_font=pygame.font.Font("freesansbold.ttf", 50)

def game_over_test():
	over_text=over_font.render("GAME OVER",True,(255,255,0))
	screen.blit(over_text, (150,150))
	show_score(textX,textY)

#Adding Player Image
playerImg=pygame.image.load("space-invaders.png")
playerX=300
playerY=500
playerX_change=0

def player(x,y):
	screen.blit(playerImg,(x,y))

#Adding Enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_enemies=5

for i in range(num_enemies):
	enemyImg.append(pygame.image.load("coronavirus.png"))
	enemyX.append(random.randint(0,562))
	enemyY.append(random.randint(10,30))
	enemyX_change.append(0.3)
	enemyY_change.append(25)

def enemy(x,y,i):
	screen.blit(enemyImg[i],(x,y))

#Bullet
bullet=pygame.image.load("bullet.png")
bulletX=0
bulletY=500
bulletX_change=0
bulletY_change=2
bullet_state="ready"
# ready- Can't see the bullet on screen
# fire- Bullet is currently moving

def fire_bullet(x,y):
	global bullet_state
	bullet_state="fire"
	screen.blit(bullet,(x+16,y-10))


def is_Collision(enemyX,enemyY,bulletX,bulletY):
	distance=math.sqrt(math.pow((enemyX-bulletX),2)+math.pow((enemyY-bulletY),2))
	if distance<25:
		return True
	else:
		return False

#game loop
running=True
while running:

    #Filling colors into the gameplay screen
    screen.fill((0,0,128))

    #background
    screen.blit(background,(0,0))

    #Option to quit game screen
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
        	try:
        		high_output.write(str(high_score_value))
        	except:
        		pass
        	running= False

        #if keystroke is pressed, check if its left or right
        if event.type==pygame.KEYDOWN:
        	#moving the player
        	if event.key==pygame.K_LEFT:
        		#print("Left Key pressed")
        		playerX_change=-0.5
        	if event.key==pygame.K_RIGHT:
        		#print("Right Key pressed")
        		playerX_change=0.5
        	#firing the bullet
        	if event.key==pygame.K_SPACE and bullet_state is "ready":
        		bullet_sound=mixer.Sound("laser.wav")
        		bullet_sound.play()
        		bulletX=playerX
        		fire_bullet(bulletX,bulletY)


        #Check if key is released
        if event.type==pygame.KEYUP:
        	if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
        		#print("Keystroke has been released")
        		playerX_change=0

    #Incrementing the playerX value
    playerX+=playerX_change


    #Adding game Boundary
    if playerX<0:
    	playerX=0
    if playerX>562:
    	playerX=562

    #movement of enemy
    for i in range(num_enemies):

    	if enemyY[i]>445 and enemyX[i]>250 and enemyX[i]<350:
    		for j in range(num_enemies):
    			enemyY[j]=2000
    		game_over_test()
    		if(score_value>int(high_score_value)):
    			high_score_value=score_value
	    		try:
	    			high_output.write(str(high_score_value))
	    		except :
	    			pass
    		high_output.close()
    		break


    	enemyX[i]+=enemyX_change[i]

    	if enemyX[i]>562:
    		enemyX_change[i]=-enemyX_change[i]
    		enemyY[i]+=enemyY_change[i]

    	if enemyX[i]<0:
    		enemyX_change[i]=-enemyX_change[i]
    		enemyY[i]+=enemyY_change[i]

    	#Collision
    	collision=is_Collision(enemyX[i],enemyY[i],bulletX,bulletY)
    	if collision:
    		score_value+=1
    		bulletY=500
    		bullet_state="ready"
    		#speed up enemy
    		enemyX_change[i]=enemyX_change[i]+np.sign(enemyX_change[i])*0.05
    		enemyY_change[i]+=3

    		enemyX[i]=random.randint(0,562)
    		enemyY[i]=random.randint(10,30)
    		collision=False

    	#Calling Enemy function
    	enemy(enemyX[i],enemyY[i],i)    	

    #Bullet Movement

    #Reseting the bullet for multiple fire
    if bulletY<=0:
    	bulletY=500
    	bullet_state="ready"

    if bullet_state is "fire":
    	fire_bullet(bulletX,bulletY)
    	bulletY-=bulletY_change

    #Displaying the score
    show_score(textX, textY)

    #Displaying High Score
    show_high(highX,highY)

    #Calling the player function
    player(playerX,playerY)
    
    #updating the display
    pygame.display.update()
