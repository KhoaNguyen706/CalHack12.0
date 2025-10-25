import speech_recognition as sr

def get_voice(timeout=None, phrase_time_limit=None):
    """
    Record audio from microphone and convert to text using Google Speech Recognition.
    
    Args:
        timeout (float, optional): Maximum number of seconds to wait for phrase to start
        phrase_time_limit (float, optional): Maximum number of seconds to allow a phrase to continue
    
    Returns:
        str: Recognized text, or None if recognition failed
    """
    r = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait.")
            # Adjust for ambient noise and set threshold
            r.adjust_for_ambient_noise(source, duration=1)
            
            print("Listening... Speak now!")
            # Record audio
            audio = r.listen(source, 
                           timeout=timeout,
                           phrase_time_limit=phrase_time_limit)
            
            print("Processing speech...")
            try:
                # Use Google's Web Speech API to convert to text
                text = r.recognize_google(audio)
                print(f"Recognized: {text}")
                return text
                
            except sr.UnknownValueError:
                print("Could not understand audio")
                return None
                
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                return None
                
    except sr.WaitTimeoutError:
        print("Timeout: No speech detected")
        return None
        
    except Exception as e:
        print(f"Error accessing microphone: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    text = get_voice(timeout=5, phrase_time_limit=10)
    if text:
        print(f"You said: {text}")