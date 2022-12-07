# SLMC601 V1.7 Python USB-RS485 Interface

## General Command Structure

### Integer-Based Commands
```
python3 SLMC601V17_RS485_COM_TX /dev/ttyUSB# X Y -v
```
`#` = The desired RS485-USB device's # - found by calling `ls /dev/etc/ttyUSB*`
`X` = SLMC command number:
```
1 - Amplitude and Bias (AAB)
2 - Voltage, Temperature, Current, and Percent State of Charge (VTCP)
3 - Cell Balance and Registers (CBR)
4 - Discharge, Charge, Alarm, and SLeep (DCAS)
``` 
`Y` = SLMC DCAS Sub-Command should __ONLY__ be used when `X = 4` :
```
1 - Discharge Closed (ON)
2 - Discharge Open (OFF)
3 - Charge Closed (ON)
4 - Charge Open (ON)
5 - Clear BQ769 chip alarm
6 - Enter BQ769 sleep state
```
`-v` = Verbose output of received data (i.e. formatted, textual output)
### Optional Text-Based Commands

This interface allows text-based DCAS commands as follows:
```
python3 SLMC601V17_RS485_COM_TX /dev/ttyUSB# X Y
```
`X` = SLMC text command:
```
CHARGE - DCAS Charge Command
DISCHARGE - DCAS Discharge Command
``` 
requires the following `Y` command.

`Y` = SLMC command number:
```
ON - Closes (enables) the circuit
OFF - Opens (disables) the circuit
```

Examples:
```
python3 SLMC601V17_RS485_COM_TX /dev/ttyUSB2 CHARGE ON
```
uses `/dev/ttyUSB2` to turn `ON` the `CHARGE` circuit and enable battery charging.

```
python3 SLMC601V17_RS485_COM_TX /dev/ttyUSB5 DISCHARGE OFF
```
uses `/dev/ttyUSB5` to turn `OFF` the `DISCHARGE` circuit and prevent battery discharge.


## Amplitude and Bias (AAB)
To request Amplitude and Bias Frame:
```cli
python3 SLMC601V17_RS485_COM_TX /dev/ttyUSB# 1
```
where `#` is the ID of the RS485 USB device.

### Return:
Start Bit | Device Address | Function Code | Data Length (Bytes) | BQ769XX Amplitude Value | BQ769XX Gain Value | CRC |
|---|---|---|---|---|---|---|
0xA8 | 0x11 | 0x01 | 0x03 | 0x00-0x1F | 0x00-0x1F | ~(SUM(B0-B7) & 0x1111)+1 |

Example:
```cli
[168, 17, 1, 3, 0, 0, 0, 3]
```

## Voltage, Temperature, Current, and Percent SOC (VTCP)
To request Voltage, Temperature, Current, and Percent SOC:
```cli
python3 SLMC601V17_RS485_COM_TX /dev/ttyUSB# 2
```
where `#` is the ID of the RS485 USB device.

### Return:
Start Bit | Device Address | Function Code | Data Length (Bytes) | Cell 1 V | Cell 2 V | ... | Cell 15 V | Batt V | Temp 1 | Temp 2 | Temp 3 | Batt Current (A) | SOC | CRC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
0xA8 | 0x11 | 0x02 | 0x28 | 0x0000-0xFFFF | 0x0000-0xFFFF | ... | 0x0000-0xFFFF | 0x0000-0xFFFF | 0x0000-0xFFFF | 0x0000-0xFFFF | 0x0000-0xFFFF | -32768-32767 | 0-1000 | ~(SUM(B0-B46) & 0x1111)+1 |

Example:
```cli
[168, 17, 2, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13]
```

## Cell Balancing Registers
To request cell balance registers:
```cli
python3 SLMC601V17_RS485_COM_TX /dev/ttyUSB# 3
```
where `#` is the ID of the RS485 USB device.

### Return:
Start Bit | Device Address | Function Code | Data Length (Bytes) | Chip Status Register | Chip Balance Register 1 | Chip Balance Register 2 | Chip Balance Register 3 | Control Register 1 | Control Register 2 | Chip Protection Register 1 | Chip Protection Register 2 | Chip Protection Register 3 | Chip Setting Register Over Voltage | Chip Setting Register Under Voltage | Chip Configuration Register | CRC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
0xA8 | 0x11 | 0x03 | 0x0B | 0x00-0xFF | 0x00-0xFF | 0x00-0xFF | 0x00-0xFF | 0x00-0xFF | 0x00-0xFF | 0x00-0xFF | 0x00-0xFF | 0x00-0xFF | 0x00-0xFF | 0x00-0xFF | 0x00-0xFF | ~(SUM(B0-B46) & 0x1111)+1 |

Example:
```cli
[168, 17, 3, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9]
```

## Discharge, Charge, Alarm, and Sleep (DCAS)
To set discharge state, charge state, clear alarms, or enter sleep:
```cli
python3 SLMC601V17_RS485_COM_TX /dev/ttyUSB# 4 X
```
where `#` is the ID of the RS485 USB device and `X` indicates a command from the table below

| `X` | Command |
|-----|---------|
| 1 | Discharge Closed (ON) |
| 2 | Discharge Open (OFF) |
| 3 | Charge Closed (ON) |
| 4 | Charge Open (ON) |
| 5 | Clear BQ769 chip alarm |
| 6 | Enter BQ769 sleep state |

Note: "Discharging" state enables undervoltage protection, "charging" state enables overvoltage protection

### Return:

None. This function does not return any data.


