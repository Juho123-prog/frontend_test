<template>
  <div class="job-log-overlay-panel">
    <div class="job-log-header">
      <h2 class="job-log-title">Job Log Viewer</h2>
      <button class="job-log-close" @click="emit('close')">✕</button>
    </div>
    <div class="job-log-body">
      <p><strong>Job Name:</strong> {{ jobName }}</p>
      <p><strong>Log Type:</strong> {{ menuTypeLabel }}</p>
      <!-- 상태 표시 -->
      <div v-if="isLoading" class="job-log-status job-log-status--loading">
        로그를 불러오는 중입니다...
      </div>
      <div v-else-if="error" class="job-log-status job-log-status--error">
        {{ error }}
      </div>
      <div v-else>
        <!-- Code 로그 -->
        <div v-if="props.menuType === 'code'" class="job-log-content">
          <div v-if="terminalLog" class="job-log-code-block">
            {{ terminalLog }}
          </div>
          <div v-else class="system-log-empty">표시할 터미널 로그가 없습니다.</div>
        </div>
        <!-- System 로그 -->
        <div v-else-if="props.menuType === 'system'" class="job-log-content">
          <div v-if="jobEvents && jobEvents.length" class="job-log-events-wrapper">
            <table class="system-log-table">
              <thead>
                <tr>
                  <th>Type</th>
                  <th>Reason</th>
                  <th>Age</th>
                  <th>From</th>
                  <th>Message</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(event, idx) in jobEvents" :key="idx">
                  <td>{{ event.type }}</td>
                  <td>{{ event.reason }}</td>
                  <td>{{ event.age }}</td>
                  <td>{{ event.from }}</td>
                  <td class="system-log-message">{{ event.message }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="system-log-empty">표시할 System 로그가 없습니다.</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue';
import { getTerminalLog, getSystemLog } from '@/services/backendAPI';

const props = defineProps({
  jobName: {
    type: String,
    required: true,
  },
  menuType: {
    type: String,
    required: true,
  },
  accessToken: {
    type: String,
    required: true,
  }
});

const emit = defineEmits(['close']);

const menuTypeLabel = computed(() => {
  if (props.menuType === 'terminal') return 'Terminal Log';
  if (props.menuType === 'system') return 'System Log';
  return props.menuType || 'Unknown';
});

// 상태
const isLoading = ref(false);
const error = ref('');
const terminalLog = ref('');
const jobEvents = ref([]);



async function loadTerminalLog() {
  isLoading.value = true;
  error.value = '';
  terminalLog.value = '';
  try {
    if (!props.jobName) {
      error.value = 'Job 이름이 없습니다.';
      return;
    }
    if (!props.accessToken) {
      error.value = '접근 토큰이 없습니다. 다시 로그인 해주세요.';
      return;
    }
    const res = await getTerminalLog(props.jobName, props.accessToken);
    // 현재 backendAPI.getCodeLog는 문자열을 반환하므로 그대로 사용
    // 향후 실제 백엔드에서는 res.data.log 형태일 수 있으므로 방어적으로 처리
    if (typeof res === 'string') {
      terminalLog.value = res;
    } else if (res && typeof res === 'object') {
      if (typeof res.log === 'string') {
        terminalLog.value = res.log;
      } else if (typeof res.info === 'string') {
        terminalLog.value = res.info;
      }
      else {
        error.value = '알 수 없는 Terminal Log 응답 형식입니다.';
      }
    } else {
      error.value = 'Terminal Log를 불러오지 못했습니다.';
    }
  } catch (e) {
      if (e.status == '410'){
        error.value = e.response.data.error
      }
      else{
        error.value = 'Terminal Log 요청 중 오류가 발생했습니다.';
      }


  } finally {
    isLoading.value = false;
  }
}

async function loadSystemLog() {
  isLoading.value = true;
  error.value = '';
  jobEvents.value = [];
  try {
    if (!props.jobName) {
      error.value = 'Job 이름이 없습니다.';
      return;
    }
    if (!props.accessToken) {
      error.value = '접근 토큰이 없습니다. 다시 로그인 해주세요.';
      return;
    }
    const res = await getSystemLog(props.jobName, props.accessToken);
    console.log(res);
    let data = res;
    if (typeof res === 'string') {
      try {
        data = JSON.parse(res);
      } catch {
        // 문자열 그대로인 경우, 단일 메시지로 표시
        jobEvents.value = [
          {
            type: 'Info',
            reason: 'RawLog',
            age: '',
            from: '',
            message: res,
          },
        ];
        return;
      }
    }

    // data가 바로 배열인 경우 (질문에서 주신 예시)
    if (Array.isArray(data)) {
      jobEvents.value = data.map((e) => ({
        type: e.type || '',
        reason: e.reason || '',
        // Python None이나 null 이 올 수 있으니 문자열로 안전하게 변환
        age: e.age == null ? '' : String(e.age),
        from: e.from == null ? '' : String(e.from),
        message: e.message || '',
      }));
      return;
    }

    // { events: [...] } 형태인 경우
    if (data && Array.isArray(data.events)) {
      jobEvents.value = data.events.map((e) => ({
        type: e.type || '',
        reason: e.reason || '',
        age: e.age == null ? '' : String(e.age),
        from: e.from == null ? '' : String(e.from),
        message: e.message || '',
      }));
      return;
    }

    if (data && typeof data.error === 'string') {
      if (res.status === 410){
        error.value = res.error;
      }
      error.value = data.error;
    } else {
      error.value = '알 수 없는 System Log 응답 형식입니다.';
    }
  } catch (e) {
    if (e.status == '410'){
        error.value = e.response.data.error
      }
      else{
        error.value = 'System Log 요청 중 오류가 발생했습니다.';
      }

  } finally {
    isLoading.value = false;
  }
}

async function loadLogs() {
  if (props.menuType === 'terminal') {
    await loadTerminalLog();
  } else if (props.menuType === 'system') {
    await loadSystemLog();
  }
}

onMounted(() => {
  loadLogs();
});

watch(
  () => [props.jobName, props.menuType],
  () => {
    loadLogs();
  }
);
</script>

<style scoped>
.job-log-overlay-panel {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(15, 23, 42, 0.32);
  padding: 20px 24px;
  min-width: 1200px;
  max-width: 1200px;
}

.job-log-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.job-log-title {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: #111827;
}

.job-log-close {
  background: transparent;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #6b7280;
}

.job-log-close:hover {
  color: #374151;
}

.job-log-body {
  font-size: 14px;
  color: #374151;
}

.job-log-hint {
  margin-top: 12px;
  font-size: 12px;
  color: #6b7280;
}

.job-log-status {
  margin: 12px 0;
  padding: 8px 10px;
  border-radius: 6px;
  font-size: 13px;
}

.job-log-status--loading {
  background: #eff6ff;
  color: #1d4ed8;
}

.job-log-status--error {
  background: #fef2f2;
  color: #b91c1c;
}

.job-log-content {
  margin-top: 8px;
}

.job-log-code-block {
  margin-top: 4px;
  max-height: 400px;
  overflow-y: auto;
  padding: 12px;
  border-radius: 8px;
  background: #020617;
  color: #e5e7eb;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 12px;
  line-height: 1.5;
  white-space: pre-wrap; /* \n 줄바꿈 유지 */
  word-break: break-word;
}

.system-log-empty {
  margin-top: 8px;
  padding: 10px 12px;
  border-radius: 6px;
  background: #f3f4f6;
  color: #4b5563;
  font-size: 13px;
}

.job-log-events-wrapper {
  margin-top: 4px;
  max-height: 400px;
  overflow-y: auto;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.system-log-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

.system-log-table thead {
  background: #f9fafb;
  position: sticky;
  top: 0;
  z-index: 1;
}

.system-log-table th,
.system-log-table td {
  padding: 6px 8px;
  border-bottom: 1px solid #e5e7eb;
  text-align: left;
}

.system-log-message {
  white-space: pre-wrap;
  word-break: break-word;
}
</style>