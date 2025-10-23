import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './ChatWidget.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ChatWidget = ({ isOpen, onToggle }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState('Junior');
  const [conversationId, setConversationId] = useState(null);
  const messagesEndRef = useRef(null);

  const agents = [
    { name: 'Junior Cucurella', label: 'Gerente de Agendas', avatar: '👨‍💼' },
    { name: 'Jacinto Torrelavega', label: 'Facturación', avatar: '👔' },
    { name: 'Alex Albiol', label: 'Soporte Técnico', avatar: '👨‍💻' },
    { name: 'Silvia Garcia', label: 'Integración', avatar: '👩‍💼' },
    { name: 'Blanca Garcia', label: 'RPA', avatar: '👩‍🔬' },
    { name: 'Rocío Almeida', label: 'Reputación', avatar: '/assets/rocio-chat.png', isImage: true },
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen && messages.length === 0) {
      setMessages([
        {
          role: 'assistant',
          content: '¡Hola! ¿En qué puedo ayudarte hoy?',
          agent: selectedAgent,
        },
      ]);
    }
  }, [isOpen]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(`${API}/chat`, {
        message: input,
        agent_name: selectedAgent,
        conversation_id: conversationId,
      });

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: response.data.response,
          agent: selectedAgent,
        },
      ]);

      if (!conversationId) {
        setConversationId(response.data.conversation_id);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Lo siento, hubo un error. Por favor, intenta nuevamente.',
          agent: selectedAgent,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className={`chat-widget ${isOpen ? 'open' : ''}`} data-testid="chat-widget">
        <div className="chat-header" data-testid="chat-header">
          <div>
            <h3>Chat con IA</h3>
            <p className="agent-info">Hablando con: {selectedAgent}</p>
          </div>
          <button 
            className="chat-close" 
            onClick={onToggle}
            data-testid="chat-close-btn"
          >
            ×
          </button>
        </div>

        <div className="agent-selector" data-testid="agent-selector">
          {agents.map((agent) => (
            <button
              key={agent.name}
              className={`agent-btn ${selectedAgent === agent.name ? 'active' : ''}`}
              onClick={() => setSelectedAgent(agent.name)}
              data-testid={`agent-btn-${agent.name.toLowerCase()}`}
            >
              {agent.label}
            </button>
          ))}
        </div>

        <div className="chat-messages" data-testid="chat-messages">
          {messages.map((msg, index) => {
            const agent = agents.find(a => a.name === msg.agent) || agents[0];
            return (
              <div
                key={index}
                className={`message ${msg.role}`}
                data-testid={`message-${index}`}
              >
                {msg.role === 'assistant' && (
                  <div className="message-avatar">
                    {agent.isImage ? (
                      <img src={agent.avatar} alt={agent.name} className="avatar-image" />
                    ) : (
                      <span className="avatar-emoji">{agent.avatar}</span>
                    )}
                  </div>
                )}
                <div className="message-content">
                  {msg.role === 'assistant' && (
                    <div className="agent-name">{agent.name}</div>
                  )}
                  <div>{msg.content}</div>
                </div>
              </div>
            );
          })}
          {loading && (
            <div className="message assistant" data-testid="loading-indicator">
              <div className="message-avatar">
                <span className="avatar-emoji">{agents.find(a => a.name === selectedAgent)?.avatar || '🤖'}</span>
              </div>
              <div className="message-content loading">
                <span>.</span><span>.</span><span>.</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form className="chat-input" onSubmit={sendMessage} data-testid="chat-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Escribe tu mensaje..."
            disabled={loading}
            data-testid="chat-input"
          />
          <button 
            type="submit" 
            disabled={loading || !input.trim()}
            data-testid="chat-send-btn"
          >
            Enviar
          </button>
        </form>
      </div>

      <button 
        className="chat-toggle" 
        onClick={onToggle}
        data-testid="chat-toggle-btn"
      >
        💬
      </button>
    </>
  );
};

export default ChatWidget;
