import React, { useState } from 'react';
import './App.css';

function App() {
  const [recipe, setRecipe] = useState(null);
  const [isListening, setIsListening] = useState(false);

  const startListening = () => {
    setIsListening(true);
    // TODO: Implement voice recognition integration
  };

  const stopListening = () => {
    setIsListening(false);
    // TODO: Stop voice recognition
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Cooking Assistant</h1>
      </header>
      
      <main className="App-main">
        <div className="voice-control">
          <button 
            className={`mic-button ${isListening ? 'listening' : ''}`}
            onClick={isListening ? stopListening : startListening}
          >
            {isListening ? 'Stop Listening' : 'Start Listening'}
          </button>
        </div>

        {recipe && (
          <div className="recipe-display">
            <h2>{recipe.title}</h2>
            <div className="recipe-summary">
              <p>{recipe.summary}</p>
            </div>
            
            <div className="recipe-ingredients">
              <h3>Ingredients</h3>
              <ul>
                {recipe.ingredients.map((ingredient, index) => (
                  <li key={index}>{ingredient}</li>
                ))}
              </ul>
            </div>

            <div className="recipe-steps">
              <h3>Instructions</h3>
              <ol>
                {recipe.steps.map((step, index) => (
                  <li key={index}>{step}</li>
                ))}
              </ol>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;