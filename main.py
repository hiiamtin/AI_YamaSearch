import datetime
from Class import *
import json

with open('AI_YamaSearch/data.json', 'r') as f:
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
'''for e in List_Station:
    print(List_Station[e],"\n")

for e in List_Station["BKK"].getDestination():
    print(e)
    for a in e.getAirlines():
        print(a.getPrice())
'''
def uniform_cost_search(start,stop):
    if start not in List_Station:
        print("Error: key_node_start'%s' or key_node_goal'%s' not exists!!"%(start,stop))
    else:
        if start == stop:
            print("Finish: key_node_start'%s' == key_node_goal'%s' "%(start,stop))
        else:
            queue = Queue()
            father_node = {start:True}
            keySuccessors = List_Station[start].getDestination()
            for keySuccessor in keySuccessors:
                cost_node = keySuccessor.getCost()
                queue.insert(father_node,(keySuccessor,cost_node),cost_node)

            reached_goal,cumulative_cost_goal =False,0
            while not queue.is_empty():
                l = queue.remove()
                keyCurrent , cost_node = l[-1]
                father_node = l[0]
                print(father_node,"->",keyCurrent,cost_node)
                if keyCurrent.getName() == stop:
                    reached_goal = True
                    cumulative_cost_goal = cost_node
                    break
                keySuccessors = List_Station[keyCurrent.getName()].getDestination()
                new_father_node = father_node.copy()
                new_father_node[keyCurrent.getName()] = True
                if keySuccessors:
                    for keySuccessor in keySuccessors:
                        if not keySuccessor.getName() in father_node:
                            print(keySuccessor.getName())
                            cumulative_cost_goal = keySuccessor.getCost()+cost_node
                            queue.insert(new_father_node,(keySuccessor,cumulative_cost_goal),cumulative_cost_goal)
            if reached_goal:
                print("found")
            else:
                print("not found")

uniform_cost_search("BKK","JFK")