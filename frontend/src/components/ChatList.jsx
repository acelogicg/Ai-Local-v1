export default function ChatList({ chats, onNew, onOpen, current }) {
  return (
    <div className="w-72 border-r border-gray-800 flex flex-col">
      <div className="p-4 border-b border-gray-800 flex items-center justify-between">
        <h1 className="font-semibold">Conversations</h1>
        <button onClick={onNew} className="bg-blue-600 hover:bg-blue-700 px-3 py-1 rounded">New</button>
      </div>
      <div className="flex-1 overflow-y-auto">
        {chats.length === 0 && (
          <div className="p-4 text-sm opacity-60">Belum ada percakapan.</div>
        )}
        {chats.map((c) => (
          <button
            key={c.conversation_id}
            onClick={() => onOpen(c.conversation_id)}
            className={`w-full text-left px-4 py-3 hover:bg-gray-800 ${current === c.conversation_id ? 'bg-gray-800' : ''}`}
          >
            <div className="text-sm font-medium">{c.title || 'Untitled'}</div>
            <div className="text-xs opacity-60">{new Date(c.created_at).toLocaleString()}</div>
          </button>
        ))}
      </div>
    </div>
  )
}
