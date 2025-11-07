export default function MessageBubble({ role, content }) {
  const isUser = role === 'user'
  return (
    <div className={`w-full flex ${isUser ? 'justify-end' : 'justify-start'} my-1`}>
      <div className={`${isUser ? 'bg-blue-600' : 'bg-gray-800'} max-w-[80%] px-3 py-2 rounded-lg whitespace-pre-wrap break-words`}>
        <div className="text-xs opacity-80 mb-1">{isUser ? 'You' : 'AI'}</div>
        <div className="text-sm">{content}</div>
      </div>
    </div>
  )
}
