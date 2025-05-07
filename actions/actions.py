import subprocess

from rasa_sdk import Action, Tracker


class ActionTurnOnLight(Action):
    def name(self) -> str:
        return "action_turn_on_light"

    def run(self, dispatcher, tracker, domain):
        # Your logic to turn on the light
        dispatcher.utter_message(text="Light turned on.")
        return []

class ActionStartCoffeeMachine(Action):
    def name(self) -> str:
        return "action_start_coffee_machine"

    def run(self, dispatcher, tracker, domain):
        # Your logic to start the coffee machine
        dispatcher.utter_message(text="Coffee machine started.")
        return []

class ActionSetAlarm(Action):
    def name(self) -> str:
        return "action_set_alarm"

    def run(self, dispatcher, tracker, domain):
        # Your logic to set an alarm
        dispatcher.utter_message(text="Alarm set for 7 AM.")
        return []

class OpenGoogleChrome(Action):
    def name(self) -> str:
        return "action_open_chrome"

    def run(self, dispatcher, tracker, domain):
        # Your logic to set an alarm
        dispatcher.utter_message(text="Opening Google Chrome")
        subprocess.Popen(["start", "chrome"], shell=True)
        return []
    

cfh = "Default"
falkwish = "Profile 1"
ironManMusicUrl = "https://www.youtube.com/watch?v=bcyvZIoQp9A&t=848s"
classicalMusicUrl = "https://www.youtube.com/watch?v=TZ5WW1kzepo&t=1246s"

class DropNeedle(Action):
    def name(self) -> str:
        return "action_drop_needle"

    def run(self, dispatcher, tracker, domain):
        # Your logic to set an alarm
        dispatcher.utter_message(text="Dropping needle")
        subprocess.Popen(["start", "chrome", f"--profile-directory={cfh}", ironManMusicUrl], shell=True)
        return []
    
class SetVolume(Action):
    def name(self) -> str:
        return "action_set_volume"
    
    def run(self, dispatcher, tracker, domain):
        from word2number import w2n
        last_user_message = tracker.latest_message.get("text", "No user message found")
        number = -1000
        words = last_user_message.lower().split()
        for word in words:
            try:
                number = w2n.word_to_num(word)
            except ValueError:
                continue  # If not a number, keep checking
        print(f"Setting volume to {number}")
        from ctypes import POINTER, cast

        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        )
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        
        # Set volume (scale 0.0 to 1.0)
        volume.SetMasterVolumeLevelScalar(number / 100, None)
        # Use or log the message
        dispatcher.utter_message(text=f"Setting volume to {number}")
        return []