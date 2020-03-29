##### อันนี้ใช้สำหรับวัด Complexity นะจ๊ะ
##### Without GUI จะได้เป๊ะๆ

from Class import *
import json
import tracemalloc
import time

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
                print(">>> Uniform Cost Search")
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
                print(">>> Bidirectional Uniform Cost Search")
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

########## COMPLEXITY MEASUREMENT
def complexityMeasurement(init,dest):
    print("----- Uninform Search Algorithms -----\n")
    tracemalloc.start()
    start = time.time()
    uniform_cost_search(init,dest,True)
    stop = time.time()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current Mem : {current / 1000} kB")
    print(f"** Peak Mem : {peak / 1000} kB")
    tracemalloc.stop()
    print(f"** Time : {(stop - start)*1000} ms\n")

    tracemalloc.start()
    start = time.time()
    bi_uniform_cost_search(init,dest,True)
    stop = time.time()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current Mem : {current / 1000} kB")
    print(f"** Peak Mem : {peak / 1000} kB")
    tracemalloc.stop()
    print(f"** Time : {(stop - start)*1000} ms\n")



#### Test Here <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
complexityMeasurement("CDG","DFW")
############## <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


# import Image
# img = Image.open("AIMap.PNG")
# img = img.resize((668, 441), Image.ANTIALIAS