from Class import *
import json

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
print("prepare data complete!!\n\n")

def uniform_cost_search(start,stop,time):
    if start not in List_Station or stop not in List_Station:
        print("Error: key_node_start'%s' or key_node_goal'%s' not exists!!"%(start,stop))
    else:
        if start == stop:
            print("Finish: key_node_start'%s' == key_node_goal'%s' "%(start,stop))
        else:
            queue = Queue()
            father_node = {start:[]}
            keySuccessors = List_Station[start].getDestination()
            for keySuccessor in keySuccessors:
                cost_node = keySuccessor.getCost(time)
                queue.insert(father_node,(keySuccessor,cost_node),cost_node)
        
            reached_goal,cumulative_cost_goal =False,0
            while not queue.is_empty():
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
                            #print(keySuccessor.getName())
                            cumulative_cost_goal = keySuccessor.getCost(time)+cost_node
                            queue.insert(path_node,(keySuccessor,cumulative_cost_goal),cumulative_cost_goal)
            if reached_goal:
                print("=Found=")
                for e in path_node:
                    print(e+str(path_node[e])+"->",end="")
                if time:
                    print("\nTotal : "+str(cumulative_cost_goal//3600)+" hour "+str(int(cumulative_cost_goal%3600/60))+" minus")
                else:
                    print("\nTotal : %s Bath" % cumulative_cost_goal)
            else:
                print("not found")
def bi_uniform_cost_search(start,stop,time):
    if start not in List_Station or stop not in List_Station:
        print("Error: key_node_start'%s' or key_node_goal'%s' not exists!!"%(start,stop))
    else:
        if start == stop:
            print("Finish: key_node_start'%s' == key_node_goal'%s' "%(start,stop))
        else:

            queue = Queue()
            queue2 = Queue()

            father_node = {start:[]}
            father_node2 = {stop:[]}
        
            keySuccessors = List_Station[start].getDestination()
            keySuccessors2 = List_Station[stop].getDestination()
            Dstart=   {} # เก็บ cost ที่ start
            Dstop =   {} # เก็บ cost ที่ stop
            Dstart2=   {}  # เก็บ mapping start
            Dstop2 =   {}  # เก็บ mapping stop
            for keySuccessor in keySuccessors:
                cost_node = keySuccessor.getCost(time)
                queue.insert(father_node,(keySuccessor,cost_node),cost_node)     

                Dstart[ keySuccessor.getName()] =  keySuccessor.getCost(time)

                copy = father_node.copy()
                copy[keySuccessor.getName()] = str(keySuccessor.getBestAirline(time))
                Dstart2[ keySuccessor.getName()] = copy

            for keySuccessor in keySuccessors2:
                cost_node2 = keySuccessor.getCost(time)
                queue2.insert(father_node2,(keySuccessor,cost_node2),cost_node2)

                Dstop[keySuccessor.getName()] =  keySuccessor.getCost(time)

                copy = father_node2.copy()
                copy[keySuccessor.getName()] = str(keySuccessor.getBestAirline(time))
                Dstop2[ keySuccessor.getName()] = copy

            down = None # ค่า cost node ที่เชื่อกันแล้วน้อยสุด
            downtext = "" # ชื่อ
            if start in Dstop:
                down = Dstop[start]
                downtext = 'connect'         
            while True :
                try:
                    l = queue.remove()
                    l2 = queue2.remove()
                except:
                    break    
                keyCurrent , cost_node = l[-1]
                keyCurrent2 , cost_node2 = l2[-1]

                father_node = l[0]
                father_node2 = l2[0]

                path_node = father_node.copy()
                path_node[keyCurrent.getName()]=[str(keyCurrent.getBestAirline(time))]

                path_node2 = father_node2.copy()
                path_node2[keyCurrent2.getName()]=[str(keyCurrent2.getBestAirline(time))]
                
                if keyCurrent.getName() not in Dstart:
                    Dstart[keyCurrent.getName()] =  cost_node
                    copy = father_node.copy()
                    copy[keyCurrent.getName()] = str(keyCurrent.getBestAirline(time))
                    Dstart2[ keyCurrent.getName()] = copy
                if keyCurrent2.getName() not in Dstop:
                    Dstop[keyCurrent2.getName()] =  cost_node2
                    copy = father_node2.copy()
                    copy[keyCurrent2.getName()] = str(keyCurrent2.getBestAirline(time))
                    Dstop2[ keyCurrent2.getName()] = copy
                # if  keyCurrent.getName() == keyCurrent2.getName(): #เพิ่มได้ถ้าไม่กลัวมีบัค keyCurrent.getName()  in Dstop or keyCurrent2.getName() in Dstart or 
                #     reached_goal = True
                #     break

                if keyCurrent.getName() in Dstart and keyCurrent.getName() in Dstop   :
                    if down == None:
                        down = Dstart[keyCurrent.getName()]+Dstop[keyCurrent.getName()]
                        downtext =  keyCurrent.getName()
                    elif down > Dstart[keyCurrent.getName()]+Dstop[keyCurrent.getName()]:
                        down = Dstart[keyCurrent.getName()]+Dstop[keyCurrent.getName()]
                        downtext =  keyCurrent.getName()
                else:
                    keySuccessors = List_Station[keyCurrent.getName()].getDestination()
                    if keySuccessors:
                        for keySuccessor in keySuccessors:
                            if not keySuccessor.getName() in father_node  :
                                cumulative_cost_goal = keySuccessor.getCost(time)+cost_node
                                queue.insert(path_node,(keySuccessor,cumulative_cost_goal),cumulative_cost_goal)
                if keyCurrent2.getName() in Dstart and keyCurrent2.getName() in Dstop   :
                    if down == None:
                            down = Dstart[keyCurrent2.getName()]+Dstop[keyCurrent2.getName()]
                            downtext =  keyCurrent2.getName()
                    elif down > Dstart[keyCurrent2.getName()]+Dstop[keyCurrent2.getName()]:
                            down = Dstart[keyCurrent2.getName()]+Dstop[keyCurrent2.getName()]
                            downtext =  keyCurrent2.getName()
                else:            
                        keySuccessors2 = List_Station[keyCurrent2.getName()].getDestination()
                        if keySuccessors2:
                            for keySuccessor in keySuccessors2:
                                if not keySuccessor.getName() in father_node2  :
                                    cumulative_cost_goal2 = keySuccessor.getCost(time)+cost_node2
                                    queue2.insert(path_node2,(keySuccessor,cumulative_cost_goal2),cumulative_cost_goal2)
            
            if downtext != "":
                print("=Found=")

                if downtext  == "connect" :
                    for e in Dstart2[stop] :
                        print(e+ " "+str(Dstart2[stop][e])+"->",end=" ") 
                    if time:
                            print("\nTotal : "+str(down//3600)+" hour "+str(int(down%3600/60))+" minus")
                    else:
                        print("\nTotal : %s Bath" % down)
                else :
                    reverseStop = [i for i in Dstop2[downtext]]
                    for e in Dstart2[downtext] :
                        print(e+ " "+str(Dstart2[downtext][e])+"->",end=" ") 
                    for e in range(len(reverseStop)-2,-1,-1):
                        print(reverseStop[e]+"  " + str(Dstop2[downtext][reverseStop[e+1]])+"-> ",end= ' ')
                    if time:
                        print("\nTotal : "+str(down//3600)+" hour "+str(int(down%3600/60))+" minus")
                    else:
                        print("\nTotal : %s Bath" % down)


#print (List_Station[])
bi_uniform_cost_search("ICN","BOS",True)
uniform_cost_search("ICN","BOS",True)
