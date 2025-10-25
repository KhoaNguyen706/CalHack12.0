import React from 'react';
import './RecipeDisplay.css';

const RecipeDisplay = ({ recipe }) => {
  if (!recipe) return null;

  return (
    <div className="recipe-display">
      <h2 className="recipe-title">{recipe.title}</h2>
      
      <div className="recipe-section">
        <h3>Summary</h3>
        <p className="recipe-summary">{recipe.summary}</p>
      </div>

      <div className="recipe-section">
        <h3>Ingredients</h3>
        <ul className="ingredients-list">
          {recipe.ingredients.map((ingredient, index) => (
            <li key={index} className="ingredient-item">
              <span className="ingredient-checkbox">
                <input type="checkbox" id={`ingredient-${index}`} />
              </span>
              <label htmlFor={`ingredient-${index}`}>{ingredient}</label>
            </li>
          ))}
        </ul>
      </div>

      <div className="recipe-section">
        <h3>Instructions</h3>
        <ol className="instructions-list">
          {recipe.steps.map((step, index) => (
            <li key={index} className="instruction-item">
              <div className="step-number">{index + 1}</div>
              <div className="step-content">{step}</div>
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
};

export default RecipeDisplay;