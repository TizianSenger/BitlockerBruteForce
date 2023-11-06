import os
import subprocess
import random
import re

def GenerateKey():
    RecoveryKey = ""
    
    for i in range(1, 56):
        if i % 7 == 0:
            RecoveryKey += "-"
        else:
            RecoveryKey += str(random.randint(0, 9))

    return RecoveryKey

try:
    driveLetter = str(input("Geben Sie den Laufwerksbuchstaben ein, z.B. E:       Ihr Laufwerksbuchstabe:    "))  # Ändern Sie den Laufwerksbuchstaben nach Bedarf
    regchk = re.compile('[a-zA-Z]')
    
    if not (":" in driveLetter):
        print("Der Laufwerksbuchstabe sollte das Doppelpunktzeichen \":\" enthalten")
        exit()
    elif len(driveLetter) != 2:
        print("Der Laufwerksbuchstabe sollte aus zwei Zeichen bestehen, nur ein Buchstabe und ein Doppelpunkt")
        exit()
    elif not (regchk.match(driveLetter[0])):
        print("Der Laufwerksbuchstabe muss von A-Z sein")
        exit()
    
    ItemsX = ["░", "▒", "▓", "█", "▓", "▒"]
    countr = 1
    keySuccess = None

    while True:
        countr += 1
        rec_key = GenerateKey()
        resultX = subprocess.run(['manage-bde', '-unlock', driveLetter, '-RecoveryPassword', rec_key], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        outputStream = resultX.stdout.decode('utf-8', errors='ignore')
        outputErrorStream = resultX.stderr.decode('utf-8', errors='ignore')

        if "admini" in outputStream:
            print("Sie müssen dieses Skript mit Administratorrechten ausführen!")
            break
        elif "error occurred" in outputErrorStream:
            print("Möglicherweise existiert dieses Laufwerk nicht oder es sind andere Probleme aufgetreten!")
            break
        elif "is already unlocked" in outputStream:
            print("Es scheint, als sei dieses Laufwerk bereits entsperrt!")
            break
        if not os.path.exists(driveLetter):
            perc = ItemsX[countr % len(ItemsX)]
            print(f"{countr} Versuche! {perc}", end="\r")
            print("", end="\r")
        else:
            keySuccess = rec_key
            print(outputStream)
            print(f"{resultX.args[4]} scheint zu funktionieren! Herzlichen Glückwunsch!")
            break

    if keySuccess:
        with open('recoverykey.txt', 'w') as key_file:
            key_file.write(keySuccess)
            print(f"Der erfolgreiche Wiederherstellungsschlüssel wurde in 'recoverykey.txt' gespeichert.")

except Exception as exception:
    print(exception)
