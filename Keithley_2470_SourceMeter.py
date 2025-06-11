# -*- coding: utf-8 -*-
'''
To find your Keithley Visa Resource String (using pyvisa) run the following code:

import pyvisa

rm = pyvisa.ResourceManager()
instruments = rm.list_resources()
print(instruments)
    
'''


"""
Created on Wed Jun 11 12:52:53 2025

@author: jrjol
"""

import pyvisa
import time
import matplotlib.pyplot as plt
import numpy as np

# Initialize VISA resource manager
rm = pyvisa.ResourceManager()
keithley = rm.open_resource("USB0::0x05E6::0x2470::04639665::INSTR")


CurrentCompliance = 0.1    # compliance (max) current (A)
start = -20.0
stop = +20.0
numpoints = 50


volt_logger = []
current_logger = []

# Reset and configure Keithley 2470
keithley.write("*RST")  # Reset instrument
time.sleep(0.5) #rest

keithley.write(":SOUR:FUNC:MODE VOLT")
keithley.write(":SENS:CURR:PROT:LEV " + str(CurrentCompliance))
keithley.write(":SENS:CURR:RANGE:AUTO 1")   # set current reading range to auto (boolean)
keithley.write(":OUTP ON")                    # Output on    
# keithley.write(":SOUR:FUNC VOLT")  # Set source function to voltage
# keithley.write(":SOUR:VOLT:RANG 25")  # Set voltage range to ±1V
# keithley.write(":SENS:CURR:PROT 0.1")  # Set current compliance limit (adjust as needed) 100mA to protect the device
# keithley.write(":OUTP ON")  # Enable output

# Define voltage sweep parameters
# start_voltage = -20.0
# end_voltage = 20.0
# step_size = 1

# # Helper function to generate floating-point ranges
# def frange(start, stop, step):
#     values = []
#     while start <= stop:
#         values.append(round(start, 3))  # Ensures proper rounding for floating points
#         start += step
#     return values

# # Perform sweep
# print("Starting voltage sweep...")

# voltages = frange(start_voltage, end_voltage, step_size)  # Generate sweep values

# for v in voltages:
#     keithley.write(f":SOUR:VOLT {v}")  # Set voltage
#     volt_logger.append(v)
#     time.sleep(0.5)  # Wait for stabilization
#     print(keithley.write(":READ?"))  # Measure current
#     current = keithley.read()
#     # current_logger.append(current)
    
#     response = keithley.query(":READ?")  # Query returns a response immediately
#     # The response is typically: "VOLTAGE,CURRENT,RESISTANCE,..."
#     values = response.strip().split(',')
    
#     # Extract measured voltage and current
#     measured_voltage = float(values[0])
#     measured_current = float(values[1])
    
#     volt_logger.append(measured_voltage)
#     current_logger.append(measured_current)

#     print(f"Voltage: {measured_voltage}V | Measured Current: {measured_current}A")

for V in np.linspace(start, stop, num = numpoints, endpoint = True):
    print("Voltage: " + str(V) + "V")
    keithley.write(":SOUR:VOLT " + str(V))
    time.sleep(0.1)
    data = keithley.ask(":READ?")
    data_answer = data.split(',')
    I = eval(data_answer.pop(1)) *1e3  # what unit is the pop, and what unit it the final?
    current_logger.append(I)
    
    v_read = eval(data_answer.pop(0))
    volt_logger.append(v_read)
    
    print("Current: "+ str(current_logger[-1]) + 'mA')
    print("-------------------------------------------------")
    

keithley.write(":OUTP OFF")  # turn off

keithley.write(":SOUR:FUNC:MODE curr")
keithley.write(":SOUR:CURR " + str(CurrentCompliance))
keithley.write(":SENS:volt:PROT:LEV " + str(max(volt_logger))  )
keithley.write(":SENS:volt:RANGE:AUTO 1")

keithley.write("SYSTEM:KEY 23") # go to local control
keithley.close()


# Turn off output
keithley.write(":OUTP OFF")
keithley.close()

print("Voltage sweep completed.")

plt.plot(volt_logger, current_logger)
plt.xlabel('Voltage (V)')
plt.ylabel('Current (A)')
plt.title('CV Sweep')
plt.show()


'''
TO DO:
-20V 20V. Step size = 1V.
Sweep type. Linear Dual.  


'''