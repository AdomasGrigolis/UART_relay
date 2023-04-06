# Relays and logs payloads
# Between two Serial (UART) Ports
# Adomas Grigolis
import serial
import serial.tools.list_ports
import pythoncom
from datetime import date

def listPorts():
    ports = serial.tools.list_ports.comports()
    portList = []
    for port in ports:
        portList.append(port.name)
    if len(portList) < 1: 
        portList.append('Empty')
    return portList

# Global Data Variables
buffer1 = []
buffer2 = []
go = False

# List Ports
print("Ports: ", listPorts())
# User Inputs (Port Select)
port_1 = input("Port 1: ")
port_2 = input("Port 2: ")

ser1 = serial.Serial()
ser2 = serial.Serial()

def readFunc():
    global buffer1
    global buffer2
    pythoncom.CoInitialize()
    if ser1.is_open and ser1.inWaiting() > 0:
        buffer1.append(str(ser1.read_all().hex(sep=' ', bytes_per_sep=1)).upper())
        storeFunc(buffer1, 1)
        relay(buffer2, 1)
        buffer1=[]
    if ser2.is_open and ser2.inWaiting() > 0:
        buffer2.append(str(ser2.read_all().hex(sep=' ', bytes_per_sep=1)).upper())
        storeFunc(buffer2, 2)
        relay(buffer2, 2)
        buffer2=[]

def storeFunc(buff, sel):
    with open(str("logs/"+str(date.today())+"."+str(sel)+"."+"log.txt"), 'a+') as log_file:
        for line in buff:
            log_file.write(line)
            log_file.write('\n')

def relay(buff, sel):
    if sel == 1:
        for line in buff:
            ser2.write(bytes.fromhex(line))
    else:
        for line in buff:
            ser1.write(bytes.fromhex(line))

# Serial Setup
ser1.baudrate = 115200
ser1.stopbit = serial.STOPBITS_ONE
ser1.parity = serial.PARITY_NONE
ser1.bytesize = serial.EIGHTBITS
ser1.timeout = None
ser1.port = port_1
ser2.baudrate = 115200
ser2.stopbit = serial.STOPBITS_ONE
ser2.parity = serial.PARITY_NONE
ser2.bytesize = serial.EIGHTBITS
ser2.timeout = None
ser2.port = port_2

# Opens ports
try:
    ser1.open()
    ser2.open()
    go = True
except Exception as e:
    print("Failed to open ports: ", e)

while go:
    readFunc()