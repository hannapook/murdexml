"""
Tere maailm!

Lihtsalt testimiseks
"""

def proov():
    "For testing"
    print("See on üks proovifunktsioon")
    return "Proovi väärtus"

def main():
    "Main routine"
    print("Tere maailm!")
    return "Peafunktsiooni main väärtus"

# main kutsutakse välja ainult siis,
# kui programmi käivitatakse skriptina,
# aga ei impordita
if __name__ == '__main__':
    main()
    
