# 🏆 Guide du Participant : Territoires Algorithmiques

Bienvenue dans le hackathon **Territoires Algorithmiques : Le Duel des Agents** ! Ce document contient toutes les règles et les spécifications techniques pour vous aider à coder l'IA qui écrasera vos adversaires.

---

## 🎯 L'Objectif du Jeu
Deux agents intelligents s'affrontent pour le contrôle d'une grille de données symétrique de taille variable (généralement 20x20 ou 30x30). 
Votre mission est simple : **conquérir le plus vaste territoire** tout en survivant aux tentatives d'enfermement de votre adversaire et aux murs aléatoires/ou non présents sur le terrain.

* Le match se déroule au tour par tour.
* L'équipe ayant colorié le plus grand nombre de cases à la fin de la simulation gagne.
* La partie se termine si la limite de temps est atteinte (500 tours) ou si les deux agents sont bloqués de tous les côtés sans aucune issue.

## 👥 Les Équipes et Couleurs

Lorsque l'arbitre lance une partie, deux algorithmes s'affrontent sur le plateau de jeu :

* **L'Équipe A** (Joueur 1) : Son code est lu depuis le premier fichier défini dans `main.py` (par défaut `bots/bot_equipe_01.py`). Sur l'interface graphique, ses actions et son territoire sont représentés par la couleur **BLEUE**, et sa valeur numérique native dans la matrice est un `1`.
* **L'Équipe B** (Joueur 2) : Son code est lu depuis le second fichier (par défaut `bots/bot_equipe_02.py`). Sur l'interface graphique, elle est identifiée par une couleur **ROUGE** vibrante, et sa valeur au sein de la matrice est un `2`.


---

## 🛠️ Spécifications Techniques

Votre seul et unique travail est d'écrire la fonction d'intelligence de votre module.
Vous devez nous fournir un fichier `bot_equipe_XX.py` contenant de manière stricte une fonction principale nommée `get_move(...)`.

### La signature de la fonction

Voici le squelette obligatoire de votre IA :

```python
def get_move(grid, my_pos, opp_pos, turn_info):
    """
    Détermine votre prochain mouvement.
    
    Retourne obligatoirement une des chaînes de caractères suivantes :
    "NORD", "SUD", "EST", "OUEST" ou "REPOS"
    """
    
    # ... Votre algorithme ...
    
    return "NORD"
```

### Explication des Paramètres Entrants

Lors de chaque tour, l'arbitre principal exécute votre fichier et injecte instantanément cet état de jeu dans vos paramètres :

* `grid` (*List[List[int]]*) : Une matrice 2D lisible au format `grid[y][x]` décrivant la carte actuelle.
  * `0` : Case Neutre (ou vide)
  * `1` : Territoire contrôlé par l'équipe A
  * `2` : Territoire contrôlé par l'équipe B
  * `-1` : Mur infranchissable
* `my_pos` (*Tuple[int, int]*) : Vos coordonnées actuelles `(x, y)` sur la carte. L'origine `(0, 0)` correspond au coin Haut-Gauche.
* `opp_pos` (*Tuple[int, int]*) : Les coordonnées actuelles `(x, y)` de votre adversaire.
* `turn_info` (*Dict*) : Dictionnaire contenant :
  * `"turn"` : Le numéro du tour en cours
  * `"time_left_ms"` : (Information) La limite de temps maximale pour votre calcul (généralement 100ms)

---

## ⚠️ Règles Avancées et Pièges

Pour remporter le tournoi, votre IA devra éviter de tomber dans certains pièges structurels du moteur de jeu :

### 1. Chronomètre Implacable (100ms)
À chaque appel de `get_move`, **vous disposez d'un maximum de 100 millisecondes** pour renvoyer votre réponse. Si votre algorithme est trop lourd (boucles sur de grandes profondeurs), l'arbitre coupera votre script proprement et vous forcera à jouer `"REPOS"`.

### 2. Le Mur de Collision
Si les deux agents choisissent de se déplacer vers **la même case neutre libre au même moment** (Collision), la case se transforme de manière irrévocable en un **Mur Infranchissable** (`-1`) et vous restez tous les deux physiquement sur vos cases d'origine. C'est idéal pour bloquer l'ennemi !

### 3. Obstacles Absolus
Vous ne pouvez jamais envoyer une instruction qui vous ferait :
1. Franchir la bordure et sortir de la grille de jeu.
2. Passer sur une case valant `%1` ou `%2` (territoires déjà couverts par vous ou par l'ennemi).
3. Traverser ou aller sur un mur (`-1`).

*(Toute tentative désespérée de foncer dans le mur vous vaudra l'équivalent de la commande "REPOS" pendant ce tour).*

---

## 💡 Bot Starter "Random"

Besoin d'un point de départ ? Voici une IA ultra-simpliste qui choisit aléatoirement une case vide autour d'elle à chaque tour. Appuyez-vous dessus pour écrire vos premiers arbres conditionnels !

```python
import random

def get_move(grid, my_pos, opp_pos, turn_info):
    # Les deltas de mouvement pour chaque direction
    moves = {
        "NORD": (0, -1),
        "SUD": (0, 1),
        "EST": (1, 0),
        "OUEST": (-1, 0)
    }
    
    valid_moves = []
    x, y = my_pos
    
    # On teste les 4 points cardinaux
    for name, (dx, dy) in moves.items():
        nx, ny = x + dx, y + dy
        # Si la case appartient à la grille ET est vide (valeur 0)
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
            if grid[ny][nx] == 0:
                valid_moves.append(name)
                
    # On tire on sort un mouvement valide, sinon forfait (REPOS)
    if valid_moves:
        return random.choice(valid_moves)
    return "REPOS"
```

---

## 🚀 Comment Lancer et Tester votre IA

Pour tester vos créations et les faire s'affronter (ou vous entraîner contre les bots "Starter"), ouvrez un terminal à la racine du projet et tapez cette simple commande :

```bash
python3 main.py
```

Avant de lancer, assurez-vous de ces deux points :
1. **Renseignez vos bots :** Ouvrez le fichier `main.py` avec un éditeur et modifiez les variables tout en haut (`BOT_1_PATH` et `BOT_2_PATH`) pour indiquer le chemin vers votre propre fichier Python (ex: `"bots/bot_equipe_alpha.py"`).
2. **Dépendances :** Si le jeu ne s'ouvre pas, il vous manque le module graphique Pygame. Installez-le avec la commande : `pip install pygame`.

Une fois exécutée, une interface graphique 2D s'ouvrira et simulera la bataille d'algorithmes sous vos yeux !

*Bon courage, et que la compilation soit avec vous !*
