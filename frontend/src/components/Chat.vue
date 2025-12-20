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
      <!-- Combined Sidebar with Logo, User Info, Chat History, and Actions -->
      <aside class="chat-sidebar" :class="{ 'collapsed': isHistoryCollapsed }">
        <div class="sidebar-content">
          <!-- Logo and Toggle Section -->
          <div class="sidebar-header">
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
              <p class="brand-tagline">Intelligent Conversations</p>
            </div>
            
            <button 
              class="sidebar-toggle-btn"
              @click="toggleHistoryCollapse"
              :title="isHistoryCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
            >
              <svg v-if="isHistoryCollapsed" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="15 18 9 12 15 6"></polyline>
              </svg>
            </button>
          </div>

          <!-- User Info (Visible when not collapsed) -->
          <div v-if="!isHistoryCollapsed" class="user-section">
            <div class="user-avatar">
              <div class="avatar-initials">{{ getUserInitials }}</div>
              <div class="avatar-glow"></div>
            </div>
            <div class="user-info">
              <h3>{{ authStore.getUser?.first_name || 'User' }}</h3>
              <p class="user-email">{{ authStore.getUser?.email || '' }}</p>
            </div>
          </div>

          <!-- Chat History Section -->
          <div class="chat-history-section" :class="{ 'collapsed': isHistoryCollapsed }">
            <div class="history-header" v-if="!isHistoryCollapsed">
              <h3>💬 Conversations</h3>
              <button 
                class="new-chat-btn"
                @click="createNewThread"
                title="Start new conversation"
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
                <span>New Chat</span>
              </button>
            </div>
            
            <!-- Collapsed History Button -->
            <div v-else class="collapsed-history-header">
              <button 
                class="collapsed-new-btn"
                @click="createNewThread"
                title="New conversation"
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
              </button>
            </div>

            <!-- History List (Visible when not collapsed) -->
            <div v-if="!isHistoryCollapsed" class="history-list">
              <div v-if="loadingThreads" class="history-loading">
                <div class="history-spinner"></div>
                <span>Loading conversations...</span>
              </div>
              
              <div v-else-if="threads.length === 0" class="history-empty">
                <div class="empty-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                  </svg>
                </div>
                <p>No conversations yet</p>
                <button class="empty-btn" @click="createNewThread">
                  Start new chat
                </button>
              </div>
              
              <div v-else class="threads-container">
                <div 
                  v-for="(thread, index) in threads" 
                  :key="thread.thread_id"
                  :class="['thread-item', { 'active': currentThreadId === thread.thread_id }]"
                  @click="loadThreadMessages(thread.thread_id)"
                >
                  <div class="thread-icon">
                    <svg v-if="thread.has_pdfs" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                      <polyline points="14 2 14 8 20 8"></polyline>
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                    </svg>
                  </div>
                  
                  <div class="thread-content">
                    <div class="thread-title">
                      {{ thread.thread_title || `Conversation ${index + 1}` }}
                    </div>
                    <div class="thread-info">
                      <span class="thread-message-count">{{ thread.message_count }} messages</span>
                      <span class="thread-time">{{ formatThreadTime(thread.created_at) }}</span>
                    </div>
                    <div v-if="thread.last_message" class="thread-preview">
                      {{ thread.last_message }}
                    </div>
                  </div>
                  
                  <button 
                    v-if="currentThreadId === thread.thread_id"
                    class="thread-delete-btn"
                    @click.stop="deleteThread(thread.thread_id)"
                    title="Delete conversation"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="3 6 5 6 21 6"></polyline>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- Collapsed Threads (Visible when collapsed) -->
            <div v-else class="collapsed-threads">
              <div class="collapsed-threads-list">
                <button
                  v-for="(thread, index) in threads.slice(0, 8)"
                  :key="thread.thread_id"
                  :class="['collapsed-thread-btn', { 'active': currentThreadId === thread.thread_id }]"
                  @click="loadThreadMessages(thread.thread_id)"
                  :title="thread.thread_title || `Conversation ${index + 1}`"
                >
                  <div v-if="thread.has_pdfs" class="collapsed-pdf-indicator">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                      <polyline points="14 2 14 8 20 8"></polyline>
                    </svg>
                  </div>
                  <span>{{ index + 1 }}</span>
                </button>
              </div>
              <div v-if="threads.length > 8" class="collapsed-more">
                +{{ threads.length - 8 }} more
              </div>
            </div>
          </div>

          <!-- Sidebar Actions -->
          <div class="sidebar-actions" :class="{ 'collapsed': isHistoryCollapsed }">
            <button 
              class="sidebar-btn" 
              @click="toggleDarkMode" 
              :title="darkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
            >
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
              <span v-if="!isHistoryCollapsed">{{ darkMode ? 'Light' : 'Dark' }}</span>
            </button>
            <button class="sidebar-btn logout-btn" @click="logout">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                <polyline points="16 17 21 12 16 7"></polyline>
                <line x1="21" y1="12" x2="9" y2="12"></line>
              </svg>
              <span v-if="!isHistoryCollapsed">Logout</span>
            </button>
          </div>
        </div>
      </aside>

      <!-- Main Chat Area -->
      <main class="chat-main">
        <!-- Chat Header -->
        <header class="chat-header">
          <div class="header-content">
            <div class="header-left">
              <button 
                class="menu-toggle-btn"
                @click="toggleHistoryCollapse"
                :title="isHistoryCollapsed ? 'Show chat history' : 'Hide chat history'"
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="3" y1="12" x2="21" y2="12"></line>
                  <line x1="3" y1="6" x2="21" y2="6"></line>
                  <line x1="3" y1="18" x2="21" y2="18"></line>
                </svg>
              </button>
              <h2>💬 Cariboun AI Assistant</h2>
            </div>
            
            <div class="header-actions">
              <button 
                class="esg-report-btn"
                @click="generateESGReport"
                :disabled="!hasConversation || loading || streaming"
                title="Generate ESG Report from Conversation"
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="13"></line>
                  <line x1="16" y1="17" x2="8" y2="17"></line>
                  <polyline points="10 9 9 9 8 9"></polyline>
                </svg>
                <span>Generate ESG Report</span>
              </button>
              
              <div class="header-status">
                <div class="status-indicator" :class="{ online: isOnline }">
                  <div class="status-dot"></div>
                  <span>{{ isOnline ? 'Connected' : 'Offline' }}</span>
                </div>
                <div class="message-count">{{ messages.length }} messages</div>
              </div>
            </div>
          </div>
        </header>

        <!-- Messages Container -->
        <div class="messages-container" ref="messagesContainer">
          <!-- Welcome Message -->
          <div v-if="messages.length === 0 && !loadingMessages" class="welcome-screen">
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
                  <button class="starter-btn" @click="sendQuickQuestion('Explain what is Cariboun AI and what do it do in simple terms')">
                    🤖 What is Cariboun AI ?
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

          <!-- Loading Messages -->
          <div v-if="loadingMessages" class="loading-messages">
            <div class="loading-spinner"></div>
            <p>Loading conversation...</p>
          </div>

          <!-- Messages List -->
          <div v-else-if="messages.length > 0" class="messages-list">
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

                  <!-- PDF Attachment (if this message has a PDF) -->
                  <div v-if="message.hasPdf" class="pdf-attachment">
                    <div class="attachment-header">
                      <div class="attachment-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                          <polyline points="7 10 12 15 17 10"></polyline>
                          <line x1="12" y1="15" x2="12" y2="3"></line>
                        </svg>
                      </div>
                      <div class="attachment-info">
                        <h4>📄 ESG Report Attached</h4>
                        <p>Based on our conversation about your company</p>
                      </div>
                    </div>
                    
                    <div class="attachment-details">
                      <div class="file-info">
                        <span class="file-name">{{ message.pdfFilename }}</span>
                        <span class="file-size">{{ formatFileSize(message.pdfSize) }}</span>
                      </div>
                      <button 
                        class="download-btn"
                        @click="downloadPDF(message.id, message.pdfFilename)"
                      >
                        Download PDF
                      </button>
                    </div>
                  </div>
                    <!-- Message Actions -->
                    <div class="message-actions">
                      <button
                        class="action-btn copy-btn"
                        @click="copyToClipboard(message.content)"
                        :title="copiedMessageIndex === index ? 'Copied!' : 'Copy message'"
                        :class="{ 'copied': copiedMessageIndex === index }"
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
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Loading Indicator for Streaming -->
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
                  <span class="cancel-text">Stop</span>
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
    const threads = ref([]);
    const currentThreadId = ref(null);
    const userInput = ref('');
    const loading = ref(false);
    const streaming = ref(false);
    const loadingMessages = ref(false);
    const loadingThreads = ref(false);
    const abortController = ref(null);
    const darkMode = ref(false);
    const isOnline = ref(navigator.onLine);
    const copiedMessageIndex = ref(null);
    const copyTimeout = ref(null);
    const isHistoryCollapsed = ref(false);
    
    // Computed
    const getUserInitials = computed(() => {
      const user = authStore.getUser;
      if (!user) return 'U';
      const first = user.first_name?.[0] || '';
      const last = user.last_name?.[0] || '';
      return (first + last).toUpperCase() || 'U';
    });
    
    const canSend = computed(() => {
      return userInput.value.trim().length > 0 && !loading.value && !streaming.value && currentThreadId.value;
    });
    
    const inputPlaceholder = computed(() => {
      if (!currentThreadId.value) return 'Select or create a conversation';
      if (loading.value) return 'Cariboun AI is thinking...';
      if (streaming.value) return 'Cariboun AI is responding...';
      return 'Type your message...';
    });
    
    const hasConversation = computed(() => {
      return messages.value.length >= 2;
    });
    
    const hasPdfsInCurrentThread = computed(() => {
      return messages.value.some(msg => msg.hasPdf);
    });
    
    const pdfsInCurrentThread = computed(() => {
      return messages.value.filter(msg => msg.hasPdf).length;
    });
    
    // Methods
    const fetchUserThreads = async () => {
      try {
        loadingThreads.value = true;
        const response = await fetch(`${API_BASE_URL}/threads`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
          },
        });
        
        if (!response.ok) {
          throw new Error(`Failed to load threads: ${response.status}`);
        }
        
        const data = await response.json();
        threads.value = data;
        
        // If there are threads but no current thread selected, select the first one
        if (threads.value.length > 0 && !currentThreadId.value) {
          await loadThreadMessages(threads.value[0].thread_id);
        }
        
      } catch (error) {
        console.error('Error loading threads:', error);
      } finally {
        loadingThreads.value = false;
      }
    };
    
    const loadThreadMessages = async (threadId) => {
      try {
        console.log("selected:" , threadId);
        
        loadingMessages.value = true;
        messages.value = [];
        currentThreadId.value = threadId;
        
        const response = await fetch(`${API_BASE_URL}/chat/${threadId}/messages`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
          },
        });
        
        if (!response.ok) {
          throw new Error(`Failed to load messages: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Transform backend messages to frontend format
        messages.value = data.messages.map(msg => ({
          id: msg.id,
          role: msg.role,
          content: msg.content,
          timestamp: msg.created_at,
          isStreaming: false,
          hasPdf: msg.has_pdf || false,
          pdfFilename: msg.pdf_filename,
          pdfSize: msg.pdf_size,
        }));
        
        // Update thread in the list with latest info
        const threadIndex = threads.value.findIndex(t => t.thread_id === threadId);
        if (threadIndex !== -1) {
          threads.value[threadIndex].message_count = data.message_count;
          threads.value[threadIndex].has_pdfs = data.has_pdfs;
        }
        
      } catch (error) {
        console.error('Error loading thread messages:', error);
        messages.value = [];
      } finally {
        loadingMessages.value = false;
        nextTick(() => scrollToBottom());
      }
    };
    
    const createNewThread = async () => {
      try {
        loading.value = true;
        const response = await fetch(`${API_BASE_URL}/threads/new`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
          },
        });
        
        if (!response.ok) {
          throw new Error('Failed to create new thread');
        }
        
        const data = await response.json();
        
        // Refresh threads list
        await fetchUserThreads();
        
        // Load the new thread
        await loadThreadMessages(data.thread_id);
        
        // Focus input
        nextTick(() => {
          if (messageInput.value) {
            messageInput.value.focus();
          }
        });
        
      } catch (error) {
        console.error('Error creating new thread:', error);
        alert('Failed to create new conversation: ' + error.message);
      } finally {
        loading.value = false;
      }
    };
    
    const deleteThread = async (threadId) => {
      if (!confirm('Are you sure you want to delete this conversation? This action cannot be undone.')) {
        return;
      }
      
      try {
        const response = await fetch(`${API_BASE_URL}/threads/${threadId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
          },
        });
        
        if (!response.ok) {
          throw new Error('Failed to delete thread');
        }
        
        // Remove from local list
        threads.value = threads.value.filter(t => t.thread_id !== threadId);
        
        // If we deleted the current thread, load another one or clear
        if (currentThreadId.value === threadId) {
          if (threads.value.length > 0) {
            await loadThreadMessages(threads.value[0].thread_id);
          } else {
            currentThreadId.value = null;
            messages.value = [];
            await createNewThread();
          }
        }
        
      } catch (error) {
        console.error('Error deleting thread:', error);
        alert('Failed to delete conversation: ' + error.message);
      }
    };
    
    const sendMessage = async () => {
      if (!canSend.value || !currentThreadId.value) return;
      
      const content = userInput.value.trim();
      userInput.value = '';
      adjustTextareaHeight();
      
      // Add user message to UI
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
      
      // Refresh thread list to update message count
      await fetchUserThreads();
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
        const response = await fetch(`${API_BASE_URL}/chat/stream?thread_id=${currentThreadId.value}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authStore.token}`,
          },
          body: JSON.stringify({ 
            content,
            thread_id: currentThreadId.value
          }),
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
              if (buffer) {
                processBuffer(buffer);
                buffer = '';
              }
              break;
            }
            
            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n\n');
            buffer = lines.pop();
            
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
                    assistantMessage.content += data.delta;
                    messages.value = [...messages.value];
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
        
        assistantMessage.isStreaming = false;
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
      if (!currentThreadId.value) {
        alert('Please create or select a conversation first');
        return;
      }
      userInput.value = question;
      nextTick(() => {
        sendMessage();
      });
    };
    
    const generateESGReport = async () => {
      if (!currentThreadId.value || !hasConversation.value) {
        alert("Please select a conversation and have a conversation with the assistant first to provide company information.");
        return;
      }
      
      try {
        loading.value = true;
        
        // Show generating indicator
        const generatingMsg = {
          id: Date.now(),
          role: 'assistant',
          content: '🔍 Analyzing our conversation and generating ESG report...',
          timestamp: new Date().toISOString(),
          isStreaming: false,
        };
        messages.value.push(generatingMsg);
        scrollToBottom();
        
        // Call backend to generate ESG report
        const response = await fetch(`${API_BASE_URL}/chat/generate-esg-report?thread_id=${currentThreadId.value}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
          },
        });
        
        if (!response.ok) {
          throw new Error(`Failed to generate report: ${response.status}`);
        }
        
        const result = await response.json();
        
        // Remove the "generating" message
        messages.value.pop();
        
        // Add user's "generate report" message
        const userMessage = {
          id: Date.now(),
          role: 'user',
          content: 'Generate ESG report based on our conversation',
          timestamp: new Date().toISOString(),
        };
        messages.value.push(userMessage);
        
        // Add assistant's response with PDF attachment
        const assistantMessage = {
          id: result.message_id,
          role: 'assistant',
          content: result.success 
            ? "I've analyzed our conversation and created a comprehensive ESG report for you. The report includes all the information we discussed about your company's environmental, social, and governance practices."
            : "Sorry, I couldn't generate the ESG report.",
          timestamp: result.created_at,
          hasPdf: result.has_pdf,
          pdfFilename: result.pdf_filename,
          pdfSize: result.pdf_size,
        };
        messages.value.push(assistantMessage);
        
        scrollToBottom();
        
        // Refresh threads to update PDF indicator
        await fetchUserThreads();
        
        // Show success message
        if (result.success) {
          setTimeout(() => {
            alert("✅ ESG report generated successfully! You can download it from the chat.");
          }, 500);
        }
        
      } catch (error) {
        console.error('Error generating ESG report:', error);
        
        // Remove generating message if it exists
        if (messages.value[messages.value.length - 1]?.content?.includes('generating')) {
          messages.value.pop();
        }
        
        // Add error message
        const errorMessage = {
          id: Date.now() + 1,
          role: 'assistant',
          content: `Sorry, I encountered an error while generating the ESG report: ${error.message}`,
          timestamp: new Date().toISOString(),
          hasPdf: false,
        };
        messages.value.push(errorMessage);
        scrollToBottom();
        
      } finally {
        loading.value = false;
      }
    };
    
    const downloadPDF = async (messageId, filename) => {
      try {
        const response = await fetch(`${API_BASE_URL}/chat/download-pdf/${messageId}/`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
          },
        });
        
        if (!response.ok) {
          throw new Error('Failed to download PDF');
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
      } catch (error) {
        console.error('Error downloading PDF:', error);
        alert('Failed to download PDF: ' + error.message);
      }
    };
    
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };
    
    const formatThreadTime = (timestamp) => {
      const date = new Date(timestamp);
      const now = new Date();
      const diffMs = now - date;
      const diffMins = Math.floor(diffMs / 60000);
      const diffHours = Math.floor(diffMs / 3600000);
      const diffDays = Math.floor(diffMs / 86400000);
      
      if (diffMins < 1) return 'Just now';
      if (diffMins < 60) return `${diffMins}m ago`;
      if (diffHours < 24) return `${diffHours}h ago`;
      if (diffDays < 7) return `${diffDays}d ago`;
      return date.toLocaleDateString();
    };
    
    const formatMessageTime = (timestamp) => {
      const date = new Date(timestamp);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };
    
    const toggleHistoryCollapse = () => {
      isHistoryCollapsed.value = !isHistoryCollapsed.value;
      localStorage.setItem('chatHistoryCollapsed', isHistoryCollapsed.value);
    };
    
    const copyToClipboard = async (text) => {
      try {
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = text;
        const plainText = tempDiv.textContent || tempDiv.innerText || text;
        
        await navigator.clipboard.writeText(plainText);
        
        const index = messages.value.findIndex(msg => msg.content === text);
        copiedMessageIndex.value = index;
        
        if (copyTimeout.value) {
          clearTimeout(copyTimeout.value);
        }
        
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
        
        messages.value.splice(index, 1);
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
          const newHeight = Math.min(messageInput.value.scrollHeight, 80);
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
      marked.setOptions({
        breaks: true,
        gfm: true,
        headerIds: false,
        mangle: false,
      });
      
      const savedDarkMode = localStorage.getItem('darkMode');
      darkMode.value = savedDarkMode === 'true';
      
      const savedCollapsed = localStorage.getItem('chatHistoryCollapsed');
      isHistoryCollapsed.value = savedCollapsed === 'true';
      
      window.addEventListener('online', () => isOnline.value = true);
      window.addEventListener('offline', () => isOnline.value = false);
      
      fetchUserThreads();
      
      setTimeout(() => {
        if (messageInput.value) {
          messageInput.value.focus();
        }
      }, 100);
      
      adjustTextareaHeight();
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
      messagesContainer,
      messageInput,
      messages,
      threads,
      currentThreadId,
      userInput,
      loading,
      streaming,
      loadingMessages,
      loadingThreads,
      darkMode,
      isOnline,
      copiedMessageIndex,
      isHistoryCollapsed,
      authStore,
      getUserInitials,
      canSend,
      inputPlaceholder,
      hasConversation,
      hasPdfsInCurrentThread,
      pdfsInCurrentThread,
      sendMessage,
      sendQuickQuestion,
      copyToClipboard,
      regenerateResponse,
      generateESGReport,
      formatFileSize,
      downloadPDF,
      formatThreadTime,
      formatMessageTime,
      loadThreadMessages,
      createNewThread,
      deleteThread,
      fetchUserThreads,
      toggleHistoryCollapse,
      renderMarkdown,
      toggleDarkMode,
      cancelStream,
      logout,
      adjustTextareaHeight,
    };
  },
};
</script>

<!-- ALL CSS IN ONE SCOPE BLOCK -->
<style scoped>
/* ALL your component CSS goes here - both scoped and global styles */
/* 1. Background and Container */
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
  background: #f5f7fa;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  overflow: hidden;
  transition: background 0.3s ease;
}

.chat-wrapper.dark-mode {
  background: #0a0f1a;
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
  opacity: 0.05;
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
  width: calc(100% - 20px);
  height: calc(100% - 20px);
  max-width: 1400px;
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 2;
  animation: containerAppear 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
  margin: 10px;
}

.chat-wrapper.dark-mode .chat-container {
  background: #111827;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

@keyframes containerAppear {
  from {
    opacity: 0;
    transform: scale(0.98);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Combined Sidebar with Chat History */
.chat-sidebar {
  width: 300px;
  background: linear-gradient(135deg, #0f766e 0%, #059669 100%);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.chat-sidebar.collapsed {
  width: 70px;
}

.chat-wrapper.dark-mode .chat-sidebar {
  background: linear-gradient(135deg, #0f766e 0%, #115e59 100%);
}

.sidebar-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 1.25rem;
  overflow: hidden;
}

/* Sidebar Header */
.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.logo-section {
  flex: 1;
}

.logo-animation {
  position: relative;
  width: 50px;
  height: 50px;
  margin-bottom: 0.75rem;
}

.logo-orb {
  position: absolute;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.2);
  animation: orbPulse 3s ease-in-out infinite;
}

.orb-1 {
  width: 50px;
  height: 50px;
  animation-delay: 0s;
}

.orb-2 {
  width: 38px;
  height: 38px;
  top: 6px;
  left: 6px;
  animation-delay: 0.5s;
}

.orb-3 {
  width: 26px;
  height: 26px;
  top: 12px;
  left: 12px;
  animation-delay: 1s;
}

@keyframes orbPulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.2;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.3;
  }
}

.logo-core {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 28px;
  height: 28px;
  background: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.logo-icon {
  width: 16px;
  height: 16px;
  color: #059669;
}

.brand-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  margin: 0 0 0.125rem 0;
  letter-spacing: -0.5px;
  line-height: 1.2;
}

.ai-text {
  color: #a7f3d0;
  font-weight: 800;
}

.brand-tagline {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.75rem;
  margin: 0;
  font-weight: 400;
}

.chat-sidebar.collapsed .brand-name,
.chat-sidebar.collapsed .brand-tagline {
  display: none;
}

.sidebar-toggle-btn {
  width: 28px;
  height: 28px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
  margin-left: 0.5rem;
}

.sidebar-toggle-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: rotate(90deg);
}

.sidebar-toggle-btn svg {
  width: 14px;
  height: 14px;
}

/* User Section */
.user-section {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  animation: slideInLeft 0.4s ease-out;
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.chat-sidebar.collapsed .user-section {
  display: none;
}

.user-avatar {
  position: relative;
  width: 40px;
  height: 40px;
}

.avatar-initials {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
  position: relative;
  z-index: 1;
}

.avatar-glow {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  border-radius: 50%;
  filter: blur(4px);
  opacity: 0.3;
  animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
  from {
    opacity: 0.3;
    transform: scale(1);
  }
  to {
    opacity: 0.5;
    transform: scale(1.05);
  }
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-info h3 {
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
  margin: 0 0 0.125rem 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-email {
  font-size: 0.6875rem;
  color: rgba(255, 255, 255, 0.6);
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Chat History Section */
.chat-history-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
}

.history-header {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.history-header h3 {
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
  margin: 0;
}

.new-chat-btn {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.625rem;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.new-chat-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

.new-chat-btn svg {
  width: 12px;
  height: 12px;
}

.collapsed-history-header {
  padding: 0.75rem;
  display: flex;
  justify-content: center;
}

.collapsed-new-btn {
  width: 36px;
  height: 36px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.collapsed-new-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.collapsed-new-btn svg {
  width: 16px;
  height: 16px;
}

/* History List */
.history-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

.history-loading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.75rem;
}

.history-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.history-empty {
  padding: 1.5rem 0.5rem;
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
}

.empty-icon {
  width: 40px;
  height: 40px;
  margin: 0 auto 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-icon svg {
  width: 20px;
  height: 20px;
  color: rgba(255, 255, 255, 0.5);
}

.history-empty p {
  font-size: 0.75rem;
  margin: 0 0 0.75rem;
}

.empty-btn {
  padding: 0.375rem 0.75rem;
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.empty-btn:hover {
  background: rgba(255, 255, 255, 0.25);
}

/* Thread Items */
.threads-container {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.thread-item {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  padding: 0.625rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  animation: threadAppear 0.3s ease-out;
}

@keyframes threadAppear {
  from {
    opacity: 0;
    transform: translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.thread-item:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(2px);
  border-color: rgba(255, 255, 255, 0.2);
}

.thread-item.active {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.thread-icon {
  width: 28px;
  height: 28px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 2px;
}

.thread-icon svg {
  width: 14px;
  height: 14px;
  color: rgba(255, 255, 255, 0.7);
}

.thread-item.active .thread-icon {
  background: rgba(255, 255, 255, 0.2);
}

.thread-content {
  flex: 1;
  min-width: 0;
}

.thread-title {
  font-weight: 500;
  color: white;
  font-size: 0.75rem;
  margin-bottom: 0.125rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.thread-info {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  margin-bottom: 0.25rem;
  font-size: 0.625rem;
  color: rgba(255, 255, 255, 0.5);
}

.thread-message-count {
  color: #a7f3d0;
  font-weight: 500;
}

.thread-preview {
  font-size: 0.625rem;
  color: rgba(255, 255, 255, 0.6);
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.thread-delete-btn {
  position: absolute;
  top: 0.25rem;
  right: 0.25rem;
  width: 20px;
  height: 20px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0;
  transition: all 0.2s ease;
}

.thread-item:hover .thread-delete-btn {
  opacity: 1;
}

.thread-delete-btn:hover {
  background: rgba(239, 68, 68, 0.2);
}

.thread-delete-btn svg {
  width: 10px;
  height: 10px;
  color: #fca5a5;
}

/* Collapsed Threads */
.collapsed-threads {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.5rem;
}

.collapsed-threads-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.375rem;
  width: 100%;
}

.collapsed-thread-btn {
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.75rem;
  font-weight: 500;
}

.collapsed-thread-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-1px);
  border-color: rgba(255, 255, 255, 0.2);
}

.collapsed-thread-btn.active {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
  color: white;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.collapsed-pdf-indicator {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 10px;
  height: 10px;
  background: #10b981;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.collapsed-pdf-indicator svg {
  width: 6px;
  height: 6px;
  color: white;
}

.collapsed-more {
  margin-top: 0.5rem;
  font-size: 0.625rem;
  color: rgba(255, 255, 255, 0.5);
  text-align: center;
}

/* Sidebar Actions */
.sidebar-actions {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-actions.collapsed {
  flex-direction: row;
  justify-content: center;
  gap: 0.5rem;
}

.sidebar-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.sidebar-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-1px);
}

.sidebar-btn svg {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
}

.sidebar-actions.collapsed .sidebar-btn {
  padding: 0.5rem;
}

.sidebar-actions.collapsed .sidebar-btn span {
  display: none;
}

.logout-btn {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.2);
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.2);
}

/* Menu Toggle Button in Header */
.menu-toggle-btn {
  width: 32px;
  height: 32px;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.chat-wrapper.dark-mode .menu-toggle-btn {
  background: #374151;
  border-color: #4b5563;
  color: #d1d5db;
}

.menu-toggle-btn:hover {
  background: #e5e7eb;
}

.chat-wrapper.dark-mode .menu-toggle-btn:hover {
  background: #4b5563;
}

.menu-toggle-btn svg {
  width: 16px;
  height: 16px;
}

/* Header Left */
.header-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

/* Chat Main with subtle pattern */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  overflow: hidden;
  position: relative;
}

.chat-main::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    linear-gradient(to right, #f8fafc 1px, transparent 1px),
    linear-gradient(to bottom, #f8fafc 1px, transparent 1px);
  background-size: 20px 20px;
  opacity: 0.3;
  pointer-events: none;
}

.chat-wrapper.dark-mode .chat-main {
  background: #111827;
}

.chat-wrapper.dark-mode .chat-main::before {
  background-image: 
    linear-gradient(to right, #1e293b 1px, transparent 1px),
    linear-gradient(to bottom, #1e293b 1px, transparent 1px);
  opacity: 0.2;
}

/* Chat Header */
.chat-header {
  padding: 0.875rem 1.25rem;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  flex-shrink: 0;
  position: relative;
  z-index: 1;
}

.chat-wrapper.dark-mode .chat-header {
  background: #1f2937;
  border-bottom-color: #374151;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-header h2 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.chat-wrapper.dark-mode .chat-header h2 {
  color: #f3f4f6;
}

.header-status {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.8125rem;
  color: #6b7280;
}

.chat-wrapper.dark-mode .status-indicator {
  color: #9ca3af;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #9ca3af;
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
  font-size: 0.8125rem;
  color: #6b7280;
  font-weight: 500;
}

.chat-wrapper.dark-mode .message-count {
  color: #9ca3af;
}

/* Messages Container */
.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1.25rem;
  scroll-behavior: smooth;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
}

/* Custom Scrollbar */
.messages-container::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-track {
  background: transparent;
}

.messages-container::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
  transition: background 0.3s ease;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

.chat-wrapper.dark-mode .messages-container::-webkit-scrollbar-thumb {
  background: #4b5563;
}

.chat-wrapper.dark-mode .messages-container::-webkit-scrollbar-thumb:hover {
  background: #6b7280;
}

/* Welcome Screen */
.welcome-screen {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  position: relative;
  z-index: 1;
}

.welcome-content {
  text-align: center;
  max-width: 500px;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(229, 231, 235, 0.5);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.chat-wrapper.dark-mode .welcome-content {
  background: rgba(31, 41, 55, 0.8);
  border-color: rgba(55, 65, 81, 0.5);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.welcome-animation {
  position: relative;
  width: 100px;
  height: 100px;
  margin: 0 auto 1.5rem;
}

.welcome-orb {
  position: absolute;
  border-radius: 50%;
  border: 2px solid #10b981;
  animation: welcomeFloat 4s ease-in-out infinite;
}

.welcome-orb-1 {
  width: 100px;
  height: 100px;
  animation-delay: 0s;
  opacity: 0.15;
}

.welcome-orb-2 {
  width: 75px;
  height: 75px;
  top: 12.5px;
  left: 12.5px;
  animation-delay: 0.5s;
  opacity: 0.2;
}

@keyframes welcomeFloat {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-15px) rotate(180deg);
  }
}

.welcome-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #10b981, #059669);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.welcome-icon svg {
  width: 24px;
  height: 24px;
  color: white;
}

.welcome-content h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 0.75rem;
}

.chat-wrapper.dark-mode .welcome-content h3 {
  color: #f3f4f6;
}

.welcome-text {
  font-size: 1rem;
  color: #6b7280;
  margin-bottom: 1.5rem;
  line-height: 1.5;
}

.chat-wrapper.dark-mode .welcome-text {
  color: #9ca3af;
}

.quick-starters {
  margin-top: 1.5rem;
}

.quick-title {
  font-size: 0.9375rem;
  font-weight: 500;
  color: #6b7280;
  margin-bottom: 0.75rem;
}

.chat-wrapper.dark-mode .quick-title {
  color: #9ca3af;
}

.starter-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-width: 350px;
  margin: 0 auto;
}

.starter-btn {
  padding: 0.75rem 1rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  color: #4b5563;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.chat-wrapper.dark-mode .starter-btn {
  background: #1f2937;
  border-color: #374151;
  color: #d1d5db;
}

.starter-btn:hover {
  background: #f3f4f6;
  border-color: #d1d5db;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.chat-wrapper.dark-mode .starter-btn:hover {
  background: #374151;
  border-color: #4b5563;
}

/* Loading Messages */
.loading-messages {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 2rem;
  position: relative;
  z-index: 1;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e5e7eb;
  border-top-color: #10b981;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.chat-wrapper.dark-mode .loading-spinner {
  border-color: #374151;
  border-top-color: #10b981;
}

.loading-messages p {
  font-size: 0.9375rem;
  color: #6b7280;
}

.chat-wrapper.dark-mode .loading-messages p {
  color: #9ca3af;
}

/* Messages List */
.messages-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1rem;
}

.message {
  display: flex;
  gap: 0.875rem;
  animation: messageAppear 0.3s ease-out;
}

@keyframes messageAppear {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.user {
  flex-direction: row-reverse;
}

.message.user .message-content {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.message-avatar {
  flex-shrink: 0;
}

.avatar {
  width: 36px;
  height: 36px;
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
  font-size: 0.75rem;
}

.ai-avatar-icon svg {
  width: 18px;
  height: 18px;
  color: white;
}

.message-content {
  flex: 1;
  max-width: 85%;
  min-width: 0;
}

.message-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.375rem;
}

.message.user .message-header {
  flex-direction: row-reverse;
}

.sender-name {
  font-weight: 600;
  color: #374151;
  font-size: 0.8125rem;
}

.chat-wrapper.dark-mode .sender-name {
  color: #e5e7eb;
}

.message-time {
  font-size: 0.6875rem;
  color: #9ca3af;
}

.message-text {
  position: relative;
}

.user-message {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  padding: 0.75rem 1rem;
  border-radius: 16px 16px 4px 16px;
  line-height: 1.5;
  word-break: break-word;
  box-shadow: 0 1px 3px rgba(59, 130, 246, 0.2);
  font-size: 0.9375rem;
}

.streaming-message {
  background: #ffffff;
  padding: 0.75rem 1rem;
  border-radius: 16px 16px 16px 4px;
  line-height: 1.5;
  word-break: break-word;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  position: relative;
  font-size: 0.9375rem;
}

.chat-wrapper.dark-mode .streaming-message {
  background: #1f2937;
  border-color: #374151;
}

.streaming-cursor {
  display: inline-block;
  width: 6px;
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
  background: #ffffff;
  padding: 0.75rem 1rem;
  border-radius: 16px 16px 16px 4px;
  line-height: 1.5;
  word-break: break-word;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  font-size: 0.9375rem;
}

.chat-wrapper.dark-mode .ai-message {
  background: #1f2937;
  border-color: #374151;
}

.message-actions {
  display: flex;
  gap: 0.375rem;
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid #e5e7eb;
}

.chat-wrapper.dark-mode .message-actions {
  border-top-color: #374151;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.625rem;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #6b7280;
}

.chat-wrapper.dark-mode .action-btn {
  background: #374151;
  border-color: #4b5563;
  color: #d1d5db;
}

.action-btn:hover {
  background: #e5e7eb;
  transform: translateY(-1px);
}

.chat-wrapper.dark-mode .action-btn:hover {
  background: #4b5563;
}

.action-btn svg {
  width: 12px;
  height: 12px;
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
  gap: 0.75rem;
  padding: 1.5rem;
  position: relative;
  z-index: 1;
}

.typing-dots {
  display: flex;
  gap: 3px;
}

.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #9ca3af;
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
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
}

.chat-wrapper.dark-mode .loading-text {
  color: #9ca3af;
}

/* Input Area */
.input-area {
  padding: 1rem 1.25rem;
  background: #ffffff;
  border-top: 1px solid #e5e7eb;
  flex-shrink: 0;
  position: relative;
  z-index: 1;
}

.chat-wrapper.dark-mode .input-area {
  background: #1f2937;
  border-top-color: #374151;
}

.input-form {
  position: relative;
}

.input-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 0.5rem;
  background: #ffffff;
  border: 1.5px solid #e5e7eb;
  border-radius: 14px;
  padding: 0.625rem 0.875rem;
  transition: border-color 0.2s ease;
  min-height: 52px;
}

.chat-wrapper.dark-mode .input-wrapper {
  background: #1f2937;
  border-color: #374151;
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
  line-height: 1.4;
  color: #111827;
  background: transparent;
  max-height: 80px;
  min-height: 20px;
  padding: 0.375rem 0;
  height: 24px;
}

.chat-wrapper.dark-mode .message-input {
  color: #f3f4f6;
}

.message-input::placeholder {
  color: #9ca3af;
}

.message-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.input-actions {
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.cancel-btn {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.75rem;
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
  border-radius: 8px;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  height: 36px;
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
  width: 12px;
  height: 12px;
}

.cancel-text {
  font-size: 0.8125rem;
}

.send-btn {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
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
  width: 16px;
  height: 16px;
}

.input-hints {
  display: flex;
  justify-content: space-between;
  margin-top: 0.375rem;
  padding: 0 0.125rem;
}

.hint-text {
  font-size: 0.6875rem;
  color: #9ca3af;
}

.char-count {
  font-size: 0.6875rem;
  color: #9ca3af;
}

.char-count.warning {
  color: #dc2626;
  font-weight: 500;
}

/* Global Markdown Styles */
.message-content-inner {
  line-height: 1.6;
  color: #374151;
}

.chat-wrapper.dark-mode .message-content-inner {
  color: #e5e7eb;
}

.message-content-inner h1,
.message-content-inner h2,
.message-content-inner h3,
.message-content-inner h4,
.message-content-inner h5,
.message-content-inner h6 {
  margin-top: 1.25em;
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
  color: #f3f4f6;
}

.message-content-inner h1 { font-size: 1.375em; }
.message-content-inner h2 { font-size: 1.25em; }
.message-content-inner h3 { font-size: 1.125em; }
.message-content-inner h4 { font-size: 1em; }
.message-content-inner h5 { font-size: 0.875em; }
.message-content-inner h6 { font-size: 0.85em; }

.message-content-inner p {
  margin: 0.875em 0;
  color: #4b5563;
}

.chat-wrapper.dark-mode .message-content-inner p {
  color: #d1d5db;
}

.message-content-inner ul,
.message-content-inner ol {
  margin: 0.875em 0;
  padding-left: 1.5em;
  color: #4b5563;
}

.chat-wrapper.dark-mode .message-content-inner ul,
.chat-wrapper.dark-mode .message-content-inner ol {
  color: #d1d5db;
}

.message-content-inner li {
  margin: 0.375em 0;
}

.message-content-inner blockquote {
  margin: 1em 0;
  padding: 0.75em 1em;
  border-left: 4px solid #10b981;
  background: #f0fdf4;
  border-radius: 0 6px 6px 0;
  color: #065f46;
}

.chat-wrapper.dark-mode .message-content-inner blockquote {
  background: #064e3b;
  color: #a7f3d0;
}

.message-content-inner code {
  background: #f3f4f6;
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-size: 0.9em;
  font-family: 'SFMono-Regular', 'Consolas', 'Liberation Mono', 'Menlo', monospace;
  color: #111827;
  border: 1px solid #e5e7eb;
}

.chat-wrapper.dark-mode .message-content-inner code {
  background: #374151;
  border-color: #4b5563;
  color: #e5e7eb;
}

.message-content-inner pre {
  background: #1f2937;
  border-radius: 8px;
  padding: 1em;
  overflow-x: auto;
  margin: 1em 0;
  border: 1px solid #374151;
}

.message-content-inner pre code {
  background: none;
  padding: 0;
  color: #e5e7eb;
  border: none;
}

.message-content-inner table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
  font-size: 0.9em;
}

.message-content-inner th,
.message-content-inner td {
  border: 1px solid #e5e7eb;
  padding: 0.75em;
  text-align: left;
  color: #374151;
}

.chat-wrapper.dark-mode .message-content-inner th,
.chat-wrapper.dark-mode .message-content-inner td {
  border-color: #4b5563;
  color: #d1d5db;
}

.message-content-inner th {
  background: #f9fafb;
  font-weight: 600;
  color: #111827;
}

.chat-wrapper.dark-mode .message-content-inner th {
  background: #374151;
  color: #f3f4f6;
}

.message-content-inner a {
  color: #2563eb;
  text-decoration: none;
  font-weight: 500;
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
  border: 1px solid #e5e7eb;
}

.chat-wrapper.dark-mode .message-content-inner img {
  border-color: #4b5563;
}

.message-content-inner hr {
  margin: 1.5em 0;
  border: none;
  border-top: 2px solid #e5e7eb;
}

.chat-wrapper.dark-mode .message-content-inner hr {
  border-color: #4b5563;
}

/* PDF Attachment Styles */
.pdf-attachment {
  margin-top: 1rem;
  padding: 1.25rem;
  background: linear-gradient(135deg, #f0fdf4, #dcfce7);
  border-radius: 12px;
  border: 1px solid #bbf7d0;
}

.chat-wrapper.dark-mode .pdf-attachment {
  background: linear-gradient(135deg, #064e3b, #065f46);
  border-color: #047857;
}

.attachment-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.attachment-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #10b981, #059669);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.attachment-icon svg {
  width: 24px;
  height: 24px;
  color: white;
}

.attachment-info h4 {
  margin: 0 0 0.25rem 0;
  color: #065f46;
  font-size: 1.1rem;
}

.chat-wrapper.dark-mode .attachment-info h4 {
  color: #a7f3d0;
}

.attachment-info p {
  margin: 0;
  color: #047857;
  font-size: 0.875rem;
}

.chat-wrapper.dark-mode .attachment-info p {
  color: #86efac;
}

.attachment-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid rgba(5, 150, 105, 0.2);
}

.file-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.file-name {
  font-weight: 600;
  color: #111827;
  font-size: 0.95rem;
}

.chat-wrapper.dark-mode .file-name {
  color: #f3f4f6;
}

.file-size {
  font-size: 0.75rem;
  color: #6b7280;
}

.chat-wrapper.dark-mode .file-size {
  color: #9ca3af;
}

.download-btn {
  padding: 0.5rem 1.5rem;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.download-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

/* Header ESG Button */
.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.esg-report-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.esg-report-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.esg-report-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.esg-report-btn svg {
  width: 16px;
  height: 16px;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .chat-container {
    width: calc(100% - 16px);
    height: calc(100% - 16px);
    margin: 8px;
  }
  
  .chat-sidebar {
    width: 260px;
  }
  
  .chat-sidebar.collapsed {
    width: 60px;
  }
  
  .sidebar-content {
    padding: 1rem;
  }
}

@media (max-width: 768px) {
  .chat-container {
    width: 100%;
    height: 100%;
    margin: 0;
    border-radius: 0;
    flex-direction: column;
  }
  
  .chat-sidebar {
    width: 100%;
    height: auto;
    max-height: 200px;
  }
  
  .chat-sidebar.collapsed {
    width: 100%;
    height: 60px;
  }
  
  .sidebar-content {
    flex-direction: row;
    align-items: center;
    padding: 0.75rem;
  }
  
  .sidebar-header {
    margin-bottom: 0;
    flex: 1;
  }
  
  .logo-animation {
    width: 36px;
    height: 36px;
    margin-bottom: 0.25rem;
  }
  
  .logo-orb.orb-1 {
    width: 36px;
    height: 36px;
  }
  
  .logo-orb.orb-2 {
    width: 28px;
    height: 28px;
    top: 4px;
    left: 4px;
  }
  
  .logo-orb.orb-3 {
    width: 20px;
    height: 20px;
    top: 8px;
    left: 8px;
  }
  
  .logo-core {
    width: 20px;
    height: 20px;
  }
  
  .logo-icon {
    width: 12px;
    height: 12px;
  }
  
  .brand-name {
    font-size: 1rem;
  }
  
  .brand-tagline {
    font-size: 0.6875rem;
  }
  
  .chat-sidebar.collapsed .logo-section,
  .chat-sidebar.collapsed .brand-tagline {
    display: none;
  }
  
  .user-section {
    display: none;
  }
  
  .chat-history-section {
    display: none;
  }
  
  .sidebar-actions {
    flex-direction: row;
    padding-top: 0;
    border-top: none;
    margin-left: 0.5rem;
  }
  
  .sidebar-btn {
    padding: 0.375rem;
  }
  
  .sidebar-btn span {
    display: none;
  }
  
  .messages-container {
    padding: 0.75rem;
  }
  
  .messages-list {
    padding: 0 0.5rem;
    gap: 1.25rem;
  }
  
  .message-content {
    max-width: 90%;
  }
  
  .welcome-content {
    padding: 1rem;
    margin: 0.5rem;
  }
  
  .welcome-content h3 {
    font-size: 1.25rem;
  }
  
  .welcome-text {
    font-size: 0.9375rem;
  }
  
  .starter-buttons {
    max-width: 100%;
  }
  
  .input-area {
    padding: 0.75rem 1rem;
  }
  
  .cancel-text {
    display: none;
  }
  
  .cancel-btn {
    padding: 0.375rem;
  }
  
  .hint-text {
    font-size: 0.625rem;
  }
}
</style>