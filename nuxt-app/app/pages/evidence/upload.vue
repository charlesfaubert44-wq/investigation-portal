<script setup lang="ts">
const router = useRouter()
const toast = useToast()

const state = reactive({
  investigationId: '',
  description: '',
  location: '',
  photos: null as FileList | null
})

const loading = ref(false)

async function onSubmit() {
  loading.value = true
  try {
    // In a real app, you'd use FormData for file upload
    const formData = new FormData()
    formData.append('investigationId', state.investigationId)
    formData.append('description', state.description)
    formData.append('location', state.location)
    
    if (state.photos) {
      Array.from(state.photos).forEach((file) => {
        formData.append('photos', file)
      })
    }

    await $fetch('/api/evidence', {
      method: 'POST',
      body: {
        investigationId: state.investigationId,
        description: state.description,
        location: state.location,
        fileCount: state.photos?.length || 0
      }
    })

    toast.add({
      title: 'Evidence Uploaded',
      description: 'Evidence has been uploaded successfully.',
      color: 'success'
    })

    router.push('/evidence')
  } catch (error) {
    toast.add({
      title: 'Error',
      description: 'Failed to upload evidence.',
      color: 'error'
    })
  } finally {
    loading.value = false
  }
}

function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  state.photos = target.files
}
</script>

<template>
  <UDashboardPanel id="upload-evidence">
    <template #header>
      <UDashboardNavbar title="Upload Evidence">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>

        <template #right>
          <UButton
            to="/evidence"
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
          <h2 class="text-xl font-bold text-blue-900 mb-6">Evidence Details</h2>
          
          <form @submit.prevent="onSubmit" class="space-y-6">
            <UFormField label="Investigation ID" name="investigationId" required>
              <UInput
                v-model="state.investigationId"
                placeholder="Enter investigation ID"
                size="lg"
              />
            </UFormField>

            <UFormField label="Description" name="description" required>
              <UTextarea
                v-model="state.description"
                placeholder="Describe the evidence"
                :rows="4"
              />
            </UFormField>

            <UFormField label="Location" name="location" required>
              <UInput
                v-model="state.location"
                placeholder="Enter location where evidence was collected"
                size="lg"
              />
            </UFormField>

            <UFormField label="Upload Photos/Documents" name="photos">
              <div class="space-y-2">
                <input
                  type="file"
                  multiple
                  accept="image/*,.pdf,.doc,.docx"
                  @change="handleFileChange"
                  class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                />
                <p class="text-xs text-gray-500">
                  Upload images, PDFs, or documents. Multiple files allowed.
                </p>
              </div>
            </UFormField>

            <div class="flex gap-3 pt-4">
              <UButton
                type="submit"
                color="primary"
                size="lg"
                :loading="loading"
              >
                Upload Evidence
              </UButton>
              <UButton
                type="button"
                color="neutral"
                variant="outline"
                size="lg"
                @click="router.push('/evidence')"
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
