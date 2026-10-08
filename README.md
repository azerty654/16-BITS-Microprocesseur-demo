# 8-BITS Microprocesseur
Un mini-microprocesseur 8 bits que j’ai mis en place moi-même sous Logisim, avec une architecture conçue sur mesure, une UAL complète, plusieurs registres/sous registres et une unité de contrôle programmable (UC). Ce projet a surtout pour but de comprendre concrètement l'architecture d'un microprocesseur, comment ses différentes parties communiquent entre elles et comment un assembleur fait pour décomposer les instructions en code machine qui pilotera les différents composants du système.
Ce projet est composé en deux parties distinctes : l'assembleur écrit en python qui décompose et traduit le script écrit par l'utilisateur en micros instructions de 15 bits qui pourront être exécutées, et le microprocesseur qui interprète et exécute les instructions produites par l’assembleur.

![architecture du microprocesseur](https://github.com/azerty654/8-BITS-Microprocesseur-demo/blob/main/Project_Picture/architecture%20.png) 

# Architecture du microprocesseur 
- Dispose d'une Unité arithmétique et logique (ALU) complète : addition, soustraction, multiplication, division, opérations logiques (AND, NAND, OR, NOR, XOR, XNOR, NOT) et registres d'état
- Registres généraux adressables (7 registres principaux, 2 sous-registres dédié à L'ALU, 1 registre d'état) 
- BUS de données
- Unité de commande programmable composée de deux ROM (Instructions ROM, Data ROM) et d’un compteur intégré pour défiler les instructions à chaque tic d’horloge
- Circuits logiques (décodeur, convertisseur…) 
# Programme d'assembleur
- Dispose d’un jeu d'instructions (`ADD`, ``SUB``, ``MULT``, ``DIV``, ``AND``, ``NAND``, ``OR``, ``NOR``, ``XOR``, ``XNOR``, ``NOT``, ``MOVE``, ``WRITE``, ``JUMP``, ``JPOS``, ``JNEG``, ``JZ``)
- Génère deux fichiers en **.txt** (``data.txt`` et ``instructions.txt``) qui devront être chargés dans les deux ROM de l'unité de contrôle
- Codé en **python 3.14.0**
# Comment ça marche 
**Partie assembleur** → après avoir écrit le script dans le fichier ``programme.txt``, on exécute le code de l’assembleur en python, le programme se charge de décoder et de modifier en temps réel les données en hexadécimal dans deux fichiers distincts : le fichier ``instructions.txt`` contenant les micro-instructions en 15 bits qui seront chargé dans la ROM principale de l’unité de contrôle, et le fichier ``data.txt`` contenant toutes les valeurs codés en 8 bits (de 0 à 255 maximum) qui seront chargés dans la ROM secondaire dédié à la mémoire de l’unité de contrôle. 

![Fichiers Assembleur](https://github.com/azerty654/8-BITS-Microprocesseur-demo/blob/main/Project_Picture/fichiers_assambleur%20pic.png?raw=true)

**Partie Microprocesseur** → après avoir chargé les deux fichiers générés par l’assembleur dans la ROM des instructions et la ROM des données, on met en marche l’horloge interne du système, qui activera en premier temps le compteur intégré dans l’unité de contrôle, relié aux adresses mémoires des ROMs (entre autres, cela permettra de parcourir toutes les données stockées dans les adresses mémoire de 0 à 255 dans l’ordre). Chaque ligne du code du script (instruction) est **stockée sur 8 blocs de 15 octets chacun dans la mémoire**, Ces blocs contiennent eux-mêmes chacun une micro-instruction (J’ai fait ce choix de répartition pour mieux gérer l’emplacement mémoire de chaque instruction et les séparer les unes des autres, ce qui est notamment indispensable pour les instructions `JUMP` pour faire des sauts entre les lignes du code).

![UC](https://github.com/azerty654/8-BITS-Microprocesseur-demo/blob/main/Project_Picture/CU.png?raw=true)


