<template>
  <div class="default-container">
    <div class="card">
      <h1 class="title">Welcome 👋</h1>
      <p class="subtitle">여기는 default 페이지입니다.</p>

      <div class="divider" />

      <p class="description">
        버튼을 눌러<br />
        원하는 화면으로 이동하세요.
      </p>

      <!-- 버튼 영역 -->
      <div class="button-group">
        <button class="btn primary" @click="goA">
          A 화면
        </button>
        <button class="btn secondary" @click="goB">
          B 화면
        </button>
        <button class="btn secondary" @click="goC">
          C 화면
        </button>
        <button class="btn secondary" @click="goD">
          D 화면
        </button>
        <button class="btn secondary" @click="goE">
          E 화면
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goA = () => router.push('/a')
const goB = () => router.push('/b')
const goC = () => router.push('/c')
const goD = () => router.push('/d')
const goE = () => router.push('/e')
</script>

<style scoped>
.default-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa, #e4ecf7);
}

.card {
  background: white;
  padding: 48px 56px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  text-align: center;
  max-width: 420px;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: #1f2937;
}

.subtitle {
  font-size: 1.1rem;
  color: #4b5563;
  margin-bottom: 24px;
}

.divider {
  height: 1px;
  background: #e5e7eb;
  margin: 24px 0;
}

.description {
  font-size: 0.95rem;
  color: #6b7280;
  line-height: 1.6;
}

/* 버튼 스타일 */
.button-group {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-top: 32px;
}

.btn {
  padding: 12px 28px;
  border-radius: 999px;
  font-size: 0.95rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

/* 메인 버튼 */
.btn.primary {
  background: #4f46e5;
  color: white;
}

.btn.primary:hover {
  background: #4338ca;
  transform: translateY(-1px);
}

/* 서브 버튼 */
.btn.secondary {
  background: #eef2ff;
  color: #4338ca;
}

.btn.secondary:hover {
  background: #e0e7ff;
  transform: translateY(-1px);
}
</style>
