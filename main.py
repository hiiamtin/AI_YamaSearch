import datetime
from Class import *
BKK = StationNode("BKK",[])
HKG = StationNode("HKG",[])
ICN = StationNode("ICN",[])
SFO = StationNode("SFO",[])

BKK.addDestination(DesNode(HKG,[Airline("THAI",8846,datetime.time(2,45)),Airline("United",39852,datetime.time(12,20))]))
BKK.addDestination(DesNode(ICN,[Airline("THAI2",8846,datetime.time(2,45))]))
HKG.addDestination(DesNode(SFO,[Airline("United2",39852,datetime.time(12,20))]))
print(BKK)
print(HKG)
