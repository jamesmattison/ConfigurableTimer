"""
ConfigurableTimer .01
----------------------

Requirements:
playsound
twilio.rest
(XPBX), (ALERTMX)
Classes:
class Timer
    class TimerThread
    class TimerTarget
    class TimerError
    class OneShot (not implemented)


"""

from datetime import datetime
from time import sleep, strftime
import sys
import threading

SEND_TO = "test@example.com" # change before use
SMS_TO = "+18008188888" #if 1-800-818-8888


######################## superclass Timer #####################################


class Timer:
    """ Timer: replaces alarm class. Starts TimerThread.

    TimerThread then executes the timer targer (todo).
    Use:
        alm = Alarm("sms|call|email|wav", testmode)
        alm.start_timer(when, message, todo="sms", testmode=False, verbose=True
        *args, **kwargs)
    """
    #  Timer. variables (superclass vars)
    i = 0
    FAIL = "\u001b[41m[FAIL]\u001b[47;0m"
    OK = "\u001b[32m[ OK ]\u001b[47;0m"
    allowed_todos = ["sms", "call", "email", "wav"]
    timer_threads = []

    def __init__(self, alarm_type, fn="/vx/mond0lib/STILL.wav", testmode=False, verbose=True):
        self.fn = fn
        self.alarm_type = "sms"
        if alarm_type in Timer.allowed_todos:
            self.todo = alarm_type
        if alarm_type == "wav":
            if fn is None:
                print("You must specify fn to a proper WAV file!")

        self.testmode = testmode
        self.verbose = verbose
        self.tn = "xTT-" + str(Timer.i)
        self.timer_init = True
        self.at = None
        self.init_time = datetime.now().strftime("(%d):%H:%M:%S")
        self.msg = None
        self.tinfo = None


    def start(self, when, message, tn=None, verbose=True, *args, **kwargs):
        """ start() does the following.

        1. Concatenates the data into tinfo
        2. Initializes the timer, and starts it.
        3. Returns after starting and awaits additional ordrs."""
        
        try:
            #pdb.set_trace()
            self.when = when
            self.msg = message
            if tn is not None:
                self.tn = tn
            if not self.timer_init:
                raise NotInitialized("Timer() was not initialized before start_timer called!")
            ct = datetime.now()
            dy = int(ct.day)
            if when.endswith("@"):
                dy += 1
                self.when = self.when[0:len(when) - 1]   #remove the trailing @

            hr = int(self.when.split(":")[0])
            mn = int(self.when.split(":")[1])
            sc = 0
            self.at = ct.replace(day=dy, hour=hr, minute=mn, second=sc)
            if self.at < ct:
                raise TimerInPast 
            if self.testmode:
                ct = self.at   #if testmode, make ct=at so alarm triggers right now
                print("\n\tTestmode: {}.".format(self.testmode))
            self.tinfo = {
                "tid": Timer.i,
                "name": self.tn,
                "init_time": self.init_time,
                "alarm_time": self.at,
                "testmode": self.testmode,
                "todo": self.todo,
                "message": self.msg,
                "verbose": self.verbose,
                "fn": self.fn
            }
            Timer.i += 1
            x = TimerThread(self.tinfo)
            x.start()
            Timer.timer_threads.append(x)
            print("\t{} |{}| Started and appended to master list.".format(Timer.OK, self.tinfo['name']))
            return
        except Exception as e:
            print("\n\t{} Caught exception in start: {}. ".format(Timer.FAIL, e))
            return False


    def status(self):
        """ Iterates through the timers in the class and prints information."""
        print("\n\t[STATUS]")
        print("\n\t# active timers: {}".format(len(Timer.timer_threads)))
        for n in range(0, len(Timer.timer_threads)):
            active = Timer.timer_threads[n].isAlive()
            print("\n\tID: {}\n\tName: {}\n\tInit: {}    AlarmT: {}\n\tMode: {}\n\tTarget: {}"
                .format(n, Timer.timer_threads[n].tinfo['name'],
                Timer.timer_threads[n].tinfo['init_time'],
                Timer.timer_threads[n].tinfo['alarm_time'],
                Timer.timer_threads[n].tinfo['testmode'].
                Timer.timer_threads[n].tinfo['todo']))
        return True


# ***TIMERTHREAD **** ############################## TimerThread ##########################


