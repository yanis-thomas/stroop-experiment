import V1, V2


versions= {"1":("Lignes de commandes", V1.lancement_V1), "2":("Pygame", V2.lancement_V2)}

if __name__ == "__main__":
    liste_ver= "\n".join((f"- {cle} | {val[0]}" for cle,val in versions.items()))
    print(f"\nExperience de Stroop\nChoisir une version : \n{liste_ver}")
    saisie= input("Numero de la version : ")

    if saisie in versions:
        fonction_a_lancer= versions[saisie][1]
        print(f'''
------------------------------
"{versions[saisie][0]}" lancee
------------------------------
''')
        fonction_a_lancer()

    else: print(f'"{saisie}" n\'est pas une version valide')