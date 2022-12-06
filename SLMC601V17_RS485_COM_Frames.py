#Global Arrays
#  Amplitude and Bias Frame
#      HOST SEND
HST_REQ_AAB = [             int("0xA8",16),   #Start byte
                            int("0xFC",16),   #Device Address
                            int("0x01",16),   #Function Code
                            int("0x01",16),   #Data Length
                            int("0x00",16),   #Data
                            int("0x5A",16)    #CRC
]

BMS_RET_AAB =   [
                            int("A8",16),  #Start byte
                            int("11",16),  #Device Address
                            int("01",16),  #Function Code
                            int("03",16),  #Data Length
                            int("00",16),  #BQ76xx Amplitude Value (0x00-0x1F) Gain multiples of current detection, detailed on page 40 of bq769xx manual - High byte first (MSB)
                            int("00",16),  #BQ76xx Amplitude Value (0x00-0x1F) Gain multiples of current detection, detailed on page 40 of bq769xx manual - High byte first (MSB)
                            int("00",16),  #BQ76xx Bias Value (0x00-0x1F) Gain multiples of current detection, detailed on page 41 of bq769xx manual
                            int("00",16)   #CRC
                        ]
#  Voltage Temperature, Current, Power
#      HOST SEND
HST_REQ_VTCP =  [
                            int("A8",16),  #Start byte
                            int("FC",16),  #Device Address
                            int("02",16),  #Function Code
                            int("01",16),  #Data Length
                            int("00",16),  #Data
                            int("59",16)    #CRC
                        ]
#      BMS RETURN
BMS_RET_VTCP = [
                            int("A8",16),  #Start byte
                            int("11",16),  #Device Address
                            int("02",16),  #Function Code
                            int("28",16),  #Data Length
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16)    #CRC
                        ]
#  Chip Balancer
#      HOST SEND
HST_REQ_CBR =   [
                            int("A8",16),  #Start byte
                            int("FC",16),  #Device Address
                            int("03",16),  #Function Code
                            int("01",16),  #Data Length
                            int("00",16),  #Data
                            int("58",16)    #CRC
                        ]
#      BMS RETURN
BMS_RET_CBR =  [
                            int("A8",16),  #Start byte
                            int("11",16),  #Device Address
                            int("03",16),  #Function Code
                            int("0B",16),  #Data Length (0x0B =   )
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16),
                            int("00",16)    #CRC
                        ]
#  Discharge, Charge, Alert, Sleep
HST_REQ_DCAS =  [
                            int("A8",16),  #Start byte
                            int("FC",16),  #Device Address
                            int("04",16),  #Function Code
                            int("01",16),  #Data Length
                            int("00",16),  #Data
                            int("00",16)    #CRC
                        ]