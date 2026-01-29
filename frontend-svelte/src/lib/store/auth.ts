import { writable } from 'svelte/store'
import { authAPI } from '$lib/services/api'

export interface User {
  id: number
  email: string
  role: string
  [key: string]: any
}

export interface AuthState {
  user: User | null
  token: string | null
  loading: boolean
  error: string | null
  isAuthenticated: boolean
  isAdmin: boolean
}

function createAuthStore() {
  const initialState: AuthState = {
    user: null,
    token: null,
    loading: false,
    error: null,
    isAuthenticated: false,
    isAdmin: false
  }

  const { subscribe, set, update } = writable<AuthState>(initialState)

  function setAuth(authToken: string, userData: User) {
    update(() => ({
      user: userData,
      token: authToken,
      loading: false,
      error: null,
      isAuthenticated: true,
      isAdmin: userData.role === 'ADMINISTRATEUR'
    }))

    localStorage.setItem('token', authToken)
    localStorage.setItem('user', JSON.stringify(userData))
  }

  function clearAuth() {
    set(initialState)
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  function checkAuth() {
    const savedToken = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')

    if (savedToken && savedUser) {
      const userData = JSON.parse(savedUser)
      set({
        user: userData,
        token: savedToken,
        loading: false,
        error: null,
        isAuthenticated: true,
        isAdmin: userData.role === 'ADMINISTRATEUR'
      })
    }
  }

  async function login(email: string, password: string) {
    update(state => ({ ...state, loading: true, error: null }))

    try {
      const response = await authAPI.login(email, password)
      const { access_token, user: userData } = response.data

      setAuth(access_token, userData)
      return { success: true }
    } catch (err: any) {
      const errorData = err.response?.data?.detail
      let message = 'Erreur de connexion'

      if (typeof errorData === 'object') {
        message = errorData.message || message
        update(state => ({ ...state, error: message, loading: false }))
        return {
          success: false,
          error: message,
          attemptsRemaining: errorData.attempts_remaining,
          minutesRemaining: errorData.minutes_remaining
        }
      } else {
        message = errorData || message
        update(state => ({ ...state, error: message, loading: false }))
        return { success: false, error: message }
      }
    }
  }

  async function logout() {
    try {
      await authAPI.logout()
    } catch (err) {
      console.error('Erreur lors de la déconnexion:', err)
    } finally {
      clearAuth()
    }
  }

  return {
    subscribe,
    setAuth,
    clearAuth,
    checkAuth,
    login,
    logout
  }
}

export const authStore = createAuthStore()
