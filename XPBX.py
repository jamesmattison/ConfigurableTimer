from twilio.rest import Client

"""PBXAlert: Class for creating outgoing instances of Twilio services.

Includes: send_sms(message), callout(url_of_twiML)
"""
from_numbers = {"main": MAIN_NUMBER,
        "tf": TOLLFREE_NUMBER
        }


class PBXAlert:
    """PBX using Twilio to send_sms and callout (for alerts)."""

    def __init__(self, to_number=None, **kwargs):
        """init: import client, set to/from nums"""
        self.selfsid = 
        self.auth_code = 
        # if from_number.startswith('+'):
        #     self.from_number = from_number
        # else:
        #     if from_number in from_numbers.keys():
        #         self.from_number = from_numbers.values[from_number]
        #     else:
        #         print("Number must either start with + and be in account, or\
        #          be in allowed from numbers!")
        #         return False
    
        #if from_number in from_numbers.keys():
         #   self.from_number = from_numbers[from_number]
        #else:
         #   self.from_number = from_number
        #self.from_number = from_number
        self.from_number = 
        self.to_number = 
        self.client = Client(self.selfsid, self.auth_code)
        self.initialized = True
        if kwargs:
            if "msg" in kwargs:
                if kwargs[msg]:
                    self.send_sms(msg)
                    return True

    def send_sms(self, message, verbose=False):
        if self.initialized is not True:
            print("!!! You must initialize the class first.")
            return False

        sms_client = self.client
        try:
           # print("Sending message: To: {} From: {} Body: {}".format(self.to_number, self.from_number, message))
            message = sms_client.messages.create(from_=self.from_number, body=message, to=self.to_number)
            if verbose:
                print("Sent. F-> {} T-> {} Body-> {}".format(message.from_, message.to, message.body))
            return True
        except Exception as e:
            print("Caught exception: {} in send_sms; sms sending failed.".format(e))
            return False

