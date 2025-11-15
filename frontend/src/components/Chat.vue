<template>
  <div class="chat-wrapper">
    <header class="chat-header">
      <h1>💬 Cariboun AI</h1>
    </header>

    <main class="chat-body" ref="chatWindow">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['message', msg.role]"
      >
        <div class="bubble">
          <p>{{ msg.text }}</p>
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
import axios from 'axios';

import api from '../plugins/axios'
export default {
  name: "EsgBuddy",

  data() {
    return {
      messages: [],
      userInput: "",
      loading: false,
    };
  },

  mounted() {
    
    console.log(this.loadMessages());
    
  },

  methods: {
    async loadMessages() {
      // Placeholder for backend load
      this.messages = [
        {
          role: "assistant",
          text: "👋 Hello! I'm Cariboun AI — your AI assistant for sustainability and Cariboun AI insights. How can I help today?",
        },
        // {
        //     role: "user",
        //     text: "What is Cariboun AI?"
        // }
      ];

      axios.get("http://localhost:8000/chat/messages/1/")
        .then(response => {
          console.log(response.status);
          console.log(response.data);
          
          for (const msg of response.data) {
            if (msg !== "" && msg !== null && msg !== undefined) {
              this.messages.push(msg);
              // console.log(this.messages);
              
            }
          }
        })
        .catch(error => {
          console.error("Error loading messages:", error);
        });
    },

    async handleSend() {
      if (!this.userInput.trim()) return;

      const userMessage = {
        role: "user",
        text: this.userInput.trim(),
      };

      this.messages.push(userMessage);
      this.userInput = "";
      this.loading = true;
      this.scrollToBottom();

      // Simulate backend delay
      // setTimeout(() => {
      //   const reply = {
      //     role: "assistant",
      //     text: "This is a sample response from Cariboun AI! 🌿",
      //   };
      //   this.messages.push(reply);
      //   this.loading = false;
      //   this.scrollToBottom();
      // }, 1000);
      api.post("http://localhost:8000/chat/send-message/", {
        message: this.userInput.trim()
      })
      .then(response => {
        const reply = {
          role: "assistant",
          text: response.data.reply
        };
        this.messages.push(reply);
      })
      .catch(error => {
        console.error("Error sending message:", error);
      })
      .finally(() => {
        this.loading = false;
        this.scrollToBottom();
      });
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
  padding: 0.85rem 1rem;
  border-radius: 16px;
  word-break: break-word;
  line-height: 1.5;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  backdrop-filter: none;
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
    