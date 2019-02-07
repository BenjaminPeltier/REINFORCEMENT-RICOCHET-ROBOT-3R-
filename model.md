# Caractéristiques

* Taille grille : 16x16
* Nombre couleur pions : 4
* Formes de murs : 4
* Fin : 1 (4 couleurs possible)

# Noms des murs

* |    : 1
*    | : 2
* - : 4
* _ : 8

# Noms des pions

* Rouge : 16
* Bleu : 32
* Vert : 64
* Jaune : 128

# Noms des fins

* Rouge : 256
* Bleu : 512
* Vert : 1024
* Jaune : 2048

# Représentation d'une case

Représentation d'une case où on trouve un pion vert sur une position d'arrivée verte.

```JSON
{
    "LeftWall": 0, 
    "RightWall": 0, 
    "UpWall": 0, 
    "DownWall": 0, 
    "Red": 0,
    "Blue": 0,
    "Green": 0,
    "Yellow": 1,
    "RedWin": 0,
    "BlueWin": 0,
    "GreenWin": 0,
    "YellowWin": 1,
}
```