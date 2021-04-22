export const state = () => ({
  ticker: {},
})

export const mutations = {
  ticker(state, value) {
    let date = new Date(value.local_last_update * 1000)
    value.local_last_update = date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds()
    state.ticker = value
  },
}

export const actions = {
  makeQuote: async (context, value) => {
    let response = await fetch('http://localhost:8889/quote/ticker/' + value)
    let data = await response.json()

    context.commit('ticker', data)
  },
}
