# README #

Ce README donne les instructions pour exécuter, construire et créer un installateur pour le code permettant d'ajouter une camera au spectromètre présenté dans le lien suivant.
https://www.youtube.com/watch?v=LIKMNlLCGL0&t=0s

This README gives the instructions to run, build and create an installer for the code to add a camera to the spectrometer presented in the link above.

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
