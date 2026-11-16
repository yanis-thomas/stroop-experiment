from rich import print
import time, random

liste_couleurs= {"ROUGE":"#FF0000", "BLEU":"#00A1FF", "VERT":"#00FFA6", "JAUNE":"#EEF23D", "ORANGE":"#FAC819", 
                 "VIOLET":"#BF08FF", "ROSE":"#FFA1ED"}


# Variables de "gestion" du test
# i correspond au numero du test
i=0
ARRET= "STOP"
sauvegardes_tests= []

# Variables de tests
choix_texte, choix_encre_nom, choix_encre_hexa= "", "", ""
congruence= False
saisie= ""
debut, fin = None, None
duree = 0



# BOUCLE DU PROGRAMME PRINCIPAL
while saisie != ARRET:

    print(f"Test ",i+1)

    #Selection du mot et de l'encre, determination de la nature du tirage (congruent ou non)
    congruence= random.choice([True, False])

    choix_texte= random.choice(list(liste_couleurs.keys()))
    
    if not congruence : 
        choix_encre_nom= random.choice(list(liste_couleurs.keys()))
        # Si on souhaite que la couleur du texte et la couleur de l'encre soient toujours différentes
        while choix_texte==choix_encre_nom:
            choix_encre_nom= random.choice(list(liste_couleurs.keys()))
    
    else:
        choix_encre_nom= choix_texte
    
    choix_encre_hexa= liste_couleurs[choix_encre_nom]



    # Affichage et mesure du temps de réaction
    print(f"[{choix_encre_hexa}]{choix_texte}[/{choix_encre_hexa}]")
    debut = time.perf_counter()

    saisie= input().strip().upper()

    fin= time.perf_counter()
    duree = fin-debut



    # Evaluation de la reponse saisie
    if saisie != ARRET:
        if saisie==choix_encre_nom: 
            sauvegardes_tests.append({"numero":i+1, "reussi":True})
        else:
            sauvegardes_tests.append({"numero":i+1, "reussi":False})
            
        sauvegardes_tests[i].update({
            "congruence": congruence,
            "duree": duree, 
            "texte":choix_texte, 
            "encre":choix_encre_nom, 
            "saisie":saisie
        })
       
        i+=1
        print("\n")


if len(sauvegardes_tests) > 0:
    # Affichage des résulats du test
    print(f"\n\nFin des tests | {i} tests effectués\n")
    for resultat in sauvegardes_tests:
        print(f"""{resultat["numero"]} - 
    {"[#00FFA6]Succes[/#00FFA6]" if resultat["reussi"] else "[#FF0000]Echec[/#FF0000]"}
    Congruence : {resultat["congruence"]} ;
    Temps saisie : {resultat["duree"]:.6f}" ; 
    Texte affiché + Couleur : [{liste_couleurs[resultat["encre"]]}]{resultat["texte"]}[/{liste_couleurs[resultat["encre"]]}] - \
({resultat["encre"]}); 
    Texte saisi : {resultat["saisie"]}
    """)


    # Calcul des variables statistiques du test
    nb_reussite= sum(1 for essai in sauvegardes_tests if essai["reussi"])
    taux_reussite= (nb_reussite/len(sauvegardes_tests))*100
    print(f"\nTaux de reussite : {taux_reussite:.2f}%")

    duree_congru= [essai["duree"] for essai in sauvegardes_tests if essai["reussi"] and essai["congruence"]]
    t_react_congru, nb_congru= sum(duree_congru), len(duree_congru)
    if nb_congru>0:
        moy_react_congru= t_react_congru/nb_congru
        print(f"Temps react moyen congru : {moy_react_congru:.3f}s")

    duree_incongru= [essai["duree"] for essai in sauvegardes_tests if essai["reussi"] and not essai["congruence"]]
    t_react_incongru, nb_incongru= sum(duree_incongru), len(duree_incongru)
    if nb_incongru>0:
        moy_react_incongru= t_react_incongru/nb_incongru
        print(f"Temps react moyen incongru : {moy_react_incongru:.3f}s")

    if nb_congru > 0 and nb_incongru > 0:
        print(f"Effet Stroop : {(moy_react_incongru - moy_react_congru):.3f}s")


else: print("Aucun test n'a ete realise")
