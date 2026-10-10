import os

DOSSIER = os.path.dirname(os.path.abspath(__file__))
FICHIER_ENTREE = os.path.join(DOSSIER, "programme.txt")
FICHIER_INSTR = os.path.join(DOSSIER, "instructions.txt")
FICHIER_DATA = os.path.join(DOSSIER, "data.txt")

TAILLE_SLOT = 8                      # chaque instruction occupe 8 lignes de ROM
MOT_VIDE = "00-00-00-000-0000-0-0"   # remplissage des lignes inutilisées (sans op)

# Chaque ligne = (mot de 15 bits, la valeur 8 bits est-elle écrite dans la data ?)
BLOC_MOVE = [
    ("00-10-00-{r1}-0000-0-0", False),
    ("01-10-00-{r1}-0000-0-0", False),
    ("00-10-00-{r1}-0000-0-0", False),
    ("10-01-00-{r2}-0000-0-0", False),
    ("10-00-00-{r2}-0000-0-0", False),
    ("00-00-00-{r2}-0000-0-0", False),
]

BLOC_WRITE = [
    ("00-01-00-{r1}-0000-0-1", True),
    ("00-00-00-{r1}-0000-0-1", True),
    ("00-00-00-{r1}-0000-0-0", True),
]

# READ : met la valeur du registre sur le bus (un seul mot)
BLOC_READ = [
    ("00-10-00-{r1}-0000-0-0", False),
]

# CLEAR : remet le registre à zéro (un seul mot)
BLOC_CLEAR = [
    ("00-11-00-{r1}-0000-0-0", False),
]

# Opérations ALU : OPERATION R1 R2 R3 (le code 4 bits remplace {op})
ALU_OPS = {
    "ADD":  "0001",
    "SUB":  "0010",
    "MULT": "0011",
    "DIV":  "0100",
    "AND":  "0101",
    "NAND": "0110",
    "OR":   "0111",
    "NOR":  "1000",
    "XOR":  "1001",
    "XNOR": "1010",
}

BLOC_ALU = [
    ("00-10-01-{r1}-{op}-0-0", False),
    ("00-10-00-{r1}-{op}-0-0", False),
    ("00-10-10-{r2}-{op}-0-0", False),
    ("00-10-00-{r2}-{op}-0-0", False),
    ("00-01-00-{r3}-{op}-1-0", False),
    ("00-00-00-{r3}-{op}-1-0", False),
]

# WAIT : 8 mots vides (l'instruction occupe tout son emplacement sans rien faire)
BLOC_WAIT = [("00-00-00-000-0000-0-0", False)] * 8

# Jumps : un seul mot, la valeur (adresse de saut) est écrite dans la data
BLOCS_JUMP = {
    "JUMP": [("00-00-00-000-1101-0-0", True)],
    "JPOS": [("00-00-00-000-1110-0-0", True)],
    "JNEG": [("00-00-00-000-1111-0-0", True)],
    "JZ":   [("00-11-00-000-0000-0-0", True)],
}


def reg_en_binaire(reg):
    # "R2" -> "010"
    return format(int(reg[1:]), "03b")


def lire_valeur(texte):
    # "03" -> 3 (décimal), "0x0f" -> 15, "0b101" -> 5
    texte = texte.lower()
    if texte.startswith(("0x", "0b")):
        valeur = int(texte, 0)
    else:
        valeur = int(texte, 10)
    if not 0 <= valeur <= 255:
        raise SystemExit(f"Valeur hors limites (8 bits) : {valeur}")
    return valeur


def en_hex(mot_binaire):
    # "00-01-00-001-0000-0-1" -> "0841"
    return format(int(mot_binaire.replace("-", ""), 2), "04X")


def ecrire(f_instr, f_data, mot, valeur):
    # Une ligne dans chaque fichier : même adresse garantie
    f_instr.write(en_hex(mot) + "\n")
    f_data.write(format(valeur, "02X") + "\n")


def ecrire_bloc(f_instr, f_data, bloc, valeur=0, **regs):
    if len(bloc) > TAILLE_SLOT:
        raise SystemExit(f"Bloc de {len(bloc)} lignes > {TAILLE_SLOT}")
    for mot, avec_data in bloc:
        ecrire(f_instr, f_data, mot.format(**regs), valeur if avec_data else 0)
    # Remplissage jusqu'à 8 lignes — garde le code opération si l'instruction en a un
    op_remplissage = regs.get("op", "0000")
    mot_vide = f"00-00-00-000-{op_remplissage}-0-0"
    for _ in range(TAILLE_SLOT - len(bloc)):
        ecrire(f_instr, f_data, mot_vide, 0)


with open(FICHIER_ENTREE) as f_in, \
     open(FICHIER_INSTR, "w") as f_instr, \
     open(FICHIER_DATA, "w") as f_data:

    for ligne in f_in:
        mots = ligne.split(";")[0].replace(",", " ").split()
        if not mots:
            continue
        instr = mots[0].upper()

        if instr == "MOVE":
            # Syntaxe : MOVE R1 R2
            ecrire_bloc(f_instr, f_data, BLOC_MOVE,
                        r1=reg_en_binaire(mots[1]), r2=reg_en_binaire(mots[2]))

        elif instr == "WRITE":
            # Syntaxe : WRITE 0x0f R1
            ecrire_bloc(f_instr, f_data, BLOC_WRITE, lire_valeur(mots[1]),
                        r1=reg_en_binaire(mots[2]))

        elif instr == "READ":
            # Syntaxe : READ R1
            ecrire_bloc(f_instr, f_data, BLOC_READ,
                        r1=reg_en_binaire(mots[1]))

        elif instr == "CLEAR":
            # Syntaxe : CLEAR R1
            ecrire_bloc(f_instr, f_data, BLOC_CLEAR,
                        r1=reg_en_binaire(mots[1]))

        elif instr in ALU_OPS:
            # Syntaxe : ADD R1 R2 R3
            if len(mots) != 4:
                raise SystemExit(f"{instr} attend 3 registres : {ligne.strip()}")
            ecrire_bloc(f_instr, f_data, BLOC_ALU,
                        r1=reg_en_binaire(mots[1]), r2=reg_en_binaire(mots[2]),
                        r3=reg_en_binaire(mots[3]), op=ALU_OPS[instr])

        elif instr == "WAIT":
            # Syntaxe : WAIT
            ecrire_bloc(f_instr, f_data, BLOC_WAIT)

        elif instr in BLOCS_JUMP:
            # Syntaxe : JUMP 03 / JPOS 03 / JNEG 03 / JZ 03
            ecrire_bloc(f_instr, f_data, BLOCS_JUMP[instr], lire_valeur(mots[1]))

        else:
            print("Instruction inconnue :", ligne.strip())

print("instructions.txt and data.txt ready !")