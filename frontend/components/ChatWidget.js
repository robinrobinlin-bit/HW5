import { useState, useRef, useEffect } from 'react'

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      text: '您好！我是您的機器學習 AI 助理。您可以詢問我任何關於本平台支持的 10 大機器學習演算法（如 SVM、隨機森林、K-Means、PCA）的數學原理、超參數調整、優缺點或一般 ML 問題！'
    }
  ])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    if (isOpen) {
      scrollToBottom()
    }
  }, [messages, isOpen, isTyping])

  const handleSend = async (e) => {
    if (e) e.preventDefault()
    if (!input.trim()) return

    const userText = input
    setMessages(prev => [...prev, { role: 'user', text: userText }])
    setInput('')
    setIsTyping(true)

    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: userText,
          history: messages.map(m => ({ role: m.role, content: m.text }))
        })
      })

      if (!response.ok) throw new Error('API request failed')
      const data = await response.json()
      
      setMessages(prev => [...prev, { role: 'assistant', text: data.response }])
    } catch (err) {
      console.error(err)
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        text: '對不起，我與後端助理服務失去連線。請確認 FastAPI 伺服器正在 http://localhost:8000 運行。' 
      }])
    } finally {
      setIsTyping(false)
    }
  }

  return (
    <div className="chat-widget-container">
      {/* Floating Action Button */}
      {!isOpen && (
        <button className="chat-fab" onClick={() => setIsOpen(true)}>
          <i className="fa-solid fa-comments"></i>
        </button>
      )}

      {/* Expanded Chat Box */}
      {isOpen && (
        <div className="chat-window">
          {/* Header */}
          <div className="chat-header">
            <div className="chat-header-title">
              <i className="fa-solid fa-robot"></i> JER LIAW AI 學習助理
            </div>
            <button className="chat-close-btn" onClick={() => setIsOpen(false)}>
              <i className="fa-solid fa-xmark"></i>
            </button>
          </div>

          {/* Messages Body */}
          <div className="chat-body">
            {messages.map((msg, idx) => (
              <div key={idx} className={`chat-message-row ${msg.role}`}>
                <div className={`chat-bubble ${msg.role}`}>
                  {msg.text}
                </div>
              </div>
            ))}
            
            {/* Typing indicator */}
            {isTyping && (
              <div className="chat-message-row assistant">
                <div className="chat-bubble assistant typing">
                  <span className="dot"></span>
                  <span className="dot"></span>
                  <span className="dot"></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Form Footer */}
          <form className="chat-footer" onSubmit={handleSend}>
            <input 
              type="text" 
              className="chat-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="輸入問題，例如：什麼是 SVM？"
            />
            <button type="submit" className="chat-send-btn">
              <i className="fa-solid fa-paper-plane"></i>
            </button>
          </form>
        </div>
      )}
    </div>
  )
}
