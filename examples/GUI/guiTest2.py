from appJar import gui
import time 
####################################################################################
#####################################Funzioni#######################################
####################################################################################
Clickcount = 0  
#se si premono tasti da tastiera 
def keyPress(key):
    if   key == "<Up>":
        app.increaseFont()
    elif key == "<Down>":
        app.decreaseFont()
    elif key == "<F1>":
        app.setFont(12)
         
#se si premono tasti sull'interfaccia grafica          
def ButtonPress(key):
    global Clickcount
    # aggiunge una riga chiamata "l1" con i "valori" che seguono la virgola
    # .addLabel(title, text=None)
    if   key == "Cancel":
        app.stop()
    elif key == "Submit":
        app.addLabel("l1", text="row=0\ncolumn=0")
        app.setLabelBg("l1", "red") 
    elif key == "Clicked":
        Clickcount += 1
        app.setLabel("title","Click="+str(Clickcount))
        
        
    if Clickcount >= 5:
        app.infoBox("allarme","maggiore di 5")
         
####################################################################################
################################IMPOSTAZIONI GUI####################################        
####################################################################################        

app = gui("Temperature Alarm", "400x200") # gui(titolo, dimensione finestra)
app.addLabel("title", "Press the arrow keys to change the font") # .addLabel(testo, dimensione finestra)

# associazione tasto -> funzione 
app.bindKey("<Up>", keyPress)
app.bindKey("<Down>", keyPress)
app.bindKey("<F1>", keyPress)

# link bottone -> funczione chiamata alla pressione del bottone
app.addButtons(["Submit", "Cancel", "Clicked"], ButtonPress)

app.go()
