from mlx90632.mlx90632 import Mlx90632 
from datetime import datetime
from sys import platform
import atexit
from mlx90632.MemFile import MemFile            

dev = Mlx90632("I2C-1")                         
dev.init()
dev.wait_new_data()
chip_id = dev.read_chipid()
chip_id_str = dev.chipid_str

##########################################LETTURA DATI MEMORIA PER CONTROLLO COERENZA LETTURA ############################################
##########################################################################################################################################
# print ('\n\nreading eeprom memory dump, and compare with actual content...')
# h = MemFile(dev.chipid_str + '.hex')
# # h = MemFile(dev.chipid_str + '.bin')
# print ("")
# print ("addr: data")
# print ("----  ----")
# word_data = dev.i2c_read(0x2400, 256, 'H')
# changed = False
# for p in h.get_address_data_pairs():
#     data = word_data.pop(0)
#     print ("{:04X}: {:04X} -- {:04X} -- {}".format (p[0], p[1], data, data==p[1]))
#     if data != p[1]:
#         changed = True
# if changed:
#     print ("data differs!")
# else:
#     print ("data matches!")
# 
# print ('accuracy_range: {}'.format(dev.read_ee_pc_accuracy_range()))
# 
# reading_count = 0
# previous_time = datetime.now()
# dev.reset()

##############################################################################################################################
########################################## N-LETTURE SUCCESSIVE ##############################################################
##############################################################################################################################
# numero di letture
reading_count = 0
Num_of_readings = 20
previous_time = datetime.now()
print ("\n\nReading {}x".format(Num_of_readings))


while reading_count < Num_of_readings:
    raw_data = None
    try:
        if dev.wait_new_data(2):
            raw_data = dev.read_measurement_data()
            dev.reset()
            dev.set_brownout()

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

        print("TA = {:6.2f}  | TO = {:6.2f}  | VddMon = {:6.2f}  -- {}".format (ta, to, dev.read_vddmonitor(), str(delta_time)))
    
        reading_count += 1

dev.disconnect()
