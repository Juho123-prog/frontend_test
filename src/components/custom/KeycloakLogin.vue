<template>
  <button class="login-btn" @click="login">로그인</button>
</template>
<script>
import { startKeycloakLogin } from '@/services/keycloakAuth.js';
export default {
  name: 'KeycloakLogin',
  methods: {
    async login() {
      await startKeycloakLogin();
    }
  }
};
</script>
<style scoped>
.login-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}
.login-btn:hover {
  background-color: #0056b3;
}
</style>

