<script setup lang="ts">
import type { DropdownMenuItem } from '@nuxt/ui'

defineProps<{
  collapsed?: boolean
}>()

const auth = useAuth()

const items = [[{
  label: 'Profile',
  icon: 'i-lucide-user',
  to: '/settings'
}, {
  label: 'Settings',
  icon: 'i-lucide-settings',
  to: '/settings'
}], [{
  label: 'Sign out',
  icon: 'i-lucide-log-out',
  onClick: () => {
    if (import.meta.client) {
      auth.logout({ logoutParams: { returnTo: window.location.origin } })
    }
  }
}]] satisfies DropdownMenuItem[][]

const userName = computed(() => {
  if (import.meta.client && auth.user?.value) {
    return auth.user.value.name || auth.user.value.email || 'WSCC User'
  }
  return 'WSCC User'
})
</script>

<template>
  <UDropdownMenu :items="items" :ui="{ leading: 'size-4' }">
    <UButton
      color="neutral"
      variant="ghost"
      :class="{ 'px-2': collapsed, 'justify-start': !collapsed }"
      class="w-full"
    >
      <UAvatar
        alt="User"
        size="xs"
      />

      <span v-if="!collapsed" class="truncate">{{ userName }}</span>

      <UIcon name="i-lucide-ellipsis-vertical" class="size-5 ms-auto" />
    </UButton>
  </UDropdownMenu>
</template>
