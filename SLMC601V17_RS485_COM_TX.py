#Import files
import sys
import serial
import SLMC601V17_RS485_COM_Frames as SLMC_Frames
import SLMC601V17_RS485_BQ769XX_CONFIG_LABELS as SLMC_CFG_LABELS
from time import time

#Setup Labels
i_slmc_cfg_labels = SLMC_CFG_LABELS.SLMC601V17_RS485_BQ769XX_CONFIG_LABELS()

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
usbrs485.timeout = 0.1

#Get command requested
command = sys.argv[2]
try:
    int_command = int(command)
except:
    int_command = 0

#Handle command based on command
if(int_command):

    #Check for verbose command

    verbose_command = 0
    if len(sys.argv) > 3:
        if(sys.argv[3] == "-v"):
            verbose_command = 1

    #Create byte array
    if(int_command == 1):
        fullFrameSum = sum(SLMC_Frames.HST_REQ_DCAS)
        dataSum = fullFrameSum - SLMC_Frames.HST_REQ_DCAS[-1]
        CRC = int("10000",2) - (dataSum & int("1111",2))
        SLMC_Frames.HST_REQ_DCAS[-1] = CRC
        dataToSend = bytearray(SLMC_Frames.HST_REQ_AAB)
    if(int_command == 2):
        fullFrameSum = sum(SLMC_Frames.BMS_RET_VTCP)
        dataSum = fullFrameSum - SLMC_Frames.BMS_RET_VTCP[-1]
        CRC = int("10000",2) - (dataSum & int("1111",2))
        SLMC_Frames.BMS_RET_VTCP[-1] = CRC
        dataToSend = bytearray(SLMC_Frames.HST_REQ_VTCP)
    if(int_command == 3):
        fullFrameSum = sum(SLMC_Frames.BMS_RET_CBR)
        dataSum = fullFrameSum - SLMC_Frames.BMS_RET_CBR[-1]
        CRC = int("10000",2) - (dataSum & int("1111",2))
        SLMC_Frames.BMS_RET_CBR[-1] = CRC
        dataToSend = bytearray(SLMC_Frames.HST_REQ_CBR)

    #Write data
    usbrs485.write(dataToSend)

elif(int_command == 4 or command == "CHARGE" or command == "DISCHARGE"):

    if(int_command):

        #Get data argument for byte array
        DCAS_REQ_DATA_ARG = int(sys.argv[3])

    else:

        #Get text argument for on or off
        on_off_command = sys.argv[3]

        on_off_upper = on_off_command.upper()

        if on_off_upper == "ON":

            if command == "DISCHARGE":
                DCAS_REQ_DATA_ARG = 1   #Discharge on (circuit CLOSED)
            else:
                DCAS_REQ_DATA_ARG = 3   #Charge on (circuit CLOSED)
        
        if on_off_upper == "OFF":

            if command == "DISCHARGE":
                DCAS_REQ_DATA_ARG = 2   #Discharge off (circuit OPEN)
            else:
                DCAS_REQ_DATA_ARG = 4   #Charge on (circuit OPEN)

    #Change DCAS Data List
    SLMC_Frames.HST_REQ_DCAS[4] = int(DCAS_REQ_DATA_ARG)

    fullFrameSum = sum(SLMC_Frames.HST_REQ_DCAS)
    dataSum = fullFrameSum - SLMC_Frames.HST_REQ_DCAS[-1]
    CRC = int("100000000",2) - (dataSum & int("11111111",2))
    SLMC_Frames.HST_REQ_DCAS[-1] = CRC

    #Create byte array
    dataToSend = bytearray(SLMC_Frames.HST_REQ_DCAS)

    #Write data
    usbrs485.write(dataToSend)

else:
    print("Invalid Command")
    exit()

#Sums
bytesReadCounter = 0
dataSum = 0

readState = "seekA8"
recvBytes = [0]

