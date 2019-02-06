ConfigurableTimer Documentation:
-----------------------------------------
NOTE: THIS IS A WORK IN PROGRESS, DONT TRY TO USE IT TIL I REMOVE THIS LINE
version: .01

Note: You must change some things in in the class files for it to work.


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
