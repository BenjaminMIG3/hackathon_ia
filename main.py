import pygame
import random
import time

pygame.init()
pygame.mixer.init()  # Initialiser le module de son de Pygame

# Constantes
LARGEUR_JEU, HAUTEUR_JEU = 800, 600
ESPACE_HUD = 40
LARGEUR, HAUTEUR = LARGEUR_JEU, HAUTEUR_JEU + ESPACE_HUD
TAILLE_CASE = 40
FENETRE = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Snake")

# Couleurs
BLANC = (255, 255, 255)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)
NOIR = (0, 0, 0)
GRIS = (100, 100, 100)

# Police pour le texte
font = pygame.font.Font(None, 74)  # Police pour les grands textes
font_small = pygame.font.Font(None, 36)  # Police pour les petits textes
font_credits = pygame.font.Font(None, 30)  # Police pour les crédits

# Chargement des images
background = pygame.image.load("assets/map/background.jpg")
background = pygame.transform.scale(background, (LARGEUR_JEU, HAUTEUR_JEU))

# Chargement de l'image de la tête du serpent
def charger_image(path):
    try:
        return pygame.transform.scale(pygame.image.load(path), (TAILLE_CASE, TAILLE_CASE))
    except pygame.error as e:
        print(f"Erreur lors du chargement de l'image {path}: {e}")
        return None

head_image = charger_image("assets/serpent/head.png")
if head_image is None:
    print("Erreur : l'image de la tête du serpent n'a pas pu être chargée. Utilisation d'un carré vert par défaut.")

# Chargement du son
try:
    eat_sound = pygame.mixer.Sound("assets/sounds/eats.mp3")
except pygame.error as e:
    print(f"Erreur lors du chargement du son: {e}")
    eat_sound = None

# Charger les images des nourritures et vérifier qu'elles sont valides
nourriture_images = {
    "eau": charger_image("assets/nourritures/eau.png"),
    "eclair": charger_image("assets/nourritures/eclair.png"),
    "deepseek": charger_image("assets/nourritures/deepseek.png"),
    "bard": charger_image("assets/nourritures/bard.png"),
    "chatgpt": charger_image("assets/nourritures/chatgpt.png"),
    "claude": charger_image("assets/nourritures/claude.png"),
    "copilot": charger_image("assets/nourritures/copilot.png"),
    "ia_1": charger_image("assets/nourritures/ia_1.png"),
    "ia_2": charger_image("assets/nourritures/ia_2.png")
}

# Vérifier les images chargées
for key, img in nourriture_images.items():
    if img is None:
        print(f"Image pour {key} non chargée correctement !")

icone_eau = pygame.transform.scale(nourriture_images["eau"] if nourriture_images["eau"] else pygame.Surface((20, 20)), (20, 20))
icone_eclair = pygame.transform.scale(nourriture_images["eclair"] if nourriture_images["eclair"] else pygame.Surface((20, 20)), (20, 20))

# Fonction pour dessiner un bouton
def dessiner_bouton(texte, x, y, largeur, hauteur, couleur_fond, couleur_texte):
    bouton_rect = pygame.Rect(x, y, largeur, hauteur)
    pygame.draw.rect(FENETRE, couleur_fond, bouton_rect)
    texte_surface = font_small.render(texte, True, couleur_texte)
    texte_rect = texte_surface.get_rect(center=bouton_rect.center)
    FENETRE.blit(texte_surface, texte_rect)
    return bouton_rect

