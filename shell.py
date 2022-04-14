import tkinter as tk
from tkinter import *
from deploy import *
from tkinter import ttk, messagebox
from tkinter.messagebox import showerror
from threading import Thread
from queue import Queue
from datetime import datetime


class App(tk.Tk):

    q = Queue()

    def __init__(self):
        super().__init__()

        self.window = Tk()
        self.window.title = "Let's catch some changes"
        self.window.geometry("350x410")
        self.window.configure(background="#222222")
        self.window.maxsize(350, 410)
        self.main_frame = Frame(self.window, bg='#222222')
        self.main_frame.pack()
        self.label = Label(self.main_frame, text="Copy your URL in the field below",
                           bg='#222222', fg='white', pady=5, padx=5)
        self.label.grid(column=0, row=0, pady=5, padx=5)
        self.input = Entry(self.main_frame)
        self.input.grid(column=0, row=1, pady=5, padx=5, ipadx=15, ipady=5)
        self.start_btn = Button(self.main_frame, text='Trace', padx=5,
                                pady=5, command=self.startFunc)
        self.start_btn.grid(column=0, row=3, pady=5, padx=5, sticky=W)

        self.delay_label = Label(
            self.main_frame, text="delay(ms)", fg='white', bg="#222222")
        self.delay_label.grid(column=0, row=2, padx=5, pady=5)

        self.delay_entry = Entry(self.main_frame, width=8)
        self.delay_entry.grid(column=0, row=3, padx=5, pady=5)

        self.stop_btn = Button(self.main_frame, text='Stop', padx=5,
                               pady=5, command=lambda: stop(self))
        self.stop_btn.grid(column=0, row=3, padx=5, pady=5, sticky=E)

        self.status = Text(self.main_frame, height=1, width=15)
        self.status.tag_configure("tag_name", justify='center')
        self.status.insert(END, "Waiting")
        self.status.tag_add("tag_name", "1.0", "end")
        self.status.grid(column=0, row=4, padx=5, pady=5, sticky=N)

        self.listbox = Listbox(self.main_frame)
        self.listbox.grid(column=0, row=5, padx=5, pady=5)

        self.report_btn = Button(
            self.main_frame, text='Generate a report', command=lambda: generate_report(self))
        self.report_btn.grid(column=0, row=6, padx=5, pady=5)

        self.help_btn = Button(self.main_frame, text='?', padx=7.5, pady=3,
                               command=self.instructions)
        self.help_btn.grid(column=0, row=6, sticky=E, pady=5)

        self.window.after(5000, self.checkQueue)

    def startFunc(self):
        self.th = Thread(target=check, args=(
            self.input.get(), self.window, self.q, self.delay_entry.get()))
        print(self.th)
        self.status.tag_configure("tag_name", justify='center')
        self.status.delete("1.0", "end")
        self.status.insert(END, "Tracing")
        self.status.tag_add("tag_name", "1.0", "end")
        self.th.start()

    def instructions(self):
        messagebox.showinfo("A brief instruction", "Delay between requests can be set in the input field (but the delay hardly depends on the hosting server of the website). Generate report button will create a pdf-formatted report within the \"reports\" folder. Enjoy!")

    def checkQueue(self):
        if self.status.get("1.0", "end-1c") != "Waiting" and self.status.get("1.0", "end-1c") != "Stopped":
            try:
                upd = ""
                updated = 0
                no_change = 0
                count = 0
                while(self.q.qsize() > 0):
                    print("LOOOP")
                    count = count+1
                    upd = self.q.get_nowait()
                    if upd == "No change":
                        no_change = no_change + 1
                    elif upd == "Change revealed":
                        updated = updated + 1
                print("SAS" + str(upd))
                self.listbox.insert(1, "***********")
                self.listbox.insert(1, "Am-t of requests: {}".format(count))
                self.listbox.insert(1, "Updates: {}".format(updated))
                self.listbox.insert(1, "No changes: {}".format(no_change))
                self.listbox.insert(1, "{}".format(
                    datetime.now().strftime("%H:%M:%S")))
                self.q.task_done()
            except:
                print('empty')
                print(self.q.qsize())

        self.window.after(15000, self.checkQueue)


if __name__ == "__main__":
    app = App()
    app.withdraw()
    app.mainloop()
