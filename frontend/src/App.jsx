import { useEffect, useState } from 'react'
import { newChat, sendMessage, listChats, getHistory } from './api.js'
import ChatList from './components/ChatList.jsx'
import ChatWindow from './components/ChatWindow.jsx'

export default function App() {
  const [chats, setChats] = useState([])
  const [current, setCurrent] = useState(null)
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  const refreshChats = async () => {
    const data = await listChats()
    setChats(data)
  }

  useEffect(() => { refreshChats() }, [])

  const handleNewChat = async () => {
    const c = await newChat('New Chat')
    setCurrent(c.conversation_id)
    setMessages([])
    await refreshChats()
  }

  const openChat = async (id) => {
    setCurrent(id)
    setLoading(true)
    try {
      const h = await getHistory(id)
      setMessages(h.messages || [])
    } finally {
      setLoading(false)
    }
  }

  const handleSend = async (text) => {
    if (!current) {
      const c = await newChat('Quick Chat')
      setCurrent(c.conversation_id)
      await refreshChats()
    }
    const res = await sendMessage(current || (await listChats())[0]?.conversation_id, text)
    // append locally
    setMessages(prev => [...prev, { role: 'user', content: text }, { role: 'ai', content: res.response }])
  }

  return (
    <div className="flex h-screen">
      <ChatList chats={chats} onNew={handleNewChat} onOpen={openChat} current={current} />
      <div className="flex-1 flex flex-col">
        <div className="px-4 py-3 border-b border-gray-800 flex items-center gap-2">
          <div className="font-semibold">AI Local Chat</div>
          <div className="text-xs opacity-60">Server: {import.meta.env.VITE_API_BASE || 'http://localhost:5000'}</div>
          <div className="flex-1" />
          <button onClick={refreshChats} className="text-xs bg-gray-800 px-2 py-1 rounded">Refresh</button>
        </div>
        <ChatWindow messages={messages} onSend={handleSend} disabled={loading} />
      </div>
    </div>
  )
}
