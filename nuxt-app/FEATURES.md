# WSCC Investigation Portal - Feature List

## 🏠 Dashboard

### Overview Statistics
- **Total Active Investigations**: Real-time count of ongoing cases
- **Charge Deadlines This Month**: Critical deadline tracking
- **High Risk Cases**: Priority case identification

### Quick Actions
- Create new investigation
- Upload evidence
- Access legislation library
- Generate reports

### Visual Design
- Card-based layout with WSCC blue branding
- Hover effects for better UX
- Responsive grid system

## 🔍 Investigation Management

### List View
- **Sortable Table**: View all investigations in organized table
- **Status Badges**: Visual indicators (Active, Under Review, Pending, Closed)
- **Quick Actions**: View and edit buttons per row
- **Columns**: ID, Title, Status, Deadline, Actions

### Create Investigation
- **Form Fields**:
  - Title (required)
  - Description (required, multi-line)
  - Status (dropdown: Active, Under Review, Pending, Closed)
  - Deadline (date picker)
- **Validation**: Client-side form validation
- **Toast Notifications**: Success/error feedback
- **Auto-redirect**: Returns to list after creation

### Features
- Search and filter capabilities
- Keyboard navigation
- Mobile-responsive forms
- Auto-save draft (can be added)

## 📁 Evidence Manager

### Evidence List
- **Table View**: All evidence records
- **Badge Indicators**: File count per evidence entry
- **Metadata Display**: Investigation ID, description, location, upload date
- **Quick Actions**: View and download buttons

### Upload Evidence
- **Form Fields**:
  - Investigation ID (links to case)
  - Description (detailed evidence notes)
  - Location (where evidence was collected)
  - File Upload (multiple files supported)
- **File Support**: Images, PDFs, Word documents
- **Multi-file Upload**: Upload multiple files at once
- **Progress Indicators**: Upload status feedback

### Features
- Drag-and-drop upload (can be added)
- Preview before upload
- File size validation
- Metadata extraction

## 📚 Legislation Library

### Document Browser
- **Card Layout**: Visual document cards
- **Category Badges**: Color-coded by type
  - Compensation (Blue)
  - Safety (Green)
  - Mining (Orange)
- **Jurisdiction Tags**: NT, NU, NT/NU indicators
- **External Links**: Direct access to official documents

### Search Functionality
- **Real-time Search**: Filter as you type
- **Multi-field Search**: Searches title, category, jurisdiction
- **Empty State**: Friendly message when no results

### Documents Included
1. Workers' Compensation Act (NT) - Compensation
2. Safety Regulations (NU) - Safety
3. Mine Health & Safety Act - Mining

## 📊 Reports

### Report Types
1. **Investigation Summary Report**
   - Comprehensive case overview
   - Key findings and conclusions
   
2. **Evidence Report**
   - Detailed evidence catalog
   - Chain of custody information
   
3. **Timeline Report**
   - Chronological event sequence
   - Critical date tracking
   
4. **Compliance Report**
   - Regulatory compliance check
   - Gap analysis

### Features
- One-click generation
- Export options (can be added: PDF, Excel, Word)
- Template customization
- Scheduled reports (can be added)

## ⚙️ Settings

### Profile Management
- Name editing
- Email display (read-only)
- Role display (read-only)

### Notification Preferences
- Enable/disable notifications toggle
- Email alerts toggle
- Push notifications (can be added)

### Features
- Save confirmation
- Real-time updates
- Validation feedback

## 🔐 Authentication & Security

### Auth0 Integration
- **Login Flow**: Redirect to Auth0
- **Session Management**: Automatic token refresh
- **Logout**: Clean session termination
- **User Profile**: Display name and avatar

### Security Features
- JWT token authentication
- Secure HTTP-only cookies
- Role-based access control (ready for implementation)
- Protected API routes

## 🎨 User Interface

### Design System
- **Component Library**: Nuxt UI v4
- **Icons**: Lucide icon set (1000+ icons)
- **Colors**: WSCC blue theme
  - Primary: Blue 900 (#1e3a8a)
  - Secondary: Blue 700 (#1d4ed8)
  - Accent: Blue 600 (#3b82f6)

### Layout
- **Collapsible Sidebar**: Space-saving navigation
- **Resizable Sidebar**: Customizable width
- **Responsive Design**: Mobile, tablet, desktop
- **Dark Mode Ready**: Can be toggled via theme

### Navigation
- **Sidebar Menu**: Icon-based with labels
- **Search Bar**: Cmd/Ctrl + K to open
- **Breadcrumbs**: Current location indicator
- **User Menu**: Profile and logout

## ⌨️ Keyboard Shortcuts

- `Cmd/Ctrl + K`: Open search
- `g h`: Go to Home
- `g i`: Go to Investigations
- `g e`: Go to Evidence
- `g l`: Go to Legislation
- `g s`: Go to Settings
- `n`: Toggle notifications

## 🔔 Notifications

### Notification Types
- Investigation deadlines
- New evidence uploads
- Report generation
- System alerts

### Features
- **Slideover Panel**: Non-intrusive display
- **Badge Counter**: Unread count on bell icon
- **Time Stamps**: Relative time (e.g., "2 hours ago")
- **Click to Action**: Navigate to related item

## 📱 Responsive Design

### Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Mobile Features
- Hamburger menu
- Touch-optimized buttons
- Swipe gestures (can be added)
- Bottom navigation (can be added)

## 🚀 Performance

### Optimizations
- **Code Splitting**: Load only what's needed
- **Lazy Loading**: Components load on demand
- **Image Optimization**: Automatic image compression
- **Caching**: Smart cache strategy
- **SSR**: Server-side rendering for fast first paint

### Metrics (Target)
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3.5s
- Lighthouse Score: > 90

## 🔌 API Integration

### Endpoints
- `GET /api/dashboard/summary` - Dashboard stats
- `GET /api/investigations` - List investigations
- `POST /api/investigations` - Create investigation
- `POST /api/evidence` - Upload evidence
- `GET /api/legislation` - Get legislation list

### Features
- Auto-retry on failure
- Loading states
- Error handling
- Type-safe responses

## 🎯 Accessibility

### Features (Partially Implemented)
- Keyboard navigation
- Screen reader support
- ARIA labels
- Focus indicators
- Color contrast compliance
- Skip to content links

### Standards
- WCAG 2.1 Level AA compliance (target)

## 🔄 Future Enhancements

### Planned Features
1. **Advanced Search**: Full-text search across all content
2. **File Preview**: In-browser document viewer
3. **Audit Trail**: Complete history of all actions
4. **Email Notifications**: Automated alerts
5. **Calendar Integration**: Deadline sync
6. **Export Data**: Bulk export capabilities
7. **Advanced Analytics**: Insights dashboard
8. **Mobile App**: Native iOS/Android apps
9. **Offline Mode**: Work without internet
10. **Collaboration**: Multi-user editing

### Technical Improvements
- Unit test coverage
- E2E test suite
- Performance monitoring
- Error tracking (Sentry)
- Analytics integration
- CI/CD pipeline
- Database migration tools
- Backup automation

## 📊 Browser Support

### Supported Browsers
- Chrome/Edge: Last 2 versions
- Firefox: Last 2 versions
- Safari: Last 2 versions
- Mobile Safari: iOS 12+
- Chrome Mobile: Android 8+

### Progressive Enhancement
- Core features work without JavaScript
- Enhanced features with JavaScript
- Graceful degradation for older browsers
