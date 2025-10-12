<script setup lang="ts">
interface Evidence {
  id: number
  investigationId: string
  description: string
  location: string
  uploadedAt: string
  fileCount: number
}

const { data: evidenceList } = await useAsyncData<Evidence[]>('evidence', async () => {
  // Mock data for now
  return [
    {
      id: 1,
      investigationId: '1',
      description: 'Safety equipment photos',
      location: 'Mine Site A',
      uploadedAt: '2025-10-10',
      fileCount: 3
    },
    {
      id: 2,
      investigationId: '2',
      description: 'Incident report documents',
      location: 'Office Building',
      uploadedAt: '2025-10-08',
      fileCount: 5
    }
  ]
})

const columns = [{
  key: 'investigationId',
  label: 'Investigation ID'
}, {
  key: 'description',
  label: 'Description'
}, {
  key: 'location',
  label: 'Location'
}, {
  key: 'fileCount',
  label: 'Files'
}, {
  key: 'uploadedAt',
  label: 'Uploaded'
}, {
  key: 'actions',
  label: 'Actions'
}]
</script>

<template>
  <UDashboardPanel id="evidence">
    <template #header>
      <UDashboardNavbar title="Evidence Manager">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>

        <template #right>
          <UButton
            to="/evidence/upload"
            icon="i-lucide-upload"
            color="primary"
          >
            Upload Evidence
          </UButton>
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <div class="space-y-6">
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-bold text-blue-900 mb-4">Evidence Records</h2>
          
          <UTable
            :columns="columns"
            :rows="evidenceList || []"
            :ui="{ wrapper: 'overflow-x-auto' }"
          >
            <template #fileCount-data="{ row }">
              <UBadge color="blue" variant="subtle">
                {{ row.fileCount }} files
              </UBadge>
            </template>

            <template #actions-data="{ row }">
              <div class="flex gap-2">
                <UButton
                  icon="i-lucide-eye"
                  size="xs"
                  color="neutral"
                  variant="ghost"
                >
                  View
                </UButton>
                <UButton
                  icon="i-lucide-download"
                  size="xs"
                  color="neutral"
                  variant="ghost"
                >
                  Download
                </UButton>
              </div>
            </template>
          </UTable>
        </div>
      </div>
    </template>
  </UDashboardPanel>
</template>
