# Migration Guide: From Static HTML to Nuxt UI Dashboard

## Overview

This guide documents the migration from the original static HTML/Express.js investigation portal to a modern Nuxt 3 application with the Nuxt UI Dashboard template, while maintaining all WSCC branding and functionality.

## What's New

### Architecture Changes

**Before:**
- Static HTML file (`client/index.html`)
- Vanilla JavaScript
- Express.js backend serving static files
- Auth0 via CDN script

**After:**
- Nuxt 3 full-stack application
- Vue 3 with Composition API
- Server API routes (Nitro)
- Nuxt UI v4 component library
- Auth0 Vue integration
- TypeScript support
- SSR/SPA hybrid

### Features Maintained

✅ **Dashboard Summary**
- Location: `app/pages/index.vue`
- Component: `app/components/dashboard/DashboardStats.vue`
- Shows: Total active investigations, charge deadlines, high-risk cases

✅ **Investigation Management**
- List: `app/pages/investigations/index.vue`
- Create: `app/pages/investigations/new.vue`
- Form fields: Title, description, status, deadline

✅ **Evidence Manager**
- List: `app/pages/evidence/index.vue`
- Upload: `app/pages/evidence/upload.vue`
- Supports: Multiple file uploads, descriptions, location tracking

✅ **Legislation Library**
- Location: `app/pages/legislation.vue`
- Features: Search, categorization, external links
- Data: Workers' Compensation Act, Safety Regulations, Mine Health & Safety Act

✅ **Auth0 Authentication**
- Plugin: `app/plugins/auth0.client.ts`
- Composable: `app/composables/useAuth.ts`
- Same credentials as original (domain: dev-o05e1b87irncothe.ca.auth0.com)

✅ **WSCC Branding**
- Primary: Blue 900 (#1e3a8a)
- Secondary: Blue 700 (#1d4ed8)
- Custom scrollbars, consistent color scheme throughout

### New Features

🆕 **Enhanced UI Components**
- Professional dashboard layout with collapsible sidebar
- Responsive design for mobile/tablet/desktop
- Dark mode support (via Nuxt UI)
- Toast notifications
- Search functionality (Cmd/Ctrl + K)
- Keyboard shortcuts

🆕 **Better Navigation**
- Sidebar with icons and tooltips
- Breadcrumbs and page headers
- Search command palette
- Quick actions dropdown

🆕 **Reports Section**
- New reports page for generating various report types
- Location: `app/pages/reports.vue`

🆕 **Settings Page**
- User profile management
- Notification preferences
- Location: `app/pages/settings.vue`

## API Endpoints

All original API endpoints have been recreated in Nuxt:

| Original | New Location | Method |
|----------|-------------|--------|
| `/api/dashboard/summary` | `server/api/dashboard/summary.get.ts` | GET |
| `/api/investigations` | `server/api/investigations/index.get.ts` | GET |
| `/api/investigations` | `server/api/investigations/index.post.ts` | POST |
| `/api/evidence` | `server/api/evidence.post.ts` | POST |
| `/api/legislation` | `server/api/legislation.get.ts` | GET |

## File Structure Comparison

### Before
```
/
├── client/
│   └── index.html (everything in one file)
├── server/
│   └── index.js (Express server)
└── package.json
```

### After
```
nuxt-app/
├── app/
│   ├── assets/css/
│   │   └── main.css (WSCC styles)
│   ├── components/
│   │   ├── dashboard/
│   │   ├── UserMenu.vue
│   │   └── NotificationsSlideover.vue
│   ├── composables/
│   │   ├── useDashboard.ts
│   │   └── useAuth.ts
│   ├── layouts/
│   │   └── default.vue (sidebar, nav)
│   ├── pages/
│   │   ├── index.vue (dashboard)
│   │   ├── investigations/
│   │   ├── evidence/
│   │   ├── legislation.vue
│   │   ├── reports.vue
│   │   └── settings.vue
│   ├── plugins/
│   │   └── auth0.client.ts
│   ├── app.config.ts (theme)
│   └── app.vue
├── server/
│   └── api/ (Nitro API routes)
├── nuxt.config.ts
└── package.json
```

## Integration with Existing Backend

The Nuxt app currently uses in-memory API routes for demonstration. To integrate with your existing Express backend:

### Option 1: Proxy to Express
Update API routes to proxy to the original backend:

```typescript
// server/api/dashboard/summary.get.ts
export default defineEventHandler(async (event) => {
  return await $fetch('http://localhost:3000/api/dashboard/summary')
})
```

### Option 2: Shared Database
Connect both applications to the same database and gradually migrate logic to Nuxt.

### Option 3: Full Migration
Move all backend logic from Express to Nuxt API routes and retire the Express server.

## Running the Application

### Development
```bash
cd nuxt-app
npm install
npm run dev
```
Visit: http://localhost:3000

### Production
```bash
npm run build
npm run preview
```

### Deploy
```bash
npm run build
# Deploy .output directory to any Node.js hosting
```

## Environment Variables

Create `.env` file in nuxt-app/:

```env
# Auth0 (optional, currently hardcoded)
AUTH0_DOMAIN=dev-o05e1b87irncothe.ca.auth0.com
AUTH0_CLIENT_ID=SuZaMg7UykFXNuSLFNUYoCxlEWTxiAQD

# API Configuration
API_BASE_URL=http://localhost:3000
```

## Breaking Changes

### JavaScript → TypeScript
- Files now use `.ts` and `.vue` extensions
- Type checking available with `npm run typecheck`
- Types defined in `app/types/` (can be added as needed)

### Direct DOM Manipulation → Reactive State
- No more `document.getElementById()`
- Use Vue refs and reactive state
- Example: `const state = reactive({ ... })`

### Fetch → $fetch
- Nuxt provides auto-imported `$fetch` with better error handling
- Supports TypeScript generics for response types

### Event Listeners → Vue Events
- Use `@click`, `@submit` instead of `addEventListener`
- Form handling via `@submit.prevent`

## Customization Guide

### Changing Colors
Edit `app/app.config.ts`:
```typescript
export default defineAppConfig({
  ui: {
    colors: {
      primary: 'blue', // Change to any color
      neutral: 'slate'
    }
  }
})
```

### Adding New Pages
1. Create file in `app/pages/` (e.g., `app/pages/analytics.vue`)
2. Add to navigation in `app/layouts/default.vue`
3. Automatically routed!

### Adding API Endpoints
1. Create file in `server/api/` (e.g., `server/api/users.get.ts`)
2. Export `defineEventHandler`
3. Accessible at `/api/users`

## Testing Checklist

- [ ] Dashboard loads and shows statistics
- [ ] Can create new investigation
- [ ] Can upload evidence with files
- [ ] Legislation library displays and is searchable
- [ ] Auth0 login redirects properly
- [ ] User menu shows logged-in user
- [ ] Notifications panel opens
- [ ] All navigation links work
- [ ] Mobile responsive design works
- [ ] Keyboard shortcuts work (Cmd/Ctrl + K for search)

## Support

For issues or questions about the migration:
1. Check the Nuxt documentation: https://nuxt.com
2. Check Nuxt UI documentation: https://ui.nuxt.com
3. Review the original client/index.html for reference

## Next Steps

1. **Connect to Production Database**: Update API routes to use real data
2. **Set up CI/CD**: Automate builds and deployments
3. **Add Tests**: Unit tests for components, E2E tests for workflows
4. **Performance Monitoring**: Add analytics and error tracking
5. **User Training**: Document new features for end users
