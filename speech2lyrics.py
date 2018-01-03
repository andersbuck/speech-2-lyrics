import speech_recognition as sr
from SpeechService import SpeechService

r = sr.Recognizer()
m = sr.Microphone()
speechSrv = SpeechService()
# Dict of all phrases in memory
phrases = {}
deleteLoop = False

try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Say something!")
        with m as source: audio = r.listen(source)
        print("Got it! Now to recognize it...")

        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)

            # we need some special handling here to correctly print unicode characters to standard output
            if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                print(u"You said {}".format(value).encode("utf-8"))
            else:  # this version of Python uses unicode for strings (Python 3+)
                print("You said {}".format(value))

            # If delete that is said then enter in loop for deleting phrases
            if value == "delete that s***":
                deleteLoop = True
            else:
                deleteLoop = False

            if deleteLoop == False:
                # Store spoken phrases in memory and count times spoken
                count = phrases.get(value)
                print (count)
                if count == None:
                    # Check to see if any phrases are close
                    speechSrv.isPhraseSimilar()
                        # If close highlight that this phrase will
                        # change if said again and spoken exactly the same
                        # as the change

                        # Else just update the close phrase
                    # If spoken the first time then add to phrases
                    phrases.update({value:1})
                else:
                    count += 1
                    phrases.update({value:count})
            else:
                speechSrv.deletePhrase()

            print(phrases)
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
except KeyboardInterrupt:
    pass
