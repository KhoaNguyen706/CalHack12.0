import React, { useState, useEffect } from 'react';
import './VoiceInput.css';

const VoiceInput = ({ onVoiceInput }) => {
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState(null);

  useEffect(() => {
    // Initialize speech recognition
    if (window.webkitSpeechRecognition) {
      const recognition = new window.webkitSpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        onVoiceInput(transcript);
        setIsListening(false);
      };

      recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      setRecognition(recognition);
    } else {
      console.error('Speech recognition not supported in this browser');
    }
  }, [onVoiceInput]);

  const toggleListening = () => {
    if (!recognition) {
      alert('Speech recognition is not supported in your browser. Please use Chrome.');
      return;
    }

    if (!isListening) {
      recognition.start();
      setIsListening(true);
    } else {
      recognition.stop();
      setIsListening(false);
    }
  };

  return (
    <div className="voice-input">
      <button 
        className={`mic-button ${isListening ? 'listening' : ''}`}
        onClick={toggleListening}
      >
        <div className="mic-icon">
          {isListening ? '🎤' : '🎙️'}
        </div>
        <span>{isListening ? 'Stop' : 'Start'} Listening</span>
      </button>
      {isListening && (
        <div className="listening-indicator">
          Listening...
          <div className="wave-container">
            <div className="wave"></div>
            <div className="wave"></div>
            <div className="wave"></div>
          </div>
        </div>
      )}
    </div>
  );
};

export default VoiceInput;