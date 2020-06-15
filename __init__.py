from pymouse import PyMouse
from time import sleep
import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

from PIL import Image
import pytesseract
import cv2
import os

from mycroft import MycroftSkill, intent_file_handler

class DuoAnswer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('call.duo.intent')
    def handle_call_duo(self, message):
        m = PyMouse()
        k = PyKeyboard()
        contacts = ["dad", "slayer"]
        name = message.data['contact'].lower()
        if name == "kevin":
            name = "slayer"

        if name in contacts:
            response = {'contact': name}
            self.speak_dialog('call.duo', data=response)
            command = "wmctrl -a \"Google Duo\""
            os.system(command)
            sleep(.5)
            m.click(420,90) # Click in the Duo text box
            sleep(0.5)
            k.tap_key('Delete',n=6,interval=0.05) # Delete existing characters
            k.type_string(name) # Type name of Duo contact
            sleep(0.2)
            k.tap_key('Return') # Hit Return to select contact
            sleep(1.5)
            m.click(470,380) # Click on Video Call button
        else:
            response = {'contact': name}
            self.speak_dialog('nocontact.duo', data=response)

    @intent_file_handler('answer.duo.intent')
    def handle_answer_duo(self, message):
        if is_call_incoming():
            m = PyMouse()
            m.click(470,440) # Click Answer button
        else:
            self.speak_dialog('noincoming.duo')

    @intent_file_handler('ignore.duo.intent')
    def handle_ignore_duo(self, message):
        if is_call_incoming():
            m = PyMouse()
            m.click(320,430) # Click Decline button
        else:
            self.speak_dialog('noincoming.duo')

    @intent_file_handler('end.duo.intent')
    def handle_end_duo(self, message):
        if is_call_active():
            m = PyMouse()
            m.click(400,440) # Click Hang Up button
        else:
            self.speak_dialog('noactive.duo')


"""    def screenshotocr(filename, x, y, w, h):
        win = Gdk.get_default_root_window()
        pb = Gdk.pixbuf_get_from_window(win, x, y, w, h)

        if (pb != None):
            pb.savev(filename,"png", (), ())
            # load the example image and convert it to grayscale
            image = cv2.imread(filename)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#            gray = cv2.medianBlur(gray, 3)
            # write the grayscale image to disk as a temporary file so we can
            # apply OCR to it
            filename = "/tmp/{}.png".format(os.getpid())
            cv2.imwrite(filename, gray)

            # load the image as a PIL/Pillow image, apply OCR, and then delete
            # the temporary file
            text = pytesseract.image_to_string(Image.open(filename))
            return text

    def is_call_active():
        command = "wmctrl -a \"Google Duo\""
        os.system(command)
        sleep(.25)

        m = PyMouse
        m.move(400,440)
        sleep(.5)

        k = self.screenshotocr("/tmp/screenshot.png", 340, 410, 125, 50)
        if(k == "End call"):
            return True
        else:
            return False

    def is_call_incoming():
        command = "wmctrl -a \"Google Duo\""
        os.system(command)
        sleep(.5)
        k = self.screenshotocr("/tmp/screenshot.png", 280, 95, 250, 25)

        if(k == "Duo video call" or k == "Duo voice call"):
            b = screenshotocr("/tmp/screenshot1.png", 280, 130, 150, 40)
            return True
            #check if caller is valid contact
            #if b.lower() in contacts:
            #    return True
            #else:
            #    return True
        else:
            return False


    @intent_file_handler('answer.duo.intent')
    def handle_answer_duo(self, message):
        if is_call_incoming():
            m = PyMouse()
            m.click(470,440) # Click Answer button
        else:
            self.speak_dialog('noincoming.duo')

    @intent_file_handler('ignore.duo.intent')
    def handle_ignore_duo(self, message):
        if is_call_incoming():
            m = PyMouse()
            m.click(320,430) # Click Decline button
        else:
            self.speak_dialog('noincoming.duo')

    @intent_file_handler('end.duo.intent')
    def handle_end_duo(self, message):
        if is_call_active():
            m = PyMouse()
            m.click(400,440) # Click Hang Up button
        else:
            self.speak_dialog('noactive.duo')
"""

def create_skill():
    return DuoAnswer()

def screenshotocr(filename, x, y, w, h):
    win = Gdk.get_default_root_window()
    pb = Gdk.pixbuf_get_from_window(win, x, y, w, h)

    if (pb != None):
        pb.savev(filename,"png", (), ())
        # load the example image and convert it to grayscale
        image = cv2.imread(filename)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#        gray = cv2.medianBlur(gray, 3)
        # write the grayscale image to disk as a temporary file so we can
        # apply OCR to it
        filename = "/tmp/{}.png".format(os.getpid())
        cv2.imwrite(filename, gray)

        # load the image as a PIL/Pillow image, apply OCR, and then delete
        # the temporary file
        text = pytesseract.image_to_string(Image.open(filename))
        return text

def is_call_active():
    command = "wmctrl -a \"Google Duo\""
    os.system(command)
    sleep(.25)

    m = PyMouse()
    m.move(400, 400)
    sleep(.5)

    k = screenshotocr("/tmp/screenshot.png", 340, 410, 125, 50)
    if(k == "End call"):
        return True
    else:
        return False

def is_call_incoming():
    command = "wmctrl -a \"Google Duo\""
    os.system(command)
    sleep(.5)
    k = screenshotocr("/tmp/screenshot.png", 280, 95, 250, 25)

    if(k == "Duo video call" or k == "Duo voice call"):
        b = screenshotocr("/tmp/screenshot1.png", 280, 130, 150, 40)
        return True
        #check if caller is valid contact
        #if b.lower() in contacts:
        #    return True
        #else:
        #    return True
    else:
        return False
