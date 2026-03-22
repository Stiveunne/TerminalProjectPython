import sys
import os

def exit():
    sys.exit(0)

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

def createFolder():
    folder = input("Entrer le nom du dossier : ")
    if not os.path.exists(folder):
        os.makedirs(folder)

def cd(option):
    if option == "..":
        pass

def Terminal():
    commandList = ["BJ", "exit", "ls", "createFile"]
    while True:
        command = input(">>> ")

        # Test
        if command == "BJ":
            sys.stdout.write("Gambler de merde")
            sys.exit(0)

        #Affichage de répertoire
        if command == "ls":
            ls()

        #Création d'un fichier
        if command == "createFile":
            createFile()

        # Commande de sortie
        if command == "exit":
            exit()
        elif command not in commandList:
            print(f"{command} : Commande inconnue")

if __name__ == '__main__':
    Terminal()