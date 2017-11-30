# Caso 2: Perfil de carga sem  controle
__author__ = 'Ettore Aquino'

import os
import win32com.client
import matplotlib.pyplot as plt
import re

class DSS(object):

    def __init__(self, dssFileName, hour, power_file_name, voltage_file_name):

        # Create a new instance of the DSS
        self.dssObj = win32com.client.Dispatch("OpenDSSEngine.DSS")
        self.hour = hour
        self.power_file_name = power_file_name
        self.voltage_file_name = voltage_file_name

        # Start the DSS
        if self.dssObj.Start(0) == False:
            print "DSS Failed to Start"
        else:
            # Assign a variable to each of the interfaces for easier access
            self.dssText = self.dssObj.Text
            self.dssCircuit = self.dssObj.ActiveCircuit
            self.dssSolution = self.dssCircuit.Solution

        # Always a good a idea to clear the DSS when loading a new circuit
        self.dssObj.ClearAll()

        # Load the given circuit master file into OpenDSS
        self.dssText.Command = "Compile " + dssFileName

    def clear(self):
        self.dssText.Command = "Clear"

    def mySolve(self):

        self.dssText.Command = "Set number=%s"%(self.hour)
        self.dssSolution.Solve()

        self.VA = list(self.dssCircuit.AllNodeVmagPUByPhase(1))
        self.dist_a = list(self.dssCircuit.AllNodeDistancesByPhase(1))

        self.VB = list(self.dssCircuit.AllNodeVmagPUByPhase(2))
        self.dist_b = list(self.dssCircuit.AllNodeDistancesByPhase(2))

        self.VC = list(self.dssCircuit.AllNodeVmagPUByPhase(3))
        self.dist_c = list(self.dssCircuit.AllNodeDistancesByPhase(3))

    def myShowPower(self):

        self.dssText.Command = "show power elements"

    def versionDSS(self):

        version = self.dssObj.Version
        return version

    def get_data(self):
        self.dssText.Command = "Export Powers as 'results\\pv30\\%s'"%(self.power_file_name)
        self.dssText.Command = "Export Voltages 'results\\pv30\\%s'"%(self.voltage_file_name)

def transform_list_into_sring(_list):
    return str(_list)

def take_out_commas(text):
    text = re.sub(",", "", text)
    return text

def create_data_file(voltage, file_name):
    line_length = len(voltage)
    col_length = len(voltage[0])
    dat_file = open("results\\pv30\\%s"%(file_name), "w")

    for i in range(0, col_length):
        for j in range(0, line_length):
            dat_file.write("%s %s %s\n"%(i + 1, j + 1, voltage[j][i]))
        dat_file.write("\n")
    dat_file.close()

def create_ieee13_main_pv(number_of_panels, power_of_pv):
    pv_file = open(os.path.join("C:\\", "repos", "dss-python-engine", "src", "dss-models", "ieee-13-bus", "components", "PV_IEEE13.dss"), "w")
    default_text = """
New Loadshape.Irradiance_Jan07_2017 npts=24 interval=0
~ csvfile= \"C:\\repos\\dss-python-engine\\src\\stochastic-data\\energisa-2017\\irradiance.csv\"
New Tshape.Temperature_Jan07_2017 npts=24 interval=0
~ csvfile=\"C:\\repos\\dss-python-engine\\src\\stochastic-data\\energisa-2017\\temperature.csv\"
                   """
    pv_file.write(default_text)
    pv_file.write("\n")

    for i in range(1, number_of_panels + 1):
        panel = """
New XYCurve.PV634_%s_PvsT npts=4  xarray=[0  25  75  100]  yarray=[1.2 1.0 0.8  0.6]
New XYCurve.PV634_%s_Eff npts=4  xarray=[.1  .2  .4  1.0]  yarray=[.86  .9  .93  .97] 
New PVSystem.PV634_%s phases=3 bus1=681.1.2.3 kV=0.48  kVA=%s  irrad=.98  Pmpp=25 temperature=25 PF=1 %scutin=0.1 %scutout=0.1
~ effcurve=PV634_%s_Eff  P-TCurve=PV634_%s_PvsT Daily=Irradiance_Jan07_2017  TDaily=Temperature_Jan07_2017
                """%(i, i, i, power_of_pv, "%", "%", i, i)
        pv_file.write(panel)
        pv_file.write("\n")

    pv_file.close()
                
if __name__ == '__main__':
    voltageA = []
    voltageB = []
    voltageC = []
    count = 1
    pv = 10

    for i in range(pv, 500 + pv, pv):
        create_ieee13_main_pv(count, pv)

        for j in range(1, 25):
            myObject = DSS(
                'C:\\repos\\dss-python-engine\\src\\IEEE13-main-pv.dss',
                i,
                "power_hour_%s.csv"%(j),
                "voltage_hour_%s.csv"%(j))
            myObject.mySolve()
            opendssVersion = myObject.versionDSS()
            myObject.get_data()
            voltageA.append(myObject.VA)
            voltageB.append(myObject.VB)
            voltageC.append(myObject.VC)
        count += 1

        create_data_file(voltageA, "voltage_phase_A.dat")
        create_data_file(voltageB, "voltage_phase_B.dat")
        create_data_file(voltageC, "voltage_phase_C.dat")
