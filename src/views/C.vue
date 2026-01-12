<template>
  <div class="box">
    <h2>Backend API Response</h2>

    <button @click="callApi" :disabled="loading">Call Backend API</button>
    <button @click="fetchVuefinder" :disabled="loading">Call Vuefinder API</button>

    <pre v-if="loading">Loading...</pre>
    <pre v-else-if="error" class="error">{{ error }}</pre>
    <pre v-else-if="result">{{ result }}</pre>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const result = ref(null)
const error = ref(null)
const loading = ref(false)

// 예시 access token (실제 값으로 교체)
const accessToken = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJFS3hOcmVWbnZSdXIycVFyR0dyWkR5MVJUd0RDUmVxSkVGM2RkMEdjZFVzIn0.eyJleHAiOjE3NjgxOTM4NDYsImlhdCI6MTc2ODE5MjA0NiwiYXV0aF90aW1lIjoxNzY4MTkyMDQ2LCJqdGkiOiI5OWQ2Y2VjMS1kOTdjLTQwMWMtYWEwNC1lNDI0OTIyNDhkNGQiLCJpc3MiOiJodHRwczovL2F1dGgubW9iaWxleC5rci9yZWFsbXMvbW9iaWxleCIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiIxOGIxZWZlZS1mZmFlLTQxZTktYmJjMS02NWFlYjllNWFiOWMiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJhdXRveCIsIm5vbmNlIjoiOGY1NmY2Y2MtNGM4OS00NTgyLTk2YTMtYjA2ODc0MzVlZmNhIiwic2Vzc2lvbl9zdGF0ZSI6IjVjMjVjMjI1LTE2MjYtNGRjOS04MzRjLWMyYTAzODNhM2ZjNiIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly9hdXRveC5kcmVhbWFpLmtyIiwiaHR0cDovL2F1dG94LmRyZWFtYWkua3IiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLW1vYmlsZXgiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBlbWFpbCBncm91cHMgcHJvZmlsZSIsInNpZCI6IjVjMjVjMjI1LTE2MjYtNGRjOS04MzRjLWMyYTAzODNhM2ZjNiIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwibmFtZSI6Imp1aG8gcGFyayIsImdyb3VwcyI6WyJsYWItYWltZWQiXSwicHJlZmVycmVkX3VzZXJuYW1lIjoianVob3BhcmsiLCJnaXZlbl9uYW1lIjoianVobyIsImZhbWlseV9uYW1lIjoicGFyayIsImVtYWlsIjoianVob2JhZzEyQGdtYWlsLmNvbSJ9.R3rG0glsyyi2OVyQWV39dsrJ4ZcaQhy2dTvna7dlYcFjUuMkD7vujJzLCFxAZLah1HR2Js1UWrM0R5ZTMWWPZKoUnzRihfwBp04tK9k9HyKU7dGXhyT9L6lI9d0AaqZSmPuJVWUONLLSnZaMSN1smKT-i61rb1H3W6aVeh1En5svB4kZnMvbt2R7AijEyjgG-ZsfDlm_EYsW3z_tX6kDQN5ptfFq6l5qNInrkKftnmB0AbI3nHkjyt0UICq1GApAqFxMLxgmaArX9Rgr40tXv0zhr2NugCFGxjBykb0iNMQ0mdPiffS-quo4GpvvjEcLgUuIPHuyS7rxK5BQqpPkJA'

const callApi = async () => {
  loading.value = true
  error.value = null
  result.value = null

  try {
    document.cookie = 'additionalParam1=yes; path=/'
    document.cookie = 'q=index; path=/'
    document.cookie = 'adapter=lab-aimed_directory; path=/'
    document.cookie = 'vf=1; path=/'
    const res = await fetch('https://autox.dreamai.kr/backend_api/dashboard', {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
    })

    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`)
    }

    result.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

const fetchVuefinder = async () => {
  loading.value = true
  error.value = null
  result.value = null

  try {
    const query = buildVuefinderQuery()
    const url = `https://autox.dreamai.kr/vuefinder_api/?${query}`

    const res = await fetch(url, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
    })

    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`)
    }

    result.value = await res.json()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}


function buildVuefinderQuery() {
  const cookies = getCookies()

  const params = new URLSearchParams({
    additionalParam1: cookies.additionalParam1,
    q: cookies.q,
    adapter: cookies.adapter,
    vf: cookies.vf,
  })

  return params.toString()
}

function getCookies() {
  return document.cookie
    .split('; ')
    .reduce((acc, cur) => {
      const [key, value] = cur.split('=')
      acc[key] = decodeURIComponent(value)
      return acc
    }, {})
}


</script>

<style scoped>
.box {
  padding: 16px;
  font-family: monospace;
}

button {
  margin-bottom: 12px;
}

.error {
  color: #b42318;
}
</style>
