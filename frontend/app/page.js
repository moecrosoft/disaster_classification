'use client'

import { useState } from 'react'

export default function Home() {
  const [text, setText] = useState('')
  const [result, setResults] = useState(null)
  const [submittedMessage, setSubmittedMessage] = useState('')

  const [showHistory, setShowHistory] = useState(false)
  const [messages, setMessages] = useState([])

  const [showResult, setShowResult] = useState(false)

  const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL 

  async function analyse() {
    const res = await fetch(`${BACKEND_URL}/predict`,{
      method: 'POST',
      headers: { 'Content-Type': 'application/json'},
      body: JSON.stringify({ text })
    })

    const data = await res.json()
    setResults(data.prediction)
    setSubmittedMessage(text)
    setText('')
    setShowResult(true)
  }

  async function loadHistory(){
    const res = await fetch(`${BACKEND_URL}/history`)
    const data = await res.json()
    setMessages(data)
    setShowHistory(true)
  }

  return (
    <div className='min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-black p-6'>
      <div className='bg-gray-800 shadow-xl rounded-2xl p-10 w-full max-w-xl flex flex-col gap-6 border border-gray-700'>
        <h1 className='text-3xl font-semibold text-center text-white'>
          Emergency Detection AI
        </h1>
        <p className='text-center text-gray-400 text-sm'>
          Enter a message and the AI will determine if it indicates an emergency. 
        </p>

        <textarea
          className='border border-gray-600 bg-gray-900 text-white rounded-xl p-4 w-full h-32 resize-none focus:outline-none focus:ring-red-500 transition placeholder-gray-400'
          placeholder='Example: Someone collapsed and needs help...'
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <div className='flex gap-4 justify-center'>
          <button
            onClick={analyse}
            className='flex-1 bg-red-600 hover:bg-red-700 text-white font-medium py-2 rounded-xl transition shadow-sm cursor-pointer text-sm'
          >
            Analyze
          </button>

          <button
            onClick={loadHistory}
            className='flex-1 bg-gray-700 hover:bg-gray-600 text-white font-semibold py-2 rounded-xl transition cursor-pointer text-sm'
          >
            History
          </button>
        </div>
      </div>

      {showResult && (
        <div className='fixed inset-0 bg-black/70 flex items-center justify-center'>
          <div className='bg-gray-800 w-full max-w-lg rounded-xl p-6 shadow-xl border border-gray-700'>
            <div className='flex justify-between items-center mb-4'>
              <h2 className='text-xl font-bold text-white'>AI Prediction</h2>
              <button
                onClick={() => setShowResult(false)}
                className='text-red-400 font-bold text-lg cursor-pointer'
              >
                X
              </button>
            </div>
            <div className='flex flex-col gap-4'>
              <div className='text-sm text-gray-400'>Your Message</div>
              <div className='text-white font-medium'>{submittedMessage}</div>
              <div className='border-t border-gray-700 pt-2 mt-2 text-sm text-gray-400'>
                AI Result
              </div>
              <div
                className={`font-semibold ${
                  result?.split(' ')[0].toLowerCase() === "emergency"
                    ? "text-red-400"
                    : "text-green-400"
                }`}
              >
                {result}
              </div>
            </div>
          </div>
        </div>
      )}

      {showHistory && (
        <div className='fixed inset-0 bg-black/70 flex items-center justify-center'>
          <div className='bg-gray-800 w-full max-w-lg rounded-xl p-6 shadow-xl border border-gray-700'>
            <div className='flex justify-between items-center mb-4'>
              <h2 className='text-xl font-bold text-white'>Message History</h2>
              <button
                onClick={() => setShowHistory(false)}
                className='text-red-400 font-bold text-lg cursor-pointer'
              >
                X
              </button>
            </div>
            <div className='flex flex-col gap-4 max-h-96 overflow-y-auto'>
              {messages.map((m, i) => (
                <div
                  key={i}
                  className='bg-gray-900 border border-gray-700 rounded-lg p-4 flex flex-col gap-2'
                >
                  <div className='text-sm text-gray-400'>User Message</div>
                  <div className='text-white font-medium'>{m.user_message}</div>
                  <div className='border-t border-gray-700 pt-2 mt-2 text-sm text-gray-400'>
                    AI Result
                  </div>
                  <div
                    className={`font-semibold ${
                      m.ai_result?.split(' ')[0].toLowerCase() === "emergency"
                        ? "text-red-400"
                        : "text-green-400"
                    }`}
                  >
                    {m.ai_result}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}