import React, { useState } from 'react';
import './App.css';
import VoiceInput from './components/VoiceInput';
import RecipeDisplay from './components/RecipeDisplay';

function App() {
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleVoiceInput = async (input) => {
    console.log('Voice input received:', input);
    setLoading(true);
    setError(null);

    try {
      // Send request to your backend agent
      const response = await fetch('http://127.0.0.1:8000/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: input
        })
      });

      if (!response.ok) {
        throw new Error('Failed to get recipe from backend');
      }

      const data = await response.json();
      
      // Transform the response into recipe format
      setRecipe({
        title: data.title || "Recipe",
        summary: data.summary || "Generated recipe based on your request",
        ingredients: Array.isArray(data.ingredients) ? data.ingredients : [],
        steps: Array.isArray(data.steps) ? data.steps : []
      });
    } catch (err) {
      console.error('Error connecting to backend:', err);
      setError('Failed to connect to the recipe service. Please try again.');
      
      // Fallback recipe for testing if backend is not available
      if (process.env.NODE_ENV === 'development') {
        setRecipe({
          title: "Test Recipe (Fallback)",
          summary: "Backend connection failed - showing test recipe",
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
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🍳 Cooking Assistant</h1>
        <p className="subtitle">Your voice-enabled cooking companion</p>
      </header>
      
      <main className="App-main">
        <VoiceInput onVoiceInput={handleVoiceInput} disabled={loading} />
        
        {error && (
          <div className="error-message" style={{
            color: '#e74c3c',
            padding: '10px',
            margin: '10px 0',
            borderRadius: '4px',
            backgroundColor: '#fde2e2'
          }}>
            {error}
          </div>
        )}
        
        {loading ? (
          <div className="loading-indicator" style={{
            textAlign: 'center',
            padding: '20px',
            color: '#666'
          }}>
            🔄 Generating your recipe...
          </div>
        ) : (
          <RecipeDisplay recipe={recipe} />
        )}
      </main>

      <footer className="App-footer">
        <p>Say "help" for available commands</p>
      </footer>
    </div>
  );
}

export default App;