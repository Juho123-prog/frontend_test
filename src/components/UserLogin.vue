<template>
  <transition name="modal-fade">
    <div v-if="isVisible" class="modal-overlay" @click.self="close">
      <div class="modal-content">
        <div class="modal-header">
          <h2>로그인</h2>
          <button @click="close" class="close-btn">&times;</button>
        </div>
        <form @submit.prevent="submitLogin" class="login-form">
          <div class="form-group">
            <label for="username">사용자 이름</label>
            <input type="text" id="username" v-model="username" required>
          </div>
          <div class="form-group">
            <label for="password">비밀번호</label>
            <input type="password" id="password" v-model="password" required>
          </div>
          <div class="form-actions">
            <button type="submit" class="submit-btn">로그인</button>
          </div>
          <p>회원가입 문의는 <a href="https://mobilex.kr/">MobileX</a> 팀에 문의 바랍니다. </p>
        </form>
      </div>
    </div>
  </transition>
</template>

<script>
import { mobilex_login } from '@/services/backendAPI';
import { useToast } from 'vue-toastification';

export default {
  name: 'UserLogin',
  props: {
    isVisible: {
      type: Boolean,
      default: false
    }
  },
  setup() {
    const toast = useToast();
    return { toast };
  },
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    close() {
      this.$emit('close');
    },
    async submitLogin() {
      if (this.username && this.password) {
        try {
          const response = await mobilex_login(this.username, this.password);
          const response_json = response.data;
          this.$cookies.set("username", this.username);
          this.$cookies.set("refresh_token", response_json["refresh_token"]);
          this.$cookies.set("access_token", response_json["access_token"]);
          this.$emit('login', { username: this.username });
          this.close();

        } catch (error) {
          if (error.response) {
            if (error.response.status === 401) {
              this.toast.error('계정 정보가 맞지 않습니다.');
            } else if (error.response.status === 503) {
              this.toast.error('서버가 응답하지 않습니다.');
            } else {
              this.toast.error('로그인에 실패했습니다.');
            }
          } else {
            this.toast.error('로그인 요청 중 오류가 발생했습니다.');
          }
          console.error(error);
        }
      } else {
        this.toast.error('사용자 이름과 비밀번호를 입력해주세요.');
      }
    }
  }
};
</script>

<style scoped>
/* General Overlay and Content Styling */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 30px 40px;
  width: 420px;
  max-width: 95%;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  transform: scale(1);
  transition: transform 0.3s ease-out;
}

/* Modal Header */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
}

.modal-header h2 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
}

.close-btn {
  background: transparent;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #aaa;
  transition: color 0.2s ease;
}

.close-btn:hover {
  color: #333;
}

/* Form Styling */
.login-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #555;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  box-sizing: border-box; /* Important for width */
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

input[type="text"]:focus,
input[type="password"]:focus {
  outline: none;
  border-color: #ff4b2b;
  box-shadow: 0 0 0 3px rgba(255, 75, 43, 0.2);
}

/* Form Actions & Buttons */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 10px;
}

.submit-btn, .cancel-btn {
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.submit-btn {
  background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%);
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4);
}

.cancel-btn {
  background-color: #6c757d;
}

.cancel-btn:hover {
  background-color: #5a6268;
  transform: translateY(-2px);
}

/* Signup Link */
p {
  margin-top: 25px;
  text-align: center;
  color: #666;
  font-size: 14px;
}

p a {
  color: #ff416c;
  text-decoration: none;
  font-weight: 600;
}

p a:hover {
  text-decoration: underline;
}

/* Transitions */
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active .modal-content,
.modal-fade-leave-active .modal-content {
  transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.modal-fade-enter-from .modal-content,
.modal-fade-leave-to .modal-content {
  transform: scale(0.9);
  opacity: 0;
}
</style>
