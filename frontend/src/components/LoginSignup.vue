<template>
  <div class="auth-wrapper">
    <div class="auth-container">
      <h2>{{ isLogin ? "Welcome Back!" : "Create Account" }}</h2>
      <p class="subtitle">{{ isLogin ? "Sign in to continue your journey" : "Join us to get started" }}</p>

      <form @submit.prevent="handleSubmit">
        <div class="input-group">
          <input
            v-model="email"
            type="email"
            placeholder="Email"
            required
          />
          <svg class="input-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
            <polyline points="22,6 12,13 2,6"></polyline>
          </svg>
        </div>
        
        <div class="input-group">
          <input
            v-model="password"
            type="password"
            placeholder="Password"
            required
          />
          <svg class="input-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
          </svg>
        </div>

        <button type="submit" :disabled="loading" class="submit-btn">
          <span v-if="loading" class="spinner"></span>
          {{ loading ? "Please wait..." : (isLogin ? "Login" : "Sign Up") }}
        </button>
      </form>

      <p class="toggle-text">
        {{ isLogin ? "Don't have an account?" : "Already have an account?" }}
        <span class="toggle-link" @click="toggleMode">{{ isLogin ? "Sign Up" : "Login" }}</span>
      </p>

      <!-- Toast Container -->
      <div class="toast-container" :class="{'toast-visible': showToast}">
        <div class="toast" :class="toastType">
          <div class="toast-icon">
            <svg v-if="toastType === 'success'" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
            <svg v-else-if="toastType === 'error'" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="15" y1="9" x2="9" y2="15"></line>
              <line x1="9" y1="9" x2="15" y2="15"></line>
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
          </div>
          <div class="toast-content">
            <div class="toast-title">{{ toastTitle }}</div>
            <div class="toast-message">{{ toastMessage }}</div>
          </div>
          <button class="toast-close" @click="hideToast">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { useRouter } from "vue-router";

export default {
  name: "LoginSignup",
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    return { authStore, router };
  },
  data() {
    return {
      isLogin: true,
      email: "",
      password: "",
      // Toast related data
      showToast: false,
      toastType: "info", // 'success', 'error', 'info', 'warning'
      toastTitle: "",
      toastMessage: "",
      toastTimeout: null
    };
  },
  computed: {
    loading() {
      return this.authStore.isLoading;
    }
  },
  methods: {
    toggleMode() {
      this.isLogin = !this.isLogin;
      this.hideToast();
    },

    async handleSubmit() {
      this.hideToast();

      try {
        if (this.isLogin) {
          await this.authStore.login(this.email, this.password);
          this.showToastMessage(
            "success", 
            "Login Successful!", 
            "Welcome back! Redirecting to chat...",
            1000
          );
          
          setTimeout(() => {
            this.router.push('/chat');
          }, 1000);
        } else {
          await this.authStore.signup(this.email, this.password);
          this.showToastMessage(
            "success",
            "Account Created!",
            "Your account has been created successfully. You can now login.",
            1500
          );
          
          setTimeout(() => {
            this.isLogin = true;
            this.email = "";
            this.password = "";
          }, 1000);
        }
      } catch (error) {
        this.handleAuthError(error);
      }
    },

    handleAuthError(error) {
      let errorTitle = this.isLogin ? "Login Failed" : "Signup Failed";
      let errorMessage = "An unexpected error occurred. Please try again.";
      
      if (error.response) {
        const status = error.response.status;
        const data = error.response.data;
        
        if (status === 401) {
          errorTitle = "Invalid Credentials";
          errorMessage = "The email or password you entered is incorrect.";
        } else if (status === 400) {
          errorTitle = "Invalid Input";
          errorMessage = data.message || "Please check your email and password format.";
        } else if (status === 409 && !this.isLogin) {
          errorTitle = "Email Already Exists";
          errorMessage = "An account with this email already exists. Please try logging in.";
        } else if (status >= 500) {
          errorTitle = "Server Error";
          errorMessage = "Our servers are experiencing issues. Please try again later.";
        } else {
          errorMessage = data.message || "An error occurred.";
        }
      } else if (error.request) {
        errorTitle = "Network Error";
        errorMessage = "Unable to connect to the server. Please check your internet connection.";
      }
      
      this.showToastMessage("error", errorTitle, errorMessage);
    },

    // Toast methods
    showToastMessage(type, title, message, duration = 5000) {
      if (this.toastTimeout) {
        clearTimeout(this.toastTimeout);
      }
      
      this.toastType = type;
      this.toastTitle = title;
      this.toastMessage = message;
      this.showToast = true;
      
      this.toastTimeout = setTimeout(() => {
        this.hideToast();
      }, duration);
    },

    hideToast() {
      this.showToast = false;
      if (this.toastTimeout) {
        clearTimeout(this.toastTimeout);
        this.toastTimeout = null;
      }
    }
  }
};
</script>

