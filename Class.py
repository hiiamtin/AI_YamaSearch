class Airline:
    def __init__(self,name,price,time,park=None):
        self.name,self.price,self.time,self.park = name,price,time,park
    def __str__(self):
        return self.name+","+str(self.price)+","+str(self.time)+","+str(self.park)
    def getName(self):
        return self.name
    def getPrice(self):
        return self.price
    def getTime(self):
        return self.time
    def setName(self,name):
        self.name = name
    def setPrice(self,price):
        self.price = price
    def setTime(self,time):
        self.time = time

class DesNode:
    def __init__(self,station,airlines):
        self.station,self.airlines = station,airlines
    def addAirlines(self,airline):
        self.airlines.append(airline)
    def getAirlines(self):
        return self.airlines
    def getName(self):
        return self.station.getName()
    def getStation(self):
        return self.station
    def __str__(self):
        return str(self.station.getName())+[str(e) for e in self.airlines].__str__()


class StationNode:
    def __init__(self,name,destination):
        self.name,self.destination = name,destination
    def addDestination(self,des,added=False):
        check = True
        for e in self.destination:
            if e.getName() == des.getName():
                print("สถานีปลายทางนี้มีอยู่แล้ว โปรดใช้ addAirline(name,airline)"+e.getName())
                check = False
                break
        if check :
            self.destination.append(des)
            if not added:
                des.getStation().addDestination(DesNode(self,des.getAirlines()),True)

    def getName(self):
        return self.name
    def __str__(self):
        return self.name+[str(e) for e in self.destination].__str__()
