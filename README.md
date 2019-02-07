ConfigurableTimer v.01a - Unstable / LIMITED!!!!
---------------------------------------------------
Usage: 
import CT
text = CT.Timer("sms")
text.start("23:30", "Don't forget to call Frank at 9")
text.start("07:00@", "Time to wake up!", tn="Important Call reminder") # @ -> +1 day
text.start("19:00@", "Pick Bob up from O'mally's pub.") 
for t in text.timer_threads:
	t.print_t_status()


custom-built timer threads that execute events after waiting until alarm time.
      

requires: (easily bypassed)
    playsound
    twilio
** if you wish to use without twilio, remove PBXAlert lines in ThreadTargets.sms_alert



NOTE: THIS IS A WORK IN PROGRESS, AND DEFINITELY NEEDS MORE PROGRESS.
NOTE2: This also assumes you have a twilio account, though removing all mention of XBPX/PBXAlarm() should solve that (either from Timer.allowed_todos or better yet, by renoving lines 236, 237, 238 of CT.py

version: .01 | james@vixal.net/james.mattison7@gmail

Note: You must change some things in in the class files for it to work.

Basic Use:

x = CT.Timer("sms")



class Timer
	L Timer
	L TimerThread
	L TimerTargets
	L TimerError




Timer:
	Timer(alarm_type, fn=<>, testmode=False, **kwargs)
	start(when, message, tn=None, verbose=True)
	status()

TimerThread:
	TimerThread(tinfo)
	alarm_t()
	execute_alarm_target()

TimerTarget:
	TimerTarget(tinfo)
	send_sms(message, to=<>)
	callout(to)
	send_email(to, subject, message)
	play_wav(fn)
**todo: ---> system_out(to_execute)

--------------------------------------
TODO:

tinfo: tinfo = {
        "tid": Timer.i,
        "name": self.tn,
        "init_time": self.init_time,
        "alarm_time": self.at,
        "testmode": self.testmode,
        "todo": self.todo,
        "message": self.msg,
        "verbose": self.verbose
        }
