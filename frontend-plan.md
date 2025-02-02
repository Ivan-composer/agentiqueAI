# Agentique Frontend: Updated 10-Step Plan (MVP)

Below is the revised 10-step plan for building the Agentique frontend. We've:
- Removed the "social media commenting" feature from this plan (we'll handle it later)
- Added a default 15 credits for new users in the UI references (to mirror backend or a minimal approach)
- Included a minimal Profile page to show credits, skip any advanced deployment steps for now (no Vercel)
- Incorporated suggestions around partial ingestion feedback, testing, logging, etc.

## Step 1: Project Setup & Directory Structure

1. Create a new `frontend/` folder at the root of your monorepo (alongside `backend/`).  

2. Initialize a Next.js (v13+) project (App Router recommended) in `frontend/`:
   ```bash
   cd frontend
   npx create-next-app@latest --experimental-app agentique-frontend
   ```
   Alternatively, create a minimal Next.js structure with `/app/` folder if you prefer manual setup.

3. Install dependencies:
   ```bash
   npm install tailwindcss postcss autoprefixer
   npm install @shadcn/ui lucide-react  # ShadCN + icon set
   npm install axios  # or rely on fetch
   ```

4. File Structure (basic):
   ```plaintext
   frontend/
   ├── app/
   │   ├── layout.tsx
   │   ├── page.tsx  (Home / AI Search)
   │   ├── explore/
   │   ├── agent/
   │   │   └── [id]/
   │   ├── profile/
   │   ├── ...
   ├── components/
   ├── hooks/
   ├── lib/
   ├── logs/                 # storing logs for the frontend
   ├── public/
   ├── styles/
   ├── tailwind.config.js
   ├── postcss.config.js
   └── package.json
   ```

5. Test: Run `npm run dev` → ensure the local dev server shows a default Next.js page.

## Step 2: Tailwind & ShadCN Configuration + Color Palette

1. Tailwind Init:
   ```bash
   npx tailwindcss init -p
   ```

2. tailwind.config.js sample:
   ```js
   /** @type {import('tailwindcss').Config} */
   module.exports = {
     content: [
       './app/**/*.{js,ts,jsx,tsx}',
       './components/**/*.{js,ts,jsx,tsx}',
       // any other relevant paths
     ],
     theme: {
       extend: {
         colors: {
           // your primary color palette (greens, blues, violets, neutrals)
           primaryBlue: '#0098EA',
           primaryGreen: '#03CFC2',
           black: '#1E293B',
           // etc.
         },
         fontFamily: {
           inter: ['Inter', 'sans-serif'],
         },
       },
     },
     plugins: [],
   }
   ```
   Focus on mobile-first classes (`md:`, `lg:` for breakpoints) for future expansions.

3. ShadCN:
   - If you use ShadCN's CLI: `npx shadcn-ui init`
   - Provide a "theme" or "tokens" referencing your gradient combos (Green to Blue, Violet to Blue, etc.)
   - Keep lines minimal but docstrings clarifying usage

4. Inter Font:
   - Add `@fontsource/inter` or import from Google Fonts
   - Set `body { font-family: 'Inter', ... }` in `globals.css` or `app/layout.tsx`

## Step 3: Bottom Navigation & Layout

1. Create a `BottomNav` component:
   ```tsx
   // components/BottomNav.tsx
   import { HomeIcon, SearchIcon, UserIcon } from 'lucide-react'
   import Link from 'next/link'

   export function BottomNav() {
     return (
       <nav className="fixed bottom-0 w-full flex justify-around bg-white shadow-md">
         {/* Explore */}
         <Link href="/explore" className="flex flex-col items-center p-2">
           <HomeIcon className="mb-1" />
           <span>Explore</span>
         </Link>
         {/* AI Search */}
         <Link href="/" className="flex flex-col items-center p-2">
           <SearchIcon className="mb-1" />
           <span>AI Search</span>
         </Link>
         {/* Profile */}
         <Link href="/profile" className="flex flex-col items-center p-2">
           <UserIcon className="mb-1" />
           <span>Profile</span>
         </Link>
       </nav>
     )
   }
   ```

2. Use it in `layout.tsx`:
   ```tsx
   // app/layout.tsx
   import './globals.css'
   import { BottomNav } from '@/components/BottomNav'

   export default function RootLayout({ children }) {
     return (
       <html>
         <body className="min-h-screen relative font-inter">
           {children}
           <BottomNav />
         </body>
       </html>
     )
   }
   ```

3. Check on mobile dev tools to ensure it's easy to tap and doesn't overlap crucial UI.

## Step 4: Home (AI-Search) Page

1. Home = `app/page.tsx` (or `app/ai-search/page.tsx` if you prefer):
   - Title "Agentique AI" in gradient green (from #03CFC2 to #2A82EB)
   - Large text: "Solve any problem with AI-Agents"
   - Smaller text: "We'll pick the most relevant agents..."
   - Search input + Submit button

2. Search Action:
   - On submit, do `router.push("/search-results?query=" + encodeURIComponent(inputVal))` or a dedicated route
   - No direct backend call yet, or if you want to call `POST /search`, do that in a separate step

3. Minimal docstrings in code
   - e.g., `/** AI-Search home page for quick queries */`

### Testing (Step 4)

- Check on a phone viewport
- Confirm the gradient is correct
- Possibly log user's search to a local `frontend/logs/frontend.log` (if you do server components, or fallback to console logs in client code)

## Step 5: Explore Page & Agent Creation UI

1. Explore page in `app/explore/page.tsx`:
   - A button "Make AI-Agent of any Expert"
   - A list of existing AI agents (fetched from `GET /agents` if available)
   - Each agent leads to `agent/[id]` (Step 6 for chat)

2. Agent Creation flow:
   - Clicking "Make AI-Agent" → a minimal form: "Enter Telegram link"
   - On submit, call `POST /agent/create` with link
   - Show a "Scraping in progress" spinner or partial ingestion bar
     - Possibly poll `agent.status` from the backend until it's "ready"

3. Default 15 Credits:
   - On the Profile or somewhere, user sees `credits_balance` = 15 by default
   - In Explore, if no credits are needed for creating an agent, do nothing special for that

### Testing (Step 5)

- Create a test agent:
  - Use a dummy Telegram link
  - The front-end shows "loading..." or partial ingestion progress
- Once done, the new agent is in the Explore list
- If error: show a short error message. Possibly log it to `logs/frontend.log` or console

## Step 6: Chat Interface (Agent Chat)

1. Agent Chat page: `app/agent/[id]/page.tsx`
   - Show agent's name or "expert_name"
   - A message list: user messages (right side?), agent messages (left side?), or your preferred style
   - Input + "Send" button

2. Call `POST /agent/{agent_id}/chat` with user message
   - If the backend returns 403 "Not enough credits," show an error: "You have 0 credits; top up in profile"

3. Store or display conversation in local state. If you want to persist the entire chat, you can re-fetch from `GET /agent/{agent_id}/chat_messages` if that endpoint exists. Keep lines minimal.

### Testing (Step 6)

- Send a message → see the response from backend
- If credits are insufficient, confirm an error
- Logging any chat events (like "User sent message: XYZ" or "Agent responded: ABC")

## Step 7: Profile Page & Credits Display

1. Profile: `app/profile/page.tsx`:
   - Show user's name or "@user_telegram_id"
   - Display "Credits: X" (which is 15 by default for MVP)
   - Possibly a minimal "History" or "Transaction" list if you want
   - A placeholder for future top-ups or settings

2. Integration:
   - On load, do a quick fetch to backend to get user info + credits. Or use `client` state if you store it from login
   - Keep code minimal, docstrings clarifying that "In MVP, user always has 15 credits. We show it for demonstration"

### Testing (Step 7)

- Visit `/profile`, see "Credits: 15"
- If the user had some usage, ensure it shows the updated value if the backend tracks it
- Possibly do an integration test: "Sign in → check user is default 15 credits → do 2 chat messages → see if it's 13 now?"

## Step 8: Mobile-First Polishing & Partial Ingestion Progress

1. Mobile Layout:
   - Ensure each main page (Home, Explore, Agent Chat, Profile) looks good on 375px wide. Buttons ~44px tall
   - Bottom Nav never overlaps text input. Possibly add extra margin at the bottom of main content to avoid iPhone "home bar" issues

2. Partial Ingestion Feedback:
   - If scraping a large channel, show progress or an estimate "Scraping 5 / 100 messages." The backend might provide a `last_msg_id` or a "progress" field
   - Minimally mention it with a `<ProgressBar />` from ShadCN or your own

### Testing (Step 8)

- Use Chrome dev tools or a real phone to confirm the layout
- Test large channel ingestion, confirm the progress bar updates or at least a "Scraping in progress" spinner

## Step 9: Logging & Testing Approach

1. Logging:
   - Create a small `logger.ts` or similar in `frontend/logs/` if you need file-based logs for server components
   - For client code, you might do `console.log` or store logs in a minimal local array
   - If you have Next.js server routes (like API routes in `app/api/`), you can write those logs to `frontend/logs/frontend.log` with `fs.appendFileSync`
   - Keep lines minimal but docstrings for function usage

2. Testing:
   - Unit Tests: with Jest or React Testing Library for components (like the `BottomNav`, chat input)
   - Integration: Use Playwright or Cypress to simulate:
     1. Visiting the Home page, entering a search, viewing search results
     2. Going to Explore, creating an agent, verifying it appears, opening chat
   - One environment for MVP: no separate dev/prod config

### Integration Check (Step 9)

- Run `npm run test` or `npx playwright test`
- If logging works, you can open `frontend/logs/frontend.log` to see search queries or ingestion logs for any server components you have

## Step 10: Final Local Integration & "No Deployment Yet"

1. No final Vercel deployment steps. We remain local for MVP.

2. Ensure all pages & routes call the backend endpoints:
   - AI search → `POST /search`
   - Agent creation → `POST /agent/create`
   - Agent chat → `POST /agent/{agent_id}/chat`
   - Explore listing → optional `GET /agent` if the backend provides it
   - Profile → optional `GET /user` or embed user info in a minimal session approach

3. Local Confirmation:
   - Start the backend on `localhost:8000`
   - Start the frontend on `localhost:3000`
   - Perform the entire flow:
     - Home: "AI-Search" → do a query → see results (Summary / By Author) or a minimal result if you implemented the RAG unify approach
     - Explore: create an agent → partial ingestion progress → agent ready → open agent chat → message
     - Profile: see 15 credits, see if usage lowers it if the backend enforces usage

### Integration Check (Step 10)

- A final manual test:
  - Everything is local, no domain hosting
  - If you want to do a final "MVP is done" sign-off, you confirm each main feature page is functional
  - If all passes, the MVP is ready for demonstration or your next iteration

# Summary

By following these 10 steps, you'll build a mobile-first Next.js 13 frontend with ShadCN UI components, a unified color palette, minimal logging in `frontend/logs/`, partial ingestion progress for Telegram scraping, a Profile page with default 15 credits for the user, and an integrated testing approach (unit + integration). No mention of "social media commenting" is included here; that feature is reserved for a future iteration. The final environment remains local until you decide to deploy.