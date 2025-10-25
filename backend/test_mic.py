import speech_recognition as sr
import json

def list_microphones():
    """List all available microphones"""
    print("\nAvailable microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"Microphone {index}: {name}")

def test_microphone(device_index=None):
    """Test if we can access the microphone"""
    try:
        r = sr.Recognizer()
        # Use specific microphone index or default
        with sr.Microphone(device_index=device_index) as source:
            print("\nMicrophone test successful!")
            print("Adjusting for ambient noise... Speak after the beep.")
            r.adjust_for_ambient_noise(source, duration=1)
            print("*beep*")
            audio = r.listen(source, timeout=5)
            print("Audio captured successfully!")
            try:
                # Use Google's Web Speech API to recognize the audio
                text = r.recognize_google(audio)
                print(f"You said: {text}")
                result = {"text": text}
                print(json.dumps(result))
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            return True
    except Exception as e:
        print(f"\nMicrophone test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing speech recognition setup...")
    list_microphones()
    
    # Try microphone index 3 (Microphone (Realtek Audio))
    # or 4 (Microphone (Realtek HD Audio Mic input))
    print("\nTrying microphone index 3...")
    if not test_microphone(device_index=3):
        print("\nTrying microphone index 4...")
        test_microphone(device_index=4)
    