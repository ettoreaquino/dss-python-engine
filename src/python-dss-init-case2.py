# Caso 2: Perfil de carga sem  controle
__author__ = 'Ettore Aquino'

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
        print self.dist_a

    def myShowPower(self):

        self.dssText.Command = "show power elements"

    def versionDSS(self):

        version = self.dssObj.Version
        return version

    def get_data(self):
        self.dssText.Command = "Export Powers as 'results\\case2\\%s'"%(self.power_file_name)
        self.dssText.Command = "Export Voltages 'results\\case2\\%s'"%(self.voltage_file_name)

def transform_list_into_sring(_list):
    return str(_list)

def take_out_commas(text):
    text = re.sub(",", "", text)
    return text

def save_to_matalb_file(text):
    matlab_file = open("results\\case2\\matlab.m", "w")
    matlab_file.write("graph = " + text)
    matlab_file.close()

if __name__ == '__main__':
    voltage = []

    for i in range(1, 25):
        myObject = DSS(
            'C:\\repos\\dss-python-engine\\src\\IEEE13-main-case2.dss',
            i,
            "power_hour_%s.csv"%(i),
            "voltage_hour_%s.csv"%(i))
        myObject.mySolve()
        opendssVersion = myObject.versionDSS()
        myObject.get_data()
        voltage.append(myObject.VA)
    
    voltage_string = transform_list_into_sring(voltage)
    formated_voltage = take_out_commas(voltage_string)
    save_to_matalb_file(formated_voltage)
