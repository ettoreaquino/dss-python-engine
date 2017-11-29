
__author__ = 'Ettore Aquino'

import win32com.client

class DSS(object):

    def __init__(self, dssFileName):

        # Create a new instance of the DSS
        self.dssObj = win32com.client.Dispatch("OpenDSSEngine.DSS")

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
        self.dssText.Command = "Clear"
        self.dssText.Command = "Compile " + dssFileName

    def mySolve(self):

        self.dssSolution.Solve()

    def myShowPower(self):

        self.dssText.Command = "show power elements"

    def versionDSS(self):

        version = self.dssObj.Version
        return version

    def get_data(self):
        self.dssText.Command = "Export Powers as 'results\\default\\power.csv'"
        self.dssText.Command = "Export Voltages 'results\\default\\voltages.csv'"

if __name__ == '__main__':
    myObject = DSS('C:\\repos\\dss-python-engine\\src\\IEEE13-main-default-case.dss')

    myObject.mySolve()
    myObject.myShowPower()
    opendssVersion = myObject.versionDSS()
    myObject.get_data()
    print opendssVersion