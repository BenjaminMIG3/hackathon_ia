import pygame
import random

# Initialisation de Pygame
pygame.init()

# Constantes
LARGEUR, HAUTEUR = 800, 600
TAILLE_CASE = 40  # Cases deux fois plus grandes
FENETRE = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Snake")

# Couleurs
BLANC = (255, 255, 255)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)
NOIR = (0, 0, 0)
GRIS = (100, 100, 100)  # Couleur pour le cadrillage

# Classe pour le serpent
class Serpent:
    def __init__(self):
        self.taille = 1
        self.corps = [((LARGEUR // 2) - (LARGEUR // 2) % TAILLE_CASE, 
                       (HAUTEUR // 2) - (HAUTEUR // 2) % TAILLE_CASE)]
        self.direction = (TAILLE_CASE, 0)  # Départ vers la droite
        self.nouvelle_direction = self.direction

    def bouger(self):
        self.direction = self.nouvelle_direction
        tete_x, tete_y = self.corps[0]
        dx, dy = self.direction
        nouvelle_tete = ((tete_x + dx) % LARGEUR, (tete_y + dy) % HAUTEUR)
        self.corps.insert(0, nouvelle_tete)
        if len(self.corps) > self.taille:
            self.corps.pop()

    def grandir(self):
        self.taille += 1

    def collision(self):
        return self.corps[0] in self.corps[1:]

# Position initiale de la nourriture
def nouvelle_nourriture(serpent):
    while True:
        x = random.randrange(0, LARGEUR, TAILLE_CASE)
        y = random.randrange(0, HAUTEUR, TAILLE_CASE)
        if (x, y) not in serpent.corps:
            return (x, y)

# Charger et redimensionner l'image de fond
background = pygame.image.load("image.png")
background = pygame.transform.scale(background, (LARGEUR, HAUTEUR))  # Correction : LARGEUR, HAUTEUR

# Initialisation
serpent = Serpent()
nourriture = nouvelle_nourriture(serpent)
vitesse = 10
horloge = pygame.time.Clock()
en_cours = True

# Boucle principale
while en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and serpent.direction != (0, TAILLE_CASE):
                serpent.nouvelle_direction = (0, -TAILLE_CASE)
            elif event.key == pygame.K_DOWN and serpent.direction != (0, -TAILLE_CASE):
                serpent.nouvelle_direction = (0, TAILLE_CASE)
            elif event.key == pygame.K_LEFT and serpent.direction != (TAILLE_CASE, 0):
                serpent.nouvelle_direction = (-TAILLE_CASE, 0)
            elif event.key == pygame.K_RIGHT and serpent.direction != (-TAILLE_CASE, 0):
                serpent.nouvelle_direction = (TAILLE_CASE, 0)

    # Mouvement du serpent
    serpent.bouger()

    # Vérifier si le serpent mange la nourriture
    if serpent.corps[0] == nourriture:
        serpent.grandir()
        nourriture = nouvelle_nourriture(serpent)

    # Vérifier les collisions
    if serpent.collision():
        en_cours = False

    # Dessiner
    # Afficher l'image de fond
    FENETRE.blit(background, (0, 0))

    # Dessiner le cadrillage
    for x in range(0, LARGEUR, TAILLE_CASE):
        pygame.draw.line(FENETRE, GRIS, (x, 0), (x, HAUTEUR))  # Lignes verticales
    for y in range(0, HAUTEUR, TAILLE_CASE):
        pygame.draw.line(FENETRE, GRIS, (0, y), (LARGEUR, y))  # Lignes horizontales

    # Dessiner le serpent et la nourriture par-dessus
    for segment in serpent.corps:
        pygame.draw.rect(FENETRE, VERT, (segment[0], segment[1], TAILLE_CASE, TAILLE_CASE))
    pygame.draw.rect(FENETRE, ROUGE, (nourriture[0], nourriture[1], TAILLE_CASE, TAILLE_CASE))

    # Mettre à jour l’affichage
    pygame.display.flip()
    horloge.tick(vitesse)

# Fermer Pygame
pygame.quit()
print(f"Score final : {serpent.taille - 1}")