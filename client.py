
import socket
from tkinter import *
from  threading import Thread
from PIL import ImageTk, Image
import random

screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None


canvas1 = None
canvas2 = None

playerName = None
nameEntry = None
nameWindow = None
gameWindow = None
rollButton = None

leftBoxes = []
rightBoxes = []

player_type = None

turn = None

def rollDice():
    global SERVER
    global player_type

    diceChoice = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684','\u2685','\u2686',]

    value = random.choice(diceChoice)
    
    if(player_type == 'player1'):
        SERVER.send(value + 'player2 Turn'.encode('utf-8'))

    if(player_type == 'player2'):
        SERVER.send(value + 'player1 Turn'.encode('utf-8'))



def leftBoard():
    global gameWindow
    global leftBoxes
    global screen_height
    global screen_width

    x = 30
    
    for box in range(11):
        if(box == 0):
            boxLabel = Label(gameWindow, font= ("Helvetica", 30), width= 2, height= 1, bg= 'red')
            boxLabel.place(x= x, y= screen_height/2 - 85) 
            leftBoxes.append(boxLabel)
            x = x+50
        else: 
            boxLabel = Label(gameWindow, font= ("Helvetica", 55), width= 2, height= 1,relief= 'ridge', bg= 'white')
            boxLabel.place(x= x, y= screen_height/2 - 100) 
            leftBoxes.append(boxLabel)
            x = x + 85

def rightBoard():
    global gameWindow   
    global rightBoxes
    global screen_height
    global screen_width

    x = 985
    
    for box in range(11):
        if(box == 10):
            boxLabel = Label(gameWindow, font= ("Helvetica", 30), width= 2, height= 1, bg= 'yellow')
            boxLabel.place(x= x, y= screen_height/2 - 85) 
            rightBoxes.append(boxLabel)
            x = x + 50
        else: 
            boxLabel = Label(gameWindow, font= ("Helvetica", 55), width= 2, height= 1, relief='ridge', bg= 'white')
            boxLabel.place(x= x, y= screen_height/2 - 100) 
            rightBoxes.append(boxLabel)
            x = x + 85

def finishingBox():
    global gameWindow   
    global screen_height
    global screen_width
    
    finishedBox = Label(gameWindow, text= 'Home', font= ("Helvetica", 32), width= 8, height= 4, bg= 'green', fg= 'white')
    finishedBox.place(x= screen_width/2 - 70, y= screen_height/2-150)

def gameWindow():
    global screen_height
    global screen_width
    global gameWindow
    global canvas2
    global player_type
    global turn
    global rollButton
    

    gameWindow = Tk()
    gameWindow.title("Ludo Ladder")
    gameWindow.attributes('-fullscreen', True)
    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()
    
    bg= ImageTk.PhotoImage(file= './assets/background.png')

    canvas2 = Canvas(gameWindow, width= 500, height= 500)
    canvas2.pack(fill= 'both', expand= True)
    canvas2.create_image(0,0, image= bg, anchor= "nw")
    canvas2.create_text(screen_width/2, screen_height/5, text="Ludo Ladder", font= ('Chalkboard SE', 100), fill= 'white')


    leftBoard()
    rightBoard()
    finishingBox()

    dice = canvas2.create_text(screen_width/2, screen_height/2 + 250, text= '\u2680', font= ("Chalkboard SE", 250), fill= 'white')

    rollButton = Button(gameWindow, text= 'Roll Dice', fg= 'black', font= ("Chalkboard SE", 15), bg = 'grey', command= rollDice, width = 20, height= 5)

    if(player_type == 'player1' and turn):
        rollButton.place(x= screen_width/2 -80, y= screen_height/2 + 400)
    else:
        rollButton.pack_forget()

    if(player_type == 'player2' and turn):
        rollButton.place(x= screen_width/2 -80, y= screen_height/2 + 400)
    else:
        rollButton.pack_forget()

    gameWindow.resizable(True, True)

    gameWindow.mainloop()

def saveName():
    global playerName
    global SERVER
    global nameEntry
    global nameWindow

    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()
    SERVER.send(playerName.encode())

    gameWindow()



#Teacher write code here for askPlayerName()
def askPlayerName():
    global nameWindow
    global nameEntry
    global screen_height
    global screen_width
    global canvas1

    nameWindow = Tk()
    nameWindow.title("Ludo Ladder")
    nameWindow.attributes('-fullscreen', True)

    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg= ImageTk.PhotoImage(file= './assets/background.png')
    canvas1 = Canvas(nameWindow, width= 500, height= 500)
    canvas1.pack(fill= 'both', expand= True)
    canvas1.create_image(0,0, image= bg, anchor= "nw")
    canvas1.create_text(screen_width/2, screen_height/5, text= "Enter Name", font= ('ChalkBoard SE', 100), fill= 'white')

    nameEntry = Entry(nameWindow, width= 15, justify= CENTER, font= ('ChalkBoard SE', 15), bd= 5, bg= 'white')
    nameEntry.place(x= screen_width/2 - 200, y= screen_height/4 + 100)

    nameButton = Button(nameWindow, text= 'Save', font= ('ChalkBoard SE', 13), width= 15, height= 2, bg= '#2ee665', bd= 3, command= saveName)
    nameButton.place(x= screen_width/2 - 150, y= screen_height/2 + 13)
    
    nameWindow.resizable(True, True)

    nameWindow.mainloop()

def recievedMessage():
    pass


def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT  = 5001
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))
    thread = Thread(target= recievedMessage)
    thread.start()

    # Creating First Window
    askPlayerName()




setup()
