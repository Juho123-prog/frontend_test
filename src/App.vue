<template>
  <div class="layout">
    <!-- 상단 고정 헤더 -->
    <header class="header">
      <h1 class="title">과제</h1>
      <p class="subtitle">Vue Router 실습</p>
    </header>

    <!-- 아래만 전환 -->
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.layout {
  min-height: 100vh;
  background-color: #f9fafb;
}

/* 상단 바 */
.header {
  background: white;
  padding: 20px 32px;
  border-bottom: 1px solid #e5e7eb;
}

.title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  color: #111827;
}

.subtitle {
  font-size: 0.9rem;
  margin-top: 4px;
  color: #6b7280;
}

/* router-view 영역 */
.content {
  padding: 32px;
}
</style>
