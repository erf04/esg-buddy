<template>
  <div class="auth-wrapper">
    <!-- Animated Background -->
    <div class="background-animation">
      <div class="bg-shape bg-shape-1"></div>
      <div class="bg-shape bg-shape-2"></div>
      <div class="bg-shape bg-shape-3"></div>
      <div class="bg-shape bg-shape-4"></div>
    </div>

    <!-- Auth Container -->
    <div class="auth-container">
      <!-- Left Panel with Logo -->
      <div class="left-panel">
        <div class="logo-section">
          <div class="logo-animation">
            <div class="logo-orb logo-orb-1"></div>
            <div class="logo-orb logo-orb-2"></div>
            <div class="logo-orb logo-orb-3"></div>
            <div class="logo-main">
              <svg class="logo-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
              </svg>
            </div>
          </div>
          <h1 class="brand-name">Cariboun<span class="ai-highlight">AI</span></h1>
          <p class="brand-tagline">Where Intelligence Meets Conversation</p>
        </div>

        <!-- Features List with Animation -->
        <div class="features-section">
          <div class="feature-item" v-for="(feature, index) in features" :key="index">
            <div class="feature-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </div>
            <span class="feature-text">{{ feature }}</span>
          </div>
        </div>

        <!-- Decorative Wave -->
        <div class="wave-animation">
          <div class="wave wave-1"></div>
          <div class="wave wave-2"></div>
          <div class="wave wave-3"></div>
        </div>
      </div>

      <!-- Right Panel with Form -->
      <div class="right-panel">
        <!-- Form Header -->
        <div class="form-header">
          <h2>{{ isLogin ? "Welcome Back" : "Create Account" }}</h2>
          <p class="header-subtitle">
            {{ isLogin ? "Sign in to continue your journey" : "Start your AI adventure today" }}
          </p>
        </div>

        <!-- Mode Toggle -->
        <div class="mode-toggle">
          <div class="toggle-buttons">
            <button 
              :class="['toggle-btn', { 'active': !isLogin }]" 
              @click="isLogin = false"
            >
              Sign Up
            </button>
            <button 
              :class="['toggle-btn', { 'active': isLogin }]" 
              @click="isLogin = true"
            >
              Login
            </button>
          </div>
          <div class="toggle-indicator" :class="{ 'login': isLogin }"></div>
        </div>

        <!-- Form Content -->
        <div class="form-content">
          <!-- Name Fields for Signup -->
          <div v-if="!isLogin" class="name-fields">
            <div class="input-group">
              <input
                v-model="firstName"
                type="text"
                placeholder="First Name"
                required
              />
              <div class="input-decoration"></div>
            </div>
            <div class="input-group">
              <input
                v-model="lastName"
                type="text"
                placeholder="Last Name"
                required
              />
              <div class="input-decoration"></div>
            </div>
          </div>

          <!-- Email Field -->
          <div class="input-group">
            <div class="input-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
              </svg>
            </div>
            <input
              v-model="email"
              type="email"
              placeholder="Email Address"
              required
            />
            <div class="input-decoration"></div>
          </div>

          <!-- Password Field -->
          <div class="input-group">
            <div class="input-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
              </svg>
            </div>
            <input
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="Password"
              required
            />
            <button 
              type="button" 
              class="password-toggle"
              @click="showPassword = !showPassword"
            >
              <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="1" y1="1" x2="23" y2="23"></line>
                <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                <line x1="1" y1="1" x2="23" y2="23"></line>
              </svg>
            </button>
            <div class="input-decoration"></div>
          </div>

          <!-- Terms Agreement for Signup -->
          <!-- <div v-if="!isLogin" class="terms-agreement">
            <label class="checkbox-container">
              <input type="checkbox" v-model="agreeTerms" />
              <span class="checkmark"></span>
              <span class="checkbox-label">I agree to the <a href="#" class="terms-link">Terms & Conditions</a></span>
            </label>
          </div> -->

          <!-- Submit Button -->
          <button 
            type="button" 
            class="submit-btn"
            :disabled="loading || (!isLogin && !agreeTerms)"
            @click="handleSubmit"
          >
            <span v-if="loading" class="spinner"></span>
            <span v-else class="btn-content">
              {{ isLogin ? "Login to Account" : "Create Account" }}
              <svg class="btn-arrow" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
              </svg>
            </span>
          </button>

          <!-- Divider -->
          <!-- <div class="divider">
            <span class="divider-text">or continue with</span>
          </div> -->

          <!-- Social Login -->
          <!-- <div class="social-login">
            <button class="social-btn google" @click="socialLogin('google')">
              <svg class="social-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              </svg>
              <span>Google</span>
            </button>
            <button class="social-btn facebook" @click="socialLogin('facebook')">
              <svg class="social-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
              </svg>
              <span>Facebook</span>
            </button>
          </div> -->

          <!-- Switch Mode -->
          <div class="switch-mode">
            <span>{{ isLogin ? "Don't have an account?" : "Already have an account?" }}</span>
            <button class="switch-link" @click="toggleMode">
              {{ isLogin ? "Sign up" : "Log in" }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { useRouter } from "vue-router";
import { onMounted } from 'vue';

export default {
  name: "LoginSignup",
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();

    onMounted(() => {
      document.body.style.overflow = 'hidden';
    });

    return { authStore, router };
  },
  data() {
    return {
      isLogin: false,
      firstName: "",
      lastName: "",
      email: "",
      password: "",
      showPassword: false,
      agreeTerms: false,
      loading: false,
      features: [
        "Smart AI Conversations",
        "Real-time Processing",
        "Secure & Private",
        "Multi-language Support"
      ]
    };
  },
  methods: {
    animateInput(fieldName) {
      console.log(`Focusing on ${fieldName}`);
    },
    
    toggleMode() {
      this.isLogin = !this.isLogin;
      this.resetForm();
    },
    
    resetForm() {
      this.firstName = "";
      this.lastName = "";
      this.email = "";
      this.password = "";
      this.agreeTerms = false;
    },
    
    async handleSubmit() {
      this.loading = true;
      
      try {
        if (this.isLogin) {
          await this.authStore.login(this.email, this.password);
          this.router.push('/chat');
        } else {
          await this.authStore.signup(this.email, this.password);
          this.isLogin = true;
          this.resetForm();
        }
      } catch (error) {
        console.error('Auth error:', error);
      } finally {
        this.loading = false;
      }
    },
    
    socialLogin(provider) {
      console.log(`Social login with ${provider}`);
      // Implement social login logic here
    }
  }
};
</script>

