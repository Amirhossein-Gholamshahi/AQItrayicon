import os.path
import sys
import PIL.Image
import multiprocessing as mp
import PyInstaller
import requests
import auto_py_to_exe
import winotify
import pystray
from winotify import Notification, audio
import time
from bs4 import BeautifulSoup
url = 'https://airnow.tehran.ir/'


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def show_notif(app_id, title, icon_path, tag):  # shows the notification
    toast = Notification(app_id=app_id, title=title, msg=tag, duration="short",
                         icon=icon_path)
    toast.set_audio(audio.SMS, loop=False)
    toast.add_actions(label="More info here", launch=url)
    toast.show()


def get_current_aqi():  # gets the current AQI value from url
    try:  # try and except for probable connection loss
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        tag = int(soup.find_all("span")[18].text)  # gets current AQI from the url
        if tag >= 150:
            show_notif("Current AQI", "Unhealthy", resource_path("additional files/AQIMORE150.jpg"), tag)
        if 100 <= tag < 150:
            show_notif("Current AQI", "Unhealthy for Sensitive Groups", resource_path("additional files/AQIBET100150.jpg"), tag)
        if tag < 100:
            show_notif("Current AQI", "Good", resource_path("additional files/AQILESS100.jpg"), tag)
    except requests.exceptions.RequestException as request_err:  # show notification if there is any connection error
        toast = Notification(app_id="Connection Error", title="Error",
                             msg="There is a problem with your connection!",
                             duration="short", icon=resource_path("additional files/error.png")
                             )
        toast.set_audio(audio.SMS, loop=False)
        toast.show()


def get_last_24hrs_aqi():  # gets the average of last days AQI  from url
    try:  # try and except for probable connection loss
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        tag = int(soup.find_all("span")[13].text)  # gets last 24-hrs AQI from the url
        if tag >= 150:
            show_notif("Last 24 hrs AQI", "Unhealthy", resource_path("additional files/AQIMORE150.jpg"), tag)
        if 100 <= tag < 150:
            show_notif("Last 24 hrs AQI", "Unhealthy for Sensitive Groups", resource_path("additional files/AQIBET100150.jpg"), tag)
        if tag < 100:
            show_notif("Last 24 hrs AQI", "Good", resource_path("additional files/AQILESS100.jpg"), tag)
    except requests.exceptions.RequestException as request_err:  # show notification if there is any connection error
        toast = Notification(app_id="Connection Error", title="Error",
                             msg="There is a problem with your connection!",
                             duration="short", icon=resource_path("additional files/error.png")
                             )
        toast.set_audio(audio.SMS, loop=False)
        toast.show()


def get_notif_everyn(n):  # send notification every n minutes
    sec = n * 60
    while True:
        try:  # try and except for probable connection loss
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            tag = int(soup.find_all("span")[18].text)  # gets AQI from the url
            if tag >= 150:
                show_notif("Current AQI", "Unhealthy", resource_path("additional files/AQIMORE150.jpg"),tag)
                time.sleep(sec)
            if 100 <= tag < 150:
                show_notif("Current AQI", "Unhealthy for Sensitive Groups", resource_path("additional files/AQIBET100150.jpg"),tag)
                time.sleep(sec)
            if tag < 100:
                show_notif("Current AQI", "Good", resource_path("additional files/AQILESS100.jpg"), tag)
                time.sleep(sec)
        except requests.exceptions.RequestException as request_err:  # show notification if there is any connection error
            toast = Notification(app_id="Connection Error", title="Error",
                                 msg="There is a problem with your connection!",
                                 duration="short", icon=resource_path("additional files/error.png")
                                 )
            toast.set_audio(audio.SMS, loop=False)
            toast.show()
            break


def get_notif_every_5mins():
    get_notif_everyn(5)


def get_notif_every_15mins():
    get_notif_everyn(15)


def get_notif_every_30mins():
    get_notif_everyn(30)


def get_notif_every_1hrs():
    get_notif_everyn(60)


if __name__ == '__main__':
    mp.freeze_support()
    p1 = mp.Process(target=get_notif_every_5mins)
    p2 = mp.Process(target=get_notif_every_15mins)
    p3 = mp.Process(target=get_notif_every_30mins)
    p4 = mp.Process(target=get_notif_every_1hrs)


    def exit_program():
        icon.stop()
        if p1.is_alive():
            p1.terminate()
        if p2.is_alive():
            p2.terminate()
        if p3.is_alive():
            p3.terminate()
        if p4.is_alive():
            p4.terminate()


    def start_p1():
        if p2.is_alive():
            p2.terminate()
        if p3.is_alive():
            p3.terminate()
        if p4.is_alive():
            p4.terminate()
        p1.start()


    def start_p2():
        if p1.is_alive():
            p1.terminate()
        if p3.is_alive():
            p3.terminate()
        if p4.is_alive():
            p4.terminate()
        p2.start()

    def start_p3():
        if p1.is_alive():
            p1.terminate()
        if p2.is_alive():
            p2.terminate()
        if p4.is_alive():
            p4.terminate()
        p3.start()

    def start_p4():
        if p1.is_alive():
            p1.terminate()
        if p3.is_alive():
            p3.terminate()
        if p2.is_alive():
            p2.terminate()
        p4.start()


    image = PIL.Image.open(resource_path("additional files/AQIicon.png"))
    icon = pystray.Icon("AirQuality index", image, menu=pystray.Menu(
        pystray.MenuItem("Get current AQI", get_current_aqi),
        pystray.MenuItem("Get last 24 hrs AQI", get_last_24hrs_aqi),
        pystray.MenuItem("Get notification every", pystray.Menu(
            pystray.MenuItem("5 mins", start_p1),
            pystray.MenuItem("15 mins", start_p2),
            pystray.MenuItem("30 mins", start_p3),
            pystray.MenuItem("1 hrs", start_p4)
        )),
        pystray.MenuItem("Exit", exit_program)
    ))
    icon.run()



