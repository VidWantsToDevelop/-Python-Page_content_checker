from win10toast import ToastNotifier
import time
import hashlib
from urllib.request import urlopen, Request
from threading import Thread
import threading
from tkinter import *


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
