import qi
import time
import sys
import socket
from client_module import create_client_connection, start_listening, close_connection


sys.path.append('C:\\Data\\Desktop\\GitHub\\EhBAI\\nao\\Nao-Client\\pythonsdk\\lib')

# Nao robot connection details (these might be constants or configured externally)
NAO_IP = "10.2.172.130"
NAO_PORT = 9559

global listener, posture, motion, animatedSpeech, session, app

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
        # print("Event detected! Value:", value)

        if value == 1001:
            self.leds.fadeRGB("FaceLeds", 0x00FF0000, 0.2)
            self.last_time = current_time  # Update the last time when bookmark 1 is hit
        elif value == 1002:
            self.leds.fadeRGB("FaceLeds", 0x000000FF, 0.2)
            if self.last_time is not None:
                duration = current_time - self.last_time
                print("Duration between Bookmark 1 and 2: ", duration, " seconds")
                self.durations.append(duration)  # Store the duration in the list
                self.last_time = None  # Reset the last time
        elif value == 1003:
            self.leds.fadeRGB("FaceLeds", 0x000F00FF, 0.2)       
        elif value ==2001:
            self.motion.setAngles("HeadYaw",0, 0.3)
        elif value ==2002:
            self.motion.setAngles("HeadYaw",1.0, 0.3)

        elif value ==2003:
            self.motion.moveTo(0.5, 0.2, 0, 1, _async=True)
        elif value ==64000:
            self.motion.rest()


def handle_message(message):
    """Handle messages received from the server by initiating speech."""
    print("Received: ", message)
    # Ensure the animatedSpeech service is properly initialized and connected
    try:

        posture.goToPosture("Stand",1)        
        
        animatedSpeech.say(message)
        
        print("Durations recorded:", listener.durations)

        # Specify the filename
        filename = 'durations.txt'

        # Writing each duration to a file, each on a new line
        with open(filename, 'w') as file:
            for duration in listener.durations:
                file.write("%s\n" % duration)  # Using string formatting compatible with Python 2.7

        print ("Durations saved to", filename)

        # motion.rest()

    except RuntimeError as e:
        print("Runtime error:", e)

def main():
    global listener, posture, motion, animatedSpeech, session, app

    host = socket.gethostname()
    port = 5000
    client_socket = create_client_connection(host, port)



    app = qi.Application(["SpeechEventListener", "--qi-url=tcp://{}:{}".format(NAO_IP, NAO_PORT)])
    app.start()
    session = app.session

    start_listening(client_socket, lambda message: handle_message(message))

    listener = SpeechEventListener(session)
    
    posture = session.service("ALRobotPosture")
    animatedSpeech = session.service("ALAnimatedSpeech")
    motion = session.service("ALMotion")
    tts = session.service("ALTextToSpeech")
    tts.setLanguage("English")
    tts.setVoice("naoenu")

    try:
        while True:
            input("Press Ctrl+C to quit.")  # Simple prompt to keep the loop running
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        motion.rest()
        close_connection(client_socket)
        listener.unsubscribe()
        app.stop()

if __name__ == '__main__':
    main()
