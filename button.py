import RPi.GPIO as GPIO
import time, threading
import abc

class Button:
    __metaclass__ = abc.ABCMeta

    def __init__(self):

        self.BUTTONLIST = [23] #button pin(s)
        GPIO.setmode(GPIO.bcm) #reference by Broadcom
        for button in self.BUTTONLIST: #for if we want to add more buttons later
            GPIO.setup(button, GPIO.IN)
        threading.Thread(target=self.check_buttons).start()

    def check_buttons(self):
        current_button_state = [False, False, False, False]
        previous_button_state = [False, False, False, False]

        while True:
            for i in range(len(self.BUTTONLIST)):
                current_button_state[i] = GPIO.input(self.BUTTONLIST[i])
                if not previous_button_state[i] and current_button_state[i]:
                    #if current_button_state is True, then Not False == True
                    #so it will set the button as pushed.
                    self.button_pushed(i)
                previous_button_state[i] = current_button_state[i]
            time.sleep(0.05)

    @abc.abstractmethod
    def button_pushed(self, button):
        #we can change what this does b/c/ it is an abstract method.
        return
