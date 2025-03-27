##This Python code will save the script into an instrument’s memory. 
# Once loaded into memory, the full test can be run by calling the 
# forwardDiff() function so that the entire script does not need to
#  be reloaded into memory.

import pyvisa as visa
rm = visa.ResourceManager()
address = "TCPIP0::192.0.0.5::inst0::INSTR" #Keithley 2450 SMU
inst = rm.open_resource(address)
inst.write("loadscript FullDiodeTest")
inst.write("function config()") # The config function
inst.write("reset()")
inst.write("smu.source.func = smu.FUNC_DC_CURRENT")
inst.write("smu.source.vlimit.level = 21")
inst.write("smu.source.autorange = smu.ON")
inst.write("smu.source.autodelay = smu.ON")
inst.write("smu.measure.func = smu.FUNC_DC_VOLTAGE")
inst.write("smu.measure.autorange = smu.ON")
inst.write("smu.measure.nplc = 1")
inst.write("end")
inst.write("function forwardv(current)")
inst.write("smu.source.level = current")
inst.write("smu.source.output = smu.ON")
inst.write("smu.measure.read()")
inst.write("smu.source.output = smu.OFF")
inst.write("return defbuffer1.readings[defbuffer1.endindex]") # changed print to return, since the logic is all in TSP now, 
# we don’t want these values printed to console
inst.write("end")
inst.write("function forwardDiff()")
inst.write("config()") # It’s okay to call other scripts from within a TSP script!
inst.write("currlist = {1E-7, 1E-6, 1E-5, 1E-4, 1E-3, 1E-2}")
inst.write("voltlist = {n = table.getn(currlist)}")
inst.write("for i , current in ipairs(currlist) do")
inst.write("voltlist[i] = forwardv(current)")
inst.write("end")
inst.write("voltDiff = math.max(unpack(voltlist)) - math.min(unpack(voltlist))")
inst.write("print(voltDiff)")
inst.write("end")
inst.write("forwardDiff()") # Run the "Main" function
inst.write("endscript")
inst.write("FullDiodeTest.save()") # Save the script, FullDiodeTest, into nonvolatile memory