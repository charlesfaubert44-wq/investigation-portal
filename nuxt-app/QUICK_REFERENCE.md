# Quick Reference Guide

## Common Tasks

### Running the Application

```bash
# Development mode (hot reload)
npm run dev

# Production build
npm run build

# Preview production
npm run preview

# Type checking
npm run typecheck
```

### Adding a New Page

1. Create file in `app/pages/`:
   ```vue
   <!-- app/pages/my-page.vue -->
   <script setup lang="ts">
   // Your logic here
   </script>

   <template>
     <UDashboardPanel id="my-page">
       <template #header>
         <UDashboardNavbar title="My Page">
           <template #leading>
             <UDashboardSidebarCollapse />
           </template>
         </UDashboardNavbar>
       </template>

       <template #body>
         <!-- Your content here -->
       </template>
     </UDashboardPanel>
   </template>
   ```

2. Add to navigation in `app/layouts/default.vue`:
   ```typescript
   {
     label: 'My Page',
     icon: 'i-lucide-star',
     to: '/my-page'
   }
   ```

### Adding a New API Route

Create file in `server/api/`:

```typescript
// server/api/my-endpoint.get.ts
export default defineEventHandler(async (event) => {
  // Your logic here
  return {
    data: 'Hello World'
  }
})

// POST example
// server/api/my-endpoint.post.ts
export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  // Process body
  return { success: true }
})
```

### Adding a New Component

```vue
<!-- app/components/MyComponent.vue -->
<script setup lang="ts">
// Props
interface Props {
  title: string
}
const props = defineProps<Props>()
</script>

<template>
  <div>
    <h3>{{ title }}</h3>
  </div>
</template>
```

Use it (auto-imported):
```vue
<MyComponent title="Hello" />
```

### Fetching Data

```typescript
// In a page or component
const { data, pending, error, refresh } = await useAsyncData('key', () => 
  $fetch('/api/endpoint')
)

// Or with useFetch
const { data } = await useFetch('/api/endpoint')
```

### Forms with Validation

```vue
<script setup lang="ts">
const state = reactive({
  name: '',
  email: ''
})

async function onSubmit() {
  try {
    await $fetch('/api/submit', {
      method: 'POST',
      body: state
    })
    toast.add({
      title: 'Success!',
      color: 'success'
    })
  } catch (error) {
    toast.add({
      title: 'Error',
      color: 'error'
    })
  }
}
</script>

<template>
  <form @submit.prevent="onSubmit">
    <UFormField label="Name" name="name" required>
      <UInput v-model="state.name" />
    </UFormField>
    
    <UButton type="submit">Submit</UButton>
  </form>
</template>
```

## Nuxt UI Components

### Common Components

```vue
<!-- Button -->
<UButton color="primary" size="lg">Click me</UButton>

<!-- Icon Button -->
<UButton icon="i-lucide-plus" square />

<!-- Input -->
<UInput v-model="value" placeholder="Enter text" />

<!-- Select -->
<USelectMenu v-model="selected" :options="options" />

<!-- Textarea -->
<UTextarea v-model="text" :rows="4" />

<!-- Badge -->
<UBadge color="blue" variant="subtle">Active</UBadge>

<!-- Table -->
<UTable :columns="columns" :rows="rows" />

<!-- Card -->
<UPageCard title="Title" description="Description" icon="i-lucide-star" />

<!-- Modal -->
<UModal v-model:open="isOpen" title="Modal Title">
  <!-- Content -->
</UModal>

<!-- Toast -->
<script setup>
const toast = useToast()
toast.add({
  title: 'Success!',
  description: 'Operation completed',
  color: 'success'
})
</script>
```

### Icons

Using Lucide icons (prefix with `i-lucide-`):

```vue
<UIcon name="i-lucide-home" />
<UIcon name="i-lucide-user" />
<UIcon name="i-lucide-settings" />
```

Browse all icons: https://lucide.dev/icons/

## State Management

### Reactive State

```typescript
// Local component state
const count = ref(0)
const user = reactive({ name: '', email: '' })

// Computed
const doubled = computed(() => count.value * 2)

// Watch
watch(() => count.value, (newVal) => {
  console.log('Count changed:', newVal)
})
```

### Shared State (Composable)

```typescript
// app/composables/useCounter.ts
export const useCounter = () => {
  const count = useState('counter', () => 0)
  
  function increment() {
    count.value++
  }
  
  return {
    count,
    increment
  }
}

// Use in any component
const { count, increment } = useCounter()
```

## Styling

### Tailwind Classes

```vue
<div class="flex items-center gap-4 p-6 bg-blue-50 rounded-lg">
  <!-- Content -->
</div>
```

### Custom CSS

Add to `app/assets/css/main.css`:

```css
.custom-class {
  /* Your styles */
}
```

### Scoped Styles

```vue
<style scoped>
.my-class {
  color: red;
}
</style>
```

