<template>
  <div class="chat-wrapper" :class="{ 'dark-mode': darkMode }">
    <!-- Animated Background -->
    <div class="chat-background">
      <div class="bg-shape shape-1"></div>
      <div class="bg-shape shape-2"></div>
      <div class="bg-shape shape-3"></div>
      <div class="bg-shape shape-4"></div>
    </div>

    <!-- Main Chat Container -->
    <div class="chat-container">
      <!-- Sidebar with Logo -->
      <aside class="chat-sidebar">
        <div class="sidebar-content">
          <!-- Animated Logo -->
          <div class="logo-section">
            <div class="logo-animation">
              <div class="logo-orb orb-1"></div>
              <div class="logo-orb orb-2"></div>
              <div class="logo-orb orb-3"></div>
              <div class="logo-core">
                <svg class="logo-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
                </svg>
              </div>
            </div>
            <h1 class="brand-name">Cariboun<span class="ai-text">AI</span></h1>
            <p class="brand-tagline">Intelligent Conversations, Infinite Possibilities</p>
          </div>

          <!-- User Info -->
          <div class="user-section">
            <div class="user-avatar">
              <div class="avatar-initials">{{ getUserInitials }}</div>
              <div class="avatar-glow"></div>
            </div>
            <div class="user-info">
              <h3>{{ authStore.getUser?.first_name || 'User' }}</h3>
              <p>{{ authStore.getUser?.email || '' }}</p>
            </div>
          </div>

          <!-- Features -->
          <div class="features-section">
            <div class="feature-item">
              <div class="feature-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
              </div>
              <span>Real-time AI Responses</span>
            </div>
            <div class="feature-item">
              <div class="feature-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
              </div>
              <span>Secure & Private</span>
            </div>
          </div>

          <!-- Actions -->
          <div class="sidebar-actions">
            <button class="sidebar-btn" @click="toggleDarkMode" :title="darkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'">
              <svg v-if="darkMode" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="5"></circle>
                <line x1="12" y1="1" x2="12" y2="3"></line>
                <line x1="12" y1="21" x2="12" y2="23"></line>
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                <line x1="1" y1="12" x2="3" y2="12"></line>
                <line x1="21" y1="12" x2="23" y2="12"></line>
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
              </svg>
              <span>{{ darkMode ? 'Light Mode' : 'Dark Mode' }}</span>
            </button>
            <button class="sidebar-btn logout-btn" @click="logout">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                <polyline points="16 17 21 12 16 7"></polyline>
                <line x1="21" y1="12" x2="9" y2="12"></line>
              </svg>
              <span>Logout</span>
            </button>
          </div>
        </div>
      </aside>

      <!-- Main Chat Area -->
      <main class="chat-main">
        <!-- Chat Header -->
        <header class="chat-header">
          <div class="header-content">
            <h2>💬 Cariboun AI Assistant</h2>
            <div class="header-status">
              <div class="status-indicator" :class="{ online: isOnline }">
                <div class="status-dot"></div>
                <span>{{ isOnline ? 'Connected' : 'Offline' }}</span>
              </div>
              <div class="message-count">{{ messages.length }} messages</div>
            </div>
          </div>
        </header>

        <!-- Messages Container -->
        <div class="messages-container" ref="messagesContainer">
          <!-- Welcome Message -->
          <div v-if="messages.length === 0" class="welcome-screen">
            <div class="welcome-content">
              <div class="welcome-animation">
                <div class="welcome-orb welcome-orb-1"></div>
                <div class="welcome-orb welcome-orb-2"></div>
                <div class="welcome-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                  </svg>
                </div>
              </div>
              <h3>Welcome to Cariboun AI! 🎉</h3>
              <p class="welcome-text">I'm your intelligent assistant, ready to help with any questions you have.</p>
              
              <div class="quick-starters">
                <p class="quick-title">Try asking me:</p>
                <div class="starter-buttons">
                  <button class="starter-btn" @click="sendQuickQuestion('Explain artificial intelligence in simple terms')">
                    🤖 Explain AI basics
                  </button>
                  <button class="starter-btn" @click="sendQuickQuestion('What are the benefits of sustainable technology?')">
                    🌱 Sustainability tips
                  </button>
                  <button class="starter-btn" @click="sendQuickQuestion('How can technology improve daily productivity?')">
                    ⚡ Productivity hacks
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Messages List -->
          <div v-else class="messages-list">
            <div
              v-for="(message, index) in messages"
              :key="message.id"
              :class="['message', message.role, { 'streaming': message.isStreaming }]"
            >
              <!-- Message Avatar -->
              <div class="message-avatar">
                <div v-if="message.role === 'user'" class="avatar user-avatar">
                  <div class="avatar-initials-small">{{ getUserInitials }}</div>
                </div>
                <div v-else class="avatar ai-avatar">
                  <div class="ai-avatar-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
                    </svg>
                  </div>
                </div>
              </div>

              <!-- Message Content -->
              <div class="message-content">
                <!-- Message Header -->
                <div class="message-header">
                  <span class="sender-name">{{ message.role === 'user' ? 'You' : 'Cariboun AI' }}</span>
                  <span class="message-time">{{ formatMessageTime(message.timestamp) }}</span>
                </div>

                <!-- Message Text -->
                <div class="message-text">
                  <!-- User Message -->
                  <div v-if="message.role === 'user'" class="user-message">
                    {{ message.content }}
                  </div>
                  
                  <!-- Streaming AI Message -->
                  <div v-else-if="message.isStreaming" class="streaming-message">
                    <span v-html="renderMarkdown(message.content)"></span>
                    <span class="streaming-cursor"></span>
                  </div>
                  
                  <!-- Completed AI Message -->
                  <div v-else class="ai-message">
                    <div class="message-content-inner" v-html="renderMarkdown(message.content)"></div>
                    <!-- Message Actions -->
                    <div class="message-actions">
                      <button
                        class="action-btn copy-btn"
                        @click="copyToClipboard(message.content)"
                        :title="copiedMessageIndex === index ? 'Copied!' : 'Copy message'"
                      >
                        <svg v-if="copiedMessageIndex === index" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M20 6L9 17l-5-5"></path>
                        </svg>
                        <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                        </svg>
                        <span>{{ copiedMessageIndex === index ? 'Copied' : 'Copy' }}</span>
                      </button>
                      <button
                        v-if="message.role === 'assistant' && !message.isStreaming"
                        class="action-btn regenerate-btn"
                        @click="regenerateResponse(index)"
                        title="Regenerate response"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M23 4v6h-6"></path>
                          <path d="M1 20v-6h6"></path>
                          <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
                        </svg>
                        <span>Regenerate</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Loading Indicator -->
            <div v-if="loading" class="loading-indicator">
              <div class="typing-dots">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
              </div>
              <p class="loading-text">Cariboun AI is thinking...</p>
            </div>
          </div>
        </div>

        <!-- Input Area -->
        <footer class="input-area">
          <form @submit.prevent="sendMessage" class="input-form">
            <div class="input-wrapper">
              <textarea
                v-model="userInput"
                ref="messageInput"
                :placeholder="inputPlaceholder"
                @keydown.enter.exact.prevent="sendMessage"
                @keydown.enter.shift.exact.prevent="userInput += '\n'"
                :disabled="loading || streaming"
                rows="1"
                class="message-input"
                @input="adjustTextareaHeight"
              ></textarea>
              
              <div class="input-actions">
                <button
                  v-if="streaming"
                  type="button"
                  class="cancel-btn"
                  @click="cancelStream"
                  title="Stop generating"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <rect x="7" y="7" width="10" height="10"></rect>
                  </svg>
                  Stop
                </button>
                
                <button
                  type="submit"
                  class="send-btn"
                  :disabled="!canSend || loading || streaming"
                  :class="{ 'sending': loading || streaming }"
                  :title="canSend ? 'Send message' : 'Type a message to send'"
                >
                  <svg v-if="loading || streaming" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <path d="M12 6v6l4 2"></path>
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="22" y1="2" x2="11" y2="13"></line>
                    <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                  </svg>
                </button>
              </div>
            </div>
            
            <div class="input-hints">
              <span class="hint-text">Press Enter to send • Shift+Enter for new line</span>
              <span class="char-count" :class="{ 'warning': userInput.length > 4000 }">
                {{ userInput.length }}/4000
              </span>
            </div>
          </form>
        </footer>
      </main>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { marked } from 'marked';
