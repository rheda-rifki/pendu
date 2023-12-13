import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

# Définition de la police
police = pygame.font.Font(None, 36)

# Chargement des mots depuis le fichier
with open("mots.txt", "r") as fichier_mots:
    mots = fichier_mots.read().splitlines()

# Choix aléatoire d'un mot
mot_a_deviner = list(random.choice(mots).upper())
mot_cache = ['_'] * len(mot_a_deviner)

# Initialisation de Pygame
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu du Pendu")

# Chargement des images du pendu
images_pendu = [pygame.image.load(f"pendu{i}.png") for i in range(7)]
image_pendu = images_pendu[0]

# Liste des lettres déjà jouées
lettres_jouees = set()

# Nombre d'erreurs autorisées
max_erreurs = 6
erreurs = 0

# Boucle principale du jeu
while True:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Affichage du mot caché
    texte_mot = police.render(" ".join(mot_cache), True, BLANC)
    fenetre.fill(NOIR)
    fenetre.blit(texte_mot, (largeur // 2 - texte_mot.get_width() // 2, 50))

    # Affichage de l'image du pendu
    fenetre.blit(image_pendu, (largeur // 2 - image_pendu.get_width() // 2, 150))

    # Affichage des lettres déjà jouées
    texte_lettres = police.render("Lettres jouées: " + " ".join(sorted(lettres_jouees)), True, BLANC)
    fenetre.blit(texte_lettres, (20, 500))

    pygame.display.flip()

    # Vérification si le joueur a gagné
    if '_' not in mot_cache:
        print("Félicitations ! Vous avez deviné le mot :", "".join(mot_a_deviner))
        pygame.quit()
        sys.exit()

    # Vérification si le joueur a perdu
    if erreurs >= max_erreurs:
        print("Dommage ! Vous avez atteint le nombre maximum d'erreurs. Le mot était :", "".join(mot_a_deviner))
        pygame.quit()
        sys.exit()

    # Attendre une touche du clavier
    touche = pygame.key.get_pressed()
    for i in range(26):
        if touche[i]:
            lettre = chr(i + ord('A'))
            if lettre not in lettres_jouees:
                lettres_jouees.add(lettre)
                if lettre in mot_a_deviner:
                    for j in range(len(mot_a_deviner)):
                        if mot_a_deviner[j] == lettre:
                            mot_cache[j] = lettre
                else:
                    erreurs += 1
                    image_pendu = images_pendu[erreurs]

# N'oubliez pas d'adapter le code en fonction de vos besoins spécifiques et de personnaliser le visuel du jeu. Vous pouvez ajouter des fonctionnalités supplémentaires pour améliorer l'expérience utilisateur.
