# Task Plan — Antigravity News Dashboard

## North Star
Build a beautiful, interactive web dashboard that scrapes and displays the latest AI news articles (last 24 hours) from newsletters and Reddit. Users can save articles that persist on refresh. Eventually backed by Supabase.

## Phases

### Phase 0: Initialization ✅
- [x] Project memory files created
- [x] claude.md initialized
- [ ] Data schema confirmed
- [ ] Blueprint approved

### Phase 1: Blueprint (In Progress)
- [x] Discovery questions answered
- [ ] Research newsletter scraping strategies (Ben's Bytes, AI Rundown, Reddit)
- [ ] Define JSON data schema in claude.md
- [ ] Confirm payload shape with user

### Phase 2: Link
- [ ] Build scraper tool for Ben's Bytes
- [ ] Build scraper tool for AI Rundown
- [ ] Build scraper tool for Reddit
- [ ] Verify all sources return data correctly

### Phase 3: Architect
- [ ] Flask/FastAPI server with scraping endpoints
- [ ] 24-hour caching layer
- [ ] Article save/persist logic (localStorage → Supabase later)
- [ ] Write architecture SOPs

### Phase 4: Stylize
- [ ] Design and build dashboard UI (HTML/CSS/JS)
- [ ] Beautiful card-based article layout
- [ ] Save article interaction
- [ ] Source filtering UI
- [ ] Responsive design

### Phase 5: Trigger
- [ ] Scheduler (24hr auto-refresh)
- [ ] Supabase integration (future)
- [ ] Deployment

## Current Focus
Phase 1 → Research scraping strategies for sources
