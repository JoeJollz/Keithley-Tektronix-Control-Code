# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 12:52:53 2025

@author: jrjol
"""

import pyvisa
import time
import matplotlib.pyplot as plt

# Initialize VISA resource manager
rm = pyvisa.ResourceManager()
keithley = rm.open_resource("USB0::0x05E6::0x2470::04639665::INSTR")  # Replace with actual USB address

volt_logger = []
current_logger = []

# Reset and configure Keithley 2470
keithley.write("*RST")  # Reset instrument
keithley.write(":SOUR:FUNC VOLT")  # Set source function to voltage
keithley.write(":SOUR:VOLT:RANG 1")  # Set voltage range to ±1V
keithley.write(":SENS:CURR:PROT 0.1")  # Set current compliance limit (adjust as needed)
keithley.write(":OUTP ON")  # Enable output

# Define voltage sweep parameters
start_voltage = -1.0
end_voltage = 1.0
step_size = 0.1

# Helper function to generate floating-point ranges
def frange(start, stop, step):
    values = []
    while start <= stop:
        values.append(round(start, 3))  # Ensures proper rounding for floating points
        start += step
    return values

# Perform sweep
print("Starting voltage sweep...")

voltages = frange(start_voltage, end_voltage, step_size)  # Generate sweep values

for v in voltages:
    keithley.write(f":SOUR:VOLT {v}")  # Set voltage
    volt_logger.append(v)
    time.sleep(0.5)  # Wait for stabilization
    keithley.write(":READ?")  # Measure current
    current = keithley.read()
    current_logger.append(current)

    print(f"Voltage: {v}V | Measured Current: {current}A")

# Turn off output
keithley.write(":OUTP OFF")
keithley.close()

print("Voltage sweep completed.")

plt.plot(volt_logger, current_logger)
plt.xlabel('Voltage (V)')
plt.ylabel('Current (A)')
plt.title('CV Sweep')
plt.show()
