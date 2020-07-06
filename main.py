import pygame
import random
import math
from pygame import mixer

#intialize pygame
pygame.init()

#create game screen
screen = pygame.display.set_mode((800,600))

#background
background = pygame.image.load('background.png')

#background sound
mixer.music.load('background_music.wav')
mixer.music.play(-1)

#caption and icon
pygame.display.set_caption("Space")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#player
playerimg = pygame.image.load('11.png')
playerx = 370
playery = 480
playerx_change = 0

#enemy
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemy = 5

for i in range(num_of_enemy):
	enemyimg.append(pygame.image.load('spaceship.png'))
	enemyx.append(random.randint(2,736))
	enemyy.append(random.randint(60,150))
	enemyx_change.append(2)
	enemyy_change.append(40)

#Bullet
bulletimg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 10
bullet_state = "ready"

#player function
def player(x,y):
	screen.blit(playerimg,(x,y))

#enemy function
def enemy(x,y,i):
	screen.blit(enemyimg[i],(x,y))

#bullet function
def fire_bullet(x,y):
	global bullet_state
	bullet_state = "fire"
	screen.blit(bulletimg, ( x , y + 10))
	screen.blit(bulletimg, ( x + 32, y + 10))

#collision function
def iscollision(enemyx,enemyy,bulletx,bullety):
	dist = math.sqrt(math.pow((enemyx-bulletx),2) + math.pow((enemyy-bullety),2))

	if dist < 35:
		return True
	else:
		return False

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textx = 10
texty = 10

#score function
def show_score(x,y):
	score = font.render("Score :" + str(score_value) ,True ,(255,255,255))
	screen.blit(score, (x,y))

#game over function

def game_over_text(msg,x,y,size):
	over_font = pygame.font.Font('freesansbold.ttf',size)
	over_text = over_font.render(msg,True ,(255,255,255))
	screen.blit(over_text,(x,y))
	

#main screen text
main_font1 = pygame.font.Font('freesansbold.ttf',40)
main_font2 = pygame.font.Font('freesansbold.ttf',20)


intro = True
screen.fill((0,0,0))
while intro:

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			pygame.quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_c:
				intro = False
			if event.key == pygame.K_q:
				pygame.quit()
		
	main_text1 = main_font1.render("Welcome to space Gunship",True ,(255,255,255))
	screen.blit(main_text1,(180,150))

	main_text2 = main_font2.render("The objective is to destory the UFO's",True,(255,255,255))
	screen.blit(main_text2,(190,300))

	main_text3 = main_font2.render("If the UFO reach your aircraft then,you will die",True,(255,255,255))
	screen.blit(main_text3,(190,330))

	main_text4 = main_font2.render("Press C to continue or Q to quit",True,(255,255,255))
	screen.blit(main_text4,(190,360))

	pygame.display.update()

#main_screen_text()

#Game Loop 
running = True

while running:
	#RGB--> Red, Green, Blue
	screen.fill((0, 0, 0))
	#background image
	screen.blit(background,(0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		#keystroke is pressed
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerx_change = -4
			if event.key == pygame.K_RIGHT:
				playerx_change = 4
			if event.key == pygame.K_SPACE:
				if bullet_state is "ready":
					bullet_sound = mixer.Sound('laser_music.wav')
					bullet_sound.play()
					bulletx = playerx
					fire_bullet(bulletx,bullety)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerx_change = 0	

	#player movement
	playerx += playerx_change

	if playerx <= 1:
		playerx = 1
	if playerx >=734:
		playerx = 734

	#enemy movement
	for i in range(num_of_enemy):

		#Game Over
		if enemyy[i] > 440: 
			for j in range(num_of_enemy):
				enemyy[j] = 2000

			game_over_text("GAME OVER",200,200,64)
			game_over_text("Press C to continue or Q to quit",240,350,20)
			break

		enemyx[i] += enemyx_change[i]
		if enemyx[i] <= 1:
			enemyx_change[i] = 2
			enemyy[i] +=enemyy_change[i]
		elif enemyx[i] >=734:
			enemyx_change[i] = -2
			enemyy[i] +=enemyy_change[i]

		#collision check
		collision = iscollision(enemyx[i],enemyy[i],bulletx,bullety)

		if collision:
			explosion_sound = mixer.Sound('explosion_music.wav')
			explosion_sound.play()
			bullety = 480
			bullet_state = "ready"
			score_value += 1
			enemyx[i] = random.randint(2,736)
			enemyy[i] = random.randint(60,150)

		enemy(enemyx[i],enemyy[i],i)

	#bullet movement
	if bullety <= 0:
		bullety = 480
		bullet_state = "ready"

	if bullet_state is "fire":
		fire_bullet(bulletx,bullety)
		bullety -= bullety_change

	#calling the function to run the game
	player(playerx,playery)
	show_score(textx,texty)
	pygame.display.update()