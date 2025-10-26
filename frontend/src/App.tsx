import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import TextBox from "./components/TextBox";
import ImageBox from "./components/ImageBox";
import './App.css'

function App() {  
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 to-blue-50 flex flex-col items-center p-8 font-sans">
      {/* Header Logos */}
      <header className="flex gap-6 items-center mb-8">
        <a href="https://vite.dev" target="_blank" rel="noreferrer">
          <img src={viteLogo} className="w-16 h-16 hover:scale-110 transition-transform" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank" rel="noreferrer">
          <img src={reactLogo} className="w-16 h-16 hover:scale-110 transition-transform" alt="React logo" />
        </a>
        <h1 className="text-4xl font-bold text-gray-800 ml-4">Vite + React</h1>
      </header>

      {/* Counter Card */}
      <div className="bg-white rounded-2xl shadow-lg p-8 w-full max-w-md text-center mb-8">
        <button
          onClick={() => setCount(count + 1)}
          className="bg-purple-500 text-white px-6 py-3 rounded-lg shadow-md hover:bg-purple-600 transition-colors"
        >
          Count is {count}
        </button>
        <p className="mt-4 text-gray-600">
          Edit <code className="bg-gray-100 px-1 rounded">src/App.tsx</code> and save to test HMR
        </p>
      </div>

      {/* Image Gallery */}
      <div className="bg-white rounded-2xl shadow-lg p-8 w-full max-w-3xl mb-8">
        <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">My Image Gallery</h2>
        <div className="flex flex-wrap justify-center gap-6">
          <ImageBox src="/myphoto.jpg" alt="My Photo" className="w-80 h-52 rounded-lg shadow-md object-cover" />
          <ImageBox src="/landscape.jpg" alt="Landscape" className="w-96 h-60 rounded-lg shadow-md object-cover" />
        </div>
      </div>

      {/* Name Input */}
      <div className="bg-white rounded-2xl shadow-lg p-8 w-full max-w-md text-center mb-8">
        <h2 className="text-2xl font-bold mb-4 text-gray-800">Enter Your Name</h2>
        <TextBox
          label="Name"
          placeholder="Type your name here..."
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="mb-4"
        />
        <p className="text-gray-700">You typed: <span className="font-semibold">{name}</span></p>
      </div>

      <footer className="mt-6 text-gray-500">
        Click on the Vite and React logos to learn more
      </footer>
    </div>
  )
}

export default App
