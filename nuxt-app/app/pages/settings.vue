<script setup lang="ts">
const state = reactive({
  name: 'WSCC User',
  email: 'user@wscc.nt.ca',
  role: 'Investigator',
  notifications: true,
  emailAlerts: true
})

const toast = useToast()

function saveSettings() {
  toast.add({
    title: 'Settings Saved',
    description: 'Your settings have been updated successfully.',
    color: 'success'
  })
}
</script>

<template>
  <UDashboardPanel id="settings">
    <template #header>
      <UDashboardNavbar title="Settings">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <div class="max-w-3xl mx-auto space-y-6">
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-bold text-blue-900 mb-6">Profile Settings</h2>
          
          <form @submit.prevent="saveSettings" class="space-y-6">
            <UFormField label="Name" name="name">
              <UInput v-model="state.name" size="lg" />
            </UFormField>

            <UFormField label="Email" name="email">
              <UInput v-model="state.email" type="email" size="lg" disabled />
            </UFormField>

            <UFormField label="Role" name="role">
              <UInput v-model="state.role" size="lg" disabled />
            </UFormField>

            <div class="pt-4 border-t">
              <h3 class="text-lg font-semibold text-blue-900 mb-4">Notifications</h3>
              
              <div class="space-y-4">
                <UFormField label="Enable Notifications" name="notifications">
                  <UToggle v-model="state.notifications" />
                </UFormField>

                <UFormField label="Email Alerts" name="emailAlerts">
                  <UToggle v-model="state.emailAlerts" />
                </UFormField>
              </div>
            </div>

            <div class="flex gap-3 pt-4">
              <UButton type="submit" color="primary" size="lg">
                Save Changes
              </UButton>
            </div>
          </form>
        </div>
      </div>
    </template>
  </UDashboardPanel>
</template>
