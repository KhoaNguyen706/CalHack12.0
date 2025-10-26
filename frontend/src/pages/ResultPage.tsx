import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router'

interface Recipe {
  name: string
  image_link: string
  step_by_step: string[]
  rating: number
  calories: number
  health: string
  difficulty: string
  ingredients_used: string[]
  detected_ingredients: string[]
  confidence: number
}

const ResultPage = () => {
  const navigate = useNavigate()
  const [recipe, setRecipe] = useState<Recipe | null>(null)

  useEffect(() => {
    
    const storedRecipe = localStorage.getItem('recipe')
    if (storedRecipe) {
      setRecipe(JSON.parse(storedRecipe))
    } else {
      
      navigate('/input')
    }
  }, [navigate])

  if (!recipe) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin text-6xl mb-4">🔄</div>
          <p className="text-xl text-gray-600">Loading recipe...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-100 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Back Button */}
        <button
          onClick={() => navigate('/input')}
          className="mb-6 px-6 py-2 backdrop-blur-md bg-white/60 rounded-full text-gray-700 font-semibold border border-blue-200 hover:bg-white/80 transition"
        >
          ← Try Another Recipe
        </button>

        {/* Success Header */}
        <div className="backdrop-blur-xl bg-white/40 rounded-3xl p-8 mb-8 shadow-xl border border-white/60 text-center">
          <div className="text-6xl mb-4">🎉</div>
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Recipe Ready!
          </h1>
          <p className="text-gray-600">
            Our AI agents worked together to create the perfect recipe for you
          </p>
        </div>

        {/* Recipe Card */}
        <div className="backdrop-blur-xl bg-white/50 rounded-3xl p-8 shadow-xl border border-white/60">
          <div className="flex flex-col lg:flex-row gap-8">
            {/* Recipe Image */}
            {/* {recipe.image_link && (
              <div className="lg:w-96 flex-shrink-0">
                <img
                  src={recipe.image_link}
                  alt={recipe.name}
                  className="w-full h-96 object-cover rounded-2xl shadow-lg border-4 border-white/60"
                />
              </div>
            )} */}

            {/* Recipe Details */}
            <div className="flex-1">
              <h2 className="text-5xl font-bold text-gray-800 mb-6">{recipe.name}</h2>
              
              {/* Stats Grid */}
              <div className="grid grid-cols-2 gap-4 mb-8">
                <div className="backdrop-blur-md bg-gradient-to-br from-blue-100/80 to-blue-200/60 rounded-2xl p-5 border border-blue-200">
                  <p className="text-gray-600 text-sm mb-1">AI Rating</p>
                  <p className="text-blue-600 text-4xl font-bold">{recipe.rating}/100</p>
                </div>
                <div className="backdrop-blur-md bg-gradient-to-br from-blue-100/80 to-blue-200/60 rounded-2xl p-5 border border-blue-200">
                  <p className="text-gray-600 text-sm mb-1">Calories</p>
                  <p className="text-blue-600 text-4xl font-bold">{recipe.calories}</p>
                </div>
                <div className="backdrop-blur-md bg-white/60 rounded-2xl p-5 border border-blue-200">
                  <p className="text-gray-600 text-sm mb-1">Health Level</p>
                  <p className="text-gray-700 text-2xl font-semibold">{recipe.health}</p>
                </div>
                <div className="backdrop-blur-md bg-white/60 rounded-2xl p-5 border border-blue-200">
                  <p className="text-gray-600 text-sm mb-1">Difficulty</p>
                  <p className="text-gray-700 text-2xl font-semibold capitalize">{recipe.difficulty}</p>
                </div>
              </div>

              {/* Ingredients */}
              <div className="mb-8">
                <h3 className="text-gray-800 text-2xl font-bold mb-4 flex items-center gap-2">
                  🥘 Ingredients Used
                </h3>
                <div className="flex flex-wrap gap-2">
                  {recipe.ingredients_used.map((ing: string, idx: number) => (
                    <span
                      key={idx}
                      className="px-5 py-2 backdrop-blur-md bg-blue-100/80 rounded-full text-blue-700 text-base font-medium border border-blue-200"
                    >
                      {ing}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Steps Section (Full Width) */}
          <div className="mt-8 pt-8 border-t-2 border-blue-200">
            <h3 className="text-gray-800 text-3xl font-bold mb-6 flex items-center gap-2">
              📋 Step by Step Instructions
            </h3>
            <div className="space-y-4">
              {recipe.step_by_step.map((step: string, idx: number) => (
                <div
                  key={idx}
                  className="backdrop-blur-md bg-white/70 rounded-xl p-5 border border-blue-200 hover:border-blue-300 transition"
                >
                  <div className="flex gap-4">
                    <span className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-400 text-white font-bold rounded-full flex items-center justify-center text-lg">
                      {idx + 1}
                    </span>
                    <span className="text-gray-700 text-lg leading-relaxed flex-1">{step}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="mt-8 flex gap-4">
            <button
              onClick={() => navigate('/input')}
              className="flex-1 py-4 px-8 bg-gradient-to-r from-blue-500 to-blue-400 text-white font-bold text-xl rounded-full shadow-lg hover:shadow-xl hover:scale-[1.02] transition-all duration-200"
            >
              🔄 Make Another Recipe
            </button>
            <button
              onClick={() => navigate('/')}
              className="flex-1 py-4 px-8 backdrop-blur-md bg-white/60 text-gray-700 font-bold text-xl rounded-full border-2 border-blue-200 hover:bg-white/80 transition"
            >
              🏠 Back to Home
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ResultPage