import datetime
import sys
import os
import tkinter as tk
from tkinter import scrolledtext

# Liste de toutes les commandes disponibles dans le terminal
commandListV2 = {
    "pwd": "Affiche le répertoire courant",
    "echo <texte>": "Affiche un texte rentré en paramètre",
    "time <option>": "Affiche la date et l'heure. -d Date only, -t Time only",
    "exit": "Quitter le terminal",
    "ls": "Affiche les éléments du répertoire courant",
    "open <chemin complet/nom>": "Ouvre le fichier rentrée en paramètre",
    "createFile": "Créer un fichier",
    "createFolder": "Créer un dossier",
    "FileTest": "Vérifie la taille et l'existence d'un fichier",
    "deleteFile": "Supprimer un fichier",
    "help": "Affiche la liste des commandes ainsi que leur description",
    "cd <chemin>": "Changer de répertoire",
    "cd ..": "Revenir au répertoire parent",
    "clear": "Nettoie le terminal"
}
# Quitte le programme
def exit_cmd():
    sys.exit(0)

# Retourne la liste des fichiers et dossiers du répertoire courant 
def ls():
    path = os.getcwd()
    output = ""
    for elem in os.listdir(path):
        chemin_entier = os.path.join(path, elem)
        if os.path.isfile(chemin_entier):
            output += f"Fichier: {elem}\n"
        elif os.path.isdir(chemin_entier):
            output += f"Dossier: {elem}\n"
    return output

#Retourne le répertoire courant
def pwd():
    return os.getcwd()

def ouvrir(terminal,fichier=None):
    if fichier:
        _ouvrir_callback(fichier,terminal)
    else:
        terminal.ask_input("Entrer le chemin ou le nom du fichier à ouvrir : ", _ouvrir_callback)

def _ouvrir_callback(fichier, terminal):
    os.system(fichier)
    terminal.ready()

# Demande le nom du fichier à créer, puis appelle le callback
def createFile(terminal, fichier=None):
    if fichier:
        _createFile_callback(fichier, terminal)
    else:
        terminal.ask_input("Entrer le nom du fichier : ", _createFile_callback)

# Crée le fichier avec le nom saisi, puis remet le prompt
def _createFile_callback(fichier, terminal):
    f = open(fichier, 'w')
    f.close()
    terminal.print_output(f"Fichier '{fichier}' créé.\n")
    terminal.ready()

# Demande le nom du fichier à supprimer, puis appelle le callback
def deleteFile(terminal, fichier=None):
    if fichier:
        _deleteFile_callback(fichier, terminal)
    else: 
        terminal.ask_input("Fichier a supprimer : ", _deleteFile_callback)

# Vérifie que le fichier existe, puis demande une confirmation avant suppression
def _deleteFile_callback(fichier_a_supprimer, terminal):
    path = os.getcwd()
    chemin_entier = os.path.join(path, fichier_a_supprimer)
    if os.path.exists(chemin_entier):
        # Demande confirmation via un second callback
        terminal.ask_input(f"Confirmer la suppression de {fichier_a_supprimer} ? (oui/non) : ",
                           lambda rep, t: _deleteFile_confirm(rep, t, fichier_a_supprimer, chemin_entier))
    else:
        terminal.print_output(f"Le fichier {fichier_a_supprimer} n'existe pas\n")
        terminal.ready()

# Supprime le fichier si l'utilisateur a confirmé avec "oui"
def _deleteFile_confirm(confirmation, terminal, fichier, chemin):
    if confirmation.lower() == "oui":
        os.remove(chemin)
        terminal.print_output(f"Fichier {fichier} supprimé\n")
    else:
        terminal.print_output("Suppression annulée\n")
    terminal.ready()

# Demande le nom du fichier à vérifier, puis appelle le callback
def FileTest(terminal, fichier=None):
    if fichier:
        _filetest_callback(fichier, terminal)
    else:
        terminal.ask_input("Entrer le nom d'un fichier a verifier : ", _filetest_callback)

# Vérifie l'existence du fichier et affiche sa taille si il existe
def _filetest_callback(fichier_test, terminal):
    if os.path.exists(fichier_test):
        taille = os.path.getsize(fichier_test)
        terminal.print_output(f"Le fichier {fichier_test} existe\nTaille : {taille} octets\n")
    else:
        terminal.print_output(f"Le fichier {fichier_test} n'existe pas\n")
    terminal.ready()

# Demande le nom du dossier à créer, puis appelle le callback
def createFolder(terminal, folder=None):
    if folder:
        _createFolder_callback(folder, terminal)
    else:
        terminal.ask_input("Entrer le nom du dossier : ", _createFolder_callback)

# Crée le dossier s'il n'existe pas déjà
def _createFolder_callback(folder, terminal):
    if not os.path.exists(folder):
        os.makedirs(folder)
        terminal.print_output(f"Dossier '{folder}' créé.\n")
    else:
        terminal.print_output(f"Le dossier '{folder}' existe déjà.\n")
    terminal.ready()

# Remonte au dossier parent si option="..", sinon demande un chemin
def cd(option=None, terminal=None):
    if option == "..":
        # Récupère le dossier parent du répertoire courant
        parent = os.path.dirname(os.getcwd())
        os.chdir(parent)
        terminal.ready()
    elif option:
        _cd_callback(option, terminal)
    else:
        terminal.ask_input("Chemin : ", _cd_callback)

# Vérifie que le chemin existe et est bien un dossier, puis s'y déplace
def _cd_callback(path, terminal):
    if os.path.exists(path):
        if os.path.isdir(path):
            os.chdir(path)
        else:
            # Le chemin existe mais c'est un fichier, pas un dossier
            terminal.print_output(f"{path} n'est pas un dossier\n")
    else:
        terminal.print_output(f"Le dossier {path} n'existe pas\n")
    terminal.ready()

