from tkinter import *
from tkinter import ttk
import random


import time


def partition(data, head, tail, draw_data, time_tick):
    border = head
    pivot = data[tail]
    draw_data(data, get_color_array(len(data), head, tail, border, border))
    time.sleep(time_tick)
    for j in range(head, tail):
        if data[j] < pivot:
            draw_data(data, get_color_array(len(data), head, tail, border, j, True))
            time.sleep(time_tick)
            data[border], data[j] = data[j], data[border]
            border += 1
        draw_data(data, get_color_array(len(data), head, tail, border, j))
        time.sleep(time_tick)
    draw_data(data, get_color_array(len(data), head, tail, border, tail, True))
    time.sleep(time_tick)
    data[border], data[tail] = data[tail], data[border]
    return border


def quick_sort(data, head, tail, draw_data, time_tick):
    if head < tail:
        partitionIdx = partition(data, head, tail, draw_data, time_tick)

        quick_sort(data, head, partitionIdx - 1, draw_data, time_tick)

        quick_sort(data, partitionIdx + 1, tail, draw_data, time_tick)


def bubble_sort(data, drawData, timeTick):
    size = len(data)
    for i in range(size-1):
        for j in range(size-i-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
                drawData(data, ['#F7E806' if x == j or x == j+1 else '#0CA8F6' for x in range(len(data))] )
                time.sleep(timeTick)
                
    drawData(data, ['#0CA8F6' for x in range(len(data))])

def merge(data, start, mid, end, drawData, timeTick):
    p = start
    q = mid + 1
    tempArray = []

    for i in range(start, end+1):
        if p > mid:
            tempArray.append(data[q])
            q+=1
        elif q > end:
            tempArray.append(data[p])
            p+=1
        elif data[p] < data[q]:
            tempArray.append(data[p])
            p+=1
        else:
            tempArray.append(data[q])
            q+=1

    for p in range(len(tempArray)):
        data[start] = tempArray[p]
        start += 1

def merge_sort(data, start, end, drawData, timeTick):
    if start < end:
        mid = int((start + end) / 2)
        merge_sort(data, start, mid, drawData, timeTick)
        merge_sort(data, mid+1, end, drawData, timeTick)

        merge(data, start, mid, end, drawData, timeTick)

        drawData(data, ['#BF01FB' if x >= start and x < mid else '#F7E806' if x == mid 
                        else '#4204CC' if x > mid and x <=end else '#0CA8F6' for x in range(len(data))])
        time.sleep(timeTick)

    drawData(data, ['#0CA8F6' for x in range(len(data))])


def get_color_array(dataLen, head, tail, border, cur_idx, isSwaping=False):
    colorArray = []
    for i in range(dataLen):

        if i >= head and i <= tail:
            colorArray.append("Grey")
        else:
            colorArray.append("White")

        if i == tail:
            colorArray[i] = "Blue"
        elif i == border:
            colorArray[i] = "Red"
        elif i == cur_idx:
            colorArray[i] = "Yellow"

        if isSwaping:
            if i == border or i == cur_idx:
                colorArray[i] = "Green"

    return colorArray


def generate():

    global data

    minval = int(minEntry.get())

    maxval = int(maxEntry.get())

    sizeval = int(sizeEntry.get())

    data = []
    for _ in range(sizeval):
        data.append(random.randrange(minval, maxval + 1))

    draw_data(data, ["Red" for _ in range(len(data))])


def draw_data(data, colorlist):
    canvas.delete("all")
    can_height = 380
    can_width = 550
    x_width = can_width / (len(data) + 1)
    offset = 30
    spacing = 10

    normalized_data = [i / max(data) for i in data]

    for i, height in enumerate(normalized_data):

        x0 = i * x_width + offset + spacing
        y0 = can_height - height * 340

        x1 = ((i + 1) * x_width) + offset
        y1 = can_height

        canvas.create_rectangle(x0, y0, x1, y1, fill=colorlist[i])
        canvas.create_text(x0 + 2, y0, anchor=SE, text=str(data[i]))
    root.update_idletasks()


def start_algorithm():
    global data

    if not data:
        return

    if algmenu.get() == "Quick Sort":
        quick_sort(data, 0, len(data) - 1, draw_data, speedbar.get())
        draw_data(data, ["Green" for x in range(len(data))])
    
    elif algmenu.get() == "Bubble Sort":
        bubble_sort(data, draw_data,  speedbar.get())

    elif algmenu.get() == "Merge Sort":
        merge_sort(data, 0, len(data)-1, draw_data, speedbar.get())

if __name__ == "__main__":
    root = Tk()
    root.title("Quick Sort Visualizer")


    root.maxsize(900, 600)
    root.config(bg="Black")

    select_alg = StringVar()
    data = []
    Mainframe = Frame(root, width=600, height=200, bg="Grey")
    Mainframe.grid(row=0, column=0, padx=10, pady=5)

    canvas = Canvas(root, width=600, height=380, bg="Grey")
    canvas.grid(row=1, column=0, padx=10, pady=5)


    Label(Mainframe, text="ALGORITHM", bg="Grey").grid(
        row=0, column=0, padx=5, pady=5, sticky=W
    )


    algmenu = ttk.Combobox(Mainframe, textvariable=select_alg, values=["Quick Sort", "Bubble Sort", "Merge Sort"])
    algmenu.grid(row=0, column=1, padx=5, pady=5)
    algmenu.current(0)


    Button(Mainframe, text="START", bg="#3fb618", command=start_algorithm).grid(
        row=1, column=3, padx=5, pady=5
    )


    speedbar = Scale(
        Mainframe,
        from_=0.10,
        to=2.0,
        length=100,
        digits=2,
        resolution=0.2,
        orient=HORIZONTAL,
        label="Select Speed",
    )
    speedbar.grid(row=0, column=2, padx=5, pady=5)


    sizeEntry = Scale(
        Mainframe, from_=3, to=60, resolution=1, orient=HORIZONTAL, label="Size"
    )
    sizeEntry.grid(row=1, column=0, padx=5, pady=5)


    minEntry = Scale(
        Mainframe, from_=0, to=10, resolution=1, orient=HORIZONTAL, label="Minimum Value"
    )
    minEntry.grid(row=1, column=1, padx=5, pady=5)


    maxEntry = Scale(
        Mainframe, from_=10, to=100, resolution=1, orient=HORIZONTAL, label="Maximum Value"
    )
    maxEntry.grid(row=1, column=2, padx=5, pady=5)


    Button(Mainframe, text="Generate", bg="#ff7518", command=generate).grid(
        row=0, column=3, padx=5, pady=5
    )
    
    Button(root, text="Quit", command=root.destroy).grid(
            row=0, column=3, padx=5, pady=5
        )

    root.mainloop()
