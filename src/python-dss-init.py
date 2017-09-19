
__author__ = 'Ettore Aquino'

import win32com.client

class OpenDSSInitializer(object):

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
            self.dssElem = self.dssCircuit.ActiveCktElement
            self.dssBus = self.dssCircuit.ActiveBus

        # Always a good a idea to clear the DSS when loading a new circuit
        self.dssObj.ClearAll()

        # Load the given circuit master file into OpenDSS
        self.dssText.Command = "Compile " + dssFileName

    def versionDSS(self):

        return self.dssObj.Version

if __name__ == '__main__':
    myObject = OpenDSSInitializer('IEEE13-main.dss')

    opendssVersion = myObject.versionDSS()
    print opendssVersion