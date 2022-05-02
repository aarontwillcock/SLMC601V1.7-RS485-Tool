#Import files
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

#Sums
bytesReadCounter = 0
dataSum = 0

readState = "seekA8"
writeState = "none"
recvBytes = [0]

def parseBytes(numBytesToRead):

    global readState
    global writeState
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
                    readState = "seekFC";

        elif(readState == "seekFC"):
                #If read byte matches second byte of HST REQ frame...
                if(int.from_bytes(recvBytes[index],"little") == int("FC",16)):

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
                elif(int.from_bytes(recvBytes[index],"little") == int("04",16)):
                    readState = "readDCAS"
                else:
                    readState = "seekA8"
                    print("Bad Sequence")

        elif(readState == "readAAB"):
                SLMC_Frames.HST_REQ_AAB[3+bytesReadCounter] = int.from_bytes(recvBytes[index],"little")
                bytesReadCounter = bytesReadCounter + 1

                if(bytesReadCounter >= len(SLMC_Frames.HST_REQ_AAB)-3):
                    dataSum = sum(SLMC_Frames.HST_REQ_AAB)
                    if(dataSum & int("1111",2) == 0):
                        print(SLMC_Frames.HST_REQ_AAB)
                        readState = "completed"
                        writeState = "sendAAB"
                    else:
                        print("Bad CRC")
                        readState = "seekA8"

        elif(readState == "readVTCP"):
                SLMC_Frames.HST_REQ_VTCP[3+bytesReadCounter] = int.from_bytes(recvBytes[index],"little");
                bytesReadCounter = bytesReadCounter + 1

                if(bytesReadCounter >= len(SLMC_Frames.HST_REQ_VTCP)-3):
                    dataSum = sum(SLMC_Frames.HST_REQ_VTCP)
                    if(dataSum & int("1111",2) == 0):
                        print(SLMC_Frames.HST_REQ_VTCP)
                        readState = "completed"
                        writeState = "sendVTCP"
                    else:
                        print("Bad CRC")
                        readState = "seekA8"

        elif(readState == "readCBR"):
                SLMC_Frames.HST_REQ_CBR[3+bytesReadCounter] = int.from_bytes(recvBytes[index],"little")
                bytesReadCounter = bytesReadCounter + 1

                if(bytesReadCounter >= len(SLMC_Frames.HST_REQ_CBR)-3):
                    dataSum = sum(SLMC_Frames.HST_REQ_CBR)
                    if(dataSum & int("1111",2) == 0):
                        print(SLMC_Frames.HST_REQ_CBR)
                        readState = "completed"
                        writeState = "sendCBR"
                    else:
                        print("Bad CRC")
                        readState = "seekA8"

        elif(readState == "readDCAS"):
                SLMC_Frames.HST_REQ_DCAS[3+bytesReadCounter] = int.from_bytes(recvBytes[index],"little")
                bytesReadCounter = bytesReadCounter + 1

                if(bytesReadCounter >= len(SLMC_Frames.HST_REQ_DCAS)-3):
                    dataSum = sum(SLMC_Frames.HST_REQ_DCAS)
                    if(dataSum & int("1111",2) == 0):
                        print(SLMC_Frames.HST_REQ_DCAS)
                        readState = "completed"
                        writeState = "sendDCAS"
                    else:
                        print("Bad CRC")
                        readState = "seekA8"

#While command not completed or reset
while(readState != "End"):

    recvBytes[0] = usbrs485.read(1)

    parseBytes(1)

    #If message is read
    if(readState == "completed"):

        #Create byte array for reply
        if(writeState == "sendAAB"):
            fullFrameSum = sum(SLMC_Frames.BMS_RET_AAB)
            dataSum = fullFrameSum - SLMC_Frames.BMS_RET_AAB[-1]
            CRC = int("10000",2) - (dataSum & int("1111",2))
            SLMC_Frames.BMS_RET_AAB[-1] = CRC
            dataToSend = bytearray(SLMC_Frames.BMS_RET_AAB)
        if(writeState == "sendVTCP"):
            fullFrameSum = sum(SLMC_Frames.BMS_RET_VTCP)
            dataSum = fullFrameSum - SLMC_Frames.BMS_RET_VTCP[-1]
            CRC = int("10000",2) - (dataSum & int("1111",2))
            SLMC_Frames.BMS_RET_VTCP[-1] = CRC
            dataToSend = bytearray(SLMC_Frames.BMS_RET_VTCP)
        if(writeState == "sendCBR"):
            fullFrameSum = sum(SLMC_Frames.BMS_RET_CBR)
            dataSum = fullFrameSum - SLMC_Frames.BMS_RET_CBR[-1]
            CRC = int("10000",2) - (dataSum & int("1111",2))
            SLMC_Frames.BMS_RET_CBR[-1] = CRC
            dataToSend = bytearray(SLMC_Frames.BMS_RET_CBR)
        
        #Reply
        usbrs485.write(dataToSend)

        readState = "seekA8"
        writeState = "none"
        