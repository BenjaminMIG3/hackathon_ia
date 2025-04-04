import pygame
import random

# Initialisation de pygame
pygame.init()

# Définition des constantes
WIDTH, HEIGHT = 600, 400
SNAKE_SIZE = 10
VELOCITY = 10
WHITE, GREEN, RED, BLACK, GRID_COLOR = (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0), (50, 50, 50)

# Création de la fenêtre
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Charger l'image de fond
background = pygame.image.load("image.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Adapter à la taille de la fenêtre

# Fonction principale du jeu
def game():
    snake_pos = [[100, 50]]
    direction = 'RIGHT'
    food_pos = [random.randrange(1, WIDTH//SNAKE_SIZE) * SNAKE_SIZE,
                random.randrange(1, HEIGHT//SNAKE_SIZE) * SNAKE_SIZE]
    running, grow = True, False
    clock = pygame.time.Clock()

    while running:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'
                elif event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'

        # Déplacement du serpent
        x, y = snake_pos[0]
        if direction == 'LEFT': x -= SNAKE_SIZE
        if direction == 'RIGHT': x += SNAKE_SIZE
        if direction == 'UP': y -= SNAKE_SIZE
        if direction == 'DOWN': y += SNAKE_SIZE
        snake_pos.insert(0, [x, y])

        # Vérification de la collision avec la nourriture
        if snake_pos[0] == food_pos:
            food_pos = [random.randrange(1, WIDTH//SNAKE_SIZE) * SNAKE_SIZE,
                        random.randrange(1, HEIGHT//SNAKE_SIZE) * SNAKE_SIZE]
        else:
            snake_pos.pop()

        # Vérification des collisions avec les murs ou le corps du serpent
        if (x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or snake_pos[0] in snake_pos[1:]):
            running = False

        # Affichage
        win.blit(background, (0, 0))  # Dessiner l'image de fond
        
        # Dessiner le quadrillage
        for i in range(0, WIDTH, SNAKE_SIZE):
            pygame.draw.line(win, GRID_COLOR, (i, 0), (i, HEIGHT))
        for j in range(0, HEIGHT, SNAKE_SIZE):
            pygame.draw.line(win, GRID_COLOR, (0, j), (WIDTH, j))
        
        pygame.draw.rect(win, RED, (*food_pos, SNAKE_SIZE, SNAKE_SIZE))
        for segment in snake_pos:
            pygame.draw.rect(win, GREEN, (*segment, SNAKE_SIZE, SNAKE_SIZE))
        pygame.display.update()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    game()
