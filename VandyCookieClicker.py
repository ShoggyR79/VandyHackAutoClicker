from tkinter import *
click = 0
amount = 1
cost1 = 50
cost2 = 250
cost3 = 500
cost4 = 1000
window = Tk()
window.title("Clicker game")
window.geometry('400x250')
lbl = Label(window, text="Start Clicking!")
lbl.grid(column=0, row=0)

milk_man = Label(window, text="$"+str(cost1))
milk_man.grid(column=0, row=10)
ingredients1 = Label(window, text="$"+str(cost2))
ingredients1.grid(column=0, row=20)
grandmas = Label(window, text="$"+str(cost3))
grandmas.grid(column=0, row=30)
factory = Label(window, text="$"+str(cost4))
factory.grid(column=0, row=40)
def clicked():
    global click
    global amount
    click += amount
    lbl.configure(text= click)
def buy1():    
    global amount    
    global click    
    global cost1    
    if click >= cost1:    
      click = click - cost1    
      amount = amount + 1    
      cost1 = round(cost1*1.15)   
      milk_man.configure(text="$"+str(cost1))
      lbl.configure(text=click)
def buy2():    
    global amount    
    global click    
    global cost2    
    if click >= cost2:   
      click = click - cost2    
      amount = amount + 5    
      cost2 = round(cost2*1.15)    
      ingredients1.configure(text="$"+str(cost2))    
      lbl.configure(text=click)
def buy3():   
    global amount   
    global click    
    global cost3    
    if click >= cost3:    
      click = click - cost3    
      amount = amount + 10    
      cost3 = round(cost4*1.15)    
      grandmas.configure(text="$"+str(cost3))    
      lbl.configure(text=click)
def buy4():   
    global amount   
    global click    
    global cost3    
    if click >= cost4:    
      click = click - cost4    
      amount = amount + 20    
      cost4 = round(cost3*1.15)    
      factory.configure(text="$"+str(cost4))    
      lbl.configure(text=click)
cookie = PhotoImage(file='vandyResized.png')
btn = Button(window, image=cookie, command=clicked)
btn.grid(column=10, row=0)
btn = Button(window, text="Milk", command=buy1)
btn.grid(column=10, row=10)
btn = Button(window, text="Ingredients", command=buy2)
btn.grid(column=10, row=20)
btn = Button(window, text="Grandmas", command=buy3)
btn.grid(column=10, row=30)
btn = Button(window, text="Factory", command=buy4)
btn.grid(column=10, row=40)
window.mainloop()
