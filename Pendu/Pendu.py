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

def choisir_mot():
    with open("mots.txt", "r") as fichier_mots:
        mots = fichier_mots.read().splitlines()
    return random.choice(mots).upper()

def afficher_mot_cache(mot, lettres_trouvees):
    mot_cache = ""
    for lettre in mot:
        if lettre in lettres_trouvees:
            mot_cache += lettre
        else:
            mot_cache += "_"
    return mot_cache

def dessiner_pendu(erreurs):
    if erreurs >= 1:
        pygame.draw.rect(fenetre, BLANC, (100, 350, 300, 2))
    if erreurs >= 2:
        pygame.draw.rect(fenetre, BLANC, (175, 50, 2, 300))
    if erreurs >= 3:
        pygame.draw.rect(fenetre, BLANC, (175, 50, 200, 2))
    if erreurs >= 4:
        pygame.draw.line(fenetre, BLANC, (175, 100), (200, 50), 2)
    if erreurs >= 5:
        pygame.draw.rect(fenetre, BLANC, (375, 50, 2, 50))
    if erreurs >= 6:
        pygame.draw.ellipse(fenetre, BLANC, (350, 100, 50, 50), 1)
    if erreurs >= 7:
        pygame.draw.rect(fenetre, BLANC, (375, 150, 1, 100))
    if erreurs >= 8:
        pygame.draw.line(fenetre, BLANC, (375, 175), (340, 150), 1)
    if erreurs >= 9:
        pygame.draw.line(fenetre, BLANC, (375, 175), (410, 150), 1)
    if erreurs >= 10:
        pygame.draw.line(fenetre, BLANC, (375, 250), (340, 275), 1)
    if erreurs >= 11:
        pygame.draw.line(fenetre, BLANC, (375, 250), (410, 275), 1)

def afficher_message_fin(partie_gagnee):
    if partie_gagnee:
        message = "Félicitations ! Vous avez deviné le mot : " + "".join(mot_a_deviner)
    else:
        message = "Dommage ! Vous avez atteint le nombre maximum d'erreurs. Le mot était : " + "".join(mot_a_deviner)

    texte_message = police.render(message, True, BLANC)
    fenetre.blit(texte_message, (largeur // 2 - texte_message.get_width() // 2, hauteur // 2 - texte_message.get_height() // 2))
    pygame.display.flip()

    pygame.time.delay(3000)  # Attendre 3 secondes
    afficher_menu()

def nouvelle_partie():
    global mot_a_deviner, lettres_jouees, erreurs, mot_cache
    mot_a_deviner = choisir_mot()
    lettres_jouees = set()
    erreurs = 0
    mot_cache = ['_'] * len(mot_a_deviner)

def afficher_menu():
    texte_titre = police.render("Jeu du Pendu", True, BLANC)
    fenetre.blit(texte_titre, (largeur // 2 - texte_titre.get_width() // 2, 50))

    texte_nouvelle_partie = police.render("Appuyez sur une touche pour commencer", True, BLANC)
    fenetre.blit(texte_nouvelle_partie, (largeur // 2 - texte_nouvelle_partie.get_width() // 2, hauteur // 2 - texte_nouvelle_partie.get_height() // 2))

    pygame.display.flip()

    attente_touche()

def attente_touche():
    attente = True
    while attente:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evenement.type == pygame.KEYDOWN:
                attente = False

# Initialisation de Pygame
largeur, hauteur = 1100, 800
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu du Pendu")

# Boucle principale du jeu
while True:
    afficher_menu()

    nouvelle_partie()

    # Boucle principale du jeu
    while True:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evenement.type == pygame.KEYDOWN:
                if evenement.key >= pygame.K_a and evenement.key <= pygame.K_z:
                    lettre = chr(evenement.key - pygame.K_a + ord('A'))
                    if lettre not in lettres_jouees:
                        lettres_jouees.add(lettre)
                        if lettre in mot_a_deviner:
                            for j in range(len(mot_a_deviner)):
                                if mot_a_deviner[j] == lettre:
                                    mot_cache[j] = lettre
                        else:
                            erreurs += 1

        # Affichage du mot caché
        texte_mot = police.render(" ".join(mot_cache), True, BLANC)
        fenetre.fill(NOIR)
        fenetre.blit(texte_mot, (largeur // 2 - texte_mot.get_width() // 2, 50))

        # Dessiner le pendu
        dessiner_pendu(erreurs)

        # Affichage des lettres déjà jouées
        texte_lettres = police.render("Lettres jouées: " + " ".join(sorted(lettres_jouees)), True, BLANC)
        fenetre.blit(texte_lettres, (20, 500))

        pygame.display.flip()

        # Vérification si le joueur a gagné
        if '_' not in mot_cache:
            afficher_message_fin(True)

        # Vérification si le joueur a perdu
        if erreurs >= 11:
            afficher_message_fin(False)