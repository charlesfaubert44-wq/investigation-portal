export default defineEventHandler(async (event) => {
  // This would connect to your existing backend API
  // For now, returning the same data structure as the original
  return {
    total: 24,
    deadlines: 5,
    highRisk: 7
  }
})
