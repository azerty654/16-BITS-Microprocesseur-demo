# 8-BITS Microprocesseur
Un mini-microprocesseur 8 bits que j’ai conçu moi-même sous Logisim, avec une architecture conçu UAL complète, plusieurs registres et une unité de contrôle programmable (UC). Ce projet a surtout pour but de comprendre concrètement l'architecture d'un microprocesseur, comment ses différentes parties communiquent entre elles et comment un assembleur fait pour décomposer les instructions en code machine qui pilotera les différents composants du système.
Ce projet est composé en deux parties distinctes : l'assembleur écrit en python qui décompose et traduit le script écrit par l'utilisateur en code machine de 15 bits qui pourra être exécuté, et le microprocesseur qui exécute et gère les instructions produites par le script Python.
# Architecture du microprocesseur 
- Unité arithmétique et logique (ALU) complète : addition, soustraction, multiplication, division, opérations logiques (AND, NAND, OR, NOR, XOR, XNOR, NOT) et registres d'état
- Registres généraux adressables (7 registres principaux, 2 sous-registres dédié à L'ALU, 1 registre d'état) 
- BUS de données
- Unité de commande programmable composé de deux ROM (Instructions ROM, Data ROM)
- Circuits logiques
# Programme d'assembleur
- codé en python
- jeu d'instructions (ADD, SUB, MULT, DIV, AND, NAND, OR, NOR, XOR, XNOR, NOT, JUMP, JPOS, JNEG, JZ)
- génère deux fichiers en .txt (data.txt et instructions.txt) qui devront être chargés dans les deux ROM de l'unité de contrôle
- 
