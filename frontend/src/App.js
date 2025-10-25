import React, { useState } from 'react';
import './App.css';
import VoiceInput from './components/VoiceInput';
import RecipeDisplay from './components/RecipeDisplay';

function App() {
  const [recipe, setRecipe] = useState(null);

  const handleVoiceInput = (input) => {
    // TODO: Connect with backend
    console.log('Voice input received:', input);
    
    // Temporary mock recipe for testing
    setRecipe({
      title: "Test Recipe",
      summary: "This is a test recipe to demonstrate the UI.",
      ingredients: [
        "2 cups flour",
        "1 cup sugar",
        "3 eggs",
        "1 cup milk"
      ],
      steps: [
        "Mix dry ingredients in a bowl",
        "Beat eggs and milk together",
        "Combine wet and dry ingredients",
        "Bake at 350°F for 30 minutes"
      ]
    });
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🍳 Cooking Assistant</h1>
        <p className="subtitle">Your voice-enabled cooking companion</p>
      </header>
      
      <main className="App-main">
        <VoiceInput onVoiceInput={handleVoiceInput} />
        <RecipeDisplay recipe={recipe} />
      </main>

      <footer className="App-footer">
        <p>Say "help" for available commands</p>
      </footer>
    </div>
  );
}

export default App;