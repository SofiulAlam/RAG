"""
Seed data for prompt templates
Run this to populate the database with initial templates
"""

templates_data = [
    {
        "name": "SaaS Dashboard",
        "category": "Dashboard",
        "description": "Modern SaaS dashboard with analytics, user management, and data visualization",
        "framework": "Next.js",
        "template_prompt": """Create a modern SaaS dashboard application using Next.js:

Project Name: {app_name}
Primary Color: {primary_color}

## Layout
- Responsive sidebar navigation with collapsible menu
- Top bar with search, notifications, and user menu
- Main content area with breadcrumbs
- Dark mode toggle

## Features
1. **Dashboard Home**
   - Key metrics cards (users, revenue, growth, etc.)
   - Interactive charts using recharts
   - Recent activity feed
   - Quick action buttons

2. **Data Tables**
   - Sortable and filterable tables
   - Pagination
   - Row selection
   - Export to CSV
   - Search functionality

3. **User Management**
   - User list with CRUD operations
   - User roles and permissions
   - User profile pages

4. **Settings**
   - Account settings
   - Notification preferences
   - Theme customization
   - API keys management

## Technical Requirements
- Next.js 14 with App Router
- TypeScript strict mode
- Tailwind CSS + shadcn/ui components
- Responsive design (mobile-first)
- Loading states and error boundaries
- Form validation
- Dark mode support

## Design
- Clean, modern interface
- Consistent spacing and typography
- Smooth transitions and animations
- Professional color scheme based on {primary_color}
- High-quality icons from lucide-react""",
        "preview_image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400",
    },
    {
        "name": "E-commerce Store",
        "category": "E-commerce",
        "description": "Full-featured online store with cart, checkout, and product management",
        "framework": "Next.js",
        "template_prompt": """Create a modern e-commerce store application:

Store Name: {store_name}
Product Category: {category}

## Features
1. **Product Catalog**
   - Product grid/list view with filters
   - Product search with autocomplete
   - Category navigation
   - Product detail pages with image gallery
   - Related products section

2. **Shopping Cart**
   - Add/remove items
   - Quantity adjustment
   - Cart persistence
   - Cart summary with totals

3. **Checkout**
   - Multi-step checkout process
   - Shipping address form
   - Payment information (UI only)
   - Order summary and confirmation

4. **User Features**
   - Product wishlist
   - Order history
   - User reviews and ratings
   - Product comparison

## Design
- Beautiful product cards with hover effects
- High-quality product images from Unsplash
- Mobile-optimized shopping experience
- Sticky cart button on mobile
- Trust badges and secure checkout UI

## Technical Stack
- Next.js 14 with TypeScript
- Tailwind CSS for styling
- Zustand for cart state management
- Form validation with proper error handling
- Responsive design (320px+)
- SEO optimized""",
        "preview_image": "https://images.unsplash.com/photo-1472851294608-062f824d29cc?w=400",
    },
    {
        "name": "Landing Page",
        "category": "Marketing",
        "description": "High-converting landing page with hero section, features, and CTA",
        "framework": "Next.js",
        "template_prompt": """Create a high-converting landing page:

Product/Service: {product_name}
Target Audience: {audience}

## Sections
1. **Hero Section**
   - Compelling headline and subheadline
   - Eye-catching background image/gradient
   - Primary CTA button
   - Product screenshot or illustration
   - Social proof (customer count, ratings)

2. **Features Section**
   - 3-6 key features with icons
   - Brief descriptions
   - Benefits-focused copy

3. **How It Works**
   - 3-4 step process
   - Visual timeline or cards
   - Clear explanations

4. **Social Proof**
   - Customer testimonials with photos
   - Company logos (trusted by)
   - Statistics and achievements

5. **Pricing** (if applicable)
   - 2-3 pricing tiers
   - Feature comparison
   - Popular plan highlight

6. **FAQ Section**
   - 5-8 common questions
   - Expandable accordion

7. **Final CTA**
   - Compelling call-to-action
   - Email signup or demo request
   - Trust indicators

## Design Requirements
- Modern, professional design
- Smooth scroll animations
- Mobile-responsive
- Fast loading
- Optimized images from Unsplash
- Accessibility compliant
- SEO meta tags

## Technical Stack
- Next.js 14
- TypeScript
- Tailwind CSS
- Framer Motion for animations
- Contact form with validation""",
        "preview_image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400",
    },
    {
        "name": "Blog Platform",
        "category": "Content",
        "description": "Modern blog with markdown support, categories, and comments",
        "framework": "Next.js",
        "template_prompt": """Create a modern blog platform:

Blog Name: {blog_name}
Topic/Niche: {niche}

## Features
1. **Homepage**
   - Featured posts carousel
   - Latest posts grid
   - Category filters
   - Search functionality
   - Newsletter signup

2. **Blog Post Page**
   - Markdown rendering
   - Code syntax highlighting
   - Table of contents
   - Reading time estimate
   - Author bio
   - Share buttons
   - Related posts

3. **Category Pages**
   - Posts filtered by category
   - Category description
   - Pagination

4. **Author Pages**
   - Author bio and photo
   - List of author's posts
   - Social links

5. **Search**
   - Full-text search
   - Search suggestions
   - Filter by category/date

## Design
- Clean, readable typography
- Proper spacing for readability
- Beautiful header images
- Dark mode support
- Print-friendly post layout

## Technical Stack
- Next.js 14 with App Router
- MDX for markdown
- Syntax highlighting
- SEO optimization
- RSS feed
- Sitemap
- Open Graph meta tags""",
        "preview_image": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=400",
    },
    {
        "name": "Portfolio Website",
        "category": "Personal",
        "description": "Professional portfolio to showcase projects and skills",
        "framework": "Next.js",
        "template_prompt": """Create a professional portfolio website:

Name: {name}
Profession: {profession}

## Sections
1. **Hero Section**
   - Professional photo
   - Name and title
   - Brief tagline
   - CTA buttons (contact, resume)
   - Social media links

2. **About**
   - Professional bio
   - Skills and expertise
   - Experience timeline
   - Education

3. **Projects/Work**
   - Project cards with images
   - Project details on click
   - Tech stack tags
   - Live demo and GitHub links
   - Filter by technology

4. **Skills**
   - Skill categories
   - Proficiency indicators
   - Tool/technology logos

5. **Experience**
   - Work history
   - Timeline layout
   - Achievements

6. **Contact**
   - Contact form
   - Email, phone, location
   - Social links
   - Availability status

## Design
- Modern, professional aesthetic
- Smooth animations
- Interactive elements
- Mobile-responsive
- Fast loading
- Accessibility compliant

## Technical Stack
- Next.js 14
- TypeScript
- Tailwind CSS
- Framer Motion
- Contact form with validation
- Resume download link""",
        "preview_image": "https://images.unsplash.com/photo-1487017159836-4e23ece2e4cf?w=400",
    },
    {
        "name": "Task Manager",
        "category": "Productivity",
        "description": "Todo list and task management application",
        "framework": "Next.js",
        "template_prompt": """Create a modern task management application:

## Features
1. **Task List**
   - Add, edit, delete tasks
   - Mark as complete/incomplete
   - Task priority levels (high, medium, low)
   - Due dates
   - Task categories/labels
   - Drag and drop reordering

2. **Filters and Views**
   - All tasks
   - Active tasks
   - Completed tasks
   - Filter by priority
   - Filter by due date
   - Search tasks

3. **Projects/Lists**
   - Multiple project lists
   - Color-coded projects
   - Project-specific tasks
   - Archive completed projects

4. **Task Details**
   - Task description
   - Subtasks/checklist
   - Comments/notes
   - Attachments (UI)
   - Activity log

5. **Calendar View**
   - Monthly calendar
   - Tasks by due date
   - Drag to reschedule

## Design
- Clean, minimal interface
- Keyboard shortcuts
- Quick add input
- Smooth animations
- Dark mode
- Mobile-responsive

## Technical Stack
- Next.js 14
- TypeScript
- Tailwind CSS + shadcn/ui
- Local storage persistence
- Drag and drop (dnd-kit)
- Date picker
- Keyboard navigation""",
        "preview_image": "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=400",
    },
    {
        "name": "Chat Interface",
        "category": "Communication",
        "description": "Real-time chat application with channels and DMs",
        "framework": "Next.js",
        "template_prompt": """Create a modern chat interface:

## Features
1. **Channel List**
   - Public channels
   - Private channels
   - Direct messages
   - Unread indicators
   - Channel search
   - Create new channels

2. **Chat Area**
   - Message list with infinite scroll
   - Message composition
   - File uploads (UI)
   - Emoji picker
   - Reply to messages
   - Edit/delete messages
   - Message reactions

3. **User Features**
   - User profile
   - Online/offline status
   - Typing indicators
   - User search
   - User mentions (@username)

4. **Rich Messages**
   - Markdown support
   - Code blocks with syntax highlighting
   - Link previews
   - Image/video embeds
   - File attachments

5. **Sidebar**
   - Channel members list
   - Channel details
   - Pinned messages
   - Shared files

## Design
- Slack/Discord-inspired layout
- Three-column layout
- Clean, modern design
- Dark mode support
- Mobile-responsive
- Smooth animations

## Technical Stack
- Next.js 14
- TypeScript
- Tailwind CSS
- Markdown rendering
- Emoji support
- Virtualized message list
- Optimistic UI updates""",
        "preview_image": "https://images.unsplash.com/photo-1577563908411-5077b6dc7624?w=400",
    },
    {
        "name": "Admin Panel",
        "category": "Dashboard",
        "description": "Complete admin panel with user, content, and analytics management",
        "framework": "Next.js",
        "template_prompt": """Create a comprehensive admin panel:

## Features
1. **Dashboard**
   - Overview statistics
   - Charts and graphs
   - Recent activity
   - Quick actions
   - System health indicators

2. **User Management**
   - User list with search and filters
   - Create/edit users
   - User roles and permissions
   - User activity logs
   - Bulk actions

3. **Content Management**
   - CRUD for content items
   - Rich text editor
   - Media library
   - Categories and tags
   - Draft/publish workflow

4. **Analytics**
   - Traffic analytics
   - User engagement metrics
   - Revenue reports
   - Custom date ranges
   - Export reports

5. **Settings**
   - General settings
   - Email templates
   - API configuration
   - Integrations
   - Backup/restore

6. **Notifications**
   - System notifications
   - Email notifications
   - Push notifications settings

## Design
- Professional admin UI
- Data-dense tables
- Clear navigation
- Responsive layout
- Loading states
- Empty states
- Error handling

## Technical Stack
- Next.js 14
- TypeScript
- Tailwind CSS + shadcn/ui
- React Hook Form
- Data tables with sorting/filtering
- Charts (recharts)
- File uploads
- CSV export""",
        "preview_image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400",
    },
]


async def seed_templates(db):
    """Seed the database with initial templates"""
    from app.models.template import Template

    for template_data in templates_data:
        template = Template(**template_data)
        db.add(template)

    await db.commit()
    print(f"Seeded {len(templates_data)} templates")
