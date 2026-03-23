import sys
import os

commandList = {"BJ" : "test", "exit" :"Ferme le terminal", "ls" : "Affiche les fichiers et dossiers du répertoire courant", "createFile" : "Créer un fichier", "createFolder":"Créer un dossier", "FileTest":"Vérifie la taille et l'existence d'un fichier", "deleteFile":"Supprime un fichier","help":"Affiche la liste des commandes ainsi que leur description","cd":"Changer de répertoire","clear":"Nettoie le terminal"}

def exit():
    sys.exit(0)

def clear():
    os.system("cls")

def ls():
    path = os.getcwd()
    for elem in os.listdir(path):
        chemin_entier = os.path.join(path, elem)
        if os.path.isfile(chemin_entier):
            print(f"Fichier: {elem}")
        elif os.path.isdir(chemin_entier):
            print(f"Dossier: {elem}")

def createFile():
    fichier = input("Entrer le nom du fichier : ")
    f = open(fichier,'w')
    f.close()

def deleteFile():
    path = os.getcwd()
    fichier_a_supprimer = input("Fichier a supprimer : ")
    chemin_entier = os.path.join(path, fichier_a_supprimer)
    if os.path.exists(chemin_entier):
        confirmation = input(
            f"Confirmer la suppression de {fichier_a_supprimer} ? (oui/non) : ")  # validation de la supression
        if confirmation.lower() == "oui":
            os.remove(fichier_a_supprimer)
            print(f"Fichier {fichier_a_supprimer} supprime")
        else:
            print("Suppression annulee")
    elif not os.path.exists(fichier_a_supprimer):
        print(f"Le fichier {fichier_a_supprimer} n existe pas")

def FileTest():
    fichier_test = input("Entrez le nom d un fichier a verifier : ")
    if os.path.exists(fichier_test):
        print(f"Le fichier {fichier_test} existe")
        taille = os.path.getsize(fichier_test)
        print(f"Taille : {taille} octets")
    else:
        print(f"Le fichier {fichier_test} n existe pas")

def createFolder():
    folder = input("Entrer le nom du dossier : ")
    if not os.path.exists(folder):
        os.makedirs(folder)

def cd(option):
    path = input("Chemin : ")
    os.chdir(path)
    """
    Maybe faire un truc avec des paramètres de fonction afin d'implémenter .. (retour au repo parent)
    genre : if option == ".." : blablabla
    """

def help():
    global commandList
    for co,desc in commandList.items():
        print(co + ": " + desc +"\n")

def Terminal():
    global commandList
    while True:
        command = input(f"{os.getcwd()} >>> ")

        # Test
        if command == "BJ":
            sys.stdout.write("Gambler de merde")
            sys.exit(0)

        #Commande Clear (nettoyage du terminal)
        if command == "clear":
            clear()

        #Affichage de répertoire courant
        if command == "ls":
            ls()

        #Création d'un fichier
        if command == "createFile":
            createFile()

        #Suppression d'un fichier
        if command == "deleteFile":
            deleteFile()

        #Vérification : Taille et Existence d'un fichier
        if command == "FileTest":
            FileTest()

        #Création d'un dossier
        if command == "createFolder":
            createFolder()

        #Commande d'aide
        if command == "help":
            help()

        # Commande de sortie
        if command == "exit":
            exit()
        elif command not in commandList:
            print(f"{command} : Commande inconnue")

if __name__ == '__main__':
    Terminal()