## Navigation

### Programmatic Navigation

```typescript
const router = useRouter()

// Navigate
router.push('/investigations')

// With query params
router.push({ path: '/search', query: { q: 'test' } })

// Go back
router.back()
```

### Links

```vue
<!-- Using NuxtLink -->
<NuxtLink to="/investigations">View Investigations</NuxtLink>

<!-- Using UButton -->
<UButton to="/investigations">View</UButton>
```

## Environment Variables

Create `.env`:

```env
API_BASE_URL=http://localhost:3000
AUTH0_DOMAIN=your-domain.auth0.com
```

Access in code:

```typescript
const config = useRuntimeConfig()
console.log(config.public.apiBaseUrl)
```

Define in `nuxt.config.ts`:

```typescript
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.API_BASE_URL
    }
  }
})
```

## TypeScript

### Type Definitions

```typescript
// Define types
interface User {
  id: number
  name: string
  email: string
}

// Use in component
const user = ref<User | null>(null)

// Props
interface Props {
  title: string
  count?: number
}
const props = defineProps<Props>()

// Emit
interface Emits {
  (e: 'update', value: string): void
}
const emit = defineEmits<Emits>()
```

## Authentication

### Check Auth Status

```typescript
const auth = useAuth()

// Is authenticated
if (auth.isAuthenticated.value) {
  // User is logged in
}

// Get user
const user = auth.user.value

// Login
auth.loginWithRedirect()

// Logout
auth.logout({ logoutParams: { returnTo: window.location.origin } })
```

## Debugging

### Console Logging

```typescript
console.log('Debug:', value)
console.error('Error:', error)
```

### Vue Devtools

Install browser extension for Vue 3:
- Chrome/Edge: Vue.js devtools
- Firefox: Vue.js devtools

### Server Logs

Check terminal where `npm run dev` is running.

## Performance

### Lazy Load Components

```vue
<script setup>
const MyHeavyComponent = defineAsyncComponent(() =>
  import('~/components/MyHeavyComponent.vue')
)
</script>
```

### Optimize Images

Use `<NuxtImg>` for automatic optimization:

```vue
<NuxtImg src="/image.jpg" width="400" height="300" />
```

## Common Patterns

### Loading State

```vue
<script setup>
const loading = ref(false)

async function fetchData() {
  loading.value = true
  try {
    const data = await $fetch('/api/data')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <UButton :loading="loading" @click="fetchData">
    Load Data
  </UButton>
</template>
```

### Confirmation Dialog

```vue
<script setup>
const confirmOpen = ref(false)

function handleDelete() {
  confirmOpen.value = true
}

async function confirmDelete() {
  await $fetch('/api/delete', { method: 'DELETE' })
  confirmOpen.value = false
}
</script>

<template>
  <UButton @click="handleDelete">Delete</UButton>
  
  <UModal v-model:open="confirmOpen" title="Confirm Delete">
    <p>Are you sure?</p>
    <template #footer>
      <UButton @click="confirmDelete">Yes, Delete</UButton>
      <UButton variant="ghost" @click="confirmOpen = false">Cancel</UButton>
    </template>
  </UModal>
</template>
```

## Useful Resources

- **Nuxt Docs**: https://nuxt.com/docs
- **Nuxt UI**: https://ui.nuxt.com
- **Vue 3 Docs**: https://vuejs.org
- **Tailwind CSS**: https://tailwindcss.com
- **Lucide Icons**: https://lucide.dev
- **TypeScript**: https://www.typescriptlang.org

## Troubleshooting

### Port Already in Use

```bash
# Kill process on port 3000
npx kill-port 3000

# Or use different port
PORT=3001 npm run dev
```

### Module Not Found

```bash
# Clear cache and reinstall
rm -rf node_modules .nuxt
npm install
```

### Build Errors

```bash
# Check types
npm run typecheck

# Clear Nuxt cache
rm -rf .nuxt
```

### Hot Reload Not Working

1. Check file is saved
2. Restart dev server
3. Clear browser cache

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd/Ctrl + K` | Open search |
| `g h` | Go to home |
| `g i` | Go to investigations |
| `g e` | Go to evidence |
| `g l` | Go to legislation |
| `g s` | Go to settings |
| `n` | Toggle notifications |

## File Naming Conventions

- **Pages**: kebab-case (e.g., `my-page.vue`)
- **Components**: PascalCase (e.g., `MyComponent.vue`)
- **Composables**: camelCase starting with `use` (e.g., `useAuth.ts`)
- **API Routes**: kebab-case with HTTP method (e.g., `my-route.get.ts`)
- **Types**: PascalCase interfaces (e.g., `User`, `Investigation`)

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "Add my feature"

# Push to remote
git push origin feature/my-feature

# Create pull request on GitHub
```

---

**Need Help?** Check the full documentation in README.md or consult the Nuxt/Nuxt UI documentation.
