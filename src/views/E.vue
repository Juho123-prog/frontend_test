<template>
  <div class="page">
    <h2>API Request Tester</h2>

    <div class="form">
      <label>
        Method
        <select v-model="method">
          <option value="GET">GET</option>
          <option value="POST">POST</option>
        </select>
      </label>

      <label>
        Query Params (JSON)
        <textarea v-model="paramsText" placeholder='{"adapter":"lab-aimed_directory","vf":"1"}' />
      </label>

      <label v-if="method === 'POST'">
        Body (JSON)
        <textarea v-model="bodyText" placeholder='{"path":"lab-aimed_directory://"}' />
      </label>

      <button @click="sendRequest" :disabled="loading">
        {{ loading ? 'Sending...' : 'Send Request' }}
      </button>
    </div>

    <div class="response" v-if="response">
      <h3>Response</h3>
      <pre>{{ response }}</pre>
    </div>

    <div class="error" v-if="error">
      <h3>Error</h3>
      <pre>{{ error }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const method = ref('GET')
const paramsText = ref('{"adapter":"lab-aimed_directory","vf":"1"}')
const bodyText = ref('{}')

const response = ref(null)
const error = ref(null)
const loading = ref(false)

const sendRequest = async () => {
  response.value = null
  error.value = null
  loading.value = true

  try {
    const params = JSON.parse(paramsText.value || '{}')
    const body = JSON.parse(bodyText.value || '{}')

    const url = new URL('https://autox.dreamai.kr/juhotest')

    Object.entries(params).forEach(([k, v]) => {
      url.searchParams.append(k, v)
    })

    const res = await fetch(url.toString(), {
      method: method.value,
      headers: {
        'Content-Type': 'application/json',
      },
      body: method.value === 'POST' ? JSON.stringify(body) : undefined,
    })

    const text = await res.text()
    try {
      response.value = JSON.stringify(JSON.parse(text), null, 2)
    } catch {
      response.value = text
    }
  } catch (e) {
    error.value = e.toString()
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.page {
  max-width: 900px;
  margin: 40px auto;
  font-family: system-ui, sans-serif;
}

.form {
  display: grid;
  gap: 16px;
}

label {
  display: flex;
  flex-direction: column;
  font-weight: 600;
}

textarea {
  min-height: 100px;
  font-family: monospace;
}

button {
  width: 180px;
  padding: 8px;
  cursor: pointer;
}

.response, .error {
  margin-top: 24px;
}

pre {
  background: #111;
  color: #0f0;
  padding: 16px;
  overflow: auto;
}

.error pre {
  background: #300;
  color: #f88;
}
</style>
