
# This script uses Keithely Test Scripting Processing (TSP)Language

# In particular this script measures I for set U with a Keithlery SMU 2470   
import pyvisa
import time
import csv
import numpy

csv_list = []

rm = pyvisa.ResourceManager()

#ANNOYING IPv4 changes every day!
address = "TCPIP0::141.52.65.151::inst0::INSTR" #Keithley 2470 SMU

inst = rm.open_resource(address,open_timeout=10000)
inst.write("reset()")

vstart = 0
vstep = -10
vstop = -(210 + 1)  # range() function is exclusive of stop value!
currlimit = 1E-5

inst.write("smu.source.func = smu.FUNC_DC_VOLTAGE")
inst.write("smu.source.ilimit.level = " + str(currlimit))
#inst.write("smu.source.autorange = smu.ON")
inst.write(f"smu.source.range = {vstop}")
#inst.write("smu.source.autodelay = smu.ON")
#inst.write("smu.source.delay = 2")
inst.write("smu.measure.func = smu.FUNC_DC_CURRENT")
#inst.write("smu.measure.autorange = smu.ON")
inst.write(f"smu.measure.range = {currlimit}")
inst.write("smu.measure.nplc = 10")
inst.write("smu.source.output = smu.ON")

inst.write("testData = buffer.make(100)")
#print(inst.query("print(testData.n)"))

voltlist = list(range(vstart, vstop, vstep)) # list of currents to source
print(voltlist)
currlist = [None for volt in voltlist] # Create an empty array for current measurements the same size as our source list
for i, voltage in enumerate(voltlist): # Loop over the current source list
    inst.write("smu.source.level = " + str(voltage))
    print(f"Voltage: {voltlist[i]}")
    #inst.write("smu.source.output = smu.ON")
    time.sleep(2)
    inst.write("smu.measure.read(testData)")
    #inst.write("smu.source.output = smu.OFF")
    inst.write("waitcomplete()")
    #print(inst.query("print(testData.n)"))
    currlist[i] = inst.query("print(testData.readings[testData.endindex])") #Grab the last reading
    currlist[i] = float(currlist[i]) # .query returns a string, so it must be casted to a number
    print(f"Current: {currlist[i]}")
    csv_list.append([voltlist[i],currlist[i]])
    
print(currlist)
#print(inst.query("print(testData.readings)"))

# Element-wise multiplication gives resistance R U/I
result = [ volt / curr for curr, volt in zip(currlist, voltlist)]

print(result)

# Print U/I to csv file
if True:

    # Output CSV filename
    filename = input("Input the Filename: ")

    #Convert list to numpy array
    csv_array = numpy.array(csv_list)
    
    # Write np array to csv
    header = "Voltage,Current"
    numpy.savetxt('../csv/{}.csv'.format(filename),
                  csv_array,
                  delimiter=",",
                  fmt='%s',
                  header=header)


