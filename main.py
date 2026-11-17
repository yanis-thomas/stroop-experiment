from classes import *
from rich import print
import pygame



# 1. Initialisation

# Definition de constantes pour la taille de la fenetre
LARGEUR, HAUTEUR= 800, 600
# Taux de rafraichissement du programme
FPS= 60  

# Initialiser tt les modules de pygame pour faire fonctionner le programme
pygame.init()
# Definir la fenetre, sa taille (LARGEUR, HAUTEUR)
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
# Definir le titre de la fenetre
pygame.display.set_caption("Experience de Stroop - v1.0.0")
# Definir une horloge/des ticks/des FPS, afin d'eviter de surchauffer le proco pour rien, 60 c'est suffisant
# En gros, le nbr de fois par seconde que le prog se met a jour/la boucle while s'execute
clock = pygame.time.Clock()


# Polices et couleurs classiques pour l'affichage de textes dans Pygame

# Polices d'ecritures
police_classique= pygame.font.SysFont("Arial", 22, bold=False)
police_titre= pygame.font.SysFont("Arial", 40, bold=True)

# Nuances de gris (pour le background et les textes classiques hors test)
NOIR = (20, 20, 20) # Pour l'arriere plan
GRIS = (120, 120, 120)
BLANC= (255, 255, 255)


# Indique que le prog est en cours et permet d'indiquer a la fenêtre (la boucle while) que tant 
# qu'on est en True, on continue. En gros py game continue de tourner
running= True


# Variables d'affichage personalisee pour les stats de l'experience
txt_taux= "N/A"
txt_congru= "N/A"
txt_incongru= "N/A"
txt_stroop= "N/A"


# Variables de l'experience
experience = Experience()
saisie= None
export_csv= False

# Variables de gestion des evenements (pour gerer affichage Pygame et Terminal)
statut= "DEBUT"
fini= False



