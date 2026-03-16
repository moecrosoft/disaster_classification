'use client'

import { useState } from 'react'

export default function Home(){
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)

  const [showHistory, setShowHistory] = useState(false)
  const [messages, setMessages] = useState([])

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
    setText('')
  }

  async function loadHistory(){
    const res = await fetch('http://localhost:8000/history')
    const data = await res.json()

    setMessages(data)
    setShowHistory(true)
  }

  return(
    <div className='min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-black p-6'>

      <div className='bg-gray-800 shadow-xl rounded-2xl p-10 w-full max-w-xl flex flex-col gap-6 border border-gray-700'>

        <h1 className='text-3xl font-semibold text-center text-white'>
          Emergency Detection AI
        </h1>

        <p className='text-center text-gray-400 text-sm'>
          Enter a message and the AI will determine if it indicates an emergency.
        </p>

        <textarea
          className='border border-gray-600 bg-gray-900 text-white rounded-xl p-4 w-full h-32 resize-none focus:outline-none focus:ring-2 focus:ring-red-500 transition placeholder-gray-400'
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

        <button
          onClick={loadHistory}
          className='bg-gray-700 hover:bg-gray-600 text-white font-semibold py-3 rounded-xl transition cursor-pointer'
        >
          View History
        </button>

        {result && (
          <div className='rounded-xl p-4 text-center border border-gray-600 bg-gray-900'>
            <span className='text-gray-400 text-sm'>
              Prediction
            </span>
            <div className='text-xl font-semibold text-white mt-1'>
              {result}
            </div>
          </div>
        )}

      </div>


      {showHistory && (
        <div className='fixed inset-0 bg-black/70 flex items-center justify-center'>

          <div className='bg-gray-800 w-full max-w-lg rounded-xl p-6 shadow-xl border border-gray-700'>

            <div className='flex justify-between items-center mb-4'>
              <h2 className='text-xl font-bold text-white'>
                Message History
              </h2>

              <button
                onClick={()=>setShowHistory(false)}
                className='text-red-400 font-bold text-lg cursor-pointer'
              >
                X
              </button>
            </div>


            <div className='flex flex-col gap-4 max-h-96 overflow-y-auto'>

              {messages.map((m,i)=>(
                <div
                  key={i}
                  className='bg-gray-900 border border-gray-700 rounded-lg p-4 flex flex-col gap-2'
                >

                  <div className='text-sm text-gray-400'>
                    User Message
                  </div>

                  <div className='text-white font-medium'>
                    {m.user_message}
                  </div>

                  <div className='border-t border-gray-700 pt-2 mt-2 text-sm text-gray-400'>
                    AI Result
                  </div>

                  <div className='text-green-400 font-semibold'>
                    {m.ai_result}
                  </div>

                </div>
              ))}

            </div>

          </div>

        </div>
      )}

    </div>
  )
}