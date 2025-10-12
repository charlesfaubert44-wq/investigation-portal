# WSCC Investigation Management Portal

A modern, full-featured investigation management portal built with Nuxt 3 and Nuxt UI Dashboard template, maintaining WSCC (Workers' Safety and Compensation Commission) branding.

## Features

### 🏠 Dashboard
- Real-time statistics for active investigations
- Quick action cards for common tasks
- Overview of charge deadlines and high-risk cases

### 🔍 Investigation Management
- Create and manage investigation cases
- Track investigation status and deadlines
- Comprehensive investigation details

### 📁 Evidence Manager
- Upload and manage evidence files
- Support for photos, PDFs, and documents
- Link evidence to specific investigations
- Track evidence location and collection details

### 📚 Legislation Library
- Browse relevant legislation and regulations
- Search functionality for quick access
- Organized by category and jurisdiction
- Direct links to official documentation

### 📊 Reports
- Generate various investigation reports
- Export data in multiple formats
- Timeline and compliance reports

### ⚙️ Settings
- User profile management
- Notification preferences
- System configuration

## Technology Stack

- **Framework**: Nuxt 3
- **UI Library**: Nuxt UI v4
- **Authentication**: Auth0
- **Styling**: Tailwind CSS
- **Icons**: Lucide Icons
- **Build Tool**: Vite

## Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Configuration

### Auth0 Setup
The application uses Auth0 for authentication. The credentials are configured in:
- `app/plugins/auth0.client.ts`

To use your own Auth0 instance:
1. Create an Auth0 account and application
2. Update the domain and clientId in the Auth0 plugin
3. Configure callback URLs in your Auth0 dashboard

### API Integration
The application includes API routes in `server/api/` that can be connected to your existing backend:
- `/api/dashboard/summary` - Dashboard statistics
- `/api/investigations` - Investigation CRUD operations
- `/api/evidence` - Evidence management
- `/api/legislation` - Legislation library

## WSCC Branding

The application maintains WSCC branding with:
- **Primary Color**: Blue 900 (#1e3a8a)
- **Secondary Color**: Blue 700 (#1d4ed8)
- **Accent Color**: Blue 600 (#3b82f6)

Branding is implemented through:
- Custom CSS variables in `app/assets/css/main.css`
- Nuxt UI color configuration in `app/app.config.ts`
- Component-level styling throughout the application

## Project Structure

```
app/
├── assets/          # CSS and static assets
├── components/      # Vue components
│   ├── dashboard/   # Dashboard components
│   ├── investigations/
│   ├── evidence/
│   └── legislation/
├── composables/     # Shared composables
├── layouts/         # Layout templates
├── pages/           # Application pages
│   ├── investigations/
│   ├── evidence/
│   └── legislation/
├── plugins/         # Nuxt plugins (Auth0)
└── app.config.ts    # App configuration

server/
└── api/             # API routes
    ├── dashboard/
    ├── investigations/
    └── evidence.post.ts
```

## Development

The application uses:
- TypeScript for type safety
- Vue 3 Composition API
- Auto-imported components and composables
- Server-side rendering (SSR) support

## Deployment

Build the application for production:

```bash
npm run build
```

The output will be in `.output/` directory, ready for deployment to any Node.js hosting service.

## Original Backend Integration

To integrate with the existing Express backend (`/server/index.js`):
1. Update API routes in `server/api/` to proxy to the Express backend
2. Or deploy both applications and configure CORS
3. Update API endpoints in components as needed

## License

Internal WSCC project - All rights reserved.
