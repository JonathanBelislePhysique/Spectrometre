# README (Français) #

Ce README donne les instructions pour exécuter, construire et créer un installateur pour le code permettant d'ajouter une caméra au spectromètre présenté dans le lien suivant.
https://www.youtube.com/watch?v=LIKMNlLCGL0&t=0s

Voici le lien pour télécharger un installateur Windows permettant d'installer une version fonctionnelle du logiciel du spectromètre.
https://etudiantcegeplapocatiereqc-my.sharepoint.com/:u:/g/personal/jbelisle_cegeplapocatiere_qc_ca/EcsTr57cTApBoVmnSrnNA4YBxlXAEklCfjzaFOEjbKdREA?e=XwXGxn

### Description du dépôt? ###

* L'interface utilisateur utilise PyQt5
* Le fichier main.py est le fichier principal pour lancer l'interface utilisateur
* Les spécifications de construction sont dans le fichier main.spec
* Les styles de l'interface utilisateur sont dans le fichier style.css
* Les dossiers build et dist sont automatiquement créés et complétés par la commande : pyinstaller main.spec
* Le dossier installer contient le fichier pour créer un installateur, le fichier .ifg peut être ouvert avec le logiciel InstallForge (https://installforge.net/)
* Les chemins de fichier du fichier .ifg sont absolus et doivent être changé pour chaque utilisateur.

### Comment faire la mise en place? ###

* Interpréteur de base testé : Python 3.9
* Environnement virtuel : pip install -r requirements.txt
* Instruction pour la construction : pyinstaller main.spec
* Instructions pour l'installateur : Télécharger InstallForge (https://installforge.net/) ouvrir le fichier installer/spectrometre_techno_installteur.ifp
* Pour un tutoriel sur la construction avec PyInstaller et pour faire un installateur avec InstallForge (https://www.pythonguis.com/tutorials/packaging-pyqt5-pyside2-applications-windows-pyinstaller/)

# README (English) #

This README gives the instructions to run, build and create an installer for the code to add a camera to the spectrometer presented in the link below.
https://www.youtube.com/watch?v=LIKMNlLCGL0&t=0s

Here is the link to download a Windows installer to install the software for the spectrometer.
https://etudiantcegeplapocatiereqc-my.sharepoint.com/:u:/g/personal/jbelisle_cegeplapocatiere_qc_ca/EcsTr57cTApBoVmnSrnNA4YBxlXAEklCfjzaFOEjbKdREA?e=XwXGxn

### What is this repository for? ###

* The GUI uses PyQt5
* The file main.py is the main file to run the GUI
* Building specifications are in main.spec
* The styles of the interface are in style.css
* The folders build and dist are automatically created and populated by the command : pyinstaller main.spec
* The folder installer contains the files to create an installer where the .ifg file can be opened with InstallForge
* The filepaths in the .ifg file are absolute and needs to be changed for each user

### How do I get set up? ###

* Base interpreter tested : Python 3.9
* Virtural environnement : pip install -r requirements.txt
* Building instruction : pyinstaller main.spec
* Installer instruction : Download InstallForge (https://installforge.net/) and open installer/spectrometre_techno_installteur.ifp
* For a tutorial how to build code with PyInstaller and to create an installer with InstallForge (https://www.pythonguis.com/tutorials/packaging-pyqt5-pyside2-applications-windows-pyinstaller/)
