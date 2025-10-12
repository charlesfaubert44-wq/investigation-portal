import { createAuth0 } from '@auth0/auth0-vue'

export default defineNuxtPlugin((nuxtApp) => {
  const config = useRuntimeConfig()
  
  // Using the Auth0 credentials from the original client
  const auth0 = createAuth0({
    domain: 'dev-o05e1b87irncothe.ca.auth0.com',
    clientId: 'SuZaMg7UykFXNuSLFNUYoCxlEWTxiAQD',
    authorizationParams: {
      redirect_uri: typeof window !== 'undefined' ? window.location.origin : ''
    }
  })

  nuxtApp.vueApp.use(auth0)
})
