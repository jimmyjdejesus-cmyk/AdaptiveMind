import React, { useState } from 'react';

// Minimal ChatPane stub to unblock dev server
const ChatPane = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const send = () => {
    if (!input.trim()) return;
    setMessages((prev) => [...prev, { role: 'user', content: input }]);
    setInput('');
  };

  return (
    <div className="pane chat-pane" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div className="messages" style={{ flex: 1, overflow: 'auto', padding: '8px' }}>
        {messages.map((m, i) => (
          <div key={i} className="message" style={{ marginBottom: 8 }}>
            <strong>{m.role}:</strong> {m.content}
          </div>
        ))}
      </div>
      <div className="composer" style={{ display: 'flex', gap: 8, padding: 8, borderTop: '1px solid #333' }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
          style={{ flex: 1 }}
        />
        <button onClick={send}>Send</button>
      </div>
    </div>
  );
};

export default ChatPane;

