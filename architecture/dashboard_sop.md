# SOP: Dashboard

## Goal
Serve a beautiful, interactive web dashboard that displays scraped articles. Users can filter by source and save articles that persist across sessions.

## Endpoints
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Serve dashboard HTML |
| GET | `/api/articles` | Return cached articles JSON |
| POST | `/api/refresh` | Force fresh scrape, return new articles |
| GET | `/logo` | Serve the Neatly logo |

## Frontend Behavior
1. On load → fetch `/api/articles`
2. Render article cards in grid
3. Apply active source filter
4. Mark saved articles from localStorage
5. Refresh button → POST `/api/refresh` → re-render

## Saved Articles
- localStorage key: `ag_saved_articles`
- Stores array of article IDs: `["id1", "id2"]`
- Persists across page refreshes
- "Saved" filter pill shows only saved articles

## Filter Pills
- All (default)
- Ben's Bites
- The AI Rundown
- Reddit
- Saved (shows saved count badge)

## Design Rules
- Background: #08090A
- Accent: #21c9d0 (teal)
- Cards: #0F1011 with 1px rgba(255,255,255,0.06) border
- Source badges: color-coded per source
- Font: SF Pro Display (headings), Inter (body)
- Card hover: lift + teal border glow

## Source Badge Colors
- Ben's Bites: #21c9d0
- The AI Rundown: #8B5CF6
- Reddit: #FF6314
