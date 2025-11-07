import { useEffect, useRef, useState } from 'react'
import MessageBubble from './MessageBubble.jsx'

export default function ChatWindow({ messages, onSend, disabled }) {
  const [text, setText] = useState('')
  const [busy, setBusy] = useState(false)
  const viewRef = useRef(null)

  useEffect(() => {
    if (viewRef.current) {
      viewRef.current.scrollTop = viewRef.current.scrollHeight
    }
  }, [messages, busy])

  const submit = async (e) => {
    e.preventDefault()
    if (!text.trim() || busy) return
    try {
      setBusy(true)
      await onSend(text.trim())
      setText('')
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="flex-1 flex flex-col">
      <div ref={viewRef} className="flex-1 overflow-y-auto p-4 space-y-1">
        {messages && messages.map((m, i) => (
          <MessageBubble key={i} role={m.role} content={m.content} />
        ))}
        {!messages?.length && (
          <div className="h-full w-full flex items-center justify-center opacity-60">
            <div>Tidak ada pesan. Mulai ketik untuk berbicara dengan AI lokal.</div>
          </div>
        )}
      </div>
      <form onSubmit={submit} className="border-t border-gray-800 p-3 flex gap-2">
        <input
          className="flex-1 bg-gray-800 rounded px-3 py-2 outline-none"
          placeholder="Ketik pesan lalu Enter..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          disabled={disabled || busy}
        />
        <button
          className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded disabled:opacity-50"
          disabled={disabled || busy || !text.trim()}
        >
          {busy ? 'Mengirim...' : 'Kirim'}
        </button>
      </form>
    </div>
  )
}
