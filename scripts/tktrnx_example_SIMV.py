import visa
rm = visa.ResourceManager()
address = "TCPIP0::192.0.0.1::inst0::INSTR" #Keithley 2450 SMU
inst = rm.open_resource(address)
inst.write("reset()")
inst.write("smu.source.func = smu.FUNC_DC_CURRENT")
inst.write("smu.source.vlimit.level = 21")
inst.write("smu.source.autorange = smu.ON")
inst.write("smu.source.autodelay = smu.ON")
inst.write("smu.measure.func = smu.FUNC_DC_VOLTAGE")
inst.write("smu.measure.autorange = smu.ON")
inst.write("smu.measure.nplc = 1")
currlist = [1E-7, 1E-6, 1E-5, 1E-4, 1E-3, 1E-2] # list of currents to source
voltlist = [None for curr in currlist] # Create an empty array for voltage measurements the same size as our source list
for i, current in enumerate(currlist): # Loop over the current source list
    inst.write("smu.source.level = "+str(current))
    inst.write("smu.source.output = smu.ON")
    inst.write("smu.measure.read()")
    inst.write("smu.source.output = smu.OFF")
    voltlist[i] = inst.query("print(defbuffer1.readings[defbuffer1.endindex])") #Grab the last reading
    voltlist[i] = float(voltlist[i]) # .query returns a string, so it must be casted to a number
voltDiff = max(voltlist) - min(voltlist)
print(voltDiff)