from mlx90632.mlx90632 import Mlx90632           # def __init__ è lo standard per python per poter importare la classe 
                                                 # from directory.dir import Dir                                                 
                                                 # per ogni livello dell'albero delle directory devi aggiungere un import path 

# dev = Mlx90632('mlx://evb:90632/1')            # stabilisce che tipo di device si sta usando e la comunicazione tra sensore e pc
dev = Mlx90632('I2C-1')                          # stabilisce che il dev è collegato via I2C, la libreria che utilizzeremo 
dev.init()                                       # legge la EEPROM ed effettua la calibrazione iniziale dei parametri.
dev.wait_new_data()                              # aspetta fintantochè c'è un dato disponibile 
raw_data = dev.read_measurement_data()           # legge la nuova misura grezza 
ta, to = dev.do_compensation(raw_data)           # elabora la misura grezza appena letta sulla base della calibrazione iniziale  
print ("TA: {} -- TO: {} DegC".format (ta, to))  # temperatura ambiente TA, temperatura dell'oggetto puntato TO
