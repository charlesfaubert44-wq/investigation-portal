<script setup lang="ts">
interface Investigation {
  id: number
  title: string
  description: string
  status: string
  deadline: string
  createdAt: string
}

const { data: investigations, refresh } = await useAsyncData<Investigation[]>('investigations', () => 
  $fetch('/api/investigations')
)

const columns = [{
  key: 'id',
  label: 'ID'
}, {
  key: 'title',
  label: 'Title'
}, {
  key: 'status',
  label: 'Status'
}, {
  key: 'deadline',
  label: 'Deadline'
}, {
  key: 'actions',
  label: 'Actions'
}]
</script>

<template>
  <UDashboardPanel id="investigations">
    <template #header>
      <UDashboardNavbar title="Investigations">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>

        <template #right>
          <UButton
            to="/investigations/new"
            icon="i-lucide-plus"
            color="primary"
          >
            New Investigation
          </UButton>
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <div class="space-y-6">
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-bold text-blue-900 mb-4">Active Investigations</h2>
          
          <UTable
            :columns="columns"
            :rows="investigations || []"
            :ui="{ wrapper: 'overflow-x-auto' }"
          >
            <template #status-data="{ row }">
              <UBadge
                :color="row.status === 'Active' ? 'blue' : row.status === 'Under Review' ? 'yellow' : 'gray'"
                variant="subtle"
              >
                {{ row.status }}
              </UBadge>
            </template>

            <template #actions-data="{ row }">
              <div class="flex gap-2">
                <UButton
                  icon="i-lucide-eye"
                  size="xs"
                  color="neutral"
                  variant="ghost"
                  :to="`/investigations/${row.id}`"
                >
                  View
                </UButton>
                <UButton
                  icon="i-lucide-edit"
                  size="xs"
                  color="neutral"
                  variant="ghost"
                >
                  Edit
                </UButton>
              </div>
            </template>
          </UTable>
        </div>
      </div>
    </template>
  </UDashboardPanel>
</template>
