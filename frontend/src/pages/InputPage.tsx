import { useState } from 'react'
import { useNavigate } from 'react-router'

const InputPage = () => {
  const navigate = useNavigate()
  const [image, setImage] = useState<File | null>(null)
  const [imagePreview, setImagePreview] = useState<string>('')
  const [prompt, setPrompt] = useState('')
  const [loading, setLoading] = useState(false)
  const [currentStep, setCurrentStep] = useState(0)
  const [retryCount, setRetryCount] = useState(0)
  const [statusMessage, setStatusMessage] = useState('')

  const steps = [
    { id: 1, name: 'Detect Ingredients', icon: '🔍', agent: 'Vision Agent' },
    { id: 2, name: 'Summarize Action', icon: '📝', agent: 'Action Agent' },
    { id: 3, name: 'Cook Recipe', icon: '👨‍🍳', agent: 'Cooker Agent' },
    { id: 4, name: 'Food Advisor Check', icon: '✅', agent: 'Advisor Agent' },
    { id: 5, name: 'Recipe Ready', icon: '🎉', agent: 'Complete' }
  ]

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      setImage(file)
      
      const reader = new FileReader()
      reader.onloadend = () => {
        setImagePreview(reader.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const pollRecipeStatus = async (requestId: string) => {
  let attempts = 0
  const maxAttempts = 60 // 5 minutes max
  let lastStep = 0

    const stepMap: Record<string, number> = {
      detect: 1,
      summarize: 2,
      cook: 3,
      advisor: 4,
      retry: 3,
      done: 5,
    }

  const poll = async () => {
    try {
      const response = await fetch(`http://localhost:8080/api/recipe/result/${requestId}`)
      const data = await response.json()

      const backendStep = stepMap[data.step] || 1

      // Only update if step changed
      if (backendStep !== lastStep) {
        setTimeout(() => {
          setCurrentStep(backendStep)
          setStatusMessage(data.message || '')
          lastStep = backendStep
          console.log(lastStep)
        }, 1200) // 1.2s delay between steps
      } else {
        setCurrentStep(backendStep)
        setStatusMessage(data.message || '')
        console.log(lastStep)
      }

      if (data.status === 'completed' && data.data) {
        setTimeout(() => {
          setCurrentStep(5)
          setStatusMessage('🎉 Recipe is ready!')
          localStorage.setItem('recipe', JSON.stringify(data.data))
          navigate('/result')
        }, 1200)
        return
      } else if (data.status === 'retrying') {
        setRetryCount(data.retry_count || 0)
        setStatusMessage(data.message)
        console.log(lastStep)
      }

    } catch (error) {
      console.error('Polling error:', error)
    }

    attempts++
    if (attempts < maxAttempts) {
      setTimeout(() => poll(), 2000)
    } else {
      alert('Request timed out. Please try again.')
      setLoading(false)
      setCurrentStep(0)
    }
  }

  poll()
}

  const handleSubmit = async () => {
    if (!image || !prompt) {
      alert('Please upload an image and enter a prompt!')
      return
    }

    setLoading(true)
    setCurrentStep(1)
    setRetryCount(0)
    setStatusMessage('🔍 Detecting ingredients...')

    const formData = new FormData()
    formData.append('image', image)
    formData.append('text', prompt)

    try {
      // Step 1: Send initial request
      const response = await fetch('http://localhost:8080/recipe/generate', {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()
      
      if (data.request_id) {
        // Start polling immediately for real-time status updates
        pollRecipeStatus(data.request_id)
      } else {
        alert('Failed to start recipe generation')
        setLoading(false)
        setCurrentStep(0)
      }
    } catch (error) {
      console.error('Error:', error)
      alert('Error generating recipe')
      setLoading(false)
      setCurrentStep(0)
    }
}
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800 p-6 relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse"></div>
      </div>

      <div className="max-w-4xl mx-auto relative z-10">
        {/* Back Button */}
        <button
          onClick={() => navigate('/')}
          disabled={loading}
          className="mb-6 backdrop-blur-2xl bg-white/10 px-6 py-3 rounded-full text-white font-medium border border-white/20 hover:bg-white/15 transition-all duration-200 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span>←</span> Back to Home
        </button>

        {/* Header Card */}
        <div className="backdrop-blur-3xl bg-white/10 rounded-[2.5rem] p-8 mb-6 shadow-2xl border border-white/20">
          <div className="relative">
            <h1 className="text-5xl font-bold text-white mb-3">
              📸 Upload Your Fridge
            </h1>
            <p className="text-white/70 text-lg">
              Let our AI agents discover the perfect recipe for you
            </p>
          </div>
        </div>

        {/* Progress Flow - Only show when loading */}
        {loading && (
          <div className="backdrop-blur-3xl bg-white/10 rounded-[2.5rem] p-8 mb-6 shadow-2xl border border-white/20">
            <h3 className="text-white text-xl font-bold mb-6 text-center">
              🤖 AI Agents Working Together
            </h3>
            
            {/* Progress Steps */}
            <div className="relative">
              {/* Progress Line */}
              <div className="absolute top-6 left-0 right-0 h-1 bg-white/10 rounded-full">
                <div 
                  className="h-full bg-gradient-to-r from-green-400 to-green-500 rounded-full transition-all duration-1000 ease-out"
                  style={{ width: `${(currentStep / steps.length) * 100}%` }}
                ></div>
              </div>

              {/* Steps */}
              <div className="relative flex justify-between">
                {steps.map((step, index) => {
                  const isCompleted = currentStep > step.id
                  const isActive = currentStep === step.id
                  const isPending = currentStep < step.id

                  return (
                    <div key={step.id} className="flex flex-col items-center">
                      {/* Step Circle */}
                      <div
                        className={`w-12 h-12 rounded-full flex items-center justify-center border-2 transition-all duration-500 mb-3 ${
                          isCompleted
                            ? 'bg-green-500 border-green-400 scale-110'
                            : isActive
                            ? 'bg-white/20 border-white/40 backdrop-blur-xl animate-pulse scale-110'
                            : 'bg-white/5 border-white/20 backdrop-blur-xl'
                        }`}
                      >
                        <span className="text-2xl">
                          {isCompleted ? '✓' : step.icon}
                        </span>
                      </div>

                      {/* Step Info */}
                      <div className="text-center">
                        <p
                          className={`text-xs font-semibold mb-1 transition-all duration-300 ${
                            isActive || isCompleted
                              ? 'text-white'
                              : 'text-white/40'
                          }`}
                        >
                          {step.name}
                        </p>
                        <p
                          className={`text-xs transition-all duration-300 ${
                            isActive
                              ? 'text-green-400 font-medium'
                              : isCompleted
                              ? 'text-green-500'
                              : 'text-white/30'
                          }`}
                        >
                          {step.agent}
                        </p>
                      </div>

                      {/* Retry indicator for cooking step */}
                      {step.id === 3 && isActive && retryCount > 0 && (
                        <div className="mt-2 backdrop-blur-xl bg-yellow-500/20 px-3 py-1 rounded-full border border-yellow-400/30 animate-pulse">
                          <p className="text-yellow-400 text-xs font-medium">
                            Retry #{retryCount}
                          </p>
                        </div>
                      )}
                    </div>
                  )
                })}
              </div>
            </div>

            {/* Current Status Message */}
            <div className="mt-6 text-center">
              <div className="backdrop-blur-xl bg-white/10 rounded-2xl p-4 border border-white/20">
                <p className="text-white/80 text-sm">
                  {statusMessage}
                </p>
              </div>
            </div>

            {/* Retry Info */}
            {retryCount > 0 && (
              <div className="mt-4 backdrop-blur-xl bg-yellow-500/10 rounded-2xl p-4 border border-yellow-400/30 text-center">
                <p className="text-yellow-400 text-sm font-medium">
                  ⚠️ Recipe quality was below 85. Our Cooker Agent is improving it (Attempt {retryCount}/3)
                </p>
              </div>
            )}
          </div>
        )}

        {/* Input Form Card */}
        <div className="backdrop-blur-3xl bg-white/10 rounded-[2.5rem] p-8 shadow-2xl border border-white/20">
          <div className="space-y-6">
            {/* Image Upload */}
            <div>
              <label className="block text-white text-lg font-semibold mb-3">
                Upload Image
              </label>
              
              {imagePreview ? (
                <div className="relative group">
                  <img
                    src={imagePreview}
                    alt="Preview"
                    className="w-full h-72 object-cover rounded-3xl border-2 border-white/30"
                  />
                  <button
                    onClick={() => {
                      setImage(null)
                      setImagePreview('')
                    }}
                    disabled={loading}
                    className="absolute top-4 right-4 backdrop-blur-xl bg-red-500/80 px-5 py-2 text-white rounded-full font-semibold border border-white/30 hover:bg-red-600 transition opacity-0 group-hover:opacity-100 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    ✕ Remove
                  </button>
                </div>
              ) : (
                <label className={`flex flex-col items-center justify-center w-full h-72 border-2 border-dashed border-white/30 rounded-3xl backdrop-blur-xl bg-white/5 hover:bg-white/10 transition-all duration-200 ${loading ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'}`}>
                  <div className="flex flex-col items-center justify-center">
                    <div className="backdrop-blur-xl bg-white/10 rounded-2xl p-4 mb-4 border border-white/20">
                      <p className="text-5xl">📷</p>
                    </div>
                    <p className="mb-2 text-xl font-semibold text-white">
                      Click to upload
                    </p>
                    <p className="text-sm text-white/60">PNG, JPG, JPEG or WEBP</p>
                  </div>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    disabled={loading}
                    className="hidden"
                  />
                </label>
              )}
            </div>

            {/* Prompt Input */}
            <div>
              <label className="block text-white text-lg font-semibold mb-3">
                What do you want to cook?
              </label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                disabled={loading}
                placeholder="e.g., I want spicy Thai food in 30 minutes with healthy ingredients"
                rows={4}
                className="w-full p-5 rounded-3xl backdrop-blur-xl bg-white/10 border-2 border-white/20 text-white placeholder-white/40 focus:outline-none focus:border-white/40 focus:bg-white/15 transition-all duration-200 resize-none disabled:opacity-50 disabled:cursor-not-allowed"
              />
            </div>

            {/* Submit Button */}
            <button
              onClick={handleSubmit}
              disabled={loading || !image || !prompt}
              className="group relative w-full py-5 backdrop-blur-2xl bg-white/15 text-white font-bold text-xl rounded-full shadow-lg border border-white/30 hover:bg-white/25 hover:scale-[1.01] transition-all duration-300 disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:scale-100"
            >
              <div className="absolute inset-0 rounded-full bg-gradient-to-r from-blue-400/20 to-purple-400/20 blur-xl group-hover:blur-2xl transition-all duration-300"></div>
              
              {loading ? (
                <span className="relative flex items-center justify-center gap-3">
                  <svg className="animate-spin h-6 w-6" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Generating Recipe...
                </span>
              ) : (
                <span className="relative flex items-center justify-center gap-3">
                  <span className="text-2xl">🚀</span>
                  Generate Recipe
                </span>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default InputPage