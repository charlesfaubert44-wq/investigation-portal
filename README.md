# WSCC Investigation Portal

## 🎉 New Nuxt UI Dashboard Integration

The investigation portal has been successfully upgraded with the **Nuxt UI Dashboard template** while maintaining all original functionality and WSCC branding!

### 🚀 Quick Start (New Application)

```bash
cd nuxt-app
npm install
npm run dev
```

Visit: http://localhost:3000

### 📚 Documentation

- **[Integration Summary](INTEGRATION_SUMMARY.md)** - Complete overview of changes
- **[nuxt-app/README.md](nuxt-app/README.md)** - Main documentation
- **[nuxt-app/MIGRATION_GUIDE.md](nuxt-app/MIGRATION_GUIDE.md)** - Detailed migration guide
- **[nuxt-app/DEPLOYMENT.md](nuxt-app/DEPLOYMENT.md)** - Deployment instructions
- **[nuxt-app/FEATURES.md](nuxt-app/FEATURES.md)** - Feature list

## Legacy Application

The original HTML/Express application is preserved in:
- `client/` - Original HTML interface
- `server/` - Original Express backend

### Run Legacy Version

```bash
npm install
npm start
```

## What's New

✅ Modern Nuxt 3 framework with Vue 3  
✅ Professional dashboard UI with Nuxt UI components  
✅ Collapsible/resizable sidebar navigation  
✅ Enhanced mobile responsiveness  
✅ Keyboard shortcuts and search  
✅ TypeScript for better code quality  
✅ All WSCC branding maintained  
✅ All original features preserved and enhanced  

## Project Structure

```
/
├── nuxt-app/          # 🆕 New Nuxt 3 application
├── client/            # 📁 Legacy HTML interface  
├── server/            # 📁 Legacy Express backend
└── README.md          # This file
```

## Features

- **Dashboard**: Real-time statistics and quick actions
- **Investigations**: Create and manage investigation cases
- **Evidence Manager**: Upload and track evidence files
- **Legislation Library**: Browse relevant legislation
- **Reports**: Generate various investigation reports
- **Settings**: User preferences and configuration
- **Auth0 Integration**: Secure authentication

## Technology

### New Stack
- Nuxt 3 + Vue 3
- Nuxt UI v4
- TypeScript
- Tailwind CSS
- Auth0 Vue

### Legacy Stack
- HTML + Vanilla JavaScript
- Express.js
- Auth0 CDN

## Next Steps

1. Review the [Integration Summary](INTEGRATION_SUMMARY.md)
2. Test the new application
3. Deploy to staging environment
4. Train users on new features
5. Gradually deprecate legacy version

---

**WSCC Investigation Management Portal** - Modernized with Nuxt UI Dashboard
