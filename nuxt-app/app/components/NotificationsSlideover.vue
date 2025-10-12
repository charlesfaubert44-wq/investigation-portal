<script setup lang="ts">
const { isNotificationsSlideoverOpen } = useDashboard()

const notifications = ref([
  {
    id: 1,
    title: 'Investigation Deadline Approaching',
    description: 'Case #1 deadline is in 3 days',
    time: '2 hours ago',
    icon: 'i-lucide-alert-circle',
    color: 'yellow'
  },
  {
    id: 2,
    title: 'New Evidence Uploaded',
    description: 'Evidence added to Case #2',
    time: '5 hours ago',
    icon: 'i-lucide-file-plus',
    color: 'blue'
  },
  {
    id: 3,
    title: 'Report Generated',
    description: 'Summary report for Case #1 is ready',
    time: '1 day ago',
    icon: 'i-lucide-file-check',
    color: 'green'
  }
])
</script>

<template>
  <USlideover v-model:open="isNotificationsSlideoverOpen" title="Notifications">
    <div class="p-4 space-y-4">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        class="p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors cursor-pointer"
      >
        <div class="flex gap-3">
          <div 
            :class="`p-2 rounded-full ${notification.color === 'yellow' ? 'bg-yellow-100' : notification.color === 'blue' ? 'bg-blue-100' : 'bg-green-100'}`"
          >
            <UIcon 
              :name="notification.icon" 
              :class="`size-5 ${notification.color === 'yellow' ? 'text-yellow-600' : notification.color === 'blue' ? 'text-blue-600' : 'text-green-600'}`"
            />
          </div>
          <div class="flex-1">
            <h4 class="font-semibold text-sm text-gray-900">{{ notification.title }}</h4>
            <p class="text-sm text-gray-600 mt-1">{{ notification.description }}</p>
            <p class="text-xs text-gray-400 mt-2">{{ notification.time }}</p>
          </div>
        </div>
      </div>

      <div v-if="notifications.length === 0" class="text-center py-12">
        <UIcon name="i-lucide-bell-off" class="size-12 text-gray-400 mx-auto mb-2" />
        <p class="text-gray-500">No notifications</p>
      </div>
    </div>
  </USlideover>
</template>
