import tkinter as tk
import os

def playSingle():

    #Windows 11
    #os.system('python snakesingle.py')

    #MacOS
    os.system('python3 snakesingle.py')

def playMulti():

    #Windows 11
    #os.system('python snakemulti.py')
    
    #MacOS
    os.system('python3 snakemulti.py')

#print(str(globals.SCALE))

menu = tk.Tk()

menu.geometry("480x320")
menu.title("Snake Game Menu")

label = tk.Label(menu, text="Snake Game!", font=('Arial', 15))
label.pack(pady=20)

button = tk.Button(menu, text = "Start Singleplayer Game", font=('Arial', 13), command = playSingle)
button.pack(pady=20)

button2 = tk.Button(menu, text = "Start Multiplayer Game", font=('Arial', 13), command = playMulti)
button2.pack(pady=20)

menu.mainloop()