<style scoped>
/* Your existing styles remain the same */
.auth-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: "Inter", sans-serif;
  padding: 20px;
}

.auth-container {
  width: 100%;
  max-width: 480px;
  padding: 3rem 2.5rem;
  background: #ffffff;
  border-radius: 20px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
}

.auth-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(to right, #ff7eb3, #ff758c, #ff7eb3);
  background-size: 200% 100%;
  animation: gradientMove 3s ease infinite;
}

@keyframes gradientMove {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.auth-container h2 {
  margin-bottom: 0.5rem;
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  transition: all 0.3s ease;
}

.subtitle {
  margin-bottom: 2rem;
  color: #6b7280;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.auth-container form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.input-group {
  position: relative;
}

.auth-container input {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
  border-radius: 12px;
  border: 2px solid #e5e7eb;
  outline: none;
  font-size: 1rem;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.auth-container input:focus {
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
  transform: translateY(-2px);
}

.input-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1.25rem;
  height: 1.25rem;
  color: #9ca3af;
  transition: all 0.3s ease;
}

.auth-container input:focus + .input-icon {
  color: #8b5cf6;
}

.submit-btn {
  padding: 1rem;
  border-radius: 12px;
  border: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 3.5rem;
}

.submit-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.submit-btn:active {
  transform: translateY(-1px);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.spinner {
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid transparent;
  border-top: 2px solid #ffffff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 0.5rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.toggle-text {
  margin-top: 1.5rem;
  font-size: 0.95rem;
  color: #6b7280;
  transition: all 0.3s ease;
}

.toggle-link {
  color: #8b5cf6;
  cursor: pointer;
  margin-left: 0.25rem;
  font-weight: 600;
  transition: all 0.3s ease;
  position: relative;
}

.toggle-link:hover {
  color: #7c3aed;
}

.toggle-link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: #8b5cf6;
  transition: width 0.3s ease;
}

.toggle-link:hover::after {
  width: 100%;
}

/* Toast Styles */
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
  transform: translateX(400px);
  opacity: 0;
  transition: all 0.4s cubic-bezier(0.68, -0.55, 0.27, 1.55);
}

.toast-visible {
  transform: translateX(0);
  opacity: 1;
}

.toast {
  display: flex;
  align-items: flex-start;
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  min-width: 320px;
  max-width: 400px;
  animation: toastSlideIn 0.4s ease;
  position: relative;
  overflow: hidden;
}

.toast::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
}

.toast.success {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #166534;
}

.toast.success::before {
  background: #22c55e;
}

.toast.error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
}

.toast.error::before {
  background: #ef4444;
}

.toast.info {
  background: #eff6ff;
  border: 1px solid #dbeafe;
  color: #1e40af;
}

.toast.info::before {
  background: #3b82f6;
}

.toast.warning {
  background: #fffbeb;
  border: 1px solid #fed7aa;
  color: #92400e;
}

.toast.warning::before {
  background: #f59e0b;
}

.toast-icon {
  flex-shrink: 0;
  width: 1.5rem;
  height: 1.5rem;
  margin-right: 0.75rem;
  margin-top: 0.125rem;
}

.toast-content {
  flex: 1;
  text-align: left;
}

.toast-title {
  font-weight: 600;
  font-size: 0.95rem;
  margin-bottom: 0.25rem;
}

.toast-message {
  font-size: 0.875rem;
  opacity: 0.9;
  line-height: 1.4;
}

.toast-close {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  margin-left: 0.5rem;
  border-radius: 4px;
  color: inherit;
  opacity: 0.7;
  transition: all 0.2s ease;
  flex-shrink: 0;
  width: 1.5rem;
  height: 1.5rem;
}

.toast-close:hover {
  opacity: 1;
  background: rgba(0, 0, 0, 0.1);
}

@keyframes toastSlideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Responsive */
@media (max-width: 480px) {
  .auth-container {
    padding: 2rem 1.5rem;
    max-width: 100%;
  }
  
  .auth-container h2 {
    font-size: 1.75rem;
  }
  
  .auth-container input,
  .auth-container button {
    font-size: 0.95rem;
  }
  
  .toast-container {
    right: 10px;
    left: 10px;
  }
  
  .toast {
    min-width: auto;
    max-width: none;
  }
}
</style>