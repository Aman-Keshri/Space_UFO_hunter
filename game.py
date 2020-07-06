import pygame
import random
import math
import os
from pygame import mixer
import time

#intialize pygame
pygame.init()

#create game screen
screen = pygame.display.set_mode((800,600))

#background
background = pygame.image.load(os.path.join("assets","background.png"))

#background sound
mixer.music.load(os.path.join("assets","background_music.wav"))
mixer.music.play(-1)

#caption and icon
pygame.display.set_caption("Space")
icon = pygame.image.load(os.path.join("assets","icon.png"))
pygame.display.set_icon(icon)

#Bullet
bullet_state = "ready"

#enemy
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemy = 5

#player function
def player(x,y,playerimg):
	screen.blit(playerimg,(x,y))

#enemy function
def enemy(x,y,i,enemyimg):
	screen.blit(enemyimg[i],(x,y))

#bullet function
def fire_bullet(x,y,bulletimg):
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

font = pygame.font.Font('freesansbold.ttf',32)

#level
level_value = 1

levelx = 590
levely = 10

#level function
def show_level(x,y):
	level = font.render("Level :" + str(level_value) ,True ,(255,255,255))
	screen.blit(level, (x,y))

#score
score_value = 0

textx = 10
texty = 10

#score function
def show_score(x,y):
	score = font.render("Score :" + str(score_value) ,True ,(255,255,255))
	screen.blit(score, (x,y))

#main screen text
main_font1 = pygame.font.Font('freesansbold.ttf',40)
main_font2 = pygame.font.Font('freesansbold.ttf',20)

#game over function
def game_over_text(msg,x,y,size):

	over_font = pygame.font.Font('freesansbold.ttf',size)
	over_text = over_font.render(msg,True ,(255,255,255))
	screen.blit(over_text,(x,y))

#enemy
def create_enemey(num_of_enemy):
	for i in range(num_of_enemy):
		if i%2 == 0:
			enemyimg.append(pygame.image.load(os.path.join("assets","spaceship.png")))
		else:
			enemyimg.append(pygame.image.load(os.path.join("assets","alien.png")))
		enemyx.append(random.randint(2,736))
		enemyy.append(random.randint(60,150))
		enemyx_change.append(2)
		enemyy_change.append(40)


def main_screen():

	intro = True
	screen.fill((0,0,0))
	main_icon = pygame.image.load(os.path.join("assets","invaders.png"))

	while intro:

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					intro = False
					game_loop()
				if event.key == pygame.K_q:
					pygame.quit()
			
		main_text1 = main_font1.render("Welcome to Space Gunship",True ,(255,255,255))
		screen.blit(main_text1,(130,150))

		main_text2 = main_font2.render("The objective is to destory the UFO's",True,(255,255,255))
		screen.blit(main_text2,(205,400))

		main_text3 = main_font2.render("If the UFO reach your aircraft then,you will die",True,(255,255,255))
		screen.blit(main_text3,(165,430))

		main_text4 = main_font2.render("Press C to continue or Q to quit",True,(255,255,255))
		screen.blit(main_text4,(225,460))

		screen.blit(main_icon,(330,250))
		pygame.display.update()



#game over page
def game_over():

	g_over = True

	while g_over:
		screen.fill((0,0,0))
		screen.blit(background,(0,0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				g_over = False
				pygame.quit()

			#keystroke is pressed
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					g_over = False
					main_screen()
					break

				if event.key == pygame.K_q:
					pygame.quit()

		game_over_text("GAME OVER",200,200,64)
		game_over_text("Press Q to quit or Restart to play again",200,350,20)
		pygame.display.update()



#Game Loop
def game_loop():

	running = True

	#player
	playerimg = pygame.image.load(os.path.join("assets","11.png"))
	playerx = 370
	playery = 480
	playerx_change = 0

	#enemy
	global enemyimg
	global enemyx
	global enemyy 
	global enemyx_change 
	global enemyy_change 
	global num_of_enemy

	num_of_enemy=5
	
	create_enemey(num_of_enemy)

	#Bullet
	bulletimg = pygame.image.load(os.path.join("assets","bullet.png"))
	bulletx = 0
	bullety = 480
	bulletx_change = 0
	bullety_change = 10

	global bullet_state 
	global score_value
	global level_value

	g_over = False
	k=1
	level = 1
	
	while running:
		#RGB--> Red, Green, Blue
		screen.fill((0, 0, 0))
		#background image
		screen.blit(background,(0,0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()

			#keystroke is pressed
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					playerx_change = -4
				if event.key == pygame.K_RIGHT:
					playerx_change = 4
				if event.key == pygame.K_SPACE:
					if bullet_state is "ready":
						bullet_sound = mixer.Sound(os.path.join("assets","laser_music.wav"))
						bullet_sound.play()
						bulletx = playerx
						fire_bullet(bulletx,bullety,bulletimg)
				if event.key == pygame.K_r:
					score_value = 0
					game_loop()
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
			if enemyy[i] > 465: 
				for j in range(num_of_enemy):
					enemyy[j] = 2000
				g_over = True
				game_over()	
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
				explosion_sound = mixer.Sound(os.path.join("assets","explosion_music.wav"))
				explosion_sound.play()
				bullety = 480
				bullet_state = "ready"
				score_value += 1
				enemyx[i] = random.randint(2,736)
				enemyy[i] = random.randint(60,150)
		
				if score_value > (10*k):
					k+=1
					if num_of_enemy < 10:
						num_of_enemy += 1
						create_enemey(num_of_enemy)
					increment = 4
					enemyx_change[i] +=increment 
					enemyy[i] +=enemyy_change[i]
					level_value += 1

	

			enemy(enemyx[i],enemyy[i],i,enemyimg)

		#bullet movement
		if bullety <= 0:
			bullety = 480
			bullet_state = "ready"

		if bullet_state is "fire":
			fire_bullet(bulletx,bullety,bulletimg)
			bullety -= bullety_change

		#calling the function to run the game
		player(playerx,playery,playerimg)
		show_score(textx,texty)
		show_level(levelx,levely)
		pygame.display.update()

main_screen()
