import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    isLoading: false,
    error: null,
    notification: null
  }),

  actions: {
    setLoading(value) {
      this.isLoading = value
    },

    setError(error) {
      this.error = error
      if (error) {
        setTimeout(() => {
          this.error = null
        }, 5000)
      }
    },

    setNotification(message, type = 'info') {
      this.notification = { message, type }
      setTimeout(() => {
        this.notification = null
      }, 5000)
    }
  }
})
