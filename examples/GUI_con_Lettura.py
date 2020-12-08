from appJar import gui

from mlx90632.mlx90632 import Mlx90632 
from datetime import datetime
from sys import platform
import atexit
from mlx90632.MemFile import MemFile   

import time 
############Inizializzazione sensore temp######################### 
dev = Mlx90632("I2C-1")                         
dev.init()
dev.wait_new_data()
chip_id = dev.read_chipid()
chip_id_str = dev.chipid_str

####################################################################################
#####################################Funzioni#######################################
####################################################################################
 
#se si premono tasti sull'interfaccia grafica          
def ButtonPress(key):
    # aggiunge una riga chiamata "l1" con i "valori" che seguono la virgola
    # .addLabel(title, text=None)
    if   key == "Esci":
        app.stop()
    elif key == "Misura":
        ##############################################################################################################################
        ########################################## N-LETTURE SUCCESSIVE ##############################################################
        ##############################################################################################################################
        # numero di letture
        reading_count = 0
        Num_of_readings = 10
        previous_time = datetime.now()
        print ("\n\nReading {}x".format(Num_of_readings))


        while reading_count < Num_of_readings:
            raw_data = None
            try:
                if dev.wait_new_data(2):
                    raw_data = dev.read_measurement_data()
                    dev.reset()
                    dev.set_brownout()
                    time.sleep(0.5)

                # print (raw_data)
            except Exception as e:
                dev.clear_error()
                print(e)
                pass

            if raw_data is not None:
                ta, to = dev.do_compensation(raw_data)
                now_time = datetime.now()
                delta_time = now_time - previous_time
                previous_time = now_time
                ## data -> GUI 
                app.addLabel(reading_count, text="TA = {:6.2f}  | TO = {:6.2f}  | Vdd = {:6.2f}  -- {}".format (ta, to, dev.read_vddmonitor(), str(delta_time)),colspan=1)
                if to>30:
                  app.setLabelBg(reading_count, "red")
                else:
                    app.setLabelBg(reading_count, "green")
                reading_count += 1

        dev.disconnect()
                      
####################################################################################
################################IMPOSTAZIONI GUI####################################        
####################################################################################        

app = gui("Temperature Alarm", "500x500") # gui(titolo, dimensione finestra)
app.addLabel("title", "Premi 'misura' per eseguire il controllo della temperatura") # .addLabel(testo, dimensione finestra)
# link bottone -> funczione chiamata alla pressione del bottone
app.addButtons(["Misura", "Esci"], ButtonPress)

app.go()