import { useAuth0 } from '@auth0/auth0-vue'

export const useAuth = () => {
  if (import.meta.client) {
    return useAuth0()
  }
  
  // Server-side fallback
  return {
    isLoading: ref(false),
    isAuthenticated: ref(false),
    user: ref(null),
    loginWithRedirect: () => {},
    logout: () => {},
    getAccessTokenSilently: () => Promise.resolve('')
  }
}
