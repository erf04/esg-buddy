<template>
  <div class="chat-wrapper">
    <header class="chat-header">
      <h1>💬 Cariboun AI</h1>
      <button @click="logout" class="logout-btn">Logout</button>
    </header>

    <main class="chat-body" ref="chatWindow">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['message', msg.role]"
      >
        <div class="bubble">
          <!-- Message header with copy button -->
          <div class="message-header">
            <span class="message-role">{{ msg.role === 'user' ? 'You' : 'Assistant' }}</span>
            <button 
              @click="copyMessage(msg.content)"
              :class="['copy-btn', { 'copied': copiedIndex === index }]"
              :title="copiedIndex === index ? 'Copied!' : 'Copy message'"
            >
              <svg v-if="copiedIndex === index" class="copy-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 6L9 17l-5-5"></path>
              </svg>
              <svg v-else class="copy-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
              </svg>
              <span class="copy-text">{{ copiedIndex === index ? 'Copied!' : 'Copy' }}</span>
            </button>
          </div>
          
          <!-- Render user messages as plain text -->
          <div v-if="msg.role === 'user'" class="message-text">
            {{ msg.content }}
          </div>
          
          <!-- Render assistant messages as Markdown -->
          <div 
            v-else 
            class="message-content markdown-body" 
            v-html="renderMarkdown(msg.content)"
          ></div>
        </div>
      </div>

      <div v-if="loading" class="loading">
        <span class="dot"></span><span class="dot"></span><span class="dot"></span>
      </div>
    </main>

    <footer class="chat-footer">
      <input
        v-model="userInput"
        @keyup.enter="handleSend"
        type="text"
        placeholder="Type your message..."
      />
      <button @click="handleSend" :disabled="loading">Send</button>
    </footer>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import apiClient from '@/plugins/axios';
import { marked } from 'marked';
import DOMPurify from 'dompurify';

export default {
  name: "Chat",
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  },
  data() {
    return {
      messages: [],
      userInput: "",
      loading: false,
      copiedIndex: null,
      copyTimeout: null
    };
  },
  mounted() {
    marked.setOptions({
      breaks: true,
      gfm: true,
      headerIds: false,
      mangle: false
    });
    
    this.loadMessages();
  },
  methods: {
    renderMarkdown(content) {
      if (!content) return '';
      const rawHtml = marked.parse(content);
      return DOMPurify.sanitize(rawHtml);
    },

    async copyMessage(content) {
      try {
        // Create a temporary element to strip HTML tags if it's markdown
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = content;
        const plainText = tempDiv.textContent || tempDiv.innerText || '';

        // Use the Clipboard API
        await navigator.clipboard.writeText(plainText);
        
        // Show success feedback
        const currentIndex = this.messages.findIndex(msg => msg.content === content);
        this.copiedIndex = currentIndex;
        
        // Clear previous timeout if exists
        if (this.copyTimeout) {
          clearTimeout(this.copyTimeout);
        }
        
        // Reset copied state after 2 seconds
        this.copyTimeout = setTimeout(() => {
          this.copiedIndex = null;
        }, 2000);
        
      } catch (err) {
        console.error('Failed to copy message:', err);
        // Fallback for older browsers
        this.fallbackCopyTextToClipboard(content);
      }
    },

    fallbackCopyTextToClipboard(text) {
      const textArea = document.createElement('textarea');
      textArea.value = text;
      
      // Avoid scrolling to bottom
      textArea.style.top = '0';
      textArea.style.left = '0';
      textArea.style.position = 'fixed';
      
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      
      try {
        const successful = document.execCommand('copy');
        if (successful) {
          const currentIndex = this.messages.findIndex(msg => msg.content === text);
          this.copiedIndex = currentIndex;
          
          if (this.copyTimeout) {
            clearTimeout(this.copyTimeout);
          }
          
          this.copyTimeout = setTimeout(() => {
            this.copiedIndex = null;
          }, 2000);
        }
      } catch (err) {
        console.error('Fallback copy failed:', err);
      }
      
      document.body.removeChild(textArea);
    },

    async loadMessages() {
      this.loading = true;
      
      this.messages = [
        {
          role: "assistant",
          content: "👋 **Hello!** I'm Cariboun AI — your AI assistant for sustainability and Cariboun AI insights. \n\nHow can I help today?",
        },
      ];

      try {
        const response = await apiClient.get('/chat/messages/',
          {
            headers:{
              Authorization:`Bearer ${this.authStore.token}`
            }
          }
        );
        
        for (const msg of response.data) {
          if (msg && msg.content) {
            this.messages.push(msg);
          }
        }
      } catch (error) {
        console.error("Error loading messages:", error);
        if (error.response?.status === 401) {
          this.authStore.logout();
          this.$router.push('/login');
        }
      } finally {
        this.loading = false;
        this.scrollToBottom();
      }
    },

    async handleSend() {
      if (!this.userInput.trim()) return;

      const content = this.userInput.trim();
      const userMessage = {
        role: "user",
        content: content,
      };

      this.messages.push(userMessage);
      this.userInput = "";
      this.loading = true;
      this.scrollToBottom();

      try {
        const response = await apiClient.post("/chat/send-message/", {
          content: content
        },
        {
          headers:{
              Authorization:`Bearer ${this.authStore.token}`
            }
        });
        
        const reply = {
          role: "assistant",
          content: response.data.content
        };
        this.messages.push(reply);
      } catch (error) {
        console.error("Error sending message:", error);
        if (error.response?.status === 401) {
          this.authStore.logout();
          this.$router.push('/login');
        }
      } finally {
        this.loading = false;
        this.scrollToBottom();
      }
    },

    logout() {
      this.authStore.logout();
      this.$router.push('/login');
    },

    scrollToBottom() {
      this.$nextTick(() => {
        const chatWindow = this.$refs.chatWindow;
        if (chatWindow) {
          chatWindow.scrollTop = chatWindow.scrollHeight;
        }
      });
    },
  },
  beforeUnmount() {
    // Clean up timeout when component is destroyed
    if (this.copyTimeout) {
      clearTimeout(this.copyTimeout);
    }
  }
};
</script>

