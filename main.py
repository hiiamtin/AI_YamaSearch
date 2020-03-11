from Class import *
import time
import json
from tkinter import *

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
            count=0
            while not queue.is_empty():
                count+=1
                l = queue.remove()
                keyCurrent , cost_node = l[-1]
                father_node = l[0]
                #print(father_node,"->",keyCurrent,cost_node)
                path_node = father_node.copy()
                path_node[keyCurrent.getName()]=[str(keyCurrent.getBestAirline(time))]
                update_gui(path_node)
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
                print("=uniform-cost-search-Found=")
                for e in path_node:
                    print(e+str(path_node[e])+"->",end="")
                if time:
                    print("\nTotal : "+str(cumulative_cost_goal//3600)+" hour "+str(int(cumulative_cost_goal%3600/60))+" minus")
                else:
                    print("\nTotal : %s Baht" % cumulative_cost_goal)
            else:
                print("not found")
            print(count)
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
                            elif not keySuccessor.getName() in Dstart and down == None  :
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
                print("=Bi-Direct-Found=")
                if downtext  == "connect" :
                    for e in Dstart[stop][0] :
                        print(e+""+str(Dstart[stop][0][e])+"->",end=" ")
                    if time:
                        print("\nTotal : "+str(down//3600)+" hour "+str(int(down%3600/60))+" minus")
                    else:
                        print("\nTotal : %s Baht" % down)
                else :
                    reverseStop = [i for i in Dstop[downtext][0]]
                    for e in Dstart[downtext][0] :
                        print(e+""+str(Dstart[downtext][0][e])+"->",end="")
                    for e in range(len(reverseStop)-2,-1,-1):
                        print(reverseStop[e]+""+str(Dstop[downtext][0][reverseStop[e+1]])+"->",end=' ')
                    if time:
                        print("\nTotal : "+str(down//3600)+" hour "+str(int(down%3600/60))+" minus")
                    else:
                        print("\nTotal : %s Baht" % down)
            else :
                print("Not Found :C")
            print(count)

List_Station_Position = {}
def drawStation(start,stop):
    if start in List_Station_Position and stop in List_Station_Position:
        x_start,y_start = List_Station_Position[start]
        x_stop,y_stop = List_Station_Position[stop]
        canvas.create_line(x_start,y_start,x_stop,y_stop,fill ='red')
    else:
        print("Error!!")

def update_gui(path_node):
    strgp = ""
    for e in path_node:
         strgp+=e+str(path_node[e])+"->"
    allsearchgp.append(strgp)
    

    
    
#start_time = time.time()
#bi =bi_uniform_cost_search("BKK","LGA",True)
##end = time.tisme()
##print(end-start_time)

##start_time = time.time()
#uni =uniform_cost_search("BKK","LGA",True)
#for i in List_Station:
#    for j in List_Station:
#        bi =bi_uniform_cost_search(i,j,False)
#        uni =uniform_cost_search(i,j,False)
#        if (bi != uni):
#            print(bi)
#            print(uni)
#            print("Failed :(")
#            break;
#end = time.time()
#print(end-start_time)

def getString(li):
    return li.pop(0)
idt = []
def clicked():
    if btn['text'] == "Search":
        btn['text'] = "Cancle"     
        la['text'] = "wait for Searching..."
        uniform_cost_search("BKK","LGA",True)
        times1 = 1000
        times2 = times1
        for i in allsearchgp:
            print(i)
            message(times2,i)
            times2+=times1
    elif btn['text'] == "Cancle":
        print("Cancle")
        for e in idt:
            print(e)
            root.after_cancel(e)
        la['text'] = "Please Click for Search."
        btn['text'] = 'Search'

def message(times,i):
    idd=root.after(times,lambda: la.config(text=i))
    idt.append(idd)

root = Tk()
root.title("AI YamaSearch")
root.geometry('900x800')
home = Frame(root)

allsearchgp = []

label1 = Label(root,text= "AI YamaSearch",font = ("Arial",20))
start_text = Label(root,text= "Start :", font = ("Arial",18))
des_text = Label(root,text= "Destination :", font = ("Arial",18))
label1.grid(row=0,column=1, columnspan = 6)
la = Label(root, text = "Please Click for Search.", font = ("Arial Bold",12))
la.grid(row = 4 ,column =1 ,columnspan = 6)
btn = Button(root, text = "Search", bg = "black", fg = "red", command = clicked)


# get input using entry class

txt = Entry(root, width = 10, font = ("Arial",18))
txt2 = Entry(root, width = 10, font = ("Arial",18))

# use the grid function as usual to add it to the root

txt.grid(column = 3, row = 3)
start_text.grid(column = 2, row = 3)
des_text.grid(column = 4, row = 3)
txt2.grid(column = 5, row = 3)



# set focus to entry widget -> can write text right away

txt.focus()

selected = IntVar()

rad1 = Radiobutton(root,text='Uniform_Cost_Search', value=1, variable=selected ,font = ("Arial",12))

rad2 = Radiobutton(root,text='Bi_Direction_Uniform_Cost_Search', value=2, variable=selected, font = ("Arial",12))


btn.grid(column = 6, row = 3)


rad1.grid(column = 3, row = 2)
rad2.grid(column = 4, row = 2)





# Set the value for Spinbox


canvas = Canvas(root, width = 890, height = 548)  
img = PhotoImage(file="AI_YamaSearch/AIMap.PNG")      
canvas.create_image(20,20, anchor=NW, image=img)  
canvas.grid(column = 1, row = 1, columnspan = 6)
canvas.create_line(0,0,100,100,fill ='red')
root.mainloop()