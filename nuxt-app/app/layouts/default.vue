<script setup lang="ts">
import type { NavigationMenuItem } from '@nuxt/ui'

const route = useRoute()
const open = ref(false)

const links = [[{
  label: 'Dashboard',
  icon: 'i-lucide-home',
  to: '/',
  onSelect: () => {
    open.value = false
  }
}, {
  label: 'Investigations',
  icon: 'i-lucide-folder-search',
  to: '/investigations',
  onSelect: () => {
    open.value = false
  }
}, {
  label: 'Evidence',
  icon: 'i-lucide-files',
  to: '/evidence',
  onSelect: () => {
    open.value = false
  }
}, {
  label: 'Legislation',
  icon: 'i-lucide-book-open',
  to: '/legislation',
  onSelect: () => {
    open.value = false
  }
}, {
  label: 'Reports',
  icon: 'i-lucide-file-text',
  to: '/reports',
  onSelect: () => {
    open.value = false
  }
}], [{
  label: 'Settings',
  icon: 'i-lucide-settings',
  to: '/settings',
  onSelect: () => {
    open.value = false
  }
}]] satisfies NavigationMenuItem[][]

const groups = computed(() => [{
  id: 'links',
  label: 'Go to',
  items: links.flat()
}])
</script>

<template>
  <UDashboardGroup unit="rem">
    <UDashboardSidebar
      id="default"
      v-model:open="open"
      collapsible
      resizable
      class="bg-blue-950/95"
      :ui="{ footer: 'lg:border-t lg:border-blue-800' }"
    >
      <template #header="{ collapsed }">
        <UButton
          color="primary"
          variant="ghost"
          :class="{ 'px-2': collapsed }"
          class="w-full justify-start mb-2"
        >
          <div v-if="!collapsed" class="flex flex-col items-start">
            <span class="font-bold text-lg text-white">WSCC</span>
            <span class="text-xs text-blue-200">Investigation Portal</span>
          </div>
          <UIcon v-else name="i-lucide-shield-check" class="size-6 text-white" />
        </UButton>
      </template>

      <template #default="{ collapsed }">
        <UDashboardSearchButton :collapsed="collapsed" class="bg-blue-900/50 ring-blue-700" />

        <UNavigationMenu
          :collapsed="collapsed"
          :items="links[0]"
          orientation="vertical"
          tooltip
          popover
          class="text-blue-100"
        />

        <UNavigationMenu
          :collapsed="collapsed"
          :items="links[1]"
          orientation="vertical"
          tooltip
          class="mt-auto text-blue-100"
        />
      </template>

      <template #footer="{ collapsed }">
        <UserMenu :collapsed="collapsed" />
      </template>
    </UDashboardSidebar>

    <UDashboardSearch :groups="groups" />

    <slot />

    <NotificationsSlideover />
  </UDashboardGroup>
</template>