<style scoped>
/* Layout */
.chat-wrapper {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
  background: #f9fafb;
  font-family: "Inter", sans-serif;
}

/* Header */
.chat-header {
  flex-shrink: 0;
  background: #1e293b;
  color: #fff;
  text-align: center;
  padding: 1rem;
  font-size: 1.3rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logout-btn {
  background: #ef4444;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.logout-btn:hover {
  background: #dc2626;
}

/* Chat body */
.chat-body {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background: #f1f5f9;
}

/* Messages */
.message {
  display: flex;
  width: 100%;
}

.message.user {
  justify-content: flex-end;
}

.message.assistant {
  justify-content: flex-start;
}

.bubble {
  max-width: 75%;
  padding: 1rem 1.25rem;
  border-radius: 16px;
  word-break: break-word;
  line-height: 1.6;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
}

/* User messages */
.message.user .bubble {
  background: #2563eb;
  color: #ffffff;
  border-bottom-right-radius: 4px;
}

/* Assistant messages */
.message.assistant .bubble {
  background: #ffffff;
  color: #111827;
  border-bottom-left-radius: 4px;
  border: 1px solid #e2e8f0;
}

/* Message header */
.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.message.user .message-header {
  border-bottom-color: rgba(255, 255, 255, 0.3);
}

.message-role {
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  opacity: 0.8;
}

.message.user .message-role {
  color: rgba(255, 255, 255, 0.9);
}

.message.assistant .message-role {
  color: #6b7280;
}

/* Copy button */
.copy-btn {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  background: transparent;
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  padding: 0.3rem 0.6rem;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  color: inherit;
}

.message.user .copy-btn {
  border-color: rgba(255, 255, 255, 0.4);
  color: rgba(255, 255, 255, 0.9);
}

.message.assistant .copy-btn {
  border-color: #d1d5db;
  color: #6b7280;
}

.copy-btn:hover {
  background: rgba(0, 0, 0, 0.05);
  transform: translateY(-1px);
}

.message.user .copy-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.copy-btn.copied {
  background: #10b981;
  border-color: #10b981;
  color: white;
}

.copy-icon {
  width: 14px;
  height: 14px;
}

.copy-text {
  font-weight: 500;
}

/* Message content */
.message-text {
  margin: 0;
  white-space: pre-wrap;
  line-height: 1.6;
}

.message-content {
  margin: 0;
}

/* Input area */
.chat-footer {
  display: flex;
  flex-shrink: 0;
  padding: 0.75rem;
  background: #ffffff;
  border-top: 1px solid #e2e8f0;
  align-items: center;
}

.chat-footer input {
  flex: 1;
  padding: 0.6rem 0.8rem;
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  outline: none;
  font-size: 1rem;
  transition: border 0.2s;
}

.chat-footer input:focus {
  border-color: #2563eb;
}

.chat-footer button {
  margin-left: 0.5rem;
  padding: 0.6rem 1.2rem;
  background: #2563eb;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.chat-footer button:hover {
  background: #1d4ed8;
}

.chat-footer button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Loading animation */
.loading {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 4px;
  color: #64748b;
  padding-left: 0.5rem;
}

.dot {
  width: 8px;
  height: 8px;
  background-color: #94a3b8;
  border-radius: 50%;
  animation: blink 1.4s infinite both;
}

.dot:nth-child(2) {
  animation-delay: 0.2s;
}
.dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes blink {
  0%, 80%, 100% {
    opacity: 0.3;
  }
  40% {
    opacity: 1;
  }
}

/* Responsive design */
@media (max-width: 768px) {
  .chat-header {
    font-size: 1.1rem;
    padding: 0.75rem;
  }

  .bubble {
    max-width: 85%;
    font-size: 0.95rem;
    padding: 0.8rem 1rem;
  }

  .message-header {
    margin-bottom: 0.5rem;
  }

  .copy-btn {
    padding: 0.2rem 0.4rem;
    font-size: 0.7rem;
  }

  .copy-text {
    display: none; /* Hide text on mobile, show only icon */
  }

  .chat-footer input {
    font-size: 0.9rem;
  }

  .chat-footer button {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }
}
</style>

<style>
/* Global Markdown Styles */
.markdown-body {
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.7;
  color: #374151;
  font-size: 0.95rem;
}

.markdown-body h1 {
  font-size: 1.5em;
  font-weight: 700;
  margin: 1.2em 0 0.8em 0;
  padding-bottom: 0.3em;
  border-bottom: 2px solid #e5e7eb;
  color: #111827;
}

.markdown-body h2 {
  font-size: 1.3em;
  font-weight: 600;
  margin: 1.5em 0 0.8em 0;
  color: #1f2937;
  padding-bottom: 0.2em;
  border-bottom: 1px solid #e5e7eb;
}

.markdown-body h3 {
  font-size: 1.15em;
  font-weight: 600;
  margin: 1.3em 0 0.6em 0;
  color: #374151;
}

.markdown-body h4 {
  font-size: 1.05em;
  font-weight: 600;
  margin: 1.2em 0 0.5em 0;
  color: #4b5563;
}

.markdown-body h5,
.markdown-body h6 {
  font-size: 1em;
  font-weight: 600;
  margin: 1em 0 0.5em 0;
  color: #6b7280;
}

.markdown-body p {
  margin: 0.8em 0;
  color: #4b5563;
}

.markdown-body ul,
.markdown-body ol {
  margin: 0.8em 0;
  padding-left: 1.8em;
}

.markdown-body li {
  margin: 0.4em 0;
  color: #4b5563;
}

.markdown-body li > p {
  margin: 0.4em 0;
}

.markdown-body blockquote {
  margin: 1.2em 0;
  padding: 0.8em 1.2em;
  border-left: 4px solid #3b82f6;
  background-color: #f8fafc;
  border-radius: 0 6px 6px 0;
  color: #64748b;
}

.markdown-body blockquote p {
  margin: 0;
  font-style: italic;
}

.markdown-body code {
  background-color: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  padding: 0.2em 0.4em;
  font-family: "SFMono-Regular", "Consolas", "Liberation Mono", "Menlo", monospace;
  font-size: 0.9em;
  color: #dc2626;
}

.markdown-body pre {
  background-color: #1f2937;
  border-radius: 8px;
  padding: 1.2em;
  overflow-x: auto;
  margin: 1.2em 0;
  border: 1px solid #374151;
}

.markdown-body pre code {
  background: none;
  border: none;
  padding: 0;
  color: #e5e7eb;
  font-size: 0.9em;
}

.markdown-body table {
  border-collapse: collapse;
  width: 100%;
  margin: 1.2em 0;
  font-size: 0.9em;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.markdown-body table th {
  background-color: #f8fafc;
  font-weight: 600;
  color: #374151;
}

.markdown-body table th,
.markdown-body table td {
  border: 1px solid #e5e7eb;
  padding: 0.75em 1em;
  text-align: left;
}

.markdown-body table tr:nth-child(even) {
  background-color: #f9fafb;
}

.markdown-body a {
  color: #2563eb;
  text-decoration: none;
  font-weight: 500;
}

.markdown-body a:hover {
  color: #1d4ed8;
  text-decoration: underline;
}

.markdown-body strong {
  font-weight: 600;
  color: #111827;
}

.markdown-body em {
  font-style: italic;
  color: #6b7280;
}

.markdown-body hr {
  margin: 2em 0;
  border: none;
  border-top: 2px solid #e5e7eb;
}

.markdown-body img {
  max-width: 100%;
  height: auto;
  border-radius: 6px;
  margin: 1em 0;
}

/* Ensure proper spacing in nested lists */
.markdown-body ul ul,
.markdown-body ol ol,
.markdown-body ul ol,
.markdown-body ol ul {
  margin: 0.2em 0;
}

/* Style for task lists */
.markdown-body input[type="checkbox"] {
  margin-right: 0.5em;
}

/* Better line breaks */
.markdown-body br {
  content: "";
  display: block;
  margin: 0.5em 0;
}
</style>  