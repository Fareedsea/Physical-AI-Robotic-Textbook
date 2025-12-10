/**
 * API client for the Physical AI & Humanoid Robotics Textbook RAG system
 * Provides methods for interacting with the backend API from the frontend
 */

class TextbookApiClient {
  constructor(baseURL = '/api') {
    this.baseURL = baseURL;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
  }

  /**
   * Make an API request
   * @param {string} endpoint - API endpoint
   * @param {string} method - HTTP method
   * @param {Object} body - Request body (for POST, PUT, PATCH)
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} API response
   */
  async request(endpoint, method = 'GET', body = null, params = null) {
    let url = `${this.baseURL}${endpoint}`;

    // Add query parameters if provided
    if (params) {
      const queryString = new URLSearchParams(params).toString();
      url += `?${queryString}`;
    }

    const config = {
      method,
      headers: { ...this.defaultHeaders },
    };

    if (body && method !== 'GET') {
      config.body = JSON.stringify(body);
    }

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request error:', error);
      throw error;
    }
  }

  /**
   * Query the textbook chatbot
   * @param {string} query - User's question
   * @param {string} userId - User identifier
   * @param {string} sessionId - Session identifier
   * @param {Array} history - Conversation history
   * @returns {Promise<Object>} Chat response
   */
  async queryChatbot(query, userId = null, sessionId = null, history = null) {
    const requestBody = {
      query,
      user_id: userId,
      session_id: sessionId,
      history: history || [],
    };

    return this.request('/chat/query', 'POST', requestBody);
  }

  /**
   * Get chat history for a user
   * @param {string} userId - User identifier
   * @param {string} sessionId - Session identifier (optional)
   * @param {number} limit - Number of history items to return
   * @param {number} offset - Offset for pagination
   * @returns {Promise<Object>} Chat history
   */
  async getChatHistory(userId, sessionId = null, limit = 10, offset = 0) {
    const params = {
      user_id: userId,
      limit: limit.toString(),
      offset: offset.toString(),
    };

    if (sessionId) {
      params.session_id = sessionId;
    }

    return this.request('/chat/history', 'GET', null, params);
  }

  /**
   * Submit feedback for a chat response
   * @param {string} queryId - ID of the query being rated
   * @param {string} userId - User identifier
   * @param {number} rating - Rating from 1-5
   * @param {boolean} useful - Whether the response was useful
   * @param {string} comment - Additional feedback comment
   * @returns {Promise<Object>} Feedback submission result
   */
  async submitFeedback(queryId, userId = null, rating = null, useful = null, comment = null) {
    const requestBody = {
      query_id: queryId,
      user_id: userId,
      rating: rating,
      useful: useful,
      comment: comment,
    };

    return this.request('/chat/feedback', 'POST', requestBody);
  }

  /**
   * Search textbook content
   * @param {string} query - Search query
   * @param {Object} filters - Additional filters for search
   * @param {number} maxResults - Maximum number of results to return
   * @param {number} minRelevance - Minimum relevance threshold
   * @returns {Promise<Object>} Search results
   */
  async searchContent(query, filters = null, maxResults = 10, minRelevance = 0.0) {
    const requestBody = {
      query,
      filters: filters || null,
      max_results: maxResults,
      min_relevance: minRelevance,
    };

    return this.request('/content/search', 'POST', requestBody);
  }

  /**
   * Search textbook content using GET method (for simpler integration)
   * @param {string} query - Search query
   * @param {number} maxResults - Maximum number of results to return
   * @param {number} minRelevance - Minimum relevance threshold
   * @returns {Promise<Object>} Search results
   */
  async searchContentSimple(query, maxResults = 10, minRelevance = 0.0) {
    const params = {
      query,
      max_results: maxResults.toString(),
      min_relevance: minRelevance.toString(),
    };

    return this.request('/content/search', 'GET', null, params);
  }
}

// Create a singleton instance
const textbookApiClient = new TextbookApiClient();

// Export the class and instance
export { TextbookApiClient, textbookApiClient };

// Also provide a default export for easier usage
export default textbookApiClient;