import DOMPurify from 'dompurify';

// Base URL configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export default {
  name: 'Chat',
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    
    // Refs
    const messagesContainer = ref(null);
    const messageInput = ref(null);
    
    // State
    const messages = ref([]);
    const userInput = ref('');
    const loading = ref(false);
    const streaming = ref(false);
    const abortController = ref(null);
    const darkMode = ref(false);
    const isOnline = ref(navigator.onLine);
    const copiedMessageIndex = ref(null);
    const copyTimeout = ref(null);
    
    // Computed
    const getUserInitials = computed(() => {
      const user = authStore.getUser;
      if (!user) return 'U';
      const first = user.first_name?.[0] || '';
      const last = user.last_name?.[0] || '';
      return (first + last).toUpperCase() || 'U';
    });
    
    const canSend = computed(() => {
      return userInput.value.trim().length > 0 && !loading.value && !streaming.value;
    });
    
    const inputPlaceholder = computed(() => {
      if (loading.value) return 'Cariboun AI is thinking...';
      if (streaming.value) return 'Cariboun AI is responding...';
      return 'Type your message...';
    });
    
    // Methods
    const sendMessage = async () => {
      if (!canSend.value) return;
      
      const content = userInput.value.trim();
      userInput.value = '';
      adjustTextareaHeight();
      
      // Add user message
      const userMessage = {
        id: Date.now(),
        role: 'user',
        content,
        timestamp: new Date().toISOString(),
      };
      messages.value.push(userMessage);
      
      scrollToBottom();
      
      // Start streaming response
      await streamResponse(content);
    };
    
    const streamResponse = async (content) => {
      loading.value = true;
      streaming.value = true;
      
      // Create placeholder for streaming response
      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: '',
        timestamp: new Date().toISOString(),
        isStreaming: true,
      };
      messages.value.push(assistantMessage);
      
      scrollToBottom();
      
      // Cancel any existing stream
      if (abortController.value) {
        abortController.value.abort();
      }
      
      // Create new abort controller
      abortController.value = new AbortController();
      
      try {
        const response = await fetch(`${API_BASE_URL}/chat/stream`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authStore.token}`,
          },
          body: JSON.stringify({ content }),
          signal: abortController.value.signal,
        });
        
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        try {
          while (true) {
            const { done, value } = await reader.read();
            
            if (done) {
              // Check if there's remaining data in buffer
              if (buffer) {
                processBuffer(buffer);
                buffer = '';
              }
              break;
            }
            
            // Decode and add to buffer
            buffer += decoder.decode(value, { stream: true });
            
            // Process complete SSE messages
            const lines = buffer.split('\n\n');
            buffer = lines.pop(); // Keep incomplete message in buffer
            
            for (const line of lines) {
              if (line.startsWith('data: ')) {
                const dataStr = line.substring(6);
                
                if (dataStr === '[DONE]') {
                  assistantMessage.isStreaming = false;
                  break;
                }
                
                try {
                  const data = JSON.parse(dataStr);
                  
                  if (data.delta) {
                    // Append the delta token to the message content
                    assistantMessage.content += data.delta;
                    
                    // Force Vue to update the UI immediately
                    messages.value = [...messages.value];
                    
                    // Scroll to bottom more frequently during streaming
                    scrollToBottom();
                  }
                  
                  if (data.error) {
                    throw new Error(data.error);
                  }
                } catch (parseError) {
                  console.error('Error parsing SSE data:', parseError);
                }
              }
            }
          }
        } finally {
          reader.releaseLock();
        }
        
        // Final scroll after streaming completes
        scrollToBottom();
        
      } catch (error) {
        console.error('Streaming error:', error);
        
        if (error.name === 'AbortError') {
          console.log('Stream cancelled by user');
          assistantMessage.content += '\n\n[Response interrupted]';
        } else {
          assistantMessage.content = `Sorry, I encountered an error: ${error.message}`;
        }
        
        assistantMessage.isStreaming = false;
      } finally {
        loading.value = false;
        streaming.value = false;
        abortController.value = null;
      }
    };
    
    const processBuffer = (buffer) => {
      const lines = buffer.split('\n');
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const dataStr = line.substring(6);
          if (dataStr && dataStr !== '[DONE]') {
            try {
              const data = JSON.parse(dataStr);
              if (data.delta) {
                // Update the last message if it's streaming
                const lastMessage = messages.value[messages.value.length - 1];
                if (lastMessage && lastMessage.isStreaming) {
                  lastMessage.content += data.delta;
                }
              }
            } catch (e) {
              console.error('Error processing buffer data:', e);
            }
          }
        }
      }
    };
    
    const cancelStream = () => {
      if (abortController.value) {
        abortController.value.abort();
        streaming.value = false;
        loading.value = false;
      }
    };
    
    const sendQuickQuestion = (question) => {
      userInput.value = question;
      nextTick(() => {
        sendMessage();
      });
    };
    
    const copyToClipboard = async (text) => {
      try {
        // Strip HTML tags for plain text copy
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = text;
        const plainText = tempDiv.textContent || tempDiv.innerText || text;
        
        await navigator.clipboard.writeText(plainText);
        
        // Find message index
        const index = messages.value.findIndex(msg => msg.content === text);
        copiedMessageIndex.value = index;
        
        // Clear previous timeout
        if (copyTimeout.value) {
          clearTimeout(copyTimeout.value);
        }
        
        // Reset after 2 seconds
        copyTimeout.value = setTimeout(() => {
          copiedMessageIndex.value = null;
        }, 2000);
        
      } catch (err) {
        console.error('Failed to copy:', err);
        fallbackCopy(text);
      }
    };
    
    const fallbackCopy = (text) => {
      const textArea = document.createElement('textarea');
      textArea.value = text;
      document.body.appendChild(textArea);
      textArea.select();
      
      try {
        document.execCommand('copy');
        const index = messages.value.findIndex(msg => msg.content === text);
        copiedMessageIndex.value = index;
        
        if (copyTimeout.value) {
          clearTimeout(copyTimeout.value);
        }
        
        copyTimeout.value = setTimeout(() => {
          copiedMessageIndex.value = null;
        }, 2000);
      } catch (err) {
        console.error('Fallback copy failed:', err);
      }
      
      document.body.removeChild(textArea);
    };
    
    const regenerateResponse = async (index) => {
      if (index > 0 && messages.value[index].role === 'assistant') {
        const userMessageIndex = index - 1;
        const userMessage = messages.value[userMessageIndex];
        
        // Remove the old assistant response
        messages.value.splice(index, 1);
        
        // Resend the user message
        await streamResponse(userMessage.content);
      }
    };
    
    const renderMarkdown = (content) => {
      if (!content) return '';
      try {
        const rawHtml = marked.parse(content);
        return DOMPurify.sanitize(rawHtml);
      } catch (error) {
        console.error('Markdown rendering error:', error);
        return content;
      }
    };
    
    const adjustTextareaHeight = () => {
      nextTick(() => {
        if (messageInput.value) {
          messageInput.value.style.height = 'auto';
          const newHeight = Math.min(messageInput.value.scrollHeight, 120);
          messageInput.value.style.height = newHeight + 'px';
        }
      });
    };
    
    const scrollToBottom = () => {
      nextTick(() => {
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
        }
      });
    };
    
    const formatMessageTime = (timestamp) => {
      const date = new Date(timestamp);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };
    
    const toggleDarkMode = () => {
      darkMode.value = !darkMode.value;
      localStorage.setItem('darkMode', darkMode.value);
    };
    
    const logout = () => {
      if (abortController.value) {
        abortController.value.abort();
      }
      authStore.logout();
      router.push('/login');
    };
    
    // Lifecycle
    onMounted(() => {
      // Initialize marked
      marked.setOptions({
        breaks: true,
        gfm: true,
        headerIds: false,
        mangle: false,
      });
      
      // Load dark mode preference
      const savedDarkMode = localStorage.getItem('darkMode');
      darkMode.value = savedDarkMode === 'true';
      
      // Online/offline detection
      window.addEventListener('online', () => isOnline.value = true);
      window.addEventListener('offline', () => isOnline.value = false);
      
      // Focus input on mount
      setTimeout(() => {
        if (messageInput.value) {
          messageInput.value.focus();
        }
      }, 100);
      
      // Adjust textarea height
      adjustTextareaHeight();
      
      // Load initial messages if needed
      // loadMessages();
    });
    
    onUnmounted(() => {
      if (abortController.value) {
        abortController.value.abort();
      }
      
      if (copyTimeout.value) {
        clearTimeout(copyTimeout.value);
      }
      
      window.removeEventListener('online', () => isOnline.value = true);
      window.removeEventListener('offline', () => isOnline.value = false);
    });
    
    return {
      // Refs
      messagesContainer,
      messageInput,
      
      // State
      messages,
      userInput,
      loading,
      streaming,
      darkMode,
      isOnline,
      copiedMessageIndex,
      authStore,
      
      // Computed
      getUserInitials,
      canSend,
      inputPlaceholder,
      
      // Methods
      sendMessage,
      sendQuickQuestion,
      copyToClipboard,
      regenerateResponse,
      renderMarkdown,
      formatMessageTime,
      toggleDarkMode,
      cancelStream,
      logout,
      adjustTextareaHeight,
    };
  },
};
</script>

<style scoped>
/* Base Styles */
.chat-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  overflow: hidden;
  transition: background 0.3s ease;
}

.chat-wrapper.dark-mode {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}

/* Animated Background */
.chat-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  z-index: 1;
}

.bg-shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.1;
  filter: blur(40px);
  animation: float 20s infinite linear;
}

.shape-1 {
  width: 300px;
  height: 300px;
  background: #10b981;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
  animation-duration: 25s;
}

.shape-2 {
  width: 200px;
  height: 200px;
  background: #059669;
  bottom: 20%;
  right: 15%;
  animation-delay: 5s;
  animation-duration: 20s;
}

.shape-3 {
  width: 150px;
  height: 150px;
  background: #34d399;
  top: 50%;
  left: 20%;
  animation-delay: 10s;
  animation-duration: 15s;
}

.shape-4 {
  width: 100px;
  height: 100px;
  background: #a7f3d0;
  bottom: 10%;
  left: 50%;
  animation-delay: 15s;
  animation-duration: 30s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg);
  }
  25% {
    transform: translate(50px, -50px) rotate(90deg);
  }
  50% {
    transform: translate(-30px, 30px) rotate(180deg);
  }
  75% {
    transform: translate(-50px, -30px) rotate(270deg);
  }
}

/* Main Container */
.chat-container {
  display: flex;
  width: 95%;
  max-width: 1400px;
  height: 90vh;
  background: white;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 2;
  animation: containerAppear 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.chat-wrapper.dark-mode .chat-container {
  background: #1e293b;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

@keyframes containerAppear {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Sidebar */
.chat-sidebar {
  width: 280px;
  background: linear-gradient(135deg, #0f766e 0%, #059669 100%);
  padding: 2rem;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.chat-wrapper.dark-mode .chat-sidebar {
  background: linear-gradient(135deg, #0f766e 0%, #115e59 100%);
}

.sidebar-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* Logo Section */
.logo-section {
  margin-bottom: 2.5rem;
  animation: slideInLeft 0.6s ease-out 0.2s both;
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.logo-animation {
  position: relative;
  width: 80px;
  height: 80px;
  margin-bottom: 1rem;
}

.logo-orb {
  position: absolute;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.3);
  animation: orbPulse 3s ease-in-out infinite;
}

.orb-1 {
  width: 80px;
  height: 80px;
  animation-delay: 0s;
}

.orb-2 {
  width: 60px;
  height: 60px;
  top: 10px;
  left: 10px;
  animation-delay: 0.5s;
}

.orb-3 {
  width: 40px;
  height: 40px;
  top: 20px;
  left: 20px;
  animation-delay: 1s;
}

@keyframes orbPulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.5;
  }
}

.logo-core {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40px;
  height: 40px;
  background: white;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.logo-icon {
  width: 24px;
  height: 24px;
  color: #059669;
}

.brand-name {
  font-size: 1.75rem;
  font-weight: 800;
  color: white;
  margin: 0 0 0.5rem 0;
  letter-spacing: -0.5px;
}

.ai-text {
  color: #a7f3d0;
  font-weight: 900;
}

.brand-tagline {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.875rem;
  margin: 0;
  font-weight: 400;
}

/* User Section */
.user-section {
  margin-bottom: 2rem;
  animation: slideInLeft 0.6s ease-out 0.4s both;
}

.user-avatar {
  position: relative;
  width: 60px;
  height: 60px;
  margin-bottom: 1rem;
}

.avatar-initials {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.25rem;
  position: relative;
  z-index: 1;
}

.avatar-glow {
  position: absolute;
  top: -4px;
  left: -4px;
  right: -4px;
  bottom: -4px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  border-radius: 50%;
  filter: blur(8px);
  opacity: 0.4;
  animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
  from {
    opacity: 0.4;
    transform: scale(1);
  }
  to {
    opacity: 0.6;
    transform: scale(1.05);
  }
}

.user-info h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: white;
  margin: 0 0 0.25rem 0;
}

.user-info p {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
}

/* Features Section */
.features-section {
  margin-bottom: 2rem;
  animation: slideInLeft 0.6s ease-out 0.6s both;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
  color: white;
}

.feature-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.feature-icon svg {
  width: 100%;
  height: 100%;
  color: rgba(255, 255, 255, 0.9);
}

.feature-item span {
  font-size: 0.875rem;
  opacity: 0.9;
}

/* Sidebar Actions */
.sidebar-actions {
  margin-top: auto;
  animation: slideInLeft 0.6s ease-out 0.8s both;
}

.sidebar-btn {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 0.75rem;
  transition: all 0.2s ease;
  margin-bottom: 0.75rem;
}

.sidebar-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

.sidebar-btn svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.logout-btn {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.3);
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.2);
}

/* Main Chat Area */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #f8fafc;
  overflow: hidden;
}

.chat-wrapper.dark-mode .chat-main {
  background: #0f172a;
}

/* Chat Header */
.chat-header {
  padding: 1rem 1.5rem;
  background: white;
  border-bottom: 1px solid #e2e8f0;
  flex-shrink: 0;
}

.chat-wrapper.dark-mode .chat-header {
  background: #1e293b;
  border-bottom-color: #334155;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-header h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
}

.chat-wrapper.dark-mode .chat-header h2 {
  color: #f1f5f9;
}

.header-status {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #64748b;
}

.chat-wrapper.dark-mode .status-indicator {
  color: #94a3b8;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #94a3b8;
}

.status-indicator.online .status-dot {
  background: #10b981;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.1);
  }
}

.message-count {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.chat-wrapper.dark-mode .message-count {
  color: #94a3b8;
}

/* Messages Container */
.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  scroll-behavior: smooth;
}

/* Welcome Screen */
.welcome-screen {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.welcome-content {
  text-align: center;
  max-width: 600px;
  padding: 2rem;
}

.welcome-animation {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto 2rem;
}

.welcome-orb {
  position: absolute;
  border-radius: 50%;
  border: 2px solid #10b981;
  animation: welcomeFloat 4s ease-in-out infinite;
}

.welcome-orb-1 {
  width: 120px;
  height: 120px;
  animation-delay: 0s;
  opacity: 0.2;
}

.welcome-orb-2 {
  width: 90px;
  height: 90px;
  top: 15px;
  left: 15px;
  animation-delay: 0.5s;
  opacity: 0.3;
}

@keyframes welcomeFloat {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

.welcome-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #10b981, #059669);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.welcome-icon svg {
  width: 30px;
  height: 30px;
  color: white;
}

.welcome-content h3 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 1rem;
}

.chat-wrapper.dark-mode .welcome-content h3 {
  color: #f1f5f9;
}

.welcome-text {
  font-size: 1.125rem;
  color: #64748b;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.chat-wrapper.dark-mode .welcome-text {
  color: #94a3b8;
}

.quick-starters {
  margin-top: 2rem;
}

.quick-title {
  font-size: 1rem;
  font-weight: 500;
  color: #64748b;
  margin-bottom: 1rem;
}

.chat-wrapper.dark-mode .quick-title {
  color: #94a3b8;
}

.starter-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-width: 400px;
  margin: 0 auto;
}

.starter-btn {
  padding: 0.875rem 1.25rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  color: #475569;
  font-size: 0.9375rem;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.chat-wrapper.dark-mode .starter-btn {
  background: #1e293b;
  border-color: #334155;
  color: #cbd5e1;
}

.starter-btn:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.chat-wrapper.dark-mode .starter-btn:hover {
  background: #334155;
  border-color: #475569;
}

/* Messages List */
.messages-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
}

.message {
  display: flex;
  gap: 1rem;
  animation: messageAppear 0.3s ease-out;
}

@keyframes messageAppear {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-avatar {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
}

.ai-avatar {
  background: linear-gradient(135deg, #10b981, #059669);
}

.avatar-initials-small {
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
}

.ai-avatar-icon svg {
  width: 20px;
  height: 20px;
  color: white;
}

.message-content {
  flex: 1;
  max-width: 85%;
}

.message-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.message.user .message-header {
  flex-direction: row-reverse;
}

.sender-name {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.875rem;
}

.chat-wrapper.dark-mode .sender-name {
  color: #f1f5f9;
}

.message-time {
  font-size: 0.75rem;
  color: #94a3b8;
}

.message-text {
  position: relative;
}

.user-message {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  padding: 1rem 1.25rem;
  border-radius: 18px 18px 4px 18px;
  line-height: 1.6;
  word-break: break-word;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
}

.streaming-message {
  background: white;
  padding: 1rem 1.25rem;
  border-radius: 18px 18px 18px 4px;
  line-height: 1.6;
  word-break: break-word;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
}

.chat-wrapper.dark-mode .streaming-message {
  background: #1e293b;
  border-color: #334155;
}

.streaming-cursor {
  display: inline-block;
  width: 8px;
  height: 1.2em;
  background: #10b981;
  margin-left: 2px;
  vertical-align: middle;
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.ai-message {
  background: white;
  padding: 1rem 1.25rem;
  border-radius: 18px 18px 18px 4px;
  line-height: 1.6;
  word-break: break-word;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.chat-wrapper.dark-mode .ai-message {
  background: #1e293b;
  border-color: #334155;
}

.message-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.chat-wrapper.dark-mode .message-actions {
  border-top-color: #334155;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #64748b;
}

.chat-wrapper.dark-mode .action-btn {
  background: #334155;
  border-color: #475569;
  color: #cbd5e1;
}

.action-btn:hover {
  background: #e2e8f0;
  transform: translateY(-1px);
}

.chat-wrapper.dark-mode .action-btn:hover {
  background: #475569;
}

.action-btn svg {
  width: 14px;
  height: 14px;
}

.copy-btn.copied {
  background: #10b981;
  border-color: #10b981;
  color: white;
}

/* Loading Indicator */
.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
}

.typing-dots {
  display: flex;
  gap: 4px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #94a3b8;
  animation: typing 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }
.dot:nth-child(3) { animation-delay: 0s; }

@keyframes typing {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.loading-text {
  font-size: 0.9375rem;
  color: #64748b;
  font-weight: 500;
}

.chat-wrapper.dark-mode .loading-text {
  color: #94a3b8;
}

/* Input Area */
.input-area {
  padding: 1rem 1.5rem;
  background: white;
  border-top: 1px solid #e2e8f0;
  flex-shrink: 0;
}

.chat-wrapper.dark-mode .input-area {
  background: #1e293b;
  border-top-color: #334155;
}

.input-form {
  position: relative;
}

.input-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 0.75rem;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  padding: 0.75rem 1rem;
  transition: border-color 0.2s ease;
}

.chat-wrapper.dark-mode .input-wrapper {
  background: #1e293b;
  border-color: #334155;
}

.input-wrapper:focus-within {
  border-color: #10b981;
}

.message-input {
  flex: 1;
  border: none;
  outline: none;
  resize: none;
  font-family: inherit;
  font-size: 0.9375rem;
  line-height: 1.5;
  color: #1e293b;
  background: transparent;
  max-height: 120px;
  min-height: 24px;
  padding: 0.25rem 0;
}

.chat-wrapper.dark-mode .message-input {
  color: #f1f5f9;
}

.message-input::placeholder {
  color: #94a3b8;
}

.message-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.input-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cancel-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.chat-wrapper.dark-mode .cancel-btn {
  background: #7f1d1d;
  border-color: #991b1b;
  color: #fecaca;
}

.cancel-btn:hover {
  background: #fee2e2;
}

.chat-wrapper.dark-mode .cancel-btn:hover {
  background: #991b1b;
}

.cancel-btn svg {
  width: 14px;
  height: 14px;
}

.send-btn {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.send-btn.sending {
  animation: pulseSend 2s infinite;
}

@keyframes pulseSend {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.send-btn svg {
  width: 20px;
  height: 20px;
}

.input-hints {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  padding: 0 0.25rem;
}

.hint-text {
  font-size: 0.75rem;
  color: #94a3b8;
}

.char-count {
  font-size: 0.75rem;
  color: #94a3b8;
}

.char-count.warning {
  color: #dc2626;
  font-weight: 500;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .chat-container {
    width: 98%;
    height: 95vh;
  }
  
  .chat-sidebar {
    width: 240px;
    padding: 1.5rem;
  }
}

@media (max-width: 768px) {
  .chat-container {
    flex-direction: column;
    height: 100vh;
    border-radius: 0;
    width: 100%;
  }
  
  .chat-sidebar {
    width: 100%;
    height: auto;
    padding: 1rem;
  }
  
  .sidebar-content {
    flex-direction: row;
    align-items: center;
    gap: 1.5rem;
  }
  
  .logo-section {
    margin-bottom: 0;
    flex: 1;
  }
  
  .logo-animation {
    width: 40px;
    height: 40px;
    margin-bottom: 0.5rem;
  }
  
  .logo-orb.orb-1 {
    width: 40px;
    height: 40px;
  }
  
  .logo-orb.orb-2 {
    width: 30px;
    height: 30px;
    top: 5px;
    left: 5px;
  }
  
  .logo-orb.orb-3 {
    width: 20px;
    height: 20px;
    top: 10px;
    left: 10px;
  }
  
  .logo-core {
    width: 24px;
    height: 24px;
  }
  
  .logo-icon {
    width: 14px;
    height: 14px;
  }
  
  .brand-name {
    font-size: 1.25rem;
  }
  
  .brand-tagline {
    display: none;
  }
  
  .user-section {
    margin-bottom: 0;
    display: none;
  }
  
  .features-section {
    display: none;
  }
  
  .sidebar-actions {
    margin-top: 0;
    display: flex;
    gap: 0.5rem;
  }
  
  .sidebar-btn {
    width: auto;
    padding: 0.5rem;
  }
  
  .sidebar-btn span {
    display: none;
  }
  
  .messages-container {
    padding: 1rem;
  }
  
  .welcome-content h3 {
    font-size: 1.5rem;
  }
  
  .welcome-text {
    font-size: 1rem;
  }
  
  .starter-buttons {
    max-width: 100%;
  }
  
  .input-area {
    padding: 0.75rem;
  }
  
  .cancel-btn span {
    display: none;
  }
  
  .cancel-btn {
    padding: 0.5rem;
  }
  
  .hint-text {
    font-size: 0.7rem;
  }
}
</style>

<style>
/* Global Markdown Styles */
.message-content-inner {
  line-height: 1.7;
  color: #374151;
}

.chat-wrapper.dark-mode .message-content-inner {
  color: #cbd5e1;
}

.message-content-inner h1,
.message-content-inner h2,
.message-content-inner h3,
.message-content-inner h4,
.message-content-inner h5,
.message-content-inner h6 {
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  font-weight: 600;
  line-height: 1.25;
  color: #111827;
}

.chat-wrapper.dark-mode .message-content-inner h1,
.chat-wrapper.dark-mode .message-content-inner h2,
.chat-wrapper.dark-mode .message-content-inner h3,
.chat-wrapper.dark-mode .message-content-inner h4,
.chat-wrapper.dark-mode .message-content-inner h5,
.chat-wrapper.dark-mode .message-content-inner h6 {
  color: #f1f5f9;
}

.message-content-inner h1 { font-size: 1.5em; }
.message-content-inner h2 { font-size: 1.3em; }
.message-content-inner h3 { font-size: 1.125em; }
.message-content-inner h4 { font-size: 1em; }
.message-content-inner h5 { font-size: 0.875em; }
.message-content-inner h6 { font-size: 0.85em; }

.message-content-inner p {
  margin: 1em 0;
}

.message-content-inner ul,
.message-content-inner ol {
  margin: 1em 0;
  padding-left: 1.5em;
}

.message-content-inner li {
  margin: 0.5em 0;
}

.message-content-inner blockquote {
  margin: 1em 0;
  padding: 0.5em 1em;
  border-left: 4px solid #10b981;
  background: #f0fdf4;
  border-radius: 0 6px 6px 0;
}

.chat-wrapper.dark-mode .message-content-inner blockquote {
  background: #064e3b;
}

.message-content-inner code {
  background: #f1f5f9;
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-size: 0.9em;
  font-family: 'SFMono-Regular', 'Consolas', 'Liberation Mono', 'Menlo', monospace;
}

.chat-wrapper.dark-mode .message-content-inner code {
  background: #334155;
}

.message-content-inner pre {
  background: #1e293b;
  border-radius: 8px;
  padding: 1em;
  overflow-x: auto;
  margin: 1em 0;
}

.message-content-inner pre code {
  background: none;
  padding: 0;
  color: #e2e8f0;
}

.message-content-inner table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
}

.message-content-inner th,
.message-content-inner td {
  border: 1px solid #e2e8f0;
  padding: 0.75em;
  text-align: left;
}

.chat-wrapper.dark-mode .message-content-inner th,
.chat-wrapper.dark-mode .message-content-inner td {
  border-color: #475569;
}

.message-content-inner th {
  background: #f8fafc;
  font-weight: 600;
}

.chat-wrapper.dark-mode .message-content-inner th {
  background: #334155;
}

.message-content-inner a {
  color: #2563eb;
  text-decoration: none;
}

.message-content-inner a:hover {
  text-decoration: underline;
}

.chat-wrapper.dark-mode .message-content-inner a {
  color: #60a5fa;
}

.message-content-inner img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 1em 0;
}

.message-content-inner hr {
  margin: 2em 0;
  border: none;
  border-top: 2px solid #e2e8f0;
}

.chat-wrapper.dark-mode .message-content-inner hr {
  border-color: #475569;
}
</style>