<template>
    <vue-finder
      id='my_vuefinder'
      :request="request"
      :max-file-size="maxFileSize"
    />
</template>

<script setup>
import {getCurrentInstance, ref} from 'vue';

const request = {
  // ----- CHANGE ME! -----
  // [REQUIRED] Url for development server endpoint
  // baseUrl: "http://localhost:8005",
  // baseUrl: "https://autox.dreamai.kr/vuefinder_api",
  baseUrl: "https://autox.dreamai.kr/vuefinder_api/",
  headers: { "X-ADDITIONAL-HEADER": 'yes' },
  params: { additionalParam1: 'yes' },
  body: { additionalBody1: ['yes'] },
  // And/or transform request callback
  transformRequest: req => {
    if (req.method === 'get') {
      req.params.vf = "1"
      req.params.adapter = "lab-aimed_directory"
      // req.params.adapter = "mansu" + "_directory"
    }
    return req;
  },
  // XSRF Token header name
  xsrfHeaderName: "CSRF-TOKEN",
}
const maxFileSize = ref("100000MB")
</script>
+