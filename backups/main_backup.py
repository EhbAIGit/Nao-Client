import qi
import yaml
import time
import sys

class SpeechEventListener(object):
    """ A class to react to the ALTextToSpeech/CurrentBookMark event """

    def __init__(self, session):
        super(SpeechEventListener, self).__init__()
        self.memory = session.service("ALMemory")
        self.leds = session.service("ALLeds")
        self.subscriber = self.memory.subscriber("ALTextToSpeech/CurrentBookMark")
        self.subscriber.signal.connect(self.onBookmarkDetected)
        # This attribute keeps the subscriber reference alive
        self.last_time = None  # Track the last time a bookmark was detected
        self.durations = []  # List to store durations between bookmarks 1 and 2

    def onBookmarkDetected(self, value):
        """ Callback for event ALTextToSpeech/CurrentBookMark """
        current_time = time.time()  # Get the current time
        print("Event detected! Value:", value)

        if value == 1:
            self.leds.fadeRGB("FaceLeds", 0x00FF0000, 0.2)
            self.last_time = current_time  # Update the last time when bookmark 1 is hit
        elif value == 2:
            self.leds.fadeRGB("FaceLeds", 0x000000FF, 0.2)
            if self.last_time is not None:
                duration = current_time - self.last_time
                print("Duration between Bookmark 1 and 2: ", duration, " seconds")
                self.durations.append(duration)  # Store the duration in the list
                self.last_time = None  # Reset the last time
        elif value == 3:
            self.leds.fadeRGB("FaceLeds", 0x000F00FF, 0.2)       

def main():
    # Nao connection details
    nao_ip = "10.2.172.130"
    nao_port = 9559

    class CustomLoader(yaml.SafeLoader):
        def construct_scalar(self, node):
            value = super(CustomLoader, self).construct_scalar(node)
            return value.replace('\\\\', '\\')

    def load_yaml(file_path):
        with open(file_path, 'r') as file:
            return yaml.load(file, Loader=CustomLoader)

    utterance = load_yaml('utterances.yaml')

    # Initialize qi framework
    connection_url = "tcp://" + nao_ip + ":" + str(nao_port)
    app = qi.Application(["SpeechEventListener", "--qi-url=" + connection_url])
    app.start()
    session = app.session
    speech_event_listener = SpeechEventListener(session)

    posture = session.service("ALRobotPosture")
    animatedSpeech = session.service("ALAnimatedSpeech")
    motion = session.service("ALMotion")

    tts = session.service("ALTextToSpeech")

    ### available voices
    print( "voices available: "+str(tts.getAvailableVoices()) )
    print( "languages available: "+ str(tts.getAvailableLanguages()))
    ### Stand
    posture.goToPosture("Stand",1)

    ### Dutch
    def Set_Dutch():
        tts.setLanguage("Dutch")
        tts.setVoice("Jasmijn22Enhanced")

    ### English
    def Set_English():
        tts.setLanguage("English")
        tts.setVoice("naoenu")

    ### More Nuanced English 
    def Set_Nuanced_English():
        tts.setLanguage("English")
        tts.setVoice("naoenu")
        tts.setParameter("speed", 70) #Acceptable range is [50 - 400]. 100 default.
        tts.setParameter("pitchShift", 1) #Acceptable range is [0.5 - 4]. 0 disables the effect. 1 default.
        tts.setParameter("volume", 100)#[0 - 100] 70 is ok if robot volume is 60


    # Set_Dutch()
    Set_Nuanced_English()
    listener = SpeechEventListener(session)

    animatedSpeech.say(utterance['all_hey'])

    print("Durations recorded:", listener.durations)

    # Specify the filename
    filename = 'durations.txt'

    # Writing each duration to a file, each on a new line
    with open(filename, 'w') as file:
        for duration in listener.durations:
            file.write("%s\n" % duration)  # Using string formatting compatible with Python 2.7

    print ("Durations saved to", filename)

    motion.rest()
    # while True:
    #     # tts.say("Put that \\mrk=3\\ there.")
    #     animatedSpeech.say(utterance['emphasis_2'])
    app.stop()


if __name__ == "__main__":
    try:
        main()  # Assuming all logic is inside a main function
    except KeyboardInterrupt:
        print("KeyboardInterrupt caught, shutting down...")
        sys.exit(0)