export const state = () => ({
  ticker: {},
  errorMessage: 'There is no quote for the moment.'
})

export const mutations = {
  ticker(state, value) {
    if (Object.entries(value).length !== 0) {
      let dateTime = value.local_last_update.split(' ')
      let formatTime = (dateTime.length === 2) ? value.local_last_update : value.local_last_update * 1000
      let date = new Date(formatTime)
      value.validation_time = date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds()
    }

    state.ticker = value
  },

  errorMessage(state, value) {
    state.errorMessage = value
  }
}

export const actions = {
  makeQuote: async (context, value) => {
    let response = await fetch('http://localhost:8889/quote/ticker/' + value)
    let data = await response.json()
    let response_message = (response.ok) ? '' : data.detail
    let commitData = (response.ok) ? data : {}

    context.commit('ticker', commitData)
    context.commit('errorMessage', response_message)
  },
}
