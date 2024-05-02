from naoqi import ALProxy
import yaml
import sys

sys.path.append('C:\\Data\\Desktop\\GitHub\\EhBAI\\nao\\Nao-Client\\pythonsdk\\lib')

### Custom loading of utterances (fixed loading double backslashes)
class CustomLoader(yaml.SafeLoader):
    def construct_scalar(self, node):
        value = super(CustomLoader, self).construct_scalar(node)
        return value.replace('\\\\', '\\')

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.load(file, Loader=CustomLoader)

utterance = load_yaml('utterances.yaml')


# Connect to Nao
nao_ip = "10.2.172.130" 
nao_port = 9559   

posture = ALProxy("ALRobotPosture", nao_ip, nao_port)
animatedSpeech = ALProxy("ALAnimatedSpeech", nao_ip, nao_port)
tts = ALProxy("ALTextToSpeech", nao_ip, nao_port)
motion = ALProxy("ALMotion", nao_ip, nao_port)

### available voices
print( "voices available: "+str(tts.getAvailableVoices()) )
print( "languages available: "+ str(tts.getAvailableLanguages()))
print(tts.getParameter('pitchShift'))
print(tts.getParameter('speed'))
print ("postures family available: " + str(posture.getPostureList()))
print ("postures available: " + posture.getPostureFamily())

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
def Nuanced_English():
    tts.setVoice("naoenu")
    tts.setParameter("speed", 100) #Acceptable range is [50 - 400]. 100 default.
    tts.setParameter("pitchShift", 1) #Acceptable range is [0.5 - 4]. 0 disables the effect. 1 default.
    tts.setParameter("volume", 70)#[0 - 100] 70 is ok if robot volume is 60


# Recalling bookmarks from memory
class SpeechEventListener(object):
    """ A class to react to the ALTextToSpeech/CurrentBookMark event """

    def __init__(self, session):
        super(SpeechEventListener, self).__init__()
        self.memory = session.service("ALMemory")
        self.leds = session.service("ALLeds")
        self.subscriber = self.memory.subscriber("ALTextToSpeech/CurrentBookMark")
        self.subscriber.signal.connect(self.onBookmarkDetected)
        # This attribute keeps the subscriber reference alive

    def onBookmarkDetected(self, value):
        """ Callback for event ALTextToSpeech/CurrentBookMark """
        print("Event detected!")
        print("Value:", value)

        if value == 1:
            self.leds.fadeRGB("FaceLeds", 0x00FF0000, 0.2)
        if value == 2:
            self.leds.fadeRGB("FaceLeds", 0x000000FF, 0.2)
        if value == 3:
            self.leds.fadeRGB("FaceLeds", 0x000F00FF, 0.2)            



# Replace 'animations/Stand/Gestures/You_5' with the path to your animation
# animation_duration = animation_player.getDuration("animations/Stand/Gestures/You_5")
# print("Duration of the animation is:", animation_duration, "seconds")

Nuanced_English()
# animatedSpeech.say(utterance['showsky'])
# tts.say ("Hello there! \\wait=9\\ \\eos=1\\ It's wonderful to see you. I hope you're having a great day!")
# animatedSpeech.say(utterance['showsky'])

# animatedSpeech.say("^pCall(ALTextToSpeech.say('Hello'))")
# animatedSpeech.say('^pCall(ALRobotPosture.goToPosture("Stand",1)) Ok, I stand.') 
# animatedSpeech.say("^pCall(ALMotion.wakeUp()) Ok, I wake up.") 
# animatedSpeech.say("^start(animations/Stand/Gestures/Hey_1) Hi! How are you?")

### AnimatedSpeech
# animatedSpeech.say(utterance['startup_dutch_0'])
#animatedSpeech.say("\\rspd=100\\ \\vct=100\\ ^mode(disabled) \\wait=5\\  Hello there! \\eos=1\\ It's wonderful to see you. I hope you're having a great day!")
animatedSpeech.say(utterance['sample_builtin'])
# animatedSpeech.say(utterance['emphasis_2'])
# animatedSpeech.say(utterance['emphasis_0'])

#tts.say ("Hello there! \\wait=9\\ \\eos=1\\ It's wonderful to see you. I hope you're having a great day!")
#tts.say ("Dit is slechts een voorbeeld om over na te denken. Hallo vrienden, hoe gaat het?")





### Rest
motion.rest()