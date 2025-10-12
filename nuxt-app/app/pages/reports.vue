<script setup lang="ts">
const toast = useToast()

const reportTypes = [
  {
    id: 'summary',
    title: 'Investigation Summary Report',
    description: 'Generate a comprehensive summary of an investigation',
    icon: 'i-lucide-file-text'
  },
  {
    id: 'evidence',
    title: 'Evidence Report',
    description: 'Create a detailed report of all evidence collected',
    icon: 'i-lucide-folder'
  },
  {
    id: 'timeline',
    title: 'Timeline Report',
    description: 'Generate a chronological timeline of investigation events',
    icon: 'i-lucide-calendar'
  },
  {
    id: 'compliance',
    title: 'Compliance Report',
    description: 'Check investigation compliance with regulations',
    icon: 'i-lucide-shield-check'
  }
]

function generateReport(type: string) {
  toast.add({
    title: 'Generating Report',
    description: `Your ${type} report is being generated...`,
    color: 'info'
  })
}
</script>

<template>
  <UDashboardPanel id="reports">
    <template #header>
      <UDashboardNavbar title="Reports">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <div class="space-y-6">
        <div>
          <h2 class="text-xl font-bold text-blue-900 mb-4">Generate Reports</h2>
          <UPageGrid class="lg:grid-cols-2 gap-4">
            <UPageCard
              v-for="report in reportTypes"
              :key="report.id"
              :title="report.title"
              :description="report.description"
              :icon="report.icon"
              variant="subtle"
              :ui="{ icon: 'text-blue-600' }"
              @click="generateReport(report.title)"
              class="cursor-pointer hover:shadow-lg transition-shadow"
            >
              <template #footer>
                <UButton
                  color="primary"
                  variant="ghost"
                  size="xs"
                >
                  Generate
                </UButton>
              </template>
            </UPageCard>
          </UPageGrid>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-bold text-blue-900 mb-4">Recent Reports</h2>
          <div class="text-center py-8 text-gray-500">
            <UIcon name="i-lucide-file-x" class="size-12 mx-auto mb-2" />
            <p>No recent reports available.</p>
          </div>
        </div>
      </div>
    </template>
  </UDashboardPanel>
</template>
