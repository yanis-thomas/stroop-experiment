import time
import random
import pathlib
import csv

liste_couleurs= {"BLEU":"#00A1FF", "ROUGE":"#FF0000", "VERT":"#1DD695", "JAUNE":"#EEF23D"}
noms_couleurs = list(liste_couleurs.keys())



class Test:
    """
    Represente un Essai ainsi que toutes les proprietes qui lui sont associes (stimulus, chronometre et saisie du participant)
    """
    def __init__(self, numero):
        self.numero:int= numero
        self.reussi:bool= False
        self.congruence:bool= False
        #Chrono
        self.debut:float | None = None
        self.fin:float | None = None 
        self.duree:float | None = None
        #
        self.texte:str= ""
        self.encre:str= ""
        self.saisie:str= ""
   
    def preparer(self, test_prec: Test | None):
        """Generation d'un stimulus aleatoire, en evitant de repeter le meme mot ou la meme encre que l'essai precedent."""
        self.congruence = random.choice([True, False])
        valide = False
        while not valide:
            self.texte = random.choice(noms_couleurs)
            if not self.congruence:
                self.encre = random.choice(noms_couleurs)
                # Si on souhaite que la couleur du texte et la couleur de l'encre soient toujours différentes
                while self.texte == self.encre:
                    self.encre = random.choice(noms_couleurs)
            else:
                self.encre = self.texte
            if test_prec is None or (self.texte != test_prec.texte or self.encre != test_prec.encre):
                valide = True

    def demarrer(self):
        """Demarrer le chronometre du test"""
        self.debut= time.perf_counter()

    def finir(self, saisie):
        """Finir le test en stoppant le chronometre, puis determiner si le test a reussi ou non (saisi == encre)"""
        self.fin= time.perf_counter()
        self.duree= self.fin - self.debut
        self.saisie= saisie
        self.reussi= self.saisie == self.encre 

    def vers_dico(self) -> dict:
        """Convertir le resultat du test en un dictionnaire de donnee manipulable"""
        return {
            "numero":self.numero, 
            "reussi":self.reussi,
            "congruence":self.congruence,
            "duree":self.duree, 
            "texte":self.texte, 
            "encre":self.encre, 
            "saisie":self.saisie,
        }



class Experience:
    """
    Gere le deroulement complet d'une session experimentale, les statistiques et la sauvegarde CSV
    """
    def __init__(self):
        # Gestion des tests
        self.sauvegarde_tests: list[Test]= []
        self.test_actuel: Test | None = None

        # Calculables de l'experience
        self.taux_reussite:float | None = None 
        self.moy_react_congru:float | None = None
        self.moy_react_incongru:float | None = None
        self.effet_stroop:float | None = None

        # En plus
        self.num_experience:int | None = None


    def nouveau_test(self):
        """Creation et preparation d'un nouveau test"""
        num_test= len(self.sauvegarde_tests)+1
        prochain= Test(num_test)
        prochain.preparer(self.test_actuel)
        prochain.demarrer()
        self.test_actuel= prochain

    def test_fini(self, saisie:str):
        """Arret puis enregistrement du test dans une liste de sauvegarde """
        self.test_actuel.finir(saisie)
        self.sauvegarde_tests.append(self.test_actuel)

    def calculer_stats(self):
        """Calculer les statistiques globales de l'experience"""
        nb_reussite= sum(1 for test in self.sauvegarde_tests if test.reussi)
        self.taux_reussite= ((nb_reussite/len(self.sauvegarde_tests))*100 if len(self.sauvegarde_tests)>0 else None)

        duree_congru= [test.duree for test in self.sauvegarde_tests if test.reussi and test.congruence]
        t_react_congru, nb_congru= sum(duree_congru), len(duree_congru)
        self.moy_react_congru= (t_react_congru/nb_congru if nb_congru>0 else None)

        duree_incongru= [test.duree for test in self.sauvegarde_tests if test.reussi and not test.congruence]
        t_react_incongru, nb_incongru= sum(duree_incongru), len(duree_incongru)
        self.moy_react_incongru= (t_react_incongru/nb_incongru if nb_incongru>0 else None)

        self.effet_stroop= (self.moy_react_incongru - self.moy_react_congru if self.moy_react_congru is not None and self.moy_react_incongru is not None else None)


    def vers_dico(self, num_experience):
        """Convertir le resultat de l'experience en un dictionnaire de donnee manipulable"""
        return {
            "num_experience": num_experience,
            "nb_tests": len(self.sauvegarde_tests),
            "taux_reussite": self.taux_reussite,
            "temps_moyen_react_congru": self.moy_react_congru,
            "temps_moyen_react_incongru": self.moy_react_incongru,
            "effet_stroop": self.effet_stroop,
        }


    def exporter_csv(self):
        """Exporte les essais bruts dans 'experience_X_essais.csv' et ajoute le resume dans 'bilan_experiences.csv'."""
        
        if not self.sauvegarde_tests:
            return None

        self.calculer_stats()

        # Verification que le dossier "experiences" existe bien
        dossier_racine = pathlib.Path(__file__).resolve().parent
        dossier_exp = dossier_racine / "experiences"
        dossier_exp.mkdir(parents=True, exist_ok=True)


        ### 1 ### 
        # experience_{nb_experience}_essais.csv

        # Creation du fichier CSV de sauvegarde de l'experience
        # On cherche le numero de l'experience
        nb_experience= 1
        fichier_exp= dossier_exp/f"experience_{nb_experience}_essais.csv"
        while fichier_exp.exists():
            nb_experience+=1
            fichier_exp= dossier_exp/f"experience_{nb_experience}_essais.csv"
        # On recupere les cles du dictionnaire afin de pouvoir afficher les titres des colonnes en premier
        colonnes_exp= list(self.sauvegarde_tests[0].vers_dico().keys())
        # On en profite pour determiner le numero de l'experience
        self.num_experience= nb_experience


        ### 2 ### bilan_experiences.csv

        # Mise a jour du fichier CSV de bilan
        fichier_bilan= dossier_exp/f"bilan_experiences.csv"
        colonnes_bilan= list(self.vers_dico(nb_experience).keys())
        bilan_existe= fichier_bilan.exists()

        try:
            # mode="a" evite d'ecraser tt le fichier a chaque fois, et va ecrire a la suite
            with open(fichier_bilan, mode="a", newline="", encoding="utf-8") as fichier:
                writer= csv.DictWriter(fichier, fieldnames=colonnes_bilan, delimiter=";")
                if not bilan_existe:
                    writer.writeheader()
                writer.writerow(self.vers_dico(nb_experience))
            # Le fichier est automatiquement cree comme on ouvre en mode ecriture et qu'il n'existe pas encore
            with open(fichier_exp, mode="w", newline="", encoding="utf-8") as fichier:
                writer= csv.DictWriter(fichier, fieldnames=colonnes_exp, delimiter=";")
                writer.writeheader()
                for test in self.sauvegarde_tests:
                    writer.writerow(test.vers_dico())
        
        except PermissionError:
            print("\nERREUR : Impossible d'exporter le fichier CSV : fermez le fichier 'bilan_experiences.csv' ouvert.\n")
            return None

        return fichier_exp, fichier_bilan
        