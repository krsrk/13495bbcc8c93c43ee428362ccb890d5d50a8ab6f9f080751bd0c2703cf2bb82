<template>
  <div class="m-4 flex">
    	<input
        v-model="inputTicker"
        class="rounded-l-lg p-4 border-t mr-0 border-b border-l text-gray-800 border-gray-200 bg-white"
        placeholder="Find & Quote The Ticker ..."/>
		<button
      @click="quoteClickHandler"
      class="px-8 rounded-r-lg bg-blue-400  text-gray-800 font-bold p-4 uppercase border-white border-t border-b border-r">
      Quote
    </button>
	</div>
</template>

<script>
export default {
  name: "TheSearchBox",
  data () {
    return {
      inputTicker: ''
    }
  },
  methods: {
    quoteClickHandler() {
      if (this.validateTickerSymbol()) {
        this.$store.dispatch('stock/makeQuote', this.inputTicker)
        this.inputTicker = ''
      } else {
        this.$store.commit('stock/errorMessage', 'Only numbers and letters with uppercase and no spaces')
      }
    },
    validateTickerSymbol() {
      let input = this.inputTicker
      let regExp =  /^[A-Z0-9]+$/i

      return regExp.test(input)
    }
  }
}
</script>
