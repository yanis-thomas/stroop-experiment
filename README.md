# Expérience de Stroop (v1.0.0)

Implémentation en Python et Pygame du **paradigme de Stroop** (Stroop, 1935), conçu pour mesurer l'interférence cognitive entre la lecture automatique d'un mot et l'identification de la couleur de son encre.

## Principe expérimental

À chaque essai, un nom de couleur (🔵`BLEU`, 🔴`ROUGE`, 🟢`VERT`, 🟡`JAUNE`) s'affiche au centre de l'écran :
- **Condition congruente (50 %) :** le mot et la couleur de l'encre correspondent (ex. `ROUGE` écrit en rouge).
- **Condition incongruente (50 %) :** le mot et la couleur de l'encre diffèrent (ex. `ROUGE` écrit en bleu).

Le participant doit identifier **la couleur de l'encre** le plus rapidement et précisément possible. L'**effet Stroop** correspond à la différence entre le temps de réaction moyen en condition incongruente et en condition congruente ($TR_{\text{incongruent}} - TR_{\text{congruent}}$) sur les essais réussis.

## Contrôles

| Touche | Action |
| :--- | :--- |
| `ESPACE` | Démarrer l'expérience / Exporter les résultats en CSV (écran de fin) |
| `Flèche Gauche` | Répondre **BLEU** |
| `Flèche Droite` | Répondre **ROUGE** |
| `Flèche Haut` | Répondre **VERT** |
| `Flèche Bas` | Répondre **JAUNE** |
| `ÉCHAP` | Terminer la session en cours / Quitter le programme |

## Installation et lancement

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/yanis-thomas/stroop-experiment.git
   cd stroop-experiment
   ```

2. Installer les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

3. Lancer l'expérience :
    ```bash
    python main.py
    ```


## Architecture du projet
- ***classes.py*** : moteur expérimental orienté objet (Test pour la génération anti-répétition des stimuli et le chronométrage haute précision via time.perf_counter(), Experience pour le calcul des statistiques et l'exportation CSV).
- ***main.py*** : interface graphique Pygame, machine à états (DEBUT, EN_COURS, FIN) et affichage des résultats.

## Format des données exportées
À la fin d'une session, l'appui sur ESPACE génère deux fichiers CSV dans le dossier experiences :

- `experience_X_essais.csv` : journal essai par essai (numero, reussi, congruence, duree, texte, encre, saisie).
- `bilan_experiences.csv` : tableau récapitulatif inter-sessions (num_experience, nb_tests, taux_reussite, temps_moyen_react_congru, temps_moyen_react_incongru, effet_stroop).

## Feuille de route
- [x] v1.0.0 : Moteur expérimental POO, interface Pygame, export CSV automatisé.