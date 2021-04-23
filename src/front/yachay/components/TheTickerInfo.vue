<template>
  <div>
    <template v-if="!checkIfTickerIsEmpty">
      <table class="min-w-full table-auto">
        <thead class="justify-between">
        <tr class="bg-gray-800">
          <th class="px-16 py-2">
            <span class="text-gray-300">Symbol</span>
          </th>
          <th class="px-16 py-2">
            <span class="text-gray-300">Company</span>
          </th>
          <th class="px-16 py-2">
            <span class="text-gray-300">Primary Market</span>
          </th>

          <th class="px-16 py-2">
            <span class="text-gray-300">Price</span>
          </th>

          <th class="px-16 py-2">
            <span class="text-gray-300">Validation Time</span>
          </th>

          <th class="px-16 py-2">
            <span class="text-gray-300">Actions</span>
          </th>
        </tr>
        </thead>
        <tbody class="bg-gray-200">
        <tr class="bg-white border-4 border-gray-200">
          <td class="px-16 py-2 flex flex-row items-center">
            {{ this.ticker.symbol }}
          </td>
          <td class="px-16 py-2">
            {{ ticker.company_name }}
          </td>
          <td class="px-16 py-2">
            {{ ticker.primary_exchange }}
          </td>
          <td class="px-16 py-2">
            {{ ticker.local_price }}
          </td>

          <td class="px-16 py-2">
            <span>{{ ticker.validation_time }}</span>
          </td>
          <td class="px-16 py-2">
            <button
              class="bg-indigo-500 text-white px-4 py-2 border rounded-md hover:bg-white hover:border-indigo-500 hover:text-black ">
              Buy
            </button>
          </td>
        </tr>
        </tbody>
      </table>
    </template>
    <template v-else>
      <h4>{{ errorMessage }}</h4>
    </template>
  </div>
</template>

<script>
export default {
  name: "TheTickerInfo",
  computed: {
    ticker: {
      get() {
        return this.$store.state.stock.ticker
      },
      set(value) {
        this.$store.commit('stock/ticker', value)
      }
    },
    errorMessage: {
      get() {
        return this.$store.state.stock.errorMessage
      },
      set(value) {
        this.$store.commit('stock/errorMessage', value)
      }
    },
    checkIfTickerIsEmpty() {
      return Object.entries(this.ticker).length === 0
    }
  },
}
</script>
