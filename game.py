import pygame
import random
import math
import sys
import os

#inicializar pygame
pygame.init()

#establecer el tamaño de la pantalla

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))

#funcion para obtener la ruta de los recurosos

def resource_path(relative_path): 
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        return os.path.join(base_path,relative_path)

#cargar las imagenes de fondo
asset_background = resource_path('assets/images/background.png')
background = pygame.image.load(asset_background)

#cargar los iconos de las ventanas
asset_icon =resource_path('assets/images/ufo.png')
icon = pygame.image.load(asset_icon)


#cargar sonido de fondo
asset_sound =resource_path('assets/audios/background_music.mp3')
background_sound = pygame.mixer.music.load(asset_sound)


#cargar del jugador
asset_playerimg =resource_path('assets/images/space-invaders.png')
playerimg = pygame.image.load(asset_playerimg)

#cargar imagen de la balla
asset_bulletimg = resource_path('assets/images/bullet.png')
bulletimg = pygame.image.load(asset_bulletimg)

#cargar fuente para el texto de game over
asset_over_font = resource_path('assets/fonts/RAVIE.TTF')
over_font= pygame.font.Font(asset_over_font)

#cargar fuente para el texto de puntaje
asset_font = resource_path('assets/fonts/comicbd.ttf')
font= pygame.font.Font(asset_font)


#titulo de la ventana

pygame.display.set_caption("Alien Swarm")

#establecer icono de ventana
pygame.display.set_icon(icon)

#reproducir sonido de fondo

pygame.mixer.music.play(-1)

#crear reloj para controlar la velocidad
clock = pygame.time.Clock()

#posicion inicial del jugador
playerX = 370
playerY= 470
playerx_change = 0
playery_change= 0

#lista para almacenar posicion de los enemigos
enemyimg= []
enemyX= []
enemyY= []
enemyX_change= []
enemyY_change= []
no_of_enemies= 10

#iniciarlicar las variables para guardar las posiciones de los enemigos

for i in range(no_of_enemies):

    #imagenes de los enemigos1
    enemy1 = resource_path('assets/images/enemy1.png')
    enemyimg.append(pygame.image.load(enemy1))

    #imagenen enemigo 2
    enemy2 = resource_path('assets/images/enemy2.png')
    enemyimg.append(pygame.image.load(enemy2))

#se asigna una posicion aleatoria en X y Y para los enemigos

enemyX.append(random.randint(0, 736))
enemyY.append(random.randint(0, 150))

#se establece la velocidad de movimiento del enemigo en X y Y

enemyX_change.append(5)
enemyY_change.append(20)

#se inicializanlas variables para guardar la posicion de la bala

bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change= 10
bullet_state = "ready"


#se inicializa la puntuacion en 0
score = 0


#funcion para mostrar la puntacion en la pantalla

def show_score():
    score_value = font.render("SCORE " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (10, 10))
    
#funcion para dibujar a el jugador en la pantalla

def player(x, y):
    screen.blit(playerimg,(x , y))


#dibujar a el enemigo

# ...

def enemy(x, y , i):
    screen.blit(enemyimg[i], (x, y))

# Función para disparar la bala
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))

# ...

        

#funcion para comprobar si ha habido una colision entre la bala y el enemigo

def isCollision(enemyX, enemyY, bulletX, bullletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) +
                         (math.pow(enemyY-bulletY, 2)))
    
    if distance < 27:
        return True
    else:
        return False
    

#funcion para mostrar el texto de game over en pantalla

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    text_rect = over_text.get_rect(
        center=(int(screen_width/2), int(screen_height/2)))
    screen.blit(over_text, text_rect)


#blucle principal del juego

def gameloop():
    #declarar variables goblales

    global score
    global playerX
    global playerx_change
    global bulletX
    global bulletY
    global Collision
    global bullet_state

    in_game= True
    while in_game:
        #maneja evento, actualiza y renderiza el juego y limpia la pantalla
        screen.fill((0, 0, 0))
        screen.blit(background,(0 , 0))
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
                pygame.quit()
                sys.exit()

            if event.type ==pygame.KEYDOWN:
                #maneja el movimiento del jugador y el disparo
                if event.key == pygame.K_LEFT:
                    playerx_change = -5
                if event.key == pygame.K_RIGHT:
                    playerx_change = 5

                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = playerX
                    fire_bullet(bulletX,bulletY)
                    if event.type == pygame.KEYUP:
                        playerx_change = 0

                    
        #aqui se esta actualizando la posicion del jugador
        playerX += playerx_change

        if playerX <=0:
         playerX = 0
        elif playerX >= 736:
            playerX = 736

            #bucle que se ejecuta para todos los enemigos
            for i in range(no_of_enemies):
                if enemyY[i] > 440:
                    for j in range(no_of_enemies):
                        enemyY[j] = 2000
                    game_over_text()

                enemyX[i] += enemyX_change[i]
                if enemyX[i] <= 0:
                    enemyX_change[i] = 5
                    enemyY[i] += enemyY_change[i]
                elif enemyX[i] >= 736:
                    enemyX_change[i] = -5
                    enemyY[i] += enemyY_change[i]
            
                #aqui si ha habido una colision con un enemigo y una bala
                
                collision = isCollision (enemyX[i], enemyY[i],bulletX, bulletY)
                if collision:
                    bulletY = 454
                    bullet_state = "ready"
                    score += 1
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(0, 150)
                enemy(enemyX[i], enemyY[i], i)

            if bulletY <0:
                    bulletY = 454
                    bullet_state = "ready"
                    
            if bullet_state == "fire":
             fire_bullet(bulletX,bulletY)
            bulletY -= bulletY_change

            player(playerX, playerY)
            show_score()
            pygame.display.update

            clock.tick(120)


gameloop()