#Affiche l'heure et/ou la date, en fonction de l'option. Les deux par défaut
def time(option=None, terminal=None):
    if option:
        _time_callback(option, terminal)
    else:
        terminal.print_output(str(datetime.datetime.now()) + "\n")

def _time_callback(option, terminal):
    if option == "-t":
        terminal.print_output(str(datetime.datetime.now().strftime("%H:%M:%S"))+ "\n")
    if option == "-d":
        terminal.print_output(str(datetime.date.today()) + "\n")

def echo(option=None, terminal=None):
    if option:
        terminal.print_output(str(option) + "\n")
    else:
        terminal.ask_input("Que voulez vous echo : ",_echo_callback)

def _echo_callback(s, terminal):
    if s:
        terminal.print_output(str(s) + "\n")


# Retourne la liste des commandes disponibles sous forme de string
def help_cmd(terminal):
    for key,value in commandListV2.items():
        terminal.print_output(f"\n{key}: {value}\n")


class TerminalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Terminal")
        self.root.configure(bg="#0c0c0c")
        self.root.geometry("800x500")

        # Zone d'affichage des résultats
        self.output = scrolledtext.ScrolledText(
            root,
            bg="#0c0c0c", fg="#cccccc",
            insertbackground="#cccccc",
            font=("Consolas", 11),
            borderwidth=0,
            highlightthickness=0,
            state="disabled",
            wrap="word"
        )
        self.output.pack(fill="both", expand=True, padx=6, pady=(6, 0))

        # Configuration des couleurs selon le type de message
        self.output.tag_config("prompt", foreground="#4ec9b0")
        self.output.tag_config("error",  foreground="#f44747")
        self.output.tag_config("info",   foreground="#cccccc")

        # Ligne de saisie
        self.input_frame = tk.Frame(root, bg="#0c0c0c")
        self.input_frame.pack(fill="x", padx=6, pady=4)

        # Affichage du répertoire courant (mis à jour après chaque commande)
        self.prompt_label = tk.Label(
            self.input_frame,
            text=self._prompt_text(),
            bg="#0c0c0c", fg="#4ec9b0",
            font=("Consolas", 11)
        )
        self.prompt_label.pack(side="left")

        # Champ de saisie de la commande
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(
            self.input_frame,
            textvariable=self.input_var,
            bg="#0c0c0c", fg="#ffffff",
            insertbackground="#ffffff",
            font=("Consolas", 11),
            borderwidth=0,
            highlightthickness=0
        )
        self.input_entry.pack(side="left", fill="x", expand=True)
        self.input_entry.bind("<Return>", self._on_enter)
        self.input_entry.focus()

        # Stocke le callback en attente
        self._pending_callback = None
        self._welcome_msg = "Tapez 'help' pour voir les commandes disponibles.\n"
        self.print_output(self._welcome_msg, tag="info")

    # Retourne le chemin courant formaté pour le prompt
    def _prompt_text(self):
        return f"{os.getcwd()}> "

    def print_output(self, text, tag="info"):
        self.output.config(state="normal")
        self.output.insert("end", text, tag)
        self.output.config(state="disabled")
        self.output.see("end")

    def ask_input(self, prompt_text, callback):
        self._pending_callback = callback
        self.prompt_label.config(text=prompt_text, fg="#d7ba7d")

    # Remet le prompt normal et efface le callback en attente
    def ready(self):
        self._pending_callback = None
        self.prompt_label.config(text=self._prompt_text(), fg="#4ec9b0")

    # Appelé à chaque appui sur Entrée
    def _on_enter(self, event):
        user_input = self.input_var.get()
        # Vide le champ de saisie
        self.input_var.set("")

        # Affiche ce que l'utilisateur a tapé
        self.print_output(self.prompt_label.cget("text"), tag="prompt")
        self.print_output(user_input + "\n", tag="info")

        # Si on attend une réponse à un sous-prompt
        if self._pending_callback:
            self._pending_callback(user_input, self)
            return

        # Traitement des commandes
        parts = user_input.strip().split(" ", 1)
        command = parts[0]
        argument = parts[1] if len(parts)>1 else None

        if command == "BJ":
            self.print_output("Gambler de merde\n", tag="error")
            sys.exit(0)
        elif command == "ls":
            self.print_output(ls())
        elif command == "pwd":
            self.print_output(pwd())
        elif command == "time":
            time(argument,self)
        elif command == "open":
            ouvrir(self,argument)
        elif command == "echo":
            echo(argument,self)
        elif command.lower() == "createfile":
            createFile(self, argument)
            return
        elif command.lower() == "deletefile":
            deleteFile(self, argument)
            return
        elif command.lower() == "Filetest":
            FileTest(self, argument)
            return
        elif command.lower() == "createfolder":
            createFolder(self, argument)
            return
        elif command == "cd":
            cd(option=argument, terminal=self)
            return
        elif command == "cd ..":
            cd(option="..", terminal=self)
            return
        elif command == "clear":
            self.output.config(state="normal")
            self.output.delete("1.0", "end")
            self.output.config(state="disabled")
            self.print_output(self._welcome_msg, tag="info")

        elif command == "help":
            help_cmd(self)
        elif command == "exit":
            exit_cmd()
        elif command == "":
            pass
        else:
            self.print_output(f"{command} : Commande inconnue\n", tag="error")

        # Remet le prompt à jour avec le répertoire courant
        self.ready()


if __name__ == '__main__':
    root = tk.Tk()
    app = TerminalApp(root)
    root.mainloop()