class TimerThread(threading.Thread):
    """ gets tinfo, a dictionary containing: tid, name, init_time, alarm_time,
        testmode, todo, message
    """

    def __init__(self, tinfo, *args, **kwargs):
        self.tinfo = tinfo
        self.verbose = self.tinfo['verbose']
        self.testmode = self.tinfo['testmode']
        self.todo = self.tinfo['todo']
        threading.Thread.__init__(self, target=self.alarm_t, daemon=True)
        self.initialized = True
        if self.verbose:
            self.print_t_data()
        sleep(1)

    def alarm_t(self, **kwargs):
        """ alarm_t = the alarm timer function.

        Waits until time is up, then executs the todo action. 
        If testmode, executes immediately."""

        if self.verbose:
            print("\t{} |{}| Initialization begins.".format(Timer.OK, self.tinfo['name']))
        time_asleep = 1
        if self.testmode is False:
            while self.tinfo['alarm_time'] >= datetime.now():
                if time_asleep % 60 == 0:
                    if self.verbose:
                        print("|{}| +1 minute.".format(datetime.now().strftime("%H:%M:%S")))       
                    time_asleep += 1
                    sleep(1)
                    self.execute_alarm_target(self.tinfo)
                    return True
        elif self.testmode is True:
            print("\t{} **** TESTMODE.Forcing immediate exec!".format(Timer.OK))
            self.execute_alarm_target()
            return True
        else:
            print("\t  testmode must be True or False!")
            return False

    def execute_alarm_target(self, **kwargs):
        """ Parses the todo option from Timer and executes."""
        if not self.initialized:
            raise NotInitialized(message="Attempting to execute alarm target, but TimerThread unnitialized!")
        
        targ = TimerTarget(self.tinfo)

        if self.todo == "sms":
            targ.send_sms(self.tinfo['message'])
        elif self.todo == "email":
            targ.send_email(SEND_TO, ("{} is sending email?".format(self.tinfo['name'])), self.tinfo['message']) 
        elif self.todo == "wav":
            targ.play_wav(self.tinfo['fn'])
        else:
            print("\t{} : Todo: {} not in allowed_todos: {}".format(Timer.FAIL, self.todo, Timer.allowed_todos))

        return

    def print_t_data(self, **kwargs):
        """ Prints informational data about the thread."""
        try:
            if self.tinfo and self.initialized:
                print("\n\tTimer Information:")
                print("\t------------------")
                print("\t\t1: Test Name: {}".format(self.tinfo['name']))
                print("\t\t2: Thread ID: {}\n\t\t3: Action: {}".format(self.tinfo['tid'], self.tinfo['todo']))
                print("\t\t4: Thread Mode: {}\n\t\t5: Verbose: {}".format(self.tinfo['todo'], self.tinfo['verbose']))
                print("\t\t6: Init Time: {}\n\t\t7: Alarm Time: {}".format(self.tinfo['init_time'], self.tinfo['alarm_time'].strftime("%H:%M:%S")))
                print("\n\n")
                return True
        except Exception as e:
            print("Exception in print_t_data: {}".format(e))
            return False

###################################ENDALARMTHREAD################################

###################################TARGETS#######################################
class TimerTarget(Timer):
    """ This is the execution class of the module, in other words it plays the
    wav file, sends the text (or in future, call), and also sends the emails.
    funcs: send_sms(message), callout(DOESNTWORK!), send_email(to, subject, message)
            play_wav(fn)    
    """
    def __init__(self, tinfo, fn=None, subject=None, verbose=None, **kwargs):
        self.tinfo = tinfo
        self.verbose = True
        if verbose is not True:
            self.verbose = verbose
        fn = "STILL.wav"
        self.subject = ("Sent from TimerThread {}".format(self.tinfo['name']))
        if fn is not None:
            self.fn = fn
        if subject is not None:
            self.subject = subject
        self.tinfo = tinfo
        self.alarm_type = self.tinfo['todo']
        self.message = self.tinfo['message']
        self.fn = self.tinfo['fn']

    def send_sms(self, message, to=SMS_TO):
        """ uses twilio to send text message to ma phone"""
        try:
            from XPBX import PBXAlert
            pbx_alarm = PBXAlert()
            pbx_alarm.send_sms(self.tinfo['message'])
            if self.verbose:
                print("{} Successfully sent SMS!".format(Timer.OK))
            return True
        except Exception as e:
            print("{} Caught exception in send_sms: {}".format(Timer.FAIL, e))
            return False

    def callout(self, to=SMS_TO, **kwargs):
        """NOT IMPLEMENTED!!!"""
        print("Callout not implemented yet!")
        pass

    def send_email(self, to, subject, message):
        """ always sends email from vx-mond@vixal.net.

        requires: to, subject, message!"""

        email_to = SEND_TO
        try:
            from AlertEmail import AlertEmail
            mx_alarm = AlertEmail(email_to, self.subject, self.message)
            mx_alarm.send()
            print("\t{} |{}| Successfully sent email.".format(Timer.OK, self.tinfo['name']))
            return True
        except Exception as e:
            print("\t{} Exception in send_email! {}".format(Timer.FAIL, e))

    def play_wav(self, fn):
        file = self.fn
        if fn is not None:
            file = fn
        try:
            from playsound import playsound
            playsound(file)
            print("{} |{}| Soundfile played successfully.".format(Timer.OK, self.tinfo['name']))
            return True
        except Exception as e:
            print("{} Exception in play_way {}".format(Timer.FAIL, e))
            return False
############################################ ONESHOT ##########################
class OneShot:
    pass


################################### Errors ######################################

class TimerInPast(ValueError):
    def __init__(self, message=None):
        if message:
            print(message)
        else:
            print("You are attempting to start a timer in the past!")

class MissingRequiredArguments(ValueError):
    def __init__(self, message=None):
        if message:
            print(message)
        else:
            print("Missing the required command line arguments for a oenshot.")
class NotInitialized(ValueError):
    def __init__(self, message=None):
        if message:
            print(message)
        else:
            print("You have not initialized the class before attmepting to use a method!")
