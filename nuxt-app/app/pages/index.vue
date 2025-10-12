<script setup lang="ts">
import type { DropdownMenuItem } from '@nuxt/ui'

const { isNotificationsSlideoverOpen } = useDashboard()

const items = [[{
  label: 'New Investigation',
  icon: 'i-lucide-folder-plus',
  to: '/investigations/new'
}, {
  label: 'Upload Evidence',
  icon: 'i-lucide-upload',
  to: '/evidence/upload'
}]] satisfies DropdownMenuItem[][]
</script>

<template>
  <UDashboardPanel id="home">
    <template #header>
      <UDashboardNavbar title="Dashboard" :ui="{ right: 'gap-3' }">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>

        <template #right>
          <UTooltip text="Notifications" :shortcuts="['N']">
            <UButton
              color="neutral"
              variant="ghost"
              square
              @click="isNotificationsSlideoverOpen = true"
            >
              <UChip color="error" inset>
                <UIcon name="i-lucide-bell" class="size-5 shrink-0" />
              </UChip>
            </UButton>
          </UTooltip>

          <UDropdownMenu :items="items">
            <UButton icon="i-lucide-plus" size="md" class="rounded-full" color="primary" />
          </UDropdownMenu>
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <div class="space-y-8">
        <section>
          <h2 class="text-2xl font-bold text-blue-900 mb-4">Dashboard Summary</h2>
          <DashboardStats />
        </section>

        <section>
          <h2 class="text-xl font-bold text-blue-900 mb-4">Quick Actions</h2>
          <UPageGrid class="lg:grid-cols-2 gap-4">
            <UPageCard
              title="Create Investigation"
              description="Start a new investigation case"
              icon="i-lucide-folder-plus"
              to="/investigations/new"
              :ui="{ icon: 'text-blue-600' }"
            />
            <UPageCard
              title="Upload Evidence"
              description="Add evidence to existing cases"
              icon="i-lucide-upload"
              to="/evidence/upload"
              :ui="{ icon: 'text-blue-600' }"
            />
            <UPageCard
              title="View Legislation"
              description="Access legislation library"
              icon="i-lucide-book-open"
              to="/legislation"
              :ui="{ icon: 'text-blue-600' }"
            />
            <UPageCard
              title="Generate Reports"
              description="Create investigation reports"
              icon="i-lucide-file-text"
              to="/reports"
              :ui="{ icon: 'text-blue-600' }"
            />
          </UPageGrid>
        </section>
      </div>
    </template>
  </UDashboardPanel>
</template>
