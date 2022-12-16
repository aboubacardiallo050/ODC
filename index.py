from re import error
from exos1 import R
from exos2 import DataTrans


def PyScript():

    print(""" 
    ###### SCRIPT DE CALCUL  ######

    1. EXERCICE 1 : Calcul de R
    2. EXERCICE 2 : Calcul de la Fonction de Data Trans
    """
          )

    I = input("Entrer le numéro de l'exercice à calculer : ")

    if I == "1":
        try:
            valeur_x = input("Entrer la valeur de x : ")
            print(f"L'expression R({valeur_x}) = {R(int(valeur_x))}")
        except error:
            print("Erreur lors du calcul de R(x) !")
            PyScript()

        print("Voulez-vous reprendre le script ?")
        reponse = input("Oui ou Non : ")

        if reponse == "Oui":
            PyScript()
        elif reponse == "Non":
            print("Merci d'avoir utilisé ce script !")
            exit()

    elif I == "2":
        taille_tableau = input("Entrer la taille du tableau (S) : ")
        nombre_tableau = input("Entrer le nombre de tableau (n) : ")

        try:
            data = DataTrans(int(taille_tableau) - 1, int(nombre_tableau) - 1)
            print("La valeur de la fonction f(x) est : ", data.f_d())
        except error as e:
            print("Il y a eu une erreur lors du calcul de la fonction f(D)")
            print("Veuillez réessayer !")
            PyScript()

        # Demander à l'utilisateur de reprendre le script ou de le quitter

        print("Voulez-vous reprendre le script ?")
        reponse = input("Oui ou Non : ")

        if reponse == "Oui":
            PyScript()
        elif reponse == "Non":
            print("Merci d'avoir utilisé ce script !")
            exit()

    else:
        print("Veuillez entrer un numéro d'exercice valide !")
        PyScript()


PyScript()
