from rich import print
import pygame
import time
import random


def lancement_V2():

    LARGEUR, HAUTEUR= 800, 600
    FPS= 60  # Images par seconde

    # 1. Initialisation
    # Initialiser tt les modules de pygame pour faire fonctionner le programme
    pygame.init()
    # Definir la fenetre, sa taille (LARGEUR, HAUTEUR)
    screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
    # Definir le titre de la fenetre
    pygame.display.set_caption("Experience de Stroop - V2")
    # Definir une horloge/des ticks/des FPS, afin d'eviter de surchauffer le proco pour rien, 60 c'est suffisant
    # En gros, le nbr de fois par seconde que le prog se met a jour/la boucle while s'execute
    clock = pygame.time.Clock()

    # Polices d'ecritures
    police_classique= pygame.font.SysFont("Arial", 22, bold=False)
    police_titre= pygame.font.SysFont("Arial", 40, bold=True)

    # Indique que le prog est en cours et permet d'indiquer a la fenêtre (la boucle while) que tant 
    # qu'on est en True, on continue
    running= True



    # Variables de gestion pour l'affichage Pygame
    statut= "DEBUT"
    affichage=""
    fini= False


    # Couleurs classiques (utilisees pour le test)
    liste_couleurs= {"BLEU":"#00A1FF", "ROUGE":"#FF0000", "VERT":"#1DD695", "JAUNE":"#EEF23D"}

    # Nuances de gris (pour le background et les textes classiques)
    NOIR = (20, 20, 20) 
    GRIS = (120, 120, 120)
    BLANC= (255, 255, 255)


    # Variables de tests
    sauvegardes_tests= []
    num_test= 0

    texte, encre= "", ()
    congruence= False
    saisie= None
    debut, fin = None, None
    duree = 0

    taux_reussite= 0
    moy_react_congru= None
    moy_react_incongru= None
    effet_stroop= None
    
    txt_congru= "N/A"
    txt_incongru= "N/A"
    txt_stroop= "N/A"


    # Fonctions et Procedures utilitaires
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


    def nouveau_test():
        texte= random.choice(list(liste_couleurs.keys()))
        congruence= random.choice([True, False])
        if not congruence : 
            encre_nom= random.choice(list(liste_couleurs.keys()))
            # Si on souhaite que la couleur du texte et la couleur de l'encre soient toujours différentes
            while texte == encre_nom:
                encre_nom= random.choice(list(liste_couleurs.keys()))
        else:
            encre_nom= texte

        encre_hexa= liste_couleurs[encre_nom]
        return texte, (encre_nom, encre_hexa), congruence


    # 2. La boucle principale, le screen
    while running:

        # A. Gestion des evenements (touches, claviers, souris, joysticks etc.)  
        for event in pygame.event.get(): 

            if event.type == pygame.QUIT:
                running= False


            if event.type == pygame.KEYDOWN:

                if statut in ("DEBUT","FIN") and event.key == pygame.K_ESCAPE:
                    running= False


                elif statut == "EN_COURS":
                    if event.key == pygame.K_LEFT:
                        saisie= "BLEU"
                    elif event.key == pygame.K_RIGHT:
                        saisie= "ROUGE"
                    elif event.key == pygame.K_UP:
                        saisie= "VERT"
                    elif event.key == pygame.K_DOWN:
                        saisie= "JAUNE"
                    
                    elif event.key == pygame.K_ESCAPE:
                        statut= "FIN"


                    if saisie is not None:
                        fin= time.perf_counter()
                        duree= fin-debut

                        if saisie== encre[0]: 
                            sauvegardes_tests.append({"numero":num_test+1, "reussi":True})
                        else:
                            sauvegardes_tests.append({"numero":num_test+1, "reussi":False})
                            
                        sauvegardes_tests[num_test].update({
                            "congruence":congruence,
                            "duree":duree, 
                            "texte":texte, 
                            "encre":encre[0], 
                            "saisie":saisie
                        })

                        saisie= None
                        num_test +=1
                        texte, encre, congruence= nouveau_test()
                        debut= time.perf_counter()
                        
                        

                elif statut == "DEBUT" and event.key == pygame.K_SPACE:
                    statut= "EN_COURS"
                    texte, encre, congruence= nouveau_test()
                    debut= time.perf_counter()




        # B. Calculs et affichage dans le terminal   
        if statut == "FIN" and not fini:
            if len(sauvegardes_tests) > 0:
                # Affichage des résulats du test
                print(f"\n\nFin des tests | {num_test} tests effectués\n")
                for resultat in sauvegardes_tests:
                    print(f"""
{resultat["numero"]} - 
    {"[#00FFA6]Succes[/#00FFA6]" if resultat["reussi"] else "[#FF0000]Echec[/#FF0000]"}
    Congruence : {resultat["congruence"]}
    Temps saisie moyen : {resultat["duree"]:.6f}s
    Texte affiché + Couleur : [{liste_couleurs[resultat["encre"]]}]{resultat["texte"]}[/{liste_couleurs[resultat["encre"]]}] - ({resultat["encre"]})
    Couleur saisi : {resultat["saisie"]}
    """)
        
        
                # Calculs des variables statistiques du test
                nb_reussite= sum(1 for essai in sauvegardes_tests if essai["reussi"])
                taux_reussite= (nb_reussite/len(sauvegardes_tests))*100
                print(f"\nTaux de reussite : {taux_reussite:.2f}%")
        
                duree_congru= [essai["duree"] for essai in sauvegardes_tests if essai["reussi"] and essai["congruence"]]
                t_react_congru, nb_congru= sum(duree_congru), len(duree_congru)
                if nb_congru>0:
                    moy_react_congru= t_react_congru/nb_congru
                txt_congru = (f"{moy_react_congru:.3f}s" if moy_react_congru is not None else "N/A")
                print(f"Temps react moyen congru : {txt_congru}")
        
                duree_incongru= [essai["duree"] for essai in sauvegardes_tests if essai["reussi"] and not essai["congruence"]]
                t_react_incongru, nb_incongru= sum(duree_incongru), len(duree_incongru)
                if nb_incongru>0: 
                    moy_react_incongru= t_react_incongru/nb_incongru
                txt_incongru = (f"{moy_react_incongru:.3f}s" if moy_react_incongru is not None else "N/A")
                print(f"Temps react moyen incongru : {txt_incongru}")

                if nb_congru > 0 and nb_incongru > 0:
                    effet_stroop= (moy_react_incongru - moy_react_congru)
                txt_stroop = (f"{effet_stroop:.3f}s" if effet_stroop is not None else "N/A")
                print(f"Effet Stroop : {(txt_stroop)}")
        
        
            else: print("Aucun test n'a ete realise")
            fini= True




        # C. Gestion de l'affichage de l'ecran
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
            afficher_texte_centre(texte, encre[1], police_titre)
            afficher_texte_coin_gauche(f"Test n°{num_test+1}", BLANC, police_classique, decalage_x=20, decalage_y=20)
            afficher_texte_coin_droit("Bleu - Flèche gauche", GRIS, police_classique, decalage_x=20, decalage_y=10)
            afficher_texte_coin_droit("Rouge - Flèche droite", GRIS, police_classique, decalage_x=20, decalage_y=35)
            afficher_texte_coin_droit("Vert - Flèche haut", GRIS, police_classique, decalage_x=20, decalage_y=60)
            afficher_texte_coin_droit("Jaune - Flèche bas", GRIS, police_classique, decalage_x=20, decalage_y=85)

            
        if statut == "FIN":
            afficher_texte_coin_gauche(f"{num_test} test(s) effectue(s)", BLANC, police_classique, decalage_x=20, decalage_y=20)
            afficher_texte_centre("Fin de l'experience",BLANC, police_titre, decalage_y=-120)
            afficher_texte_centre(f"Taux de reussite : {taux_reussite:.2f}%", BLANC, police_classique, decalage_y=-60)
            afficher_texte_centre(f"Temps react moyen congru : {txt_congru}", BLANC, police_classique, decalage_y=-20)
            afficher_texte_centre(f"Temps react moyen incongru : {txt_incongru}", BLANC, police_classique, decalage_y=20)
            afficher_texte_centre(f"Effet Stroop : {txt_stroop}", BLANC, police_classique, decalage_y=60)
            afficher_texte_centre("Pressez ECHAP pour quitter",BLANC, police_classique, decalage_y=120)   


        clock.tick(FPS)
        pygame.display.flip()

    # Quitter pygame (cette commande c'est l'inverse de pygame.init())
    pygame.quit()