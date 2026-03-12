'use client'

import { useState } from 'react'

export default function Home(){
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)

  async function analyse(){
    const res = await fetch('http://localhost:8000/predict',{
      method:'POST',
      headers:{
        'Content-Type':'application/json'
      },
      body:JSON.stringify({text})
    })

    const data = await res.json()
    setResult(data.prediction)
  }

  return(
    <div className='min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-100 to-slate-200 p-6'>

      <div className='bg-white/90 backdrop-blur shadow-xl rounded-2xl p-10 w-full max-w-xl flex flex-col gap-6 border border-gray-200'>

        <h1 className='text-3xl font-semibold text-center text-gray-800'>
          Emergency Detection AI
        </h1>

        <p className='text-center text-gray-500 text-sm'>
          Enter a message and the AI will determine if it indicates an emergency.
        </p>

        <textarea
          className='border border-gray-300 rounded-xl p-4 w-full h-32 resize-none focus:outline-none focus:ring-2 focus:ring-red-500 transition'
          placeholder='Example: Someone collapsed and needs help...'
          value={text}
          onChange={(e)=>setText(e.target.value)}
        />

        <button
          onClick={analyse}
          className='bg-red-600 hover:bg-red-700 text-white font-medium py-3 rounded-xl transition shadow-sm cursor-pointer'
        >
          Analyse Message
        </button>

        {result && (
          <div className='rounded-xl p-4 text-center border bg-slate-50'>
            <span className='text-gray-500 text-sm'>
              Prediction
            </span>
            <div className='text-xl font-semibold text-gray-800 mt-1'>
              {result}
            </div>
          </div>
        )}

      </div>

    </div>
  )
}