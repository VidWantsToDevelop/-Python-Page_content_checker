from tkinter import *
from deploy import *
from threading import Thread


window = Tk()
window.title = "Let's catch some packets"
window.geometry("350x150")
window.configure(background="#222222")
window.maxsize(350, 150)
main_frame = Frame(window, bg='#222222')
main_frame.pack()
label = Label(main_frame, text="Copy your URL in the field below",
              bg='#222222', fg='white', pady=5, padx=5)
label.grid(column=0, row=0, pady=5, padx=5)
input = Entry(main_frame)
input.grid(column=0, row=1, pady=5, padx=5, ipadx=15, ipady=5)
start_btn = Button(main_frame, text='Trace', padx=5,
                   pady=5, command=lambda: check(input.get(), window))
start_btn.grid(column=0, row=2, pady=5, padx=5, sticky=W)
stop_btn = Button(main_frame, text='Stop', padx=5,
                  pady=5, command=lambda: stop())
stop_btn.grid(column=0, row=2, padx=5, pady=5, sticky=E)
window.mainloop()
