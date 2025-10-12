<script setup lang="ts">
interface LegislationDoc {
  id: number
  title: string
  category: string
  jurisdiction: string
  url: string
}

const { data: legislation } = await useAsyncData<LegislationDoc[]>('legislation', () => 
  $fetch('/api/legislation')
)

const searchQuery = ref('')

const filteredLegislation = computed(() => {
  if (!searchQuery.value) return legislation.value || []
  
  const query = searchQuery.value.toLowerCase()
  return legislation.value?.filter(doc => 
    doc.title.toLowerCase().includes(query) ||
    doc.category.toLowerCase().includes(query) ||
    doc.jurisdiction.toLowerCase().includes(query)
  ) || []
})

const categoryColors: Record<string, string> = {
  'Compensation': 'blue',
  'Safety': 'green',
  'Mining': 'orange'
}
</script>

<template>
  <UDashboardPanel id="legislation">
    <template #header>
      <UDashboardNavbar title="Legislation Library">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>
      </UDashboardNavbar>

      <UDashboardToolbar>
        <template #left>
          <UInput
            v-model="searchQuery"
            icon="i-lucide-search"
            placeholder="Search legislation..."
            class="min-w-[300px]"
          />
        </template>
      </UDashboardToolbar>
    </template>

    <template #body>
      <div class="space-y-6">
        <div>
          <h2 class="text-xl font-bold text-blue-900 mb-4">Available Documents</h2>
          <UPageGrid class="lg:grid-cols-3 gap-4">
            <UPageCard
              v-for="doc in filteredLegislation"
              :key="doc.id"
              :title="doc.title"
              icon="i-lucide-book-open"
              :to="doc.url"
              target="_blank"
              variant="subtle"
              :ui="{ icon: 'text-blue-600' }"
            >
              <template #description>
                <div class="space-y-2">
                  <div class="flex gap-2">
                    <UBadge 
                      :color="categoryColors[doc.category] || 'gray'" 
                      variant="subtle"
                    >
                      {{ doc.category }}
                    </UBadge>
                    <UBadge color="neutral" variant="subtle">
                      {{ doc.jurisdiction }}
                    </UBadge>
                  </div>
                  <div class="flex items-center gap-2 text-sm text-blue-600">
                    <UIcon name="i-lucide-external-link" class="size-4" />
                    <span>View Document</span>
                  </div>
                </div>
              </template>
            </UPageCard>
          </UPageGrid>

          <div v-if="filteredLegislation.length === 0" class="text-center py-12">
            <UIcon name="i-lucide-search-x" class="size-12 text-gray-400 mx-auto mb-4" />
            <p class="text-gray-500">No legislation documents found.</p>
          </div>
        </div>
      </div>
    </template>
  </UDashboardPanel>
</template>
