from Class import *
import time
import json
from tkinter import *
from tkinter import messagebox as mess

from PIL import Image
from PIL import ImageTk

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
                update_gui(path_node)
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
                print("=uniform-cost-search-Found=")
                str1 = ""
                for e in path_node:
                    str1+=e+str(path_node[e])+"->"
                    print(e+str(path_node[e])+"->",end="")
                if time:
                    str1+="\nTotal : "+str(cumulative_cost_goal//3600)+" hour "+str(int(cumulative_cost_goal%3600/60))+" minus"
                    print("\nTotal : "+str(cumulative_cost_goal//3600)+" hour "+str(int(cumulative_cost_goal%3600/60))+" minus")
                else:
                    str1+="\nTotal :"+str(cumulative_cost_goal)+"Baht"
                    print("\nTotal : %s Baht" % cumulative_cost_goal)
                return str1
            else:
                return "not found"
            print(count)

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
                update_gui(path_node)
                update_gui2(path_node2)

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
                print("=Bi-Direct-Found=")
                str1 = ""
                if downtext  == "connect" :
                    update_gui(Dstart[downtext][0])
                    update_gui2(Dstop[downtext][0])
                    for e in Dstart[stop][0] :
                        str1+=e+""+str(Dstart[stop][0][e])+"->"
                        print(e+""+str(Dstart[stop][0][e])+"->",end=" ")
                    if time:
                        str1+="\nTotal : "+str(down//3600)+" hour "+str(int(down%3600/60))+" minus"
                        print("\nTotal : "+str(down//3600)+" hour "+str(int(down%3600/60))+" minus")
                    else:
                        str1+="\nTotal : "+str(down)+"Baht"  
                        print("\nTotal : %s Baht" % down)
                else :
                    update_gui(Dstart[downtext][0])
                    update_gui2(Dstop[downtext][0])
                    reverseStop = [i for i in Dstop[downtext][0]]
                    for e in Dstart[downtext][0] :
                        str1+=e+""+str(Dstart[downtext][0][e])+"->"
                        print(e+""+str(Dstart[downtext][0][e])+"->",end="")
                    for e in range(len(reverseStop)-2,-1,-1):
                        str1 +=reverseStop[e]+""+str(Dstop[downtext][0][reverseStop[e+1]])
                        print(reverseStop[e]+""+str(Dstop[downtext][0][reverseStop[e+1]])+"->",end=' ')
                    if time:
                        str1+="\nTotal : "+str(down//3600)+" hour "+str(int(down%3600/60))+" minus"
                        print("\nTotal : "+str(down//3600)+" hour "+str(int(down%3600/60))+" minus")
                    else:
                        str1+= "\nTotal : %s Baht" % down
                        print("\nTotal : %s Baht" % down)
                return str1
            else :
                print("Not Found :C")
                return "Not Found :C"
            print(count)

def drawStation(map,start,stop,times,color='red',tag='line'):
    if start in coordinates and stop in coordinates:
        x_start,y_start = coordinates[start]
        x_stop,y_stop = coordinates[stop]
        if map == 1 :
            idd = root.after(times,lambda: canvas.create_line(x_start+error_pos,y_start+error_pos,x_stop+error_pos,y_stop+error_pos,fill = color,tag=tag))
        elif map ==2:
            idd = root.after(times,lambda: canvas2.create_line(x_start+error_pos,y_start+error_pos,x_stop+error_pos,y_stop+error_pos,fill = color,tag=tag))
        else :
            print("error")
    else:
        print("Error!!")
        idd=None
    return idd

def update_gui(path_node):
    strgp = ""
    for e in path_node:
         strgp+=e+"->"
    allsearchgp.append(strgp)
def update_gui2(path_node2):
    strgp = ""
    for e in path_node2:
         strgp+=e+"->"
    allsearchgp2.append(strgp)

def rescale():
    for e in coordinates:
        x,y=coordinates[e]
        x=x*(WIDTH/890)
        y=y*(HEIGHT/548)
        coordinates[e]=[x,y]
        print(e,x,y)



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
    if txt3.get() == "":
        mess.showinfo("Title", "Please Choose Your Delay")
    elif selected.get() == 1:
        if btn['text'] == "Search":
            btn['text'] = "Cancle" 
            btn['image']= photo_2
            la['text'] = "wait for Searching..."
            start_time = time.time()
            ans  = uniform_cost_search(txt.get(),txt2.get(),True)
            endtime = (time.time() - start_time)*1000
            times1 = int(txt3.get())
            times2 = times1
            for i in allsearchgp:
                message(times2,i)
                #message3(times2,i)
                times2+=times1
            else:
                root.after(int(times2+times1),lambda: la3.config(text="ANSWER:"+ans+ "\nSearchTimes : "+str(endtime)+"ms"))
                #root.after(int(times2+times1),lambda: la3_2.config(text="ANSWER:"+ans+ "\nSearchTimes : "+str(endtime)+"ms"))
                allsearchgp.clear()

        elif btn['text'] == "Cancle":
            btn['image']= photo
            for e in idt:
                root.after_cancel(e)
            else: 
                la['text'] = "Please Click for Search."
                la2['text'] = ""
                la3['text'] = ""
                btn['text'] = 'Search'
                idt.clear()
            canvas.delete('line')
            canvas.delete('line2')
    elif selected.get() == 2 :
        if btn['text'] == "Search":
            btn['text'] = "Cancle" 
            btn['image']= photo_2
            la['text'] = "wait for Searching..."
            start_time = time.time()
            ans = bi_uniform_cost_search(txt.get(),txt2.get(),True)
            endtime = (time.time() - start_time)*1000
            times1 = int(txt3.get())
            times2 = times1
            for i in allsearchgp:
                message(times2,i)
                #message3(times2,i)
                times2+=times1
            else:
                allsearchgp.clear()
            times2 = times1
            for i in allsearchgp2:
                message2(times2,i)
                #message4(times2,i)
                times2+=times1
            else:
                allsearchgp2.clear()
                root.after(times2,lambda: la3.config(text="ANSWER:"+ans + "\nSearchTimes : "+str(endtime)+"ms"))
                #root.after(times2,lambda: la3_2.config(text="ANSWER:"+ans + "\nSearchTimes : "+str(endtime)+"ms"))
        elif btn['text'] == "Cancle":
            btn['image']= photo
            for e in idt:
                root.after_cancel(e)
            else:
                la['text'] = "Please Click for Search."
                la2['text'] = ""
                la3['text'] = ""
                btn['text'] = 'Search'
                idt.clear()
            canvas.delete('line')
            canvas.delete('line2')
def clicked_2():
    if txt3.get() == "":
        #mess.showinfo("Title", "Please Choose Your Delay")
        print()
    elif selected2.get() == 1:
        if btn['text'] == "Search":
            btn['text'] = "Cancle" 
            btn['image']= photo_2
            la_2['text'] = "wait for Searching..."
            start_time = time.time()
            ans  = uniform_cost_search(txt.get(),txt2.get(),True)
            endtime = (time.time() - start_time)*1000
            times1 = int(txt3.get())
            times2 = times1
            for i in allsearchgp:
                message3(times2,i)
                times2+=times1
            else:
                root.after(int(times2+times1),lambda: la3_2.config(text="ANSWER:"+ans+ "\nSearchTimes : "+str(endtime)+"ms"))
                allsearchgp.clear()
        elif btn['text'] == "Cancle":
            btn['image']= photo
            for e in idt:
                root.after_cancel(e)
            else: 
                la_2['text'] = "Please Click for Search."
                la2_2['text'] = ""
                la3_2['text'] = ""
                btn['text'] = 'Search'
                idt.clear()
            canvas2.delete('line')
            canvas2.delete('line2')
    elif selected2.get() == 2 :
        if btn['text'] == "Search":  
            btn['text'] = "Cancle" 
            btn['image']= photo_2
            la_2['text'] = "wait for Searching..."
            start_time = time.time()
            ans = bi_uniform_cost_search(txt.get(),txt2.get(),True)
            endtime = (time.time() - start_time)*1000
            times1 = int(txt3.get())
            times2 = times1
            for i in allsearchgp:
                message3(times2,i)
                times2+=times1
            else:
                allsearchgp.clear()
            times2 = times1
            for i in allsearchgp2:
                message4(times2,i)
                times2+=times1
            else:
                allsearchgp2.clear()
                root.after(times2,lambda: la3_2.config(text="ANSWER:"+ans + "\nSearchTimes : "+str(endtime)+"ms"))
        elif btn['text'] == "Cancle":
            btn['image']= photo
            for e in idt:
                root.after_cancel(e)
            else:
                la_2['text'] = "Please Click for Search."
                la2_2['text'] = ""
                la3_2['text'] = ""
                btn['text'] = 'Search'
                idt.clear()
            canvas2.delete('line')
            canvas2.delete('line2')
def Call_clicked():
    if 0< selected.get() <=2 and 0< selected2.get() <=2 :
        if btn['text']  == 'Search':
            clicked()
            btn['text']  = 'Search'
            clicked_2()
        else:
            clicked()
            btn['text']  = 'Cancle'
            clicked_2()
    elif  0< selected.get() <=2:
        clicked()
    elif  0< selected2.get() <=2:    
        clicked_2()
def message(times,i):
    root.after(times,lambda: canvas.delete('line'))
    idd=root.after(times,lambda: la.config(text=i))
    print(i.split("->"))
    l = i.split("->")
    prev=None
    for e in range(len(l)-1):
        if prev == None:
            prev = l[e]
        else:
            idd2=drawStation(1,prev,l[e],times)     
            prev=l[e]
            idt.append(idd2)
    idt.append(idd)
def message2(times,i):
    root.after(times,lambda: canvas.delete('line2'))
    idd=root.after(times,lambda: la2.config(text=i))
    print(i.split("->"))
    l = i.split("->")
    prev=None
    for e in range(len(l)-1):
        if prev == None:
            prev = l[e]
        else:
            idd2=drawStation(1,prev,l[e],times,'blue','line2')     
            prev=l[e]
            idt.append(idd2)
    idt.append(idd)
def message3(times,i):
    root.after(times,lambda: canvas2.delete('line'))
    idd=root.after(times,lambda: la_2.config(text=i))
    print(i.split("->"))
    l = i.split("->")
    prev=None
    for e in range(len(l)-1):
        if prev == None:
            prev = l[e]
        else:
            idd2=drawStation(2,prev,l[e],times)     
            prev=l[e]
            idt.append(idd2)
    idt.append(idd)
def message4(times,i):
    root.after(times,lambda: canvas2.delete('line2'))
    idd=root.after(times,lambda: la2_2.config(text=i))
    print(i.split("->"))
    l = i.split("->")
    prev=None
    for e in range(len(l)-1):
        if prev == None:
            prev = l[e]
        else:
            idd2=drawStation(2,prev,l[e],times,'blue','line2')     
            prev=l[e]
            idt.append(idd2)
    idt.append(idd)



root = Tk()
root.title("AI YamaSearch")
root.geometry('900x800')
home = Frame(root)


img_can = Image.open('picture/clear.png')
img_can = img_can.resize((200,120), Image.ANTIALIAS)
photo_2 = ImageTk.PhotoImage(img_can)

allsearchgp = []
allsearchgp2 = []

label1 = Label(root,text= "AI YamaSearch",font = ("Arial",20))
label1.grid(row=0,column=6, columnspan = 6)

la = Label(root, text = "Please Click for Search.", font = ("Arial Bold",12))
la.grid(row =  6 ,column =0 ,columnspan = 7)
la2 = Label(root, text = "", font = ("Arial Bold",12))
la2.grid(row = 7 ,column =0 ,columnspan = 7)
la3 = Label(root, text = "", font = ("Arial Bold",12))
la3.grid(row = 8 ,column =0 ,columnspan = 7)

la_2 = Label(root, text = "Please Click for Search.", font = ("Arial Bold",12))
la_2.grid(row =  6 ,column =9 ,columnspan = 22)
la2_2 = Label(root, text = "", font = ("Arial Bold",12))
la2_2.grid(row = 7 ,column =9 ,columnspan = 22)
la3_2 = Label(root, text = "", font = ("Arial Bold",12))
la3_2.grid(row = 8 ,column =9 ,columnspan = 22)

img = Image.open('picture/search.png')
img = img.resize((200,120), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(img)
btn = Button(root, text = "Search" ,image = photo, command = Call_clicked,borderwidth=0)

btn.grid(column = 7, row = 8, columns = 2)

# get input using entry class

txt =  Entry(root, width = 10, font = ("Arial",18))
txt2 = Entry(root, width = 10, font = ("Arial",18))
txt3 = Entry(root, width = 10, font = ("Arial",18))

# use the grid function as usual to add it to the root
start_text = Label(root,text= "Start :", font = ("Arial",18))
start_text.grid(column = 4, row = 5 ,  columnspan = 5)
txt.grid(column = 6, row = 5)

des_text = Label(root,text= "Destination :", font = ("Arial",18))
des_text.grid(column = 7, row = 5)
txt2.grid(column = 8, row = 5)

delay_text = Label(root, text = "Delay(ms):", font = ("Arial",18))
delay_text.grid(column = 9,row = 5,columnspan = 2)
txt3.grid(column = 11, row = 5,columnspan = 2)



# set focus to entry widget -> can write text right away

txt.focus()

selected = IntVar()
rad1 = Radiobutton(root,text='Uniform_Cost_Search', value=1, variable=selected ,font = ("Arial",12))
rad2 = Radiobutton(root,text='Bi_Direction_Uniform_Cost_Search', value=2, variable=selected, font = ("Arial",12))
rad3 = Radiobutton(root,text='A*_Cost_Search', value=3, variable=selected, font = ("Arial",12))

selected2 = IntVar()
rad1_2 = Radiobutton(root,text='Uniform_Cost_Search', value=1, variable=selected2 ,font = ("Arial",12))
rad2_2 = Radiobutton(root,text='Bi_Direction_Uniform_Cost_Search', value=2, variable=selected2, font = ("Arial",12))
rad3_2 = Radiobutton(root,text='A*_Cost_Search', value=3, variable=selected2, font = ("Arial",12))
# bg_img = Image.open('picture/bg.jpg')
# photo_bg = ImageTk.PhotoImage(bg_img)
# background_label = Label( image=photo_bg)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)


rad1.grid(column = 4, row = 2)
rad2.grid(column = 5, row = 2)
rad3.grid(column = 6, row = 2)


rad1_2.grid(column = 9, row = 2,columnspan = 4)
rad2_2.grid(column = 13, row = 2)
rad3_2.grid(column = 14, row = 2)

# Set the value for Spinbox
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
error_pos = 20

#890,548
WIDTH=668
HEIGHT=441
canvas = Canvas(root, width = WIDTH, height = HEIGHT)
rescale()
img = Image.open("AIMap.PNG")
img = img.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)
canvas.create_image(20,20, anchor=NW, image=img)
canvas.grid(column = 1, row = 1, columnspan = 6)
#tex.delete('1.0', END)

canvas2 = Canvas(root, width = WIDTH, height = HEIGHT)
# rescale()
# img = Image.open("AIMap.PNG")
# img = img.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
# img = ImageTk.PhotoImage(img)
canvas2.create_image(20,20, anchor=NW, image=img)
canvas2.grid(column = 9, row = 1, columnspan = 16)

# canvas = Canvas(root, width = 890, height = 548)  
# img = PhotoImage(file="AIMap.PNG")      
# canvas.create_image(20,20, anchor=NW, image=img)  

canvas.grid(column = 1, row = 1, columnspan = 6)
#canvas.create_line(0,0,100,100,fill ='red')
root.mainloop()