# Écran d'accueil
def ecran_accueil():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_bouton.collidepoint(event.pos):
                    return  # Démarrer le jeu

        FENETRE.fill(NOIR)
        # Titre
        titre = font.render("Snake Game", True, BLANC)
        titre_rect = titre.get_rect(center=(LARGEUR // 2, HAUTEUR // 3))
        FENETRE.blit(titre, titre_rect)

        # Bouton Play
        play_bouton = dessiner_bouton("Play", LARGEUR // 2 - 100, HAUTEUR // 2, 200, 50, VERT, NOIR)

        pygame.display.flip()

# Écran de fin de jeu avec crédits défilants
def ecran_fin():
    # Liste des lignes de texte pour les crédits
    credits_text = [
        "Game Over - You Win!",
        "",
        "=== Environmental Impact of AI ===",
        "Did you know?",
        "Training large AI models can consume massive amounts of energy.",
        "For example, training a single AI model like GPT-3 can emit",
        "over 626,000 pounds of CO2, equivalent to the emissions of",
        "5 cars over their lifetime!",
        "",
        "AI data centers also require significant water for cooling.",
        "In 2022, Google's data centers used 4.3 billion gallons of water.",
        "",
        "What can we do?",
        "- Use energy-efficient hardware for AI training.",
        "- Support renewable energy for data centers.",
        "- Optimize AI models to reduce computational needs.",
        "",
        "Thank you for playing!",
        "Created by THE TOUTOUZ",
        "April 2025"
    ]

    # Préparer les surfaces de texte pour les crédits
    credits_surfaces = [font_credits.render(line, True, BLANC) for line in credits_text]
    credits_heights = [surface.get_height() for surface in credits_surfaces]

    # Position initiale (en bas de l'écran)
    y_position = HAUTEUR
    vitesse_defilement = 1  # Pixels par frame

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_bouton.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        FENETRE.fill(NOIR)

        # Déplacer les crédits vers le haut
        y_position -= vitesse_defilement

        # Afficher chaque ligne de texte
        current_y = y_position
        for i, (surface, height) in enumerate(zip(credits_surfaces, credits_heights)):
            text_rect = surface.get_rect(center=(LARGEUR // 2, current_y))
            FENETRE.blit(surface, text_rect)
            current_y += height + 10  # Espacement entre les lignes

        # Si tous les crédits ont défilé hors de l'écran, réinitialiser la position
        if current_y < 0:
            y_position = HAUTEUR

        # Bouton Quit (fixe en bas de l'écran)
        quit_bouton = dessiner_bouton("Quit", LARGEUR // 2 - 100, HAUTEUR - 70, 200, 50, ROUGE, NOIR)

        pygame.display.flip()
        pygame.time.Clock().tick(60)  # 60 FPS pour un défilement fluide

# Classe pour le serpent
class Serpent:
    def __init__(self):
        self.taille = 1
        self.corps = [((LARGEUR_JEU // 2) - (LARGEUR_JEU // 2) % TAILLE_CASE,
                       (HAUTEUR_JEU // 2) - (HAUTEUR_JEU // 2) % TAILLE_CASE + ESPACE_HUD)]
        self.direction = (TAILLE_CASE, 0)
        self.nouvelle_direction = self.direction
        self.eau = 0
        self.electricite = 0
        self.max_ressource = 100
        self.segment_images = []

    def bouger(self):
        self.direction = self.nouvelle_direction
        tete_x, tete_y = self.corps[0]
        dx, dy = self.direction
        nouvelle_tete = ((tete_x + dx) % LARGEUR_JEU, ESPACE_HUD + ((tete_y - ESPACE_HUD + dy) % HAUTEUR_JEU))
        self.corps.insert(0, nouvelle_tete)
        if len(self.corps) > self.taille:
            self.corps.pop()
            if len(self.segment_images) > self.taille - 1:
                self.segment_images.pop()

    def grandir(self, type_nourriture, image_nourriture):
        self.taille += 1
        if image_nourriture:
            self.segment_images.append(image_nourriture)
        else:
            print(f"Image pour {type_nourriture} est None lors de grandir !")

        if eat_sound:
            eat_sound.play()
            pygame.time.wait(50)
            eat_sound.play()

        if type_nourriture in ["eau", "deepseek", "chatgpt"]:
            self.eau = min(self.eau + 20, self.max_ressource)
        elif type_nourriture in ["eclair", "bard", "claude", "copilot"]:
            self.electricite = min(self.electricite + 20, self.max_ressource)

    def collision(self):
        return self.corps[0] in self.corps[1:]

    def get_head_rotation(self):
        # Déterminer l'angle de rotation en fonction de la direction
        dx, dy = self.direction
        if dx == TAILLE_CASE:  # Droite
            return 0
        elif dx == -TAILLE_CASE:  # Gauche
            return 180
        elif dy == -TAILLE_CASE:  # Haut
            return 90
        elif dy == TAILLE_CASE:  # Bas
            return 270
        return 0  # Par défaut

# Classe pour la nourriture
class Nourriture:
    def __init__(self, position, type, image):
        self.position = position
        self.type = type
        self.image = image

# Nouvelle nourriture
def nouvelle_nourriture(serpent):
    while True:
        x = random.randrange(0, LARGEUR_JEU, TAILLE_CASE)
        y = random.randrange(ESPACE_HUD, HAUTEUR, TAILLE_CASE)
        if (x, y) not in serpent.corps:
            type_nourriture = random.choice(["deepseek", "bard", "chatgpt", "claude", "copilot", "ia_1", "ia_2"])
            image = nourriture_images.get(type_nourriture)
            if image is None:
                print(f"Image pour {type_nourriture} est None, on réessaie...")
                continue
            return Nourriture((x, y), type_nourriture, image)

# Afficher l'écran d'accueil
ecran_accueil()

# Initialisation du jeu
serpent = Serpent()
nourritures = [nouvelle_nourriture(serpent)]
SEUIL_NOURRITURE = 0.5
vitesse = 10
horloge = pygame.time.Clock()
en_cours = True

# Boucle principale du jeu
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

    serpent.bouger()

    tete = serpent.corps[0]
    for nourriture in nourritures[:]:
        if tete == nourriture.position:
            serpent.grandir(nourriture.type, nourriture.image)
            nourritures.remove(nourriture)
            nourritures.append(nouvelle_nourriture(serpent))

    nombre_nourritures_cible = serpent.taille // SEUIL_NOURRITURE + 1
    while len(nourritures) < nombre_nourritures_cible:
        nourritures.append(nouvelle_nourriture(serpent))

    # Vérifier si le joueur a mangé 15 nourritures (taille = 16 car on commence à 1)
    if serpent.taille >= 16:
        ecran_fin()
        break

    if serpent.collision():
        en_cours = False

    # Dessin
    FENETRE.fill(NOIR)
    FENETRE.blit(background, (0, ESPACE_HUD))

    # Grille
    for x in range(0, LARGEUR_JEU, TAILLE_CASE):
        pygame.draw.line(FENETRE, GRIS, (x, ESPACE_HUD), (x, HAUTEUR))
    for y in range(ESPACE_HUD, HAUTEUR, TAILLE_CASE):
        pygame.draw.line(FENETRE, GRIS, (0, y), (LARGEUR_JEU, y))

    # Serpent - dessiner les segments avec leurs images
    for i, segment in enumerate(serpent.corps[1:], 0):
        if i < len(serpent.segment_images) and serpent.segment_images[i] is not None:
            FENETRE.blit(serpent.segment_images[i], segment)
        else:
            print(f"Image manquante pour le segment {i}, segment_images: {len(serpent.segment_images)}")

    # Dessiner la tête avec rotation
    if head_image:
        rotated_head = pygame.transform.rotate(head_image, serpent.get_head_rotation())
        # Ajuster la position pour centrer l'image après rotation
        head_rect = rotated_head.get_rect(center=(serpent.corps[0][0] + TAILLE_CASE // 2, serpent.corps[0][1] + TAILLE_CASE // 2))
        FENETRE.blit(rotated_head, head_rect)
    else:
        pygame.draw.rect(FENETRE, VERT, (serpent.corps[0][0], serpent.corps[0][1], TAILLE_CASE, TAILLE_CASE))

    # Nourritures
    for nourriture in nourritures:
        if nourriture.image:
            FENETRE.blit(nourriture.image, nourriture.position)
        else:
            print(f"Nourriture sans image: {nourriture.type}")

    # Barres (au-dessus de l'aire de jeu)
    FENETRE.blit(icone_eau, (10, 10))
    pygame.draw.rect(FENETRE, NOIR, (40, 10, 204, 24), 2)
    pygame.draw.rect(FENETRE, (0, 0, 255), (42, 12, serpent.eau * 2, 20))

    FENETRE.blit(icone_eclair, (LARGEUR - 234, 10))
    pygame.draw.rect(FENETRE, NOIR, (LARGEUR - 204, 10, 204, 24), 2)
    pygame.draw.rect(FENETRE, (255, 255, 0), (LARGEUR - 202, 12, serpent.electricite * 2, 20))

    pygame.display.flip()
    horloge.tick(vitesse)

pygame.quit()
print(f"Score final : {serpent.taille - 1}")
print(f"Niveau d'eau final : {serpent.eau}")
print(f"Niveau d'électricité final : {serpent.electricite}")