from win10toast import ToastNotifier
import time
import hashlib
from urllib.request import urlopen, Request
from threading import Thread


def check(url, root):
    try:
        trace = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    except Exception as e:
        print("Wrong URL")
        return
    print("The program is running")
    global running
    running = True
    while running:
        root.update()
        try:
            response = urlopen(trace).read()
            firstHash = hashlib.sha224(response).hexdigest()
            print(firstHash)

            time.sleep(1)

            response = urlopen(trace).read()
            secondHash = hashlib.sha224(response).hexdigest()
            print(secondHash)
            if firstHash == secondHash:
                print("No change")
                continue
            else:
                print("Change revealed")
                response = urlopen(trace).read()
                firstHash = hashlib.sha224(response).hexdigest()

                time.sleep(1)
        except Exception as e:
            print(e)


def start(url, root):
    global th
    th = Thread(target=check(url, root))
    th.start()


def stop():
    global running
    running = False
