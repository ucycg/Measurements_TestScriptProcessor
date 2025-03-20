import pyvisa
import time
import csv

address = "TCPIP0::192.0.0.1::inst0::INSTR" #Keithley 2450 SMU IPv4

# Connect to the Keithley 2470 over TCP/IP
rm = pyvisa.ResourceManager()
inst = rm.open_resource(address)    #Keithley 2470 SMU

# Set the output to be voltage control mode
inst.write("reset()")  # Reset the inst to a known state
inst.write('SYST:PRESet')  # Perform preset settings

# Set the Keithley 2470 to Source Voltage, Measure Current mode
inst.write('FUNC "VSET"')  # Set the function to Voltage source
inst.write('SENS:FUNC "I"')  # Set the measurement to Current
inst.write('VSET:PROT 200')  # Set voltage protection (optional, 200V max)

# Set the voltage range to 200V
inst.write('VSET:RANG 200')  

# Set the current range for measurement (adjust as needed)
inst.write('SENS:CURR:RANG 1E-5')  # Set the current range (10 µA)

# Loop through voltage steps from 0V to -50V in steps of -10V
voltages = range(0, -51, -10)  # Voltage steps from 0V to -50V
for voltage in voltages:
    # Set the voltage
    inst.write(f'VSET {voltage}')
    
    # Wait for the inst to settle
    time.sleep(1)

    # Measure the current
    current = inst.query('MEAS:?')
    
    # Print the results
    print(f"Voltage: {voltage} V, Current: {current} A")

# Reset the inst to its default state at the end
inst.write('VSET 0')  # Reset voltage to 0
inst.write('OUTP OFF')  # Turn off output

print("Measurement complete.")