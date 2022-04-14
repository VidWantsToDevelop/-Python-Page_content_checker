from win10toast import ToastNotifier
import time
import hashlib
import os
from urllib.request import urlopen, Request
from threading import Thread
import threading
from tkinter import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from datetime import datetime


def check(url, root, q, entry):
    print("check")
    delay = int(entry) / 1000
    try:
        trace = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    except Exception as e:
        print("Wrong URL")
        return
    print("The program is running")
    global running
    running = True
    global notified
    notified = False
    while running:
        print("The amount of active threads is: "
              + str(threading.active_count()))
        try:
            response = urlopen(trace).read()
            firstHash = hashlib.sha224(response).hexdigest()
            print(firstHash)

            time.sleep(delay)

            response = urlopen(trace).read()
            secondHash = hashlib.sha224(response).hexdigest()
            print(secondHash)
            if firstHash == secondHash:
                print("No change")
                q.put("No change")
                continue
            else:
                if notified == False:
                    notification()
                print("Change revealed")
                q.put("Change revealed")
                response = urlopen(trace).read()
                firstHash = hashlib.sha224(response).hexdigest()

                time.sleep(delay)
            print("deploy")
            print(q.qsize())
        except Exception as e:
            print(e)


def start(url, root):
    global th
    th = Thread(target=check(url, root))
    print(th)
    th.start()


def notification():
    global notified
    print(notified)
    notified = True
    toast = ToastNotifier()
    toast.show_toast("Be aware", "The page content has been updated")


def stop(object):
    global running
    running = False
    object.status.tag_configure("tag_name", justify='center')
    object.status.delete("1.0", "end")
    object.status.insert(END, "Stopped")
    object.status.tag_add("tag_name", "1.0", "end")


def generate_report(app):
    date = datetime.today()
    first_row_grid = ('GRID', (0, 0), (-1, -1), 0.25, colors.black)
    first_row_font = ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-BoldOblique')
    titles = ["Time", "No changes", "Updates", "Requests"]
    list_of_elements = []
    table_data = []
    table_data.append(titles)

    #Get the data out of the listbox
    data = app.listbox.get(0, END)

    #Formate data
    for i in range(0, len(data), 5):
        single_row = []
        single_row.append(data[i+1])
        single_row.append(data[i+2].split(": ")[1])
        single_row.append(data[i+3].split(": ")[1])
        single_row.append(data[i+4].split(": ")[1])
        table_data.append(single_row)
    print(table_data)

    #Generate pdf
    style_sheet = getSampleStyleSheet()

    title_p = Paragraph("Report of: {}".format(
        date.strftime("%B %d, %Y")), style_sheet["Heading1"])
    list_of_elements.append(title_p)

    table = Table(table_data, colWidths=70, rowHeights=20, hAlign='LEFT')
    table.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                               ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), first_row_grid, first_row_font]))
    list_of_elements.append(table)

    try:
        file = SimpleDocTemplate("./reports/report.pdf")
        file.build(list_of_elements)
    except:
        os.mkdir("reports")
        file = SimpleDocTemplate("./reports/report.pdf")
        file.build(list_of_elements)
