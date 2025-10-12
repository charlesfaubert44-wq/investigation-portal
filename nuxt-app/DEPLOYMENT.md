# Deployment Guide

## Prerequisites

- Node.js 18+ installed
- npm or pnpm package manager
- Access to deployment platform

## Build Process

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Build for production**
   ```bash
   npm run build
   ```

   This creates a `.output` directory containing:
   - Server code in `.output/server/`
   - Static assets in `.output/public/`

3. **Test production build locally**
   ```bash
   npm run preview
   ```

## Deployment Options

### Option 1: Node.js Server (Recommended)

Deploy to any Node.js hosting platform:

**Platforms:**
- DigitalOcean App Platform
- Heroku
- Railway
- Render
- AWS EC2
- Azure App Service

**Steps:**
1. Build the application
2. Upload `.output` directory
3. Run: `node .output/server/index.mjs`
4. Set PORT environment variable if needed

**Example with PM2:**
```bash
npm install -g pm2
npm run build
pm2 start .output/server/index.mjs --name wscc-portal
```

### Option 2: Serverless (Vercel/Netlify)

**Vercel:**
```bash
npm install -g vercel
vercel deploy
```

**Netlify:**
```bash
npm install -g netlify-cli
netlify deploy --prod
```

### Option 3: Docker Container

**Dockerfile:**
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY .output .output

ENV PORT=3000
EXPOSE 3000

CMD ["node", ".output/server/index.mjs"]
```

**Build and run:**
```bash
npm run build
docker build -t wscc-portal .
docker run -p 3000:3000 wscc-portal
```

### Option 4: Static Hosting (Limited)

For static generation (loses server API routes):
```bash
npm run generate
```

Deploy `.output/public` to:
- Netlify
- Vercel
- GitHub Pages
- AWS S3 + CloudFront

**Note:** This loses server-side features. Recommend Option 1 or 2 instead.

## Environment Variables

Set these in your deployment platform:

```env
# Required
NODE_ENV=production

# Optional - Auth0
AUTH0_DOMAIN=dev-o05e1b87irncothe.ca.auth0.com
AUTH0_CLIENT_ID=SuZaMg7UykFXNuSLFNUYoCxlEWTxiAQD

# Optional - API
API_BASE_URL=https://your-api.com

# Optional - Server
PORT=3000
```

## Running Original Backend Alongside

If keeping the original Express backend:

1. Deploy Express backend separately
2. Update Nuxt API routes to proxy to it:

```typescript
// server/api/dashboard/summary.get.ts
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  return await $fetch(`${config.public.apiBaseUrl}/api/dashboard/summary`)
})
```

3. Set API_BASE_URL environment variable

## SSL/HTTPS

Most platforms (Vercel, Netlify, Render) provide automatic HTTPS.

For custom servers:
- Use Let's Encrypt certificates
- Configure reverse proxy (nginx/Apache)
- Update Auth0 callback URLs to use HTTPS

## Monitoring

### Health Check Endpoint

Add `server/api/health.get.ts`:
```typescript
export default defineEventHandler(() => {
  return {
    status: 'ok',
    timestamp: new Date().toISOString()
  }
})
```

### Recommended Services
- **Error Tracking**: Sentry
- **Performance**: New Relic, DataDog
- **Uptime**: UptimeRobot, Pingdom
- **Logs**: Papertrail, LogDNA

## Performance Optimization

1. **Enable compression**
   ```typescript
   // nuxt.config.ts
   export default defineNuxtConfig({
     nitro: {
       compressPublicAssets: true
     }
   })
   ```

2. **Cache static assets**
   - Use CDN for `.output/public`
   - Set long cache headers

3. **Database connection pooling**
   - Use connection pool for database
   - Implement caching layer (Redis)

## Rollback Strategy

1. Keep previous `.output` directories
2. Use blue-green deployment
3. Test in staging first
4. Have database backup strategy

## Checklist

- [ ] Build completes without errors
- [ ] Environment variables configured
- [ ] Auth0 callback URLs updated
- [ ] Database connections work
- [ ] SSL certificate installed
- [ ] Monitoring/logging configured
- [ ] Backup strategy in place
- [ ] Health check endpoint responding
- [ ] Test all core features post-deployment

## Troubleshooting

**Error: "Cannot find module"**
- Ensure all dependencies installed: `npm ci`
- Check Node.js version matches requirements

**Auth0 not working**
- Verify callback URLs in Auth0 dashboard
- Check environment variables
- Ensure domain uses HTTPS

**API routes returning 404**
- Verify `.output/server` contains API routes
- Check nitro preset in nuxt.config.ts
- Ensure server is running with correct base path

## Support Resources

- Nuxt Deployment Docs: https://nuxt.com/docs/getting-started/deployment
- Nuxt Discord: https://discord.com/invite/nuxt
