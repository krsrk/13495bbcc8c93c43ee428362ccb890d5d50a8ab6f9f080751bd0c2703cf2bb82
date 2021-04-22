<template>
  <div class="container mx-auto px-4">
    <TheSearchBox />
    <TheTickerInfo />
  </div>
</template>

<script>
import TheSearchBox from "../components/TheSearchBox"
import TheTickerInfo from "../components/TheTickerInfo"

export default {
  components: {
    TheSearchBox,
    TheTickerInfo,
  }
}
</script>
