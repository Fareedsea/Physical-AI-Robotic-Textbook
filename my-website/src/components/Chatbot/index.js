/**
 * React chatbot component for the Physical AI & Humanoid Robotics Textbook
 * Provides an interactive interface for querying textbook content
 */

import React, { useState, useEffect, useRef } from 'react';
import textbookApiClient from '../../utils/api-client';
import './Chatbot.css';

const Chatbot = ({ userId = null, sessionId = null, onNewResponse = null }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showFeedback, setShowFeedback] = useState(null); // Track which message to show feedback for
  const messagesEndRef = useRef(null);

  // Scroll to bottom of messages when new messages are added
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!inputValue.trim() || isLoading) {
      return;
    }

    // Add user message to the chat
    const userMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      // Get response from the chatbot API
      const response = await textbookApiClient.queryChatbot(
        inputValue,
        userId,
        sessionId,
        messages.filter(msg => msg.role === 'user' || msg.role === 'assistant')
      );

      // Add assistant response to the chat
      const assistantMessage = {
        id: response.query_id || `assistant-${Date.now()}`,
        role: 'assistant',
        content: response.response,
        sources: response.sources || [],
        confidence: response.confidence,
        timestamp: response.timestamp || new Date().toISOString(),
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Call the callback if provided
      if (onNewResponse) {
        onNewResponse(assistantMessage);
      }
    } catch (err) {
      setError('Failed to get response. Please try again.');
      console.error('Chat error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFeedback = async (queryId, rating, useful, comment = null) => {
    try {
      await textbookApiClient.submitFeedback(queryId, userId, rating, useful, comment);
      setShowFeedback(null); // Hide feedback form after submission
    } catch (err) {
      console.error('Feedback submission error:', err);
    }
  };

  const toggleFeedback = (messageId) => {
    setShowFeedback(showFeedback === messageId ? null : messageId);
  };

  const renderSources = (sources) => {
    if (!sources || sources.length === 0) {
      return null;
    }

    return (
      <div className="chatbot-sources">
        <p className="sources-title">Sources:</p>
        <ul className="sources-list">
          {sources.map((source, index) => (
            <li key={index} className="source-item">
              <a
                href={source.relative_path || source.source_url || '#'}
                target="_blank"
                rel="noopener noreferrer"
              >
                {source.title || source.chapter || 'Source'}
              </a>
              {source.chapter && <span className="source-chapter"> ({source.chapter})</span>}
            </li>
          ))}
        </ul>
      </div>
    );
  };

  const renderMessage = (message) => {
    const isUser = message.role === 'user';
    const messageClasses = `chatbot-message ${isUser ? 'user-message' : 'assistant-message'}`;

    return (
      <div key={message.id} className={messageClasses}>
        <div className="message-content">
          {message.content}
          {!isUser && message.sources && renderSources(message.sources)}
          {!isUser && message.confidence !== undefined && (
            <div className="confidence-score">
              Confidence: {(message.confidence * 100).toFixed(1)}%
            </div>
          )}
        </div>
        {!isUser && (
          <div className="message-actions">
            <button
              className="feedback-btn"
              onClick={() => toggleFeedback(message.id)}
              aria-label="Provide feedback"
            >
              👍👎
            </button>
            {showFeedback === message.id && (
              <FeedbackForm
                queryId={message.id}
                onSubmit={handleFeedback}
                onClose={() => setShowFeedback(null)}
              />
            )}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <h3>Textbook Assistant</h3>
        <p>Ask questions about Physical AI & Humanoid Robotics</p>
      </div>

      <div className="chatbot-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <p>Hello! I'm your textbook assistant. Ask me anything about Physical AI and Humanoid Robotics.</p>
            <p>Try asking: "What is Physical AI?" or "Explain humanoid robot control systems."</p>
          </div>
        ) : (
          messages.map(renderMessage)
        )}
        {isLoading && (
          <div className="chatbot-message assistant-message">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {error && (
        <div className="chatbot-error">
          {error}
        </div>
      )}

      <form className="chatbot-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask a question about the textbook..."
          disabled={isLoading}
          aria-label="Type your question"
        />
        <button
          type="submit"
          disabled={!inputValue.trim() || isLoading}
          aria-label="Send message"
        >
          Send
        </button>
      </form>
    </div>
  );
};

// Feedback form component
const FeedbackForm = ({ queryId, onSubmit, onClose }) => {
  const [rating, setRating] = useState(null);
  const [useful, setUseful] = useState(null);
  const [comment, setComment] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(queryId, rating, useful, comment);
  };

  return (
    <div className="feedback-form">
      <form onSubmit={handleSubmit}>
        <div className="feedback-options">
          <label>
            <input
              type="radio"
              name="useful"
              value="true"
              checked={useful === true}
              onChange={() => setUseful(true)}
            />
            Useful
          </label>
          <label>
            <input
              type="radio"
              name="useful"
              value="false"
              checked={useful === false}
              onChange={() => setUseful(false)}
            />
            Not Useful
          </label>
        </div>

        <div className="rating-section">
          <label>Rate (1-5):</label>
          <div className="rating-buttons">
            {[1, 2, 3, 4, 5].map(num => (
              <button
                key={num}
                type="button"
                className={`rating-btn ${rating === num ? 'selected' : ''}`}
                onClick={() => setRating(num)}
              >
                {num}
              </button>
            ))}
          </div>
        </div>

        <textarea
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          placeholder="Additional feedback..."
          rows="2"
        />

        <div className="feedback-actions">
          <button type="submit">Submit</button>
          <button type="button" onClick={onClose}>Cancel</button>
        </div>
      </form>
    </div>
  );
};

export default Chatbot;