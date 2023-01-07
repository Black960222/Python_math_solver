from pms import *
from tkinter import *
from tkinter import ttk




def solve_func(eq1,eq2):
    temp = check_variable()
    try:
        a = temp[0]
    except:
        txt1.delete(1.0,END)
        txt1.insert(1.0,eval(ent1.get()))
        return
    else:
        if ('=' not in str(ent1.get())):
            txt1.delete(1.0,END)
            txt1.insert(1.0,"請輸入 = 或 <= 或 >= 或 < 或 >")
            txt1.insert(2.0,"使其成為方程式或不等式")
        try:
            b = temp[1]
            ans_a, ans_b = solve_21(eq1,eq2,a,b)
            txt1.delete(1.0,END)
            if(ans_a == ans_b == True):
                txt1.insert(1.0,"無限多組解")
                return
            elif(ans_a == ans_b == None):
                txt1.insert(1.0,"無解")
                return
            else:
                txt1.insert(1.0,"{} = {}\n".format(a,ans_a))
                txt1.insert(2.0,"{} = {}".format(b,ans_b))
                return
        except IndexError:
            pass

    if('^2' in eq1):
        ans = solve_12(eq1,a)
        if(ans[0] == None):
            txt1.delete(1.0,END)
            txt1.insert(1.0,"{} 無實數解".format(a))
        elif(ans[1] == None):
            txt1.delete(1.0,END)
            txt1.insert(1.0,"{}1 = {}2 = {}".format(a,a,ans[0]))
        else:
            txt1.delete(1.0,END)
            txt1.insert(1.0,"{}1 = {}\n".format(a,ans[0]))
            txt1.insert(2.0,"{}2 = {}".format(a,ans[1]))
    else:
        if(">=" in eq1): equal = ">="
        elif("<=" in eq1): equal = "<="
        elif(">" in eq1): equal = ">"
        elif("<" in eq1): equal = "<"  
        else: equal = "="
        ans , equal = solve_11(eq1,a,equal)
        txt1.delete(1.0,END)
        txt1.insert(1.0,"{} {} {}".format(a,equal,str(ans)))


def update_status(*args):
    func = str(ent1.get())
    func2 = str(ent2.get())
    if(func2 != '' and func == ''):
        txt1.delete(1.0,END)
        txt1.insert(1.0,"請先輸入第一式")
        return
    if(func == ''):
        txt1.delete(1.0,END)
        txt1.insert(1.0,"請輸入一元一次方程式/一元二次方程式/一元一次不等式/二元二次方程式")
    
    if('^' in func):
        txt1.delete(1.0,END)
        txt1.insert(1.0,"請輸入一元二次方程式")
        return
    func = check_variable()
    
    if(len(func) == 0):
        txt1.delete(1.0,END)
        txt1.insert(1.0,"計算機模式")
    else:
        if (len(func) == 1):
            txt1.delete(1.0,END)
            if ('>' in func or '<' in func):
                txt1.insert(1.0,"請輸入一元一次不等式") 
            else:
                txt1.insert(1.0,"請輸入一元一次方程式")
        elif (len(func) == 2):
            txt1.delete(1.0,END)
            txt1.insert(1.0,"請輸入二元一次方程式")
        else:
            txt1.delete(1.0,END)
            txt1.insert(1.0,"不支援多於2個未知數的一次方程式")


def check_variable():
    func = str(ent1.get())

    ignore_elements = "1234567890+-*/=.^<>"
    temp = {}
    for x in range(len(ignore_elements)):
        temp['{}'.format(ignore_elements[x])] = ''
    for x, y in temp.items():
        func = func.replace(x,y)
    
    temp = []
    for x in func:
        if (x not in temp):
            temp.append(x)
    return(temp)



# Window
win = Tk()
win.title("Python math solver")


# Elements
ent1 = ttk.Entry(win,width=45,font=("Segoe UI",15))
ent2 = ttk.Entry(win,width=45,font=("Segoe UI",15))
but1 = ttk.Button(win,text="計算/求解",command=lambda: solve_func(ent1.get(),ent2.get()))
txt1 = Text(win,width=35,font=("Microsoft JhengHei UI",15))

ent1.grid(column=0,row=0,sticky=E)
but1.grid(column=1,row=0,rowspan=2,sticky=W)
ent2.grid(column=0,row=1,sticky=E)
txt1.grid(column=0,row=2,columnspan=2,sticky=NSEW)


# Text area (output)
txt1.insert(1.0,"請輸入一元一次方程式/一元二次方程式/一元一次不等式/二元二次方程式")


# Update
ent1.bind("<KeyRelease>",update_status)
ent2.bind("<KeyRelease>",update_status)

# Start
ent1.focus()
if (__name__ == "__main__"):
    win.mainloop()
