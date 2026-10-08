# 8-BITS Microprocesseur

Un **mini-microprocesseur 8 bits** que j’ai mis en place moi-même sous **Logisim**, avec une architecture conçue sur mesure, une UAL complète, plusieurs registres/sous-registres et une unité de contrôle programmable (UC). Ce projet a surtout pour but de comprendre concrètement **l'architecture d'un microprocesseur**, comment ses différentes parties communiquent entre elles et comment un assembleur fait pour décomposer les instructions en code machine qui pilotera les différents composants du système.

Ce projet est composé de deux parties distinctes : l'assembleur écrit en Python qui décompose et traduit le script écrit par l'utilisateur en micro-instructions de 15 bits qui pourront être exécutées, et le microprocesseur qui interprète et exécute les instructions produites par l’assembleur.

![architecture du microprocesseur](https://github.com/azerty654/8-BITS-Microprocesseur-demo/blob/main/Project_Picture/architecture%20.png)

# Architecture du microprocesseur

* Dispose d'une unité arithmétique et logique (ALU) complète : addition, soustraction, multiplication, division, opérations logiques (AND, NAND, OR, NOR, XOR, XNOR, NOT) et registres d'état
* Registres généraux adressables (7 registres principaux, 2 sous-registres dédiés à l'ALU, 1 registre d'état, 1 registre Work)
* BUS de données
* Unité de commande programmable composée de deux mémoires ROM (Instructions ROM, Data ROM) et d’un compteur intégré pour défiler les micro-instructions à chaque tic d’horloge
* Circuits logiques (décodeur, convertisseur…)

# Programme d'assembleur

* Dispose d’un jeu d'instructions (`ADD`, `SUB`, `MULT`, `DIV`, `AND`, `NAND`, `OR`, `NOR`, `XOR`, `XNOR`, `NOT`, `MOVE`, `WRITE`, `JUMP`, `JPOS`, `JNEG`, `JZ`)
* Génère deux fichiers en **.txt** (`data.txt` et `instructions.txt`) qui devront être chargés dans les deux ROM de l'unité de contrôle
* Codé en **Python 3.14.0**

# Comment ça marche

**Partie assembleur** → après avoir écrit le script dans le fichier `programme.txt`, on exécute le code de l’assembleur en Python, le programme se charge de décoder et de modifier en temps réel les données en hexadécimal dans deux fichiers distincts : le fichier `instructions.txt` contenant les micro-instructions de 15 bits qui seront chargées dans la mémoire ROM principale de l’unité de contrôle, et le fichier `data.txt` contenant toutes les valeurs codées en 8 bits (de 0 à 255 maximum) qui seront chargées dans la ROM secondaire dédiée à la mémoire de l’unité de contrôle.

![Fichiers Assembleur](https://github.com/azerty654/8-BITS-Microprocesseur-demo/blob/main/Project_Picture/fichiers_assambleur%20pic.png?raw=true)

**Partie Microprocesseur** → après avoir chargé les deux fichiers générés par l’assembleur dans la ROM des instructions et la ROM des données, on met en marche l’horloge interne du système, qui activera dans un premier temps le compteur intégré dans l’unité de contrôle, relié aux adresses mémoire des ROMs (entre autres, cela permettra de parcourir toutes les données stockées dans les adresses mémoire de 0 à 255 dans l’ordre). Chaque ligne du code du script (instruction) est **stockée sur 8 blocs de 15 bits chacun dans la mémoire**, ces blocs contiennent eux-mêmes chacun une micro-instruction (j’ai fait ce choix de répartition pour mieux gérer l’emplacement mémoire de chaque instruction et les séparer les unes des autres, ce qui est notamment indispensable pour les instructions `JUMP` pour faire des sauts entre les lignes du code). Une instruction prendra donc 8 fronts d'horloge pour s'exécuter (par exemple, avec une horloge à 1 MHz, le microprocesseur peut exécuter jusqu'à 125 000 instructions par seconde).

![UC](https://github.com/azerty654/8-BITS-Microprocesseur-demo/blob/main/Project_Picture/CU.png?raw=true)

* L'unité de contrôle dispose de deux sorties principales, la première est la sortie **CU_Instruction** qui se chargera de piloter les registres, les sous-registres et l'ALU et principalement leurs permissions de lecture et d'écriture. La deuxième est la sortie **value** qui se chargera de transmettre les données au bus principal du microprocesseur au bon moment en étant synchronisée avec les instructions en cours d’exécution.

![inst](https://github.com/azerty654/8-BITS-Microprocesseur-demo/blob/main/Project_Picture/15%20bits%20instructions.png?raw=true)

* Toutes les données circulent dans un seul **bus de données de 8 bits**, commun à tous les composants. Entre autres, l’ALU, les registres, les sous-registres, etc. partagent la même entrée et la même sortie de données. C’est ici que l’unité de contrôle est indispensable pour commander ces différents composants, notamment en choisissant **qui lit et écrit les données du bus, ou qui injecte ses données dans le bus** tout en synchronisant le tout ensemble

![bus](https://github.com/azerty654/8-BITS-Microprocesseur-demo/blob/main/Project_Picture/bus.png?raw=true)

# Micro-instructions

Comme dit précédemment, chaque instruction du programme est composée de micro-instructions de 15 bits chacune, leur nombre peut varier d'une instruction à l'autre (par exemple, l'instruction MOVE comporte 6 micro-instructions tandis que l'instruction WRITE n'en comporte que 3). Quand l'instruction comporte moins de 8 micro-instructions, le reste des blocs non utilisés sont automatiquement remplis par des 0 jusqu'à combler le reste.

**Répartition des bits d'instruction** → Ces bits sont arrangés ainsi (du LSB au MSB) :

* `BIT 0 (1 bit)` → autorisation de lecture des données du port **value** de l'unité de contrôle
* `BIT 1 (1 bit)` → autorisation de lecture des données du port **ALU_Result** de l'ALU
* `BIT 2 au BIT 5 (4 bits)` → code binaire de l'opération/instruction (**opcode**)
* `BIT 6 au BIT 8 (3 bits)` → sélection de l'un des **sept registres principaux** de 1 (001) à 7 (111)
* `BIT 9 au BIT 10 (2 bits)` → autorisation d'écriture des **sous-registres AB** de l'ALU
* `BIT 11 au BIT 12 (2 bits)` → sélection de l'opération des **registres principaux** (Reg_Write → 01, Reg_Read → 10, Reg_Clear → 11)
* `BIT 13 au BIT 14 (2 bits)` → sélection de l'opération du **sous-registre Work** (Work_Write → 01, Work_Read → 10, Work_Clear → 11)

**Adresses binaires des registres** → chaque code binaire correspond à l'un des sept registres

* `Registre 1` → **001**
* `Registre 2` → **010**
* `Registre 3` → **011**
* `Registre 4` → **100**
* `Registre 5` → **101**
* `Registre 6` → **110**
* `Registre 7` → **111**

**Code binaire des opérations** → chaque code binaire correspond à l'une des différentes opérations

* `ADD`
* `SUB`
* `MULT`
* `DIV`
* `AND`
* `NAND`
* `OR`
* `NOR`
* `XOR`
* `XNOR`
* `NOT`
* `JUMP`
* `JNEG`
* `JPOS`

**IMPORTANT**

Les opérations `WRITE`, `MOVE` et `CLEAR` ne font pas partie de cette liste, donc elles ne sont pas représentées sur les 4 bits de l'OPCODE, elles sont représentées respectivement par 3, 6 et 1 blocs d'instructions. D'ailleurs, les commandes qui font appel à l'ALU sont exécutées sur les mêmes 6 micro-instructions, il n'y a que **l'OPCODE** qui change selon l'instruction appelée.
