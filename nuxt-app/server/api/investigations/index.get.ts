export default defineEventHandler(async (event) => {
  // This would connect to your existing backend or database
  // For now, returning mock data
  return [
    {
      id: 1,
      title: 'Workplace Safety Incident - Mine Site A',
      description: 'Investigation into safety protocol breach',
      status: 'Active',
      deadline: '2025-11-15',
      createdAt: '2025-10-01'
    },
    {
      id: 2,
      title: 'Compensation Claim Review',
      description: 'Worker compensation claim assessment',
      status: 'Under Review',
      deadline: '2025-10-30',
      createdAt: '2025-09-15'
    }
  ]
})
