# Deployment Guide - Screener MA Kuncup

This guide covers deploying the Screener MA Kuncup to Vercel and other platforms.

## Deploying to Vercel (Recommended)

Vercel is the recommended hosting platform for Next.js applications.

### Prerequisites
- GitHub, GitLab, or Bitbucket account
- Vercel account (free at vercel.com)

### Steps

#### 1. Push to Git Repository
```bash
git remote add origin https://github.com/yourusername/screener-ma-kuncup.git
git push -u origin main
```

#### 2. Import on Vercel

**Option A: Web Dashboard**
1. Go to [vercel.com/new](https://vercel.com/new)
2. Select "Import Git Repository"
3. Enter your repository URL
4. Select "Next.js" as framework
5. In "Root Directory", specify: `vercel-screener-ma`
6. Click "Deploy"

**Option B: Vercel CLI**
```bash
npm install -g vercel
cd vercel-screener-ma
vercel --prod
```

### Configuration

#### Environment Variables (Optional)
In Vercel Dashboard > Project Settings > Environment Variables:
- No required variables (uses public Yahoo Finance API)
- Optional: `NEXT_PUBLIC_STOCKS_URL` for custom stock list

#### Regional Settings
- Auto regions: Recommended for global distribution
- Each request router to nearest edge function

#### Build Settings
- **Framework**: Next.js
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Install Command**: `npm install`

### Auto-Deploy
- Merges to `main` branch trigger automatic deployment
- Preview deployments for pull requests
- Rollback to previous deployments anytime

## Deploying to Other Platforms

### Docker (Self-Hosted)

Create `Dockerfile`:
```dockerfile
FROM node:20-alpine AS base

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

Build and run:
```bash
docker build -t screener-ma-kuncup .
docker run -p 3000:3000 screener-ma-kuncup
```

### AWS (EC2/ECS)

1. **Build Docker image**
2. **Push to ECR**: 
   ```bash
   aws configure
   # Create ECR repository
   aws ecr create-repository --repository-name screener-ma-kuncup
   docker push [YOUR_ECR_URL]/screener-ma-kuncup
   ```
3. **Deploy to ECS** or EC2 with appropriate IAM roles

### Google Cloud (Cloud Run)

```bash
gcloud run deploy screener-ma-kuncup \
  --source . \
  --platform managed \
  --region us-central1
```

### Netlify

Not recommended for API routes (use Vercel or other serverless platforms instead).

## Performance Optimization

### Edge Caching
- API responses cached for 1 hour
- Static files cached for 1 year
- Adjust in `next.config.js` headers section

### Image Optimization
- Next.js Image component for optimization
- Currently set to `unoptimized: true` for simplicity

### API Rate Limiting
- Implement if hitting Yahoo Finance rate limits
- Use Redis cache for frequently accessed data

## Monitoring

### Vercel Analytics
1. Dashboard > Analytics
2. View:
   - Page views and response times
   - API usage
   - Error rates
   - Deployment performance

### Logging
- Vercel: Automatic logs in dashboard
- Local: Check `.next/server/logs/`

## Troubleshooting

### Build Fails
- Check Node version (requires 18+)
- Verify all dependencies installed
- Check for TypeScript errors: `npm run build`

### API Timeouts
- Default Vercel timeout: 60 seconds (serverless)
- Check Yahoo Finance API status
- Reduce number of stocks per request

### High Cold Start
- Cold start typically < 1 second on Vercel
- Pre-warming functions with cron jobs helps

## Cost Estimation

### Vercel (Recommended)
- **Free tier**: Perfect for personal use
  - 100 serverless function invocations/day
  - 6 concurrent deployments
  - 100 GB bandwidth/month
  
- **Pro tier**: $20/month
  - Unlimited serverless functions
  - Team collaboration
  - Enhanced support

### Self-Hosted
- **VPS**: $5-50/month (DigitalOcean, Linode)
- **Container Runtime**: $5-100/month
- **Data Transfer**: Minimal with Yahoo Finance API

## Maintenance

### Updates
```bash
npm update
npm audit fix
npm run build
npm run test
```

### Backups
- Git repository is your backup
- Vercel keeps deployment history

### Monitoring
- Set up alerts for failed deployments
- Monitor API usage and costs
- Track performance metrics

## Security Checklist

- ✅ HTTPS everywhere (automatic on Vercel)
- ✅ Security headers set (see `next.config.js`)
- ✅ No sensitive data in environment variables (public API)
- ✅ Input validation on API routes
- ✅ Regular dependency updates
- ✅ Monitoring and logging enabled

## Support

- Vercel Docs: https://vercel.com/docs
- Next.js Docs: https://nextjs.org/docs
- GitHub Issues: Create issue for support
