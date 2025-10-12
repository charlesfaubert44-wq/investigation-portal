export default defineNuxtRouteMiddleware((to, from) => {
  // Skip auth check on client-side during initial load
  // Auth0 will handle the redirect if needed
  if (import.meta.client) {
    const auth = useAuth()
    
    // Allow navigation, Auth0 plugin will handle authentication
    return
  }
})