<style scoped>
.auth-wrapper {
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
  padding: 20px;
  overflow: hidden;
}

/* Animated Background */
.background-animation {
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

.bg-shape-1 {
  width: 300px;
  height: 300px;
  background: #10b981;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
  animation-duration: 25s;
}

.bg-shape-2 {
  width: 200px;
  height: 200px;
  background: #059669;
  bottom: 20%;
  right: 15%;
  animation-delay: 5s;
  animation-duration: 20s;
}

.bg-shape-3 {
  width: 150px;
  height: 150px;
  background: #34d399;
  top: 50%;
  left: 20%;
  animation-delay: 10s;
  animation-duration: 15s;
}

.bg-shape-4 {
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
.auth-container {
  display: flex;
  width: 100%;
  max-width: 1200px;
  height: 700px;
  background: white;
  border-radius: 32px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 2;
  animation: containerAppear 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
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

/* Left Panel */
.left-panel {
  flex: 1;
  background: linear-gradient(135deg, #0f766e 0%, #059669 100%);
  padding: 48px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}

.logo-section {
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
  margin-bottom: 24px;
}

.logo-orb {
  position: absolute;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.3);
  animation: orbPulse 3s ease-in-out infinite;
}

.logo-orb-1 {
  width: 80px;
  height: 80px;
  animation-delay: 0s;
}

.logo-orb-2 {
  width: 60px;
  height: 60px;
  top: 10px;
  left: 10px;
  animation-delay: 0.5s;
}

.logo-orb-3 {
  width: 40px;
  height: 40px;
  top: 20px;
  left: 20px;
  animation-delay: 1s;
}

.logo-main {
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

.brand-name {
  font-size: 36px;
  font-weight: 800;
  color: white;
  margin: 0 0 8px 0;
  letter-spacing: -0.5px;
}

.ai-highlight {
  color: #a7f3d0;
  font-weight: 900;
}

.brand-tagline {
  color: rgba(255, 255, 255, 0.8);
  font-size: 16px;
  margin: 0;
  font-weight: 400;
}

.features-section {
  margin-top: 40px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
  color: white;
  opacity: 0;
  animation: featureItemAppear 0.4s ease-out forwards;
}

.feature-item:nth-child(1) { animation-delay: 0.4s; }
.feature-item:nth-child(2) { animation-delay: 0.6s; }
.feature-item:nth-child(3) { animation-delay: 0.8s; }
.feature-item:nth-child(4) { animation-delay: 1s; }

@keyframes featureItemAppear {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.feature-icon {
  width: 24px;
  height: 24px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.feature-icon svg {
  width: 14px;
  height: 14px;
  color: white;
  stroke-width: 3;
}

.feature-text {
  font-size: 15px;
  font-weight: 400;
}

.wave-animation {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 80px;
  overflow: hidden;
}

.wave {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 200%;
  height: 40px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  animation: waveFlow 8s linear infinite;
}

.wave-1 {
  animation-delay: 0s;
  opacity: 0.3;
}

.wave-2 {
  animation-delay: 2s;
  opacity: 0.2;
  bottom: 20px;
}

.wave-3 {
  animation-delay: 4s;
  opacity: 0.1;
  bottom: 40px;
}

@keyframes waveFlow {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-50%);
  }
}

/* Right Panel */
.right-panel {
  flex: 1;
  padding: 48px;
  display: flex;
  flex-direction: column;
  animation: slideInRight 0.6s ease-out 0.4s both;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.form-header {
  text-align: center;
  margin-bottom: 32px;
}

.form-header h2 {
  font-size: 32px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 8px 0;
  background: linear-gradient(135deg, #0f766e 0%, #059669 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-subtitle {
  color: #64748b;
  font-size: 15px;
  margin: 0;
}

.mode-toggle {
  position: relative;
  margin-bottom: 40px;
}

.toggle-buttons {
  display: flex;
  background: #f1f5f9;
  border-radius: 16px;
  padding: 6px;
  position: relative;
}

.toggle-btn {
  flex: 1;
  padding: 16px 24px;
  border: none;
  background: transparent;
  font-size: 16px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 12px;
  z-index: 1;
}

.toggle-btn:hover {
  color: #0f766e;
}

.toggle-btn.active {
  color: #0f766e;
}

.toggle-indicator {
  position: absolute;
  top: 6px;
  left: 6px;
  width: calc(50% - 6px);
  height: calc(100% - 12px);
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
  transition: transform 0.4s cubic-bezier(0.68, -0.55, 0.27, 1.55);
}

.toggle-indicator.login {
  transform: translateX(100%);
}

.form-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.name-fields {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.input-group {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #94a3b8;
  z-index: 2;
}

.input-group input {
  width: 100%;
  padding: 18px 16px 18px 48px;
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  font-size: 15px;
  transition: all 0.3s ease;
  background: white;
  outline: none;
  position: relative;
  z-index: 1;
}

.input-group input:focus {
  border-color: #10b981;
  box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.1);
  transform: translateY(-2px);
}

.input-decoration {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #10b981, #34d399);
  transition: width 0.3s ease;
  z-index: 1;
}

.input-group input:focus ~ .input-decoration {
  width: 100%;
}

.password-toggle {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  padding: 4px;
  z-index: 2;
}

.password-toggle svg {
  width: 20px;
  height: 20px;
  transition: all 0.3s ease;
}

.password-toggle:hover svg {
  color: #10b981;
}

.terms-agreement {
  margin-top: -8px;
}

.checkbox-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 14px;
  color: #64748b;
  position: relative;
}

.checkbox-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  position: relative;
  height: 20px;
  width: 20px;
  background-color: white;
  border: 2px solid #e2e8f0;
  border-radius: 6px;
  margin-right: 12px;
  transition: all 0.3s ease;
}

.checkbox-container:hover .checkmark {
  border-color: #10b981;
}

.checkbox-container input:checked ~ .checkmark {
  background-color: #10b981;
  border-color: #10b981;
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
  left: 6px;
  top: 2px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.checkbox-container input:checked ~ .checkmark:after {
  display: block;
}

.terms-link {
  color: #10b981;
  text-decoration: none;
  font-weight: 500;
}

.terms-link:hover {
  text-decoration: underline;
}

.submit-btn {
  padding: 18px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 16px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 8px;
  position: relative;
  overflow: hidden;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 30px rgba(16, 185, 129, 0.4);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-arrow {
  width: 18px;
  height: 18px;
  transition: transform 0.3s ease;
}

.submit-btn:hover .btn-arrow {
  transform: translateX(4px);
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top: 3px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.divider {
  display: flex;
  align-items: center;
  margin: 16px 0;
  color: #94a3b8;
  font-size: 14px;
  position: relative;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
}

.divider-text {
  padding: 0 16px;
  background: white;
  z-index: 1;
}

.social-login {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.social-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 16px;
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  background: white;
  color: #475569;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.social-btn:hover {
  transform: translateY(-2px);
  border-color: #10b981;
  box-shadow: 0 8px 20px rgba(16, 185, 129, 0.1);
}

.social-btn.google:hover {
  color: #4285f4;
}

.social-btn.facebook:hover {
  color: #1877f2;
}

.social-icon {
  width: 20px;
  height: 20px;
}

.switch-mode {
  text-align: center;
  margin-top: auto;
  padding-top: 24px;
  color: #64748b;
  font-size: 14px;
  border-top: 1px solid #e2e8f0;
}

.switch-link {
  color: #10b981;
  background: none;
  border: none;
  font-weight: 600;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  margin-left: 4px;
  transition: all 0.3s ease;
}

.switch-link:hover {
  color: #059669;
  background: rgba(16, 185, 129, 0.1);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .auth-container {
    max-width: 900px;
    height: 650px;
  }
  
  .left-panel,
  .right-panel {
    padding: 32px;
  }
}

@media (max-width: 768px) {
  .auth-container {
    flex-direction: column;
    height: auto;
    max-height: 90vh;
    overflow-y: auto;
  }
  
  .left-panel {
    padding: 32px;
    min-height: 200px;
  }
  
  .right-panel {
    padding: 32px;
  }
  
  .name-fields {
    grid-template-columns: 1fr;
  }
  
  .social-login {
    grid-template-columns: 1fr;
  }
  
  .features-section {
    display: none;
  }
}

@media (max-width: 480px) {
  .auth-wrapper {
    padding: 12px;
  }
  
  .auth-container {
    border-radius: 24px;
  }
  
  .left-panel,
  .right-panel {
    padding: 24px;
  }
  
  .brand-name {
    font-size: 28px;
  }
  
  .form-header h2 {
    font-size: 24px;
  }
  
  .toggle-btn {
    padding: 14px 16px;
    font-size: 15px;
  }
}
</style>