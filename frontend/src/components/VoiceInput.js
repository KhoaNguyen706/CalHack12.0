import React, { useState } from 'react';
import './VoiceInput.css';

const VoiceInput = ({ onVoiceInput }) => {
  const [isListening, setIsListening] = useState(false);

  const toggleListening = () => {
    setIsListening(!isListening);
    // TODO: Implement actual voice recognition
    if (!isListening) {
      onVoiceInput("Start listening...");
    } else {
      onVoiceInput("Stopped listening.");
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