def printConfigModule(module,moduleLabels):

    labelOutput = ""
    valueOutput = ""

    for i in range(len(moduleLabels)):
        labelOutput += "[" + moduleLabels[i] + "]"
        labelLength = len(moduleLabels[i])
        if module & pow(2,(7-i)) :
            valueOutput += "[" + "\u2588"*labelLength + "]"
        else:
            valueOutput += "[" + " "*labelLength + "]"

    print("BIT7",end="")
    print(labelOutput,end="")
    print("BIT0")
    print("BIT7",end="")
    print(valueOutput,end="")
    print("BIT0")
    print("")

def printFrameWithDescription(BMS_RET_FRAME):

    if BMS_RET_FRAME == SLMC_Frames.BMS_RET_AAB:

        bq76xx_amplitude = (SLMC_Frames.BMS_RET_AAB[4]<<8) + SLMC_Frames.BMS_RET_AAB[5]
        print("BQ76XX Amplitude:",bq76xx_amplitude)

        bq76xx_bias = SLMC_Frames.BMS_RET_AAB[6]
        print("BQ76xx Bias (ADC Offset):",bq76xx_bias)
    
    if BMS_RET_FRAME == SLMC_Frames.BMS_RET_VTCP:

        cellString = [0]*15

        cellString[0] =  (SLMC_Frames.BMS_RET_VTCP[4]<<8) + SLMC_Frames.BMS_RET_VTCP[5]
        cellString[1] =  (SLMC_Frames.BMS_RET_VTCP[6]<<8) + SLMC_Frames.BMS_RET_VTCP[7]
        cellString[2] =  (SLMC_Frames.BMS_RET_VTCP[8]<<8) + SLMC_Frames.BMS_RET_VTCP[9]
        cellString[3] =  (SLMC_Frames.BMS_RET_VTCP[10]<<8) + SLMC_Frames.BMS_RET_VTCP[11]
        cellString[4] =  (SLMC_Frames.BMS_RET_VTCP[12]<<8) + SLMC_Frames.BMS_RET_VTCP[13]
        cellString[5] =  (SLMC_Frames.BMS_RET_VTCP[14]<<8) + SLMC_Frames.BMS_RET_VTCP[15]
        cellString[6] =  (SLMC_Frames.BMS_RET_VTCP[16]<<8) + SLMC_Frames.BMS_RET_VTCP[17]
        cellString[7] =  (SLMC_Frames.BMS_RET_VTCP[18]<<8) + SLMC_Frames.BMS_RET_VTCP[19]
        cellString[8] =  (SLMC_Frames.BMS_RET_VTCP[20]<<8) + SLMC_Frames.BMS_RET_VTCP[21]
        cellString[9] =  (SLMC_Frames.BMS_RET_VTCP[22]<<8) + SLMC_Frames.BMS_RET_VTCP[23]
        cellString[10] = (SLMC_Frames.BMS_RET_VTCP[24]<<8) + SLMC_Frames.BMS_RET_VTCP[25]
        cellString[11] = (SLMC_Frames.BMS_RET_VTCP[26]<<8) + SLMC_Frames.BMS_RET_VTCP[27]
        cellString[12] = (SLMC_Frames.BMS_RET_VTCP[28]<<8) + SLMC_Frames.BMS_RET_VTCP[29]
        cellString[13] = (SLMC_Frames.BMS_RET_VTCP[30]<<8) + SLMC_Frames.BMS_RET_VTCP[31]
        cellString[14] = (SLMC_Frames.BMS_RET_VTCP[32]<<8) + SLMC_Frames.BMS_RET_VTCP[33]

        for i in range(len(cellString)):
            output = "String "+str(i).zfill(2)+" : "+format(cellString[i]*0.001,'.3f')+"V"
            if i % 2 == 0:
                print(output,"  ",end="")
            else:
                print(output)

        print("")
        battery_voltage = (SLMC_Frames.BMS_RET_VTCP[34]<<8) + SLMC_Frames.BMS_RET_VTCP[35]
        output = "==> V Batt : " + format(battery_voltage*0.001,'.3f') + "V"
        print(output)

        temps = [-1]*3

        temps[0] = (SLMC_Frames.BMS_RET_VTCP[36]<<8) + SLMC_Frames.BMS_RET_VTCP[37]
        temps[1] = (SLMC_Frames.BMS_RET_VTCP[38]<<8) + SLMC_Frames.BMS_RET_VTCP[39]
        temps[2] = (SLMC_Frames.BMS_RET_VTCP[40]<<8) + SLMC_Frames.BMS_RET_VTCP[41]

        for i in range(len(temps)):
            output = "Temp "+str(i).zfill(2)+" : "+format(temps[i]*0.1,'.1f')+" deg C"
            print(output)

        battery_current = (SLMC_Frames.BMS_RET_VTCP[42]<<8) + SLMC_Frames.BMS_RET_VTCP[43]
        output = "I Batt : " + format(battery_current*0.01,'.2f') + "A"
        print(output)

        system_state_of_charge = (SLMC_Frames.BMS_RET_VTCP[44]<<8) + SLMC_Frames.BMS_RET_VTCP[45]
        output = "SOC : " + format(system_state_of_charge*0.1,'.1f') + "%"
        print(output)

    if BMS_RET_FRAME == SLMC_Frames.BMS_RET_CBR:

        bq76xx_system_status = SLMC_Frames.BMS_RET_CBR[4]
        bq76xx_cell_balance = [-1]*3
        for i in range(len(bq76xx_cell_balance)):
            bq76xx_cell_balance[i] = SLMC_Frames.BMS_RET_CBR[5+i]
        bq76xx_system_control = [-1]*2
        for i in range(len(bq76xx_system_control)):
            bq76xx_system_control[i] = SLMC_Frames.BMS_RET_CBR[8+i]
        bq76xx_protection = [-1]*3
        for i in range(len(bq76xx_protection)):
            bq76xx_protection[i] = SLMC_Frames.BMS_RET_CBR[10+i]
        bq76xx_over_voltage_trip = SLMC_Frames.BMS_RET_CBR[13]
        bq76xx_under_voltage_trip = SLMC_Frames.BMS_RET_CBR[14]
        bq76xx_configuration = SLMC_Frames.BMS_RET_CBR[15]
        
        print("System Status:")
        printConfigModule(bq76xx_system_status,i_slmc_cfg_labels.bq769xx_labels_systemStatus)
        print("Cell Balance 1:")
        printConfigModule(bq76xx_cell_balance[0],i_slmc_cfg_labels.bq769xx_labels_cellBalance1)
        print("Cell Balance 2:")
        printConfigModule(bq76xx_cell_balance[1],i_slmc_cfg_labels.bq769xx_labels_cellBalance2)
        print("Cell Balance 3:")
        printConfigModule(bq76xx_cell_balance[2],i_slmc_cfg_labels.bq769xx_labels_cellBalance3)
        print("System Control 1:")
        printConfigModule(bq76xx_system_control[0],i_slmc_cfg_labels.bq769xx_labels_systemControl1)
        print("System Control 2:")
        printConfigModule(bq76xx_system_control[1],i_slmc_cfg_labels.bq769xx_labels_systemControl2)
        print("Protect 1:")
        printConfigModule(bq76xx_protection[0],i_slmc_cfg_labels.bq769xx_labels_protect1)
        print("Protect 2:")
        printConfigModule(bq76xx_protection[1],i_slmc_cfg_labels.bq769xx_labels_protect2)
        print("Protect 3:")
        printConfigModule(bq76xx_protection[2],i_slmc_cfg_labels.bq769xx_labels_protect3)
        print("OV Trip:")
        printConfigModule(bq76xx_over_voltage_trip,i_slmc_cfg_labels.bq769xx_labels_OV_TRIP)
        print("UV Trip:")
        printConfigModule(bq76xx_under_voltage_trip,i_slmc_cfg_labels.bq769xx_labels_UV_TRIP)
        print("CcConfig:")
        printConfigModule(bq76xx_configuration,i_slmc_cfg_labels.bq769xx_labels_ccConfig)

