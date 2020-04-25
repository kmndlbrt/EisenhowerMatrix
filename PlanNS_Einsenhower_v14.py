import tkinter as tk
import csv

# Eisenhower Matrix
# Last update: 2020-04-24 19:48
# Developed by N.S. in Python 3.8

############################################# methods

def mouse_motion(event):
    global lastx, lasty
    current = event.widget.find_withtag("current")
    if current:
        item_id = current[0]
        if item_id < len(all_activities) + 1:
            status_bar.configure(text="You clicked on item with id %s" % (item_id))
            dx = event.x - lastx
            dy = event.y - lasty
            canvas_1.move(item_id, dx, dy)
            
    else:
        status_bar.configure(text="You didn't click on an item")
    lastx = event.x
    lasty = event.y
   
def mouse_down(event):
    global lastx, lasty
    lastx = event.x
    lasty = event.y

def mouse_release(event):
    global left_space
    current = event.widget.find_withtag("current")
    if current:
        item_id = current[0]-1
        if item_id < len(all_activities) and event.x>left_space:
            ehm_category[item_id] = verify_ehm_category(event.x, event.y)
            #print(all_activities[item_id],ehm_category[item_id])
            write_csv()

def verify_ehm_category(x,y):
    global main_width, main_height, left_space
    cat = 0
    x0 = left_space
    w = main_width
    h = main_height
    if x>x0 and x<x0+w/2 and y<h/2: cat = 1
    if x>x0+w/2 and y<h/2: cat = 2
    if x>x0 and x<x0+w/2 and y>h/2: cat = 3
    if x>x0+w/2 and y>h/2: cat = 4
    return cat

def create_label(x,y,s):
    canvas_1.create_text(x, y, text=s, anchor="w", font='Arial 12')

def write_csv():
    with open(OUTPUT_FILE_1, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Actividad",",","Eisenhower"])
        for i in range(len(all_activities)):
            writer.writerow([all_activities[i],str(ehm_category[i])])

############################################# static variables

INPUT_FILE = "input.csv"
OUTPUT_FILE_1 = "output.csv"

############################################# reading CSV

all_activities = []
ehm_category = []
headings = ""

n_prioridad_1 = 0

with open(INPUT_FILE, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    flag = 0
    for row in csv_reader:
        if flag == 0:
            headings = row
            #print(f'Column names are: {", ".join(row)}')
            flag = 1
        if row["Prioridad"]=="0":
            n_prioridad_1 += 1
        all_activities.append(row["Actividad"])
        ehm_category.append(row["Eisenhower"])

print("n_prioridad_1: ",n_prioridad_1)

############################################# config

left_space = 200
main_width = 600
main_height = 400

lastx = 0
lasty = 0

root = tk.Tk()
root.winfo_toplevel().title("PlaNS")

status_bar = tk.Label(root, anchor="w")
canvas_1 = tk.Canvas(root, background="white",
                     width=main_width+left_space, height=main_height)

left_canvas = tk.Canvas(root, background="#eee", width=1, height=400)
#left_canvas.configure(text="HERE ALL THE ACTIVITIES")

status_bar.pack(side="bottom", fill="x")
left_canvas.pack(side="left", fill="x")
canvas_1.pack(fill="both", expand=True)

############################################# numbered objects texts

dh = 0
for item in all_activities:
    canvas_1.create_text(10, 40+dh, text=item, anchor="w",
                         font='Arial 12 bold', fill = "blue")
    dh += 20
    
canvas_1.bind('<ButtonPress-1>', mouse_down)
canvas_1.bind('<B1-Motion>', mouse_motion)
canvas_1.bind('<ButtonRelease-1>', mouse_release)

############################################# other objects

canvas_1.update()
w = canvas_1.winfo_width() - left_space
h = canvas_1.winfo_height()

create_label(10,15,"Actividades")

create_label(left_space+10,15,"Importante y Urgente")
create_label(left_space+w/2+10,15,"Importante y Urgente")
create_label(left_space+10,h/2+15,"Importante y Urgente")
create_label(left_space+w/2+10,h/2+15,"Importante y Urgente")

wl = 4 # tickness of lines

#vertical lines
canvas_1.create_line(left_space+w/2, 0, left_space+w/2, h, width= wl)
canvas_1.create_line(left_space, 0, left_space, h, width= wl)
canvas_1.create_line(left_space+w-wl, 0, left_space+w-wl, h, width= wl)

#horizontal lines
canvas_1.create_line(left_space+0, h/2, left_space+w, h/2, width= wl)
canvas_1.create_line(left_space+0, wl, left_space+w, wl, width= wl)
canvas_1.create_line(left_space+0, h-wl, left_space+w, h-wl, width= wl)

root.mainloop()
