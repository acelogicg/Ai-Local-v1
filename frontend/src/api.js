import axios from 'axios'

const BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000'

export const api = axios.create({
  baseURL: BASE,
  headers: { 'Content-Type': 'application/json' },
})

// APIs
export async function newChat(title = 'New Chat') {
  const { data } = await api.post('/newchat', { title })
  return data
}

export async function sendMessage(conversation_id, prompt) {
  const { data } = await api.post('/chat', { conversation_id, prompt })
  return data
}

export async function listChats() {
  const { data } = await api.get('/conversations')
  return data
}

export async function getHistory(conversation_id) {
  const { data } = await api.get(`/history/${conversation_id}`)
  return data
}
