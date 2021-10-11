# coding:utf-8


import tkinter as tk
from tkinter import ttk, messagebox
import copy
from source import getData, GA, plot


def formatPrint(data: dict):
    list_ = list(data)
    list_.sort()
    num_str = " number "
    city_str = "   city    "
    title = num_str + city_str + "         "
    print(title*3)
    for i in range(0, len(list_), 3):
        d1 = data.get(i)
        if d1 is None:
            unit1 = ""
        else:
            d1 = d1[0]
            unit1 = " " * 3 + str(i) + " " * (len(num_str) - 3 - len(str(i))) + " " * 4 + d1 + " " * (
                        len(city_str) - 4 - len(d1)) + "       "
        d2 = data.get(i+1)
        if d2 is None:
            unit2 = ""
        else:
            d2 = d2[0]
            unit2 = " " * 3 + str(i + 1) + " " * (len(num_str) - 3 - len(str(i + 1))) + " " * 4 + d2 + " " * (
                        len(city_str) - 4 - len(d2)) + "       "
        d3 = data.get(i+2)
        if d3 is None:
            unit3 = ""
        else:
            d3 = d3[0]
            unit3 = " " * 3 + str(i + 2) + " " * (len(num_str) - 3 - len(str(i + 2))) + " " * 4 + d3 + " " * (
                        len(city_str) - 4 - len(d3)) + "     "
        print(unit1 + unit2 + unit3)


def getUserSelection(data):
    user_selection = {}
    formatPrint(data)
    print("select your route with number in the right side of city.\nevery number separate with blank.")
    print("example: \n>>> 0 1 2\nthis means a route Beijing -> Tianjin -> Shanghai -> Beijing")
    string = input("your route >>> ")
    route = string.split()
    if len(route) != len(set(route)):
        print("repeat element in your route.")
        exit(0)
    for i in route:
        try:
            i = int(i)
            if i < 0 or i > 32:
                print("unexpected character in your route.")
                exit(0)
        except ValueError as e:
            print("unexpected character in your route.\n" + e)
            exit(0)
        user_selection[i] = copy.deepcopy(data[i])
    a = input("the number of generation >>> ")
    b = input("size of group >>> ")
    return [user_selection, int(b), int(a)]


"""
def main():
    data = getData()
    your_data = getUserSelection(data)
    top = GA.start(n=your_data[2], N=your_data[1], data=your_data[0])
    plot(data, top.route)
    print("route -> ", top.route)
    print("distance -> ", top.distance)

"""
class UI():
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("遗传算法解决TSP问题")
        self.win.resizable(0, 0)
        self.data = getData()
        self.route = []
        self.chkVar = [-1]*34
        self.check = [-1]*34
        self.combobox = None
        self.start_city_var = None
        self.start_point = ""
        self.i = 0
        self.init_ui()
        self.win.mainloop()


    # init check boxes
    def init_ui(self):
        values = []
        for key in self.data:
            self.chkVar[key] = tk.IntVar()
            self.check[key] = tk.Checkbutton(self.win, text=self.data[key][0],
                                             onvalue=key, offvalue=-1, variable=self.chkVar[key])
            self.check[key].deselect()
            if key % 6 == 0:
                self.i += 1
            self.check[key].grid(column=key%6+1, row=self.i, sticky=tk.W)
            values.append(self.data[key][0])

        # combobox
        self.start_city_var = tk.StringVar()
        self.combobox = ttk.Combobox(self.win, width=8, textvariable=self.start_city_var)
        self.combobox['values'] = tuple(values)
        self.combobox.grid(column=2, row=self.i+1)
        ttk.Label(self.win, text="选择起点").grid(column=1, row=self.i+1)

        # confirm button
        ok = tk.Button(self.win, text="确定", command=self.handle)
        ok.grid(column=6, row=self.i + 1)

        # select all button
        select = tk.Button(self.win, text="全选", command=self.select_all)
        select.grid(column=5, row=self.i+1)

        # clear all button
        clear = tk.Button(self.win, text="清除已选", command=self.clear_all)
        clear.grid(column=4, row=self.i + 1)

    # select all cities
    def select_all(self):
        for key in self.data:
            self.chkVar[key].set(key)

    # clear all selected cities
    def clear_all(self):
        for key in self.data:
            self.chkVar[key].set(-1)

    def handle(self):
        self.start_point = self.start_city_var.get()
        for key in self.data:
            value = self.chkVar[key].get()
            if value == key:
                self.route.append(value)
            if self.start_point == self.data[key][0]:
                self.start_point = key
        if self.start_point == "":
            messagebox.showinfo("提示", "请选择起点城市")
            self.route.clear()
            return
        if self.start_point not in self.route:
            self.route.insert(0, self.start_point)
        dictionary = {}
        if len(self.route) < 3:
            messagebox.showinfo("提示", "请至少选择3个城市（包含起点）")
            return
        for i in self.route:
            dictionary[i] = self.data[i]
        top = GA.start(data=dictionary)
        plot(self.data, top.route, self.start_point)
        route = top.data[top.route[0]][0]
        for i in top.route[1:]:
            route = route + "->" + top.data[i][0]
        messagebox.showinfo("info", "最佳路线: %s\n路线距离：%d" % (route, top.distance))
        self.route.clear()
        self.start_point = ""



if __name__ == "__main__":
    ui_instance = UI()