# Fonctions et Procedures utilitaires
# Procedures pour gerer l'affichage des textes dans Pygame
def afficher_texte_centre(texte, couleur, police, decalage_x=0, decalage_y=0):
    surface_texte = police.render(texte, True, couleur)
    rect_texte = surface_texte.get_rect(center=(LARGEUR//2 + decalage_x, HAUTEUR//2 + decalage_y))
    screen.blit(surface_texte, rect_texte)

def afficher_texte_coin_gauche(texte, couleur, police, decalage_x=0, decalage_y=0):
    surface_texte = police.render(texte, True, couleur)
    rect_texte = surface_texte.get_rect(topleft=(decalage_x, decalage_y))
    screen.blit(surface_texte, rect_texte)

def afficher_texte_coin_droit(texte, couleur, police, decalage_x=20, decalage_y=20):
    surface_texte = police.render(texte, True, couleur)
    rect_texte = surface_texte.get_rect(topright=(LARGEUR - decalage_x, decalage_y))
    screen.blit(surface_texte, rect_texte)




# 2. La boucle principale, le screen
while running:

    # A. Gestion des evenements (touches, claviers, souris, joysticks etc.)  
    for event in pygame.event.get(): 

        # Quitter en cliquant sur la croix rouge en haut a droite
        if event.type == pygame.QUIT:
            running= False

        # Touches du clavier
        if event.type == pygame.KEYDOWN:

            # En fonction de l'etat/du statut de l'experience, on defini le role des touches necessaires

            if statut in ("DEBUT","FIN") and event.key == pygame.K_ESCAPE:
                running= False


            elif statut == "EN_COURS":
                # Saisie des couleurs a l'aide des fleches directionnelles 
                if event.key == pygame.K_LEFT:
                    saisie= "BLEU"
                elif event.key == pygame.K_RIGHT:
                    saisie= "ROUGE"
                elif event.key == pygame.K_UP:
                    saisie= "VERT"
                elif event.key == pygame.K_DOWN:
                    saisie= "JAUNE"

                # Finir le test en pressant ECHAP
                elif event.key == pygame.K_ESCAPE:
                    statut= "FIN"

                # A chaque saisie, on sauvegarde le test actuel puis on passe au suivant
                if saisie is not None:
                    experience.test_fini(saisie)
                    saisie= None
                    experience.nouveau_test()
                    

            elif statut == "DEBUT" and event.key == pygame.K_SPACE:
                # Demarrage des tests
                statut= "EN_COURS"
                experience.nouveau_test()

            elif statut == "FIN" and event.key == pygame.K_SPACE:
                if len(experience.sauvegarde_tests) > 0 and not export_csv:
                    # Permettre la sauvegarde du CSV des tests et l'ajout des stats de l'experience au CSV bilan des experiences a la fin de cette derniere
                    resultat_export= experience.exporter_csv()
                    if resultat_export is not None:
                        export_csv = True
                        print(f'''\nCreation de "experience_{experience.num_experience}_essais.csv"\nMise a jour de "bilan_experiences.csv"\n''')



    # B. Calculs et affichage dans le terminal   
    if statut == "FIN" and not fini:
        # A la fin de l'experience, afficher un bilan de chaque test, calculer les stats de l'experience, et les afficher a la suite dans le terminal
        if len(experience.sauvegarde_tests) > 0:
            # Affichage des résulats du test
            print(f"\n\nFin des tests | {len(experience.sauvegarde_tests)} tests effectués\n")
            for test in experience.sauvegarde_tests:
                print(f"""
{test.numero} - 
    {"[#00FFA6]Succes[/#00FFA6]" if test.reussi else "[#FF0000]Echec[/#FF0000]"}
    Congruence : {test.congruence}
    Temps saisie moyen : {test.duree:.6f}s
    Texte affiché + Couleur : [{liste_couleurs[test.encre]}]{test.texte}[/{liste_couleurs[test.encre]}] - ({test.encre})
    Couleur saisi : {test.saisie}
    """)
    
    
            # Calculs des variables statistiques du test, puis affichage dans le terminal
            experience.calculer_stats()

            txt_taux = f"{experience.taux_reussite:.2f}%" if experience.taux_reussite is not None else "N/A"
            print(f"\nTaux de reussite : {txt_taux}")
            
            txt_congru = (f"{experience.moy_react_congru:.3f}s" if experience.moy_react_congru is not None else "N/A")
            print(f"Temps react moyen congru : {txt_congru}")
            
            txt_incongru = (f"{experience.moy_react_incongru:.3f}s" if experience.moy_react_incongru is not None else "N/A")
            print(f"Temps react moyen incongru : {txt_incongru}")
           
            txt_stroop = (f"{experience.effet_stroop:.3f}s" if experience.effet_stroop is not None else "N/A")
            print(f"Effet Stroop : {(txt_stroop)}\n")
    
        else: print("\nAucun test n'a ete realise\n")
        fini= True



    # C. Gestion de l'affichage de l'ecran Pygame
    test = experience.test_actuel
    screen.fill(NOIR)

    if statut == "DEBUT":
        afficher_texte_centre("Experience de Stroop",BLANC, police_titre, decalage_y=-100)
        afficher_texte_centre("Pressez ESPACE pour démarrer le test",BLANC, police_classique, decalage_y=100)
        afficher_texte_centre("Quitter le test en cours avec ECHAP",BLANC, police_classique, decalage_y=200)

        afficher_texte_coin_droit("Bleu - Flèche gauche", liste_couleurs["BLEU"], police_classique, decalage_x=20, decalage_y=10)
        afficher_texte_coin_droit("Rouge - Flèche droite", liste_couleurs["ROUGE"], police_classique, decalage_x=20, decalage_y=35)
        afficher_texte_coin_droit("Vert - Flèche haut", liste_couleurs["VERT"], police_classique, decalage_x=20, decalage_y=60)
        afficher_texte_coin_droit("Jaune - Flèche bas", liste_couleurs["JAUNE"], police_classique, decalage_x=20, decalage_y=85)


    if statut == "EN_COURS":
        afficher_texte_centre(test.texte, liste_couleurs[test.encre], police_titre)
        afficher_texte_coin_gauche(f"Test n°{test.numero}", BLANC, police_classique, decalage_x=20, decalage_y=20)

        afficher_texte_coin_droit("Bleu - Flèche gauche", GRIS, police_classique, decalage_x=20, decalage_y=10)
        afficher_texte_coin_droit("Rouge - Flèche droite", GRIS, police_classique, decalage_x=20, decalage_y=35)
        afficher_texte_coin_droit("Vert - Flèche haut", GRIS, police_classique, decalage_x=20, decalage_y=60)
        afficher_texte_coin_droit("Jaune - Flèche bas", GRIS, police_classique, decalage_x=20, decalage_y=85)

        
    if statut == "FIN":
        afficher_texte_coin_gauche(f"{len(experience.sauvegarde_tests)} test(s) effectue(s)", BLANC, police_classique, decalage_x=20, decalage_y=20)
        if not export_csv and len(experience.sauvegarde_tests) > 0:
            afficher_texte_coin_droit(f"Pressez ESPACE pour", BLANC, police_classique, decalage_x=20, decalage_y=20)
            afficher_texte_coin_droit(f"exporter le CSV", BLANC, police_classique, decalage_x=76, decalage_y=46)
        elif export_csv:
            afficher_texte_coin_droit(f"CSV exporté", BLANC, police_classique, decalage_x=20, decalage_y=20)
        else: pass
        afficher_texte_centre("Fin de l'experience",BLANC, police_titre, decalage_y=-120)
        afficher_texte_centre(f"Taux de reussite : {txt_taux}", BLANC, police_classique, decalage_y=-60)
        afficher_texte_centre(f"Temps react moyen congru : {txt_congru}", BLANC, police_classique, decalage_y=-20)
        afficher_texte_centre(f"Temps react moyen incongru : {txt_incongru}", BLANC, police_classique, decalage_y=20)
        afficher_texte_centre(f"Effet Stroop : {txt_stroop}", BLANC, police_classique, decalage_y=60)
        afficher_texte_centre("Pressez ECHAP pour quitter",BLANC, police_classique, decalage_y=120)   


    # Limiter les FPS pour eviter de surconsommer des ressources de maniere inutile
    clock.tick(FPS)
    # Mettre a jour l'affichage Pygame
    pygame.display.flip()

# Quitter pygame (cette commande c'est l'inverse de pygame.init())
pygame.quit()
