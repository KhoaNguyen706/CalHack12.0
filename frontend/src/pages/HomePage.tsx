import { useNavigate } from 'react-router'


const HomePage = () => {
    const navigate = useNavigate();
  return  (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800 p-6 flex items-center justify-center relative overflow-hidden">
      
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/30 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/30 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      
      <div className="max-w-4xl mx-auto relative z-10">
        
        <div className="backdrop-blur-3xl bg-white/10 rounded-[2.5rem] p-12 shadow-2xl border border-white/20 relative">
          
          <div className="absolute inset-0 rounded-[2.5rem] bg-gradient-to-br from-white/5 to-transparent pointer-events-none"></div>
          
          <div className="relative text-center">
            {/* Icon with glass effect */}
            <div className="mb-8 inline-block">
              <div className="backdrop-blur-2xl bg-white/10 rounded-3xl p-6 border border-white/20 shadow-lg">
                <span className="text-7xl">🍳</span>
                <span className="text-7xl font-bold bg-gradient-to-r from-white via-blue-100 to-white bg-clip-text text-transparent mb-6 tracking-tight"> Hungry Flow</span>
              </div>
            </div>

            

            {/* Subtitle */}
            <h2 className="text-2xl text-white/90 mb-4 font-medium">
              The best multi AI agent app to discover your food
            </h2>

            {/* Description */}
            <p className="text-lg text-white/70 mb-3">
              Just upload your fridge picture and describe what you want!
            </p>
            
            <p className="text-white/60 text-sm mb-10 max-w-2xl mx-auto leading-relaxed">
              Our AI agent family will work together to provide the best recipe from your fridge
              and guide you step by step. Our Advisor Agent always cares about your health! 💚
            </p>

            {/* CTA Button with glass effect */}
            <button
              onClick={() => navigate('/input')}
              className="group relative py-5 px-14 backdrop-blur-2xl bg-white/15 text-white font-semibold text-xl rounded-full shadow-lg border border-white/30 hover:bg-white/25 hover:scale-[1.02] transition-all duration-300"
            >
              {/* Button glow effect */}
              <div className="absolute inset-0 rounded-full bg-gradient-to-r from-blue-400/20 to-purple-400/20 blur-xl group-hover:blur-2xl transition-all duration-300"></div>
              
              <span className="relative flex items-center justify-center gap-3">
                <span className="text-4xl"></span>
                Try it Now
              </span>
            </button>

            {/* Feature Pills */}
            <div className="mt-10 flex flex-wrap justify-center gap-3">
              <div className="backdrop-blur-xl bg-white/10 px-5 py-2 rounded-full border border-white/20 text-white/80 text-sm font-medium">
                ⚡ Fast AI Processing
              </div>
              <div className="backdrop-blur-xl bg-white/10 px-5 py-2 rounded-full border border-white/20 text-white/80 text-sm font-medium">
                🎯 Smart Ingredient Detection
              </div>
              <div className="backdrop-blur-xl bg-white/10 px-5 py-2 rounded-full border border-white/20 text-white/80 text-sm font-medium">
                💚 Health Focused
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Info Card */}
        <div className="mt-6 backdrop-blur-2xl bg-white/5 rounded-3xl p-6 border border-white/10 text-center">
          <p className="text-white/60 text-sm">
            Powered by Multi-Agent AI System • Made with ❤️ for CalHacks 12.0
          </p>
        </div>
      </div>
    </div>
  )
}

export default HomePage
