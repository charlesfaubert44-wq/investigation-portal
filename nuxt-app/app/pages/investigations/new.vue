<script setup lang="ts">
const router = useRouter()
const toast = useToast()

const state = reactive({
  title: '',
  description: '',
  status: 'Active',
  deadline: ''
})

const loading = ref(false)

const statusOptions = [
  { label: 'Active', value: 'Active' },
  { label: 'Under Review', value: 'Under Review' },
  { label: 'Pending', value: 'Pending' },
  { label: 'Closed', value: 'Closed' }
]

async function onSubmit() {
  loading.value = true
  try {
    const response = await $fetch('/api/investigations', {
      method: 'POST',
      body: state
    })

    toast.add({
      title: 'Investigation Created',
      description: 'The investigation has been created successfully.',
      color: 'success'
    })

    router.push('/investigations')
  } catch (error) {
    toast.add({
      title: 'Error',
      description: 'Failed to create investigation.',
      color: 'error'
    })
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <UDashboardPanel id="new-investigation">
    <template #header>
      <UDashboardNavbar title="Create New Investigation">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>

        <template #right>
          <UButton
            to="/investigations"
            icon="i-lucide-arrow-left"
            color="neutral"
            variant="ghost"
          >
            Back
          </UButton>
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <div class="max-w-3xl mx-auto">
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-bold text-blue-900 mb-6">Investigation Details</h2>
          
          <form @submit.prevent="onSubmit" class="space-y-6">
            <UFormField label="Title" name="title" required>
              <UInput
                v-model="state.title"
                placeholder="Enter investigation title"
                size="lg"
              />
            </UFormField>

            <UFormField label="Description" name="description" required>
              <UTextarea
                v-model="state.description"
                placeholder="Enter investigation description"
                :rows="4"
              />
            </UFormField>

            <UFormField label="Status" name="status" required>
              <USelectMenu
                v-model="state.status"
                :options="statusOptions"
                value-key="value"
                option-label="label"
              />
            </UFormField>

            <UFormField label="Deadline" name="deadline" required>
              <UInput
                v-model="state.deadline"
                type="date"
                size="lg"
              />
            </UFormField>

            <div class="flex gap-3 pt-4">
              <UButton
                type="submit"
                color="primary"
                size="lg"
                :loading="loading"
              >
                Create Investigation
              </UButton>
              <UButton
                type="button"
                color="neutral"
                variant="outline"
                size="lg"
                @click="router.push('/investigations')"
              >
                Cancel
              </UButton>
            </div>
          </form>
        </div>
      </div>
    </template>
  </UDashboardPanel>
</template>