def parseBytes(numBytesToRead):

    global readState
    global bytesReadCounter
    global recvBytes

    #Create index
    index = 0

    #For each byte in buffer...
    for index in range(numBytesToRead):
        if(readState == "seekA8"):

                #Reset number of bytes read
                bytesReadCounter = 0

                #If read byte matches first byte of HST REQ frame...
                if(int.from_bytes(recvBytes[index],"little") == int("A8",16)):

                    #Advance valid request state machine
                    readState = "seek11";

        elif(readState == "seek11"):
                #If read byte matches second byte of HST REQ frame...
                if(int.from_bytes(recvBytes[index],"little") == int("11",16)):

                    #Advance valid request state machine
                    readState = "seekCmd";
                else:
                    readState = "badSequence";
            
        elif(readState == "seekCmd"):
                #If read byte is a valid reqest...
                if(int.from_bytes(recvBytes[index],"little") == int("01",16)):
                    readState = "readAAB"
                elif(int.from_bytes(recvBytes[index],"little") == int("02",16)):
                    readState = "readVTCP"
                elif(int.from_bytes(recvBytes[index],"little") == int("03",16)):
                    readState = "readCBR"
                else:
                    readState = "seekA8"
                    print("Bad Sequence")

        elif(readState == "readAAB"):
                SLMC_Frames.BMS_RET_AAB[3+bytesReadCounter] = int.from_bytes(recvBytes[index],"little")
                bytesReadCounter = bytesReadCounter + 1

                if(bytesReadCounter >= len(SLMC_Frames.BMS_RET_AAB)-3):
                    dataSum = sum(SLMC_Frames.BMS_RET_AAB)
                    if(dataSum & int("11111111",2) == 0):
                        print(SLMC_Frames.BMS_RET_AAB)
                        if verbose_command:
                            printFrameWithDescription(SLMC_Frames.BMS_RET_AAB)
                    else:
                        print("Bad CRC")
                    readState = "End"

        elif(readState == "readVTCP"):
                SLMC_Frames.BMS_RET_VTCP[3+bytesReadCounter] = int.from_bytes(recvBytes[index],"little");
                bytesReadCounter = bytesReadCounter + 1

                if(bytesReadCounter >= len(SLMC_Frames.BMS_RET_VTCP)-3):
                    dataSum = sum(SLMC_Frames.BMS_RET_VTCP)
                    if(dataSum & int("11111111",2) == 0):
                        print(SLMC_Frames.BMS_RET_VTCP)
                        if verbose_command:
                            printFrameWithDescription(SLMC_Frames.BMS_RET_VTCP)
                    else:
                        print("Bad CRC")
                    readState = "End"

        elif(readState == "readCBR"):
                SLMC_Frames.BMS_RET_CBR[3+bytesReadCounter] = int.from_bytes(recvBytes[index],"little")
                bytesReadCounter = bytesReadCounter + 1

                if(bytesReadCounter >= len(SLMC_Frames.BMS_RET_CBR)-3):
                    dataSum = sum(SLMC_Frames.BMS_RET_CBR)
                    if(dataSum & int("11111111",2) == 0):
                        if verbose_command:
                            printFrameWithDescription(SLMC_Frames.BMS_RET_CBR)
                    else:
                        print("Bad CRC")
                    readState = "End"

#While command not completed and not timed out
start = int(time()*1000)
exeTime = 0

while(readState != "End" and exeTime < 100):

    recvBytes[0] = usbrs485.read(1)

    parseBytes(1)

    exeTime = int(time()*1000) - start