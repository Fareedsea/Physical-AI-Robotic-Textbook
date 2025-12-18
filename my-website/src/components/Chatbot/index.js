/**
 * Enhanced React chatbot component for the Physical AI & Humanoid Robotics Textbook
 * Provides an interactive interface for querying textbook content with text grounding
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import textbookApiClient from '../../utils/api-client';
import './Chatbot.css';

const Chatbot = ({ userId = null, sessionId = null, onNewResponse = null }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showFeedback, setShowFeedback] = useState(null); // Track which message to show feedback for
  const [selectedText, setSelectedText] = useState(null); // Track selected text for grounding
  const [isSelectingText, setIsSelectingText] = useState(false); // Track if user is selecting text
  const [isMobile, setIsMobile] = useState(false);
  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);

  // Check if device is mobile
  useEffect(() => {
    const checkIsMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };

    checkIsMobile();
    window.addEventListener('resize', checkIsMobile);
    return () => window.removeEventListener('resize', checkIsMobile);
  }, []);

  // Scroll to bottom of messages when new messages are added
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Handle text selection for grounding
  useEffect(() => {
    const handleGlobalSelection = () => {
      if (!isSelectingText) return;

      const selection = window.getSelection();
      if (selection && selection.toString().trim() !== '') {
        const selectedText = selection.toString().trim();
        if (selectedText.length > 0) {
          setSelectedText(selectedText);
          setIsSelectingText(false);
        }
      }
    };

    document.addEventListener('mouseup', handleGlobalSelection);
    return () => {
      document.removeEventListener('mouseup', handleGlobalSelection);
    };
  }, [isSelectingText]);

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
      selectedText: selectedText, // Include selected text if available
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      // Get response from the chatbot API with selected text context
      const response = await textbookApiClient.queryChatbot(
        inputValue,
        userId,
        sessionId,
        messages.filter(msg => msg.role === 'user' || msg.role === 'assistant'),
        selectedText // Include selected text for grounding
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
      // Clear selected text after submission
      setSelectedText(null);
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

  const startTextSelection = () => {
    setIsSelectingText(true);
    setSelectedText(null);
  };

  const clearSelectedText = () => {
    setSelectedText(null);
    setIsSelectingText(false);
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
          {isUser && message.selectedText && (
            <div className="selected-text-context">
              <p><strong>Context:</strong> "{message.selectedText}"</p>
            </div>
          )}
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
    <div className={`chatbot-container ${isMobile ? 'chatbot-container--mobile' : ''}`}>
      <div className="chatbot-header">
        <h3>Textbook Assistant</h3>
        <p>Ask questions about Physical AI & Humanoid Robotics</p>
        {selectedText && (
          <div className="selected-text-indicator">
            <p><strong>Selected text:</strong> "{selectedText.substring(0, isMobile ? 30 : 50)}{selectedText.length > (isMobile ? 30 : 50) ? '...' : ''}"</p>
            <button onClick={clearSelectedText} className="clear-selection-btn">Clear</button>
          </div>
        )}
      </div>

      <div
        ref={chatContainerRef}
        className="chatbot-messages"
      >
        {messages.length === 0 ? (
          <div className="welcome-message">
            <p>Hello! I'm your textbook assistant. Ask me anything about Physical AI and Humanoid Robotics.</p>
            <p>Try asking: "What is Physical AI?" or "Explain humanoid robot control systems."</p>
            <p className="text-grounding-instruction">
              <button onClick={startTextSelection} className="select-text-btn">Select text</button> in the textbook to ask questions specifically about it.
            </p>
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
        <div className="input-container">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder={selectedText ? "Ask about the selected text..." : "Ask a question about the textbook..."}
            disabled={isLoading}
            aria-label="Type your question"
            onKeyPress={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
          />
          <button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            aria-label="Send message"
          >
            {isMobile ? '→' : 'Send'}
          </button>
        </div>
        {selectedText && (
          <div className="selected-text-preview">
            <small>Context: "{selectedText.substring(0, isMobile ? 40 : 60)}{selectedText.length > (isMobile ? 40 : 60) ? '...' : ''}"</small>
          </div>
        )}
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