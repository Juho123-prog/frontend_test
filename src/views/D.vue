<template>
  <vue-finder 
    id="my_vuefinder"
    :driver="driver"
  />
</template>

<script setup>
import { RemoteDriver } from 'vuefinder';

const driver = new RemoteDriver({
  baseURL: 'https://autox.dreamai.kr/vuefinder_api/?additionalParam1=yes&q=index&adapter=lab-aimed_directory&vf=1'
})
</script>
