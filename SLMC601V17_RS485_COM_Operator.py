import sys
import serial
import SLMC601V17_RS485_COM_Frames as SLMC_Frames


#Determine determine which port was provided
PORT = sys.argv[1]

#Check that port provided...
#   contains ttyUSB
sizeOfPort = len(PORT)
sizeOfTTY = len("ttyUSB#")
subString = PORT[sizeOfPort-sizeOfTTY:sizeOfPort-1]
if(subString != "ttyUSB"):
    print("Error: Port is not expected USB-RS485")
#   is accessible
usbrs485 = serial.Serial(PORT,baudrate=115200)

#Get command requested
command = int(sys.argv[2])

#Handle command based on command
if(command == 1 or command == 2 or command == 3):

    #Create byte array
    if(command == 1):
        dataToSend = bytearray(SLMC_Frames.HST_REQ_AAB)
    if(command == 2):
        dataToSend = bytearray(SLMC_Frames.HST_REQ_VTCP)
    if(command == 3):
        dataToSend = bytearray(SLMC_Frames.HST_REQ_CBR)

    #Write data
    usbrs485.write(dataToSend)

    #Close
    usbrs485.close()

if(command == 4):

    #Get data argument for byte array
    DCAS_REQ_DATA_ARG = int(sys.argv[3])

    #Change DCAS Data List
    SLMC_Frames.HST_REQ_DCAS[4] = DCAS_REQ_DATA_ARG

    #Compute CRC (57 is default CRC when DATA byte = 0)
    DCAS_REQ_CRC_BYTE = 57 + DCAS_REQ_DATA_ARG

    #Set CRC
    SLMC_Frames.HST_REQ_DCAS[5] = DCAS_REQ_CRC_BYTE

    #Create byte array
    dataToSend = bytearray(SLMC_Frames.HST_REQ_DCAS)

    #Write data
    usbrs485.write(dataToSend)

    #Close
    usbrs485.close()