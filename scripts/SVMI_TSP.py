
# This script uses Keithely Test Scripting Processing (TSP)Language

# In particular this script measures I for set U with a Keithlery SMU 2470   
import pyvisa
rm = pyvisa.ResourceManager()
address = "TCPIP0::141.52.65.107::inst0::INSTR" #Keithley 2470 SMU

inst = rm.open_resource(address)
inst.write("reset()")

vstart = -50
vstep = 10
vstop = 1 # range() function is exclusive of stop value!
currlimit = 1E-1

inst.write("smu.source.func = smu.FUNC_DC_VOLTAGE")
inst.write("smu.source.ilimit.level = "+str(currlimit))
inst.write("smu.source.autorange = smu.ON")
inst.write("smu.source.autodelay = smu.ON")
inst.write("smu.measure.func = smu.FUNC_DC_CURRENT")
inst.write("smu.measure.autorange = smu.ON")
inst.write("smu.measure.nplc = 1")

voltlist = list(range(vstart, vstop, vstep)) # list of currents to source
currlist = [None for volt in voltlist] # Create an empty array for current measurements the same size as our source list
for i, voltage in enumerate(voltlist): # Loop over the current source list
    inst.write("smu.source.level = "+str(voltage))
    inst.write("smu.source.output = smu.ON")
    inst.write("smu.measure.read()")
    inst.write("smu.source.output = smu.OFF")
    currlist[i] = inst.query("print(defbuffer1.readings[defbuffer1.endindex])") #Grab the last reading
    currlist[i] = float(currlist[i]) # .query returns a string, so it must be casted to a number
print(currlist)

# Element-wise multiplication gives resistance R U/I
result = [ volt / curr for curr, volt in zip(currlist, voltlist)]

print(result)