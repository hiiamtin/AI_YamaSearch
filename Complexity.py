##### อันนี้ใช้สำหรับวัด Complexity นะจ๊ะ
##### Without GUI จะได้เป๊ะๆ

from Class import *
import json
import tracemalloc
import time
import math

with open('data.json', 'r') as f:
    distros_dict = json.load(f)
List_Station = {}
for distro in distros_dict:
    List_Station[distro] = StationNode(distro,[])

for distro in distros_dict:
    station = List_Station[distro]
    for des in distros_dict[distro]:
        if des not in List_Station:
            break
        al = []
        for e in distros_dict[distro][des][1:]:
            t = e["time"].split(":")
            al.append(Airline(e["name"],e["price"],datetime.time(int(t[0]),int(t[1]))))
        station.addDestination(DesNode(List_Station[des],al))
#print("prepare data complete!!\n\n")


def uniform_cost_search(start,stop,time):
    if start not in List_Station or stop not in List_Station:
        return "Error: key_node_start'%s' or key_node_goal'%s' not exists!!"%(start,stop)
    else:
        if start == stop:
            return"Finish: key_node_start'%s' == key_node_goal'%s' "%(start,stop)
        else:
            queue = Queue()
            father_node = {start:[]}
            keySuccessors = List_Station[start].getDestination()
            for keySuccessor in keySuccessors:
                cost_node = keySuccessor.getCost(time)
                queue.insert(father_node,(keySuccessor,cost_node),cost_node)

            reached_goal,cumulative_cost_goal =False,0
            count=0
            while not queue.is_empty():
                count+=1
                l = queue.remove()
                keyCurrent , cost_node = l[-1]
                father_node = l[0]
                #print(father_node,"->",keyCurrent,cost_node)
                path_node = father_node.copy()
                path_node[keyCurrent.getName()]=[str(keyCurrent.getBestAirline(time))]
                if keyCurrent.getName() == stop:
                    reached_goal = True
                    cumulative_cost_goal = cost_node
                    break
                keySuccessors = List_Station[keyCurrent.getName()].getDestination()
                if keySuccessors:
                    for keySuccessor in keySuccessors:
                        if not keySuccessor.getName() in father_node:
                            cumulative_cost_goal = keySuccessor.getCost(time)+cost_node
                            queue.insert(path_node,(keySuccessor,cumulative_cost_goal),cumulative_cost_goal)
            if reached_goal:
                print(">>> Uniform Cost Search ; loop =",count)
                str1 = ""
                for e in path_node:
                    str1+=e+str(path_node[e])+"->"
                    #print(e+str(path_node[e])+"->",end="")
                if time:
                    str1+="\nTotal : "+str(cumulative_cost_goal//3600)+" hour "+str(int(cumulative_cost_goal%3600/60))+" minus"
                    #print("\nTotal : "+str(cumulative_cost_goal//3600)+" hour "+str(int(cumulative_cost_goal%3600/60))+" minus")
                else:
                    str1+="\nTotal :"+str(cumulative_cost_goal)+"Baht"
                    #print("\nTotal : %s Baht" % cumulative_cost_goal)
                return str1
            else:
                return "not found"
            #print(count)

def bi_uniform_cost_search(start,stop,time):
    if start not in List_Station or stop not in List_Station:
        return "Error: key_node_start'%s' or key_node_goal'%s' not exists!!"%(start,stop)
    else:
        if start == stop:
            return "Finish: key_node_start'%s' == key_node_goal'%s' "%(start,stop)
        else:
            queue = Queue()
            queue2 = Queue()

            father_node = {start:[]}
            father_node2 = {stop:[]}

            keySuccessors = List_Station[start].getDestination()
            keySuccessors2 = List_Station[stop].getDestination()
            Dstart= {start:[father_node,0]} # เก็บ mapping,cost ที่ start
            Dstop = {stop:[father_node2,0]} # เก็บ mapping,cost ที่ stop
            down = None # ค่า cost node ที่เชื่อกันแล้วน้อยสุด
            downtext = "" # ชื่อ
            for keySuccessor in keySuccessors:
                cost_node = keySuccessor.getCost(time)
                queue.insert(father_node,(keySuccessor,cost_node),cost_node)

            for keySuccessor in keySuccessors2:
                cost_node2 = keySuccessor.getCost(time)
                queue2.insert(father_node2,(keySuccessor,cost_node2),cost_node2)
            count = 0
            while True :
                count+=1
                try:
                    l = queue.remove()
                    l2 = queue2.remove()
                except:
                    break
                keyCurrent , cost_node = l[-1]
                keyCurrent2 , cost_node2 = l2[-1]

                if down!=None:
                    if down < cost_node and down < cost_node2:
                        break

                father_node = l[0]
                father_node2 = l2[0]

                path_node = father_node.copy()
                path_node[keyCurrent.getName()]=[str(keyCurrent.getBestAirline(time))]

                path_node2 = father_node2.copy()
                path_node2[keyCurrent2.getName()]=[str(keyCurrent2.getBestAirline(time))]

                if keyCurrent.getName() not in Dstart:
                    Dstart[keyCurrent.getName()] = [path_node,cost_node]

                if keyCurrent2.getName() not in Dstop:
                    Dstop[keyCurrent2.getName()] = [path_node2,cost_node2]

                if keyCurrent.getName() in Dstart and keyCurrent.getName() in Dstop   :
                    #print("down["+str(count)+"]"+keyCurrent.getName())
                    if down == None:
                        down = Dstart[keyCurrent.getName()][1]+Dstop[keyCurrent.getName()][1]
                        downtext = keyCurrent.getName()
                    elif down > Dstart[keyCurrent.getName()][1]+Dstop[keyCurrent.getName()][1]:
                        down = Dstart[keyCurrent.getName()][1]+Dstop[keyCurrent.getName()][1]
                        downtext = keyCurrent.getName()
                else:
                    keySuccessors = List_Station[keyCurrent.getName()].getDestination()
                    if keySuccessors:
                        for keySuccessor in keySuccessors:
                            if not keySuccessor.getName() in father_node and keySuccessor.getName() not in Dstart:
                                if down != None:
                                    if down > keySuccessor.getCost(time)+cost_node :
                                        cumulative_cost_goal = keySuccessor.getCost(time)+cost_node
                                        queue.insert(path_node,(keySuccessor,cumulative_cost_goal),cumulative_cost_goal)
                                else:
                                    cumulative_cost_goal = keySuccessor.getCost(time)+cost_node
                                    queue.insert(path_node,(keySuccessor,cumulative_cost_goal),cumulative_cost_goal)
                if keyCurrent2.getName() in Dstart and keyCurrent2.getName() in Dstop   :
                    if down == None:
                            down = Dstart[keyCurrent2.getName()][1]+Dstop[keyCurrent2.getName()][1]
                            downtext = keyCurrent2.getName()
                    elif down > Dstart[keyCurrent2.getName()][1]+Dstop[keyCurrent2.getName()][1]:
                            down = Dstart[keyCurrent2.getName()][1]+Dstop[keyCurrent2.getName()][1]
                            downtext = keyCurrent2.getName()
                else:
                        keySuccessors2 = List_Station[keyCurrent2.getName()].getDestination()
                        if keySuccessors2:
                            for keySuccessor in keySuccessors2 :
                                 if not keySuccessor.getName() in father_node2 and keySuccessor.getName() not in Dstop:
                                    if down != None:
                                        if down > keySuccessor.getCost(time)+cost_node2 :
                                            cumulative_cost_goal2 = keySuccessor.getCost(time)+cost_node2
                                            queue2.insert(path_node2,(keySuccessor,cumulative_cost_goal2),cumulative_cost_goal2)
                                    else:
                                        cumulative_cost_goal2 = keySuccessor.getCost(time)+cost_node2
                                        queue2.insert(path_node2,(keySuccessor,cumulative_cost_goal2),cumulative_cost_goal2)
            if downtext != "":
                print(">>> Bidirectional Uniform Cost Search ; loop =",count)
                str1 = ""
                if downtext  == "connect" :
                    for e in Dstart[stop][0] :
                        str1+=e+""+str(Dstart[stop][0][e])+"->"
                        #print(e+""+str(Dstart[stop][0][e])+"->",end=" ")
                    if time:
                        str1+="\nTotal : "+str(down//3600)+" hour "+str(int(down%3600/60))+" minus"
                        #print("\nTotal : "+str(down//3600)+" hour "+str(int(down%3600/60))+" minus")
                    else:
                        str1+="\nTotal : "+str(down)+"Baht"  
                        #print("\nTotal : %s Baht" % down)
                else :
                    reverseStop = [i for i in Dstop[downtext][0]]
                    for e in Dstart[downtext][0] :
                        str1+=e+""+str(Dstart[downtext][0][e])+"->"
                        #print(e+""+str(Dstart[downtext][0][e])+"->",end="")
                    for e in range(len(reverseStop)-2,-1,-1):
                        str1 +=reverseStop[e]+""+str(Dstop[downtext][0][reverseStop[e+1]])
                        #print(reverseStop[e]+""+str(Dstop[downtext][0][reverseStop[e+1]])+"->",end=' ')
                    if time:
                        str1+="\nTotal : "+str(down//3600)+" hour "+str(int(down%3600/60))+" minus"
                        #print("\nTotal : "+str(down//3600)+" hour "+str(int(down%3600/60))+" minus")
                    else:
                        str1+= "\nTotal : %s Baht" % down
                        #print("\nTotal : %s Baht" % down)
                return str1
            else :
                #print("Not Found :C")
                return "Not Found :C"
            #print(count)

def a_star_search(start,stop,Heuristics,time):
    if len(Heuristics)==0:
        return "Error: Heuristics is empty!!"
    elif start not in List_Station or stop not in List_Station:
        return "Error: key_node_start'%s' or key_node_goal'%s' not exists!!"%(start,stop)
    else:
        if start == stop:
            return"Finish: key_node_start'%s' == key_node_goal'%s' "%(start,stop)
        else:
            queue = Queue()
            father_node = {start:[]}
            keySuccessors = List_Station[start].getDestination()
            for keySuccessor in keySuccessors:
                cost_node = keySuccessor.getCost(time)
                priority = cost_node+getHeuristics(keySuccessor.getName())
                #print(keySuccessor.getName(),cost_node,getHeuristics(keySuccessor.getName()),priority)
                queue.insert(father_node,(keySuccessor,cost_node),priority)

            reached_goal,cumulative_cost_goal =False,0
            count=0
            while not queue.is_empty():
                count+=1
                l = queue.remove()
                keyCurrent , cost_node = l[-1]
                father_node = l[0]
                #print(father_node,"->",keyCurrent,cost_node)
                path_node = father_node.copy()
                path_node[keyCurrent.getName()]=[str(keyCurrent.getBestAirline(time))]
                if keyCurrent.getName() == stop:
                    reached_goal = True
                    cumulative_cost_goal = cost_node
                    break
                keySuccessors = List_Station[keyCurrent.getName()].getDestination()
                if keySuccessors:
                    for keySuccessor in keySuccessors:
                        if not keySuccessor.getName() in father_node:
                            cumulative_cost_goal = keySuccessor.getCost(time)+cost_node
                            priority = cumulative_cost_goal+getHeuristics(keySuccessor.getName())
                            queue.insert(path_node,(keySuccessor,cumulative_cost_goal),priority)
            if reached_goal:
                print(">>> A* Search ; loop =",count)
                str1 = ""
                for e in path_node:
                    str1+=e+str(path_node[e])+"->"
                    #print(e+str(path_node[e])+"->",end="")
                if time:
                    str1+="\nTotal : "+str(cumulative_cost_goal//3600)+" hour "+str(int(cumulative_cost_goal%3600/60))+" minus"
                    #print("\nTotal : "+str(cumulative_cost_goal//3600)+" hour "+str(int(cumulative_cost_goal%3600/60))+" minus")
                else:
                    str1+="\nTotal :"+str(cumulative_cost_goal)+"Baht"
                    #print("\nTotal : %s Baht" % cumulative_cost_goal)
                return str1
            else:
                return "not found"
            
def rescale():
    for e in coordinates:
        x,y=coordinates[e]
        x=x*(WIDTH/890)
        y=y*(HEIGHT/548)
        coordinates[e]=[x,y]
        #print(e,x,y)
def getDistance(a,b):
    x1,y1=a
    x2,y2=b
    ans1 = int(math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2)))
    if x1 > x2:
        x = (WIDTH-x1) + x2
    else:
        x = x1 + (WIDTH-x2)
    ans2 = int(math.sqrt(math.pow(x,2)+math.pow(y1-y2,2)))
    return ans1 if ans1 < ans2 else ans2
def updateHeuristics(stop):
    h = {stop:0}
    for e in coordinates:
        if e != stop:
            h[e]=getDistance(coordinates[e],coordinates[stop])
        else:
            h[e]=0
    return h
def getHeuristics(s):
    return int(((Heuristics[s]-Heuristics_min)*((price_max-price_min)/(Heuristics_max-Heuristics_min))+price_min)*0.9)
    #return Heuristics[s]
def find_max_min(time):
    global Heuristics_min,Heuristics_max,price_min,price_max
    for e in Heuristics:
        if Heuristics[e] < Heuristics_min:
                Heuristics_min = Heuristics[e]
        if Heuristics[e] > Heuristics_max:
                Heuristics_max = Heuristics[e]
    for e in List_Station:
        for i in List_Station[e].getDestination():
            if i.getCost(time) < price_min:
                price_min = i.getCost(time)
            if i.getCost(time) > price_max:
                price_max = i.getCost(time)

########## COMPLEXITY MEASUREMENT
def complexityMeasurement(init,dest):
    global Heuristics
    print("----- Uninform Search Algorithms -----\n")
    tracemalloc.start()
    start = time.time()
    print(uniform_cost_search(init,dest,True))
    stop = time.time()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current Mem : {current / 1000} kB")
    print(f"** Peak Mem : {peak / 1000} kB")
    tracemalloc.stop()
    print(f"** Time : {(stop - start)*1000} ms\n")

    tracemalloc.start()
    start = time.time()
    print(bi_uniform_cost_search(init,dest,True))
    stop = time.time()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current Mem : {current / 1000} kB")
    print(f"** Peak Mem : {peak / 1000} kB")
    tracemalloc.stop()
    print(f"** Time : {(stop - start)*1000} ms\n")

    print("----- Heuristics Search Algorithms -----\n")
    tracemalloc.start()
    start = time.time()
    Heuristics=updateHeuristics(dest)
    find_max_min(True)
    print(a_star_search(init,dest,Heuristics,True))
    stop = time.time()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current Mem : {current / 1000} kB")
    print(f"** Peak Mem : {peak / 1000} kB")
    tracemalloc.stop()
    print(f"** Time : {(stop - start)*1000} ms\n")



#### Test Here <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
WIDTH=668
HEIGHT=441
coordinates = {'BKK' : [666,319],
               'MIA' : [229,293],
               'NRT' : [753,264],
               'HND' : [744,255],
               'PEK' : [694,243],
               'ICN' : [716,250],
               'PVG' : [707,269],
               'XMN' : [703,287],
               'TPE' : [711,292],
               'HKG' : [694,297],
               'MNL' : [711,324],
               'CAN' : [679,283],
               'CMB' : [613,342],
               'MCT' : [561,297],
               'AUH' : [548,292],
               'DOH' : [537,288],
               'KWI' : [532,287],
               'IST' : [484,241],
               'SVO' : [493,188], 
               'HEL' : [473,171],
               'VIE' : [454,218],
               'FRA' : [442,210],
               'ZRH' : [441,224],
               'CDG' : [431,216],
               'AMS' : [431,204],
               'LHR' : [418,206],
               'DUB' : [403,200],
               'LIS' : [399,250],
               'BOS' : [266,226],
               'LGA' : [252,235],
               'JFK' : [252,246],
               'YYZ' : [238,226],
               'DTW' : [224,223],
               'ORD' : [234,206],
               'ATL' : [223,264],
               'DEN' : [183,246],
               'IAH' : [192,278],
               'DFW' : [191,264],
               'LAS' : [154,258],
               'LAX' : [142,264],
               'SFO' : [132,250],
               'SEA' : [142,225],
               'YVR' : [137,213]
}
Heuristics={}
price_min,price_max=9999999,0
Heuristics_min,Heuristics_max=9999999,0
rescale()

#complexityMeasurement("BOS","MNL")
complexityMeasurement("CDG","DFW")
############## <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


# import Image
# img = Image.open("AIMap.PNG")
# img = img.resize((668, 441), Image.ANTIALIAS