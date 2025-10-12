<script setup lang="ts">
interface Stat {
  title: string
  icon: string
  value: string | number
  color?: string
}

const { data: stats } = await useAsyncData<Stat[]>('dashboard-stats', async () => {
  const response = await $fetch('/api/dashboard/summary')
  return [
    {
      title: 'Total Active Investigations',
      icon: 'i-lucide-folder-open',
      value: response.total,
      color: 'blue'
    },
    {
      title: 'Charge Deadlines This Month',
      icon: 'i-lucide-calendar-clock',
      value: response.deadlines,
      color: 'yellow'
    },
    {
      title: 'High Risk Cases',
      icon: 'i-lucide-alert-triangle',
      value: response.highRisk,
      color: 'red'
    }
  ]
}, {
  default: () => []
})
</script>

<template>
  <UPageGrid class="lg:grid-cols-3 gap-4 sm:gap-6">
    <UPageCard
      v-for="(stat, index) in stats"
      :key="index"
      :icon="stat.icon"
      :title="stat.title"
      variant="subtle"
      :ui="{
        container: 'gap-y-2',
        wrapper: 'items-start',
        leading: `p-3 rounded-full ${stat.color === 'blue' ? 'bg-blue-100 ring ring-inset ring-blue-200' : stat.color === 'yellow' ? 'bg-yellow-100 ring ring-inset ring-yellow-200' : 'bg-red-100 ring ring-inset ring-red-200'} flex-col`,
        title: 'font-normal text-muted text-xs uppercase'
      }"
      class="hover:shadow-lg transition-shadow"
    >
      <span :class="`text-3xl font-bold ${stat.color === 'blue' ? 'text-blue-700' : stat.color === 'yellow' ? 'text-yellow-600' : 'text-red-600'}`">
        {{ stat.value }}
      </span>
    </UPageCard>
  </UPageGrid>
</template>
