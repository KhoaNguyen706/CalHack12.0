import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import TextBox from "./components/TextBox";
import ImageBox from "./components/ImageBox";
import './App.css'

function App() {  
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank"> 
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>--
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>

   
    <div className="flex flex-col items-center gap-6 p-8">
      <h1 className="text-2xl font-bold">My Image Gallery</h1>
      <ImageBox src="/myphoto.jpg" alt="My Photo" className="w-80 h-52" />
      <ImageBox src="/landscape.jpg" alt="Landscape" className="w-96 h-60" />
    </div>
    </div>
    <div className="flex flex-col items-center gap-4 p-8">
      <h1 className="text-2xl font-bold">Enter Your Name</h1>
      <TextBox
        label="Name"
        placeholder="Type your name here..."
        
      />
      <p className="text-gray-700">You typed: {name}</p>
    </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
