# Smart Identity Generator

> “We don’t just create ID cards; we secure identities.”

An AI-powered end-to-end platform that transforms ordinary ID cards into secure, intelligent and verifiable digital identities. It ingests data from forms, photos or bulk spreadsheets, detects faces, learns institution branding, renders themed ID cards, and issues QR/NFC tokens for one-tap verification with live attendance tracking.

## System Highlights

- **AI face intelligence** – automatic detection, clean-up, alignment and transparent background.
- **Auto branding** – extracts logo palettes and typography cues to theme each institution automatically.
- **Secure tokens** – generates encrypted QR/NFC payloads mapped per identity for instant verification.
- **Bulk generation** – upload CSV/Excel with photo URLs for hundreds of cards per minute.
- **Cloud dashboard** – React + Tailwind glassmorphic UI with live verification feed.
- **Exports** – 300 DPI PNG, PDF print sheets and mobile wallet cards.

## Project Structure

```
backend/    FastAPI + SQLModel service (face AI, branding, tokens, exports, auth)
frontend/   Vite + React dashboard (upload form, bulk, preview, scanner, live feed)
storage/    Generated assets (created at runtime)
```

## Backend (FastAPI)

### Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # PowerShell
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Key Endpoints

| Endpoint | Description |
| --- | --- |
| `POST /api/auth/register` | Operator onboarding (hashed password + JWT) |
| `POST /api/institutions` | Create institution shell |
| `POST /api/institutions/{id}/branding` | Upload logo → palette + typography detection |
| `POST /api/identities` | Single ID generation (form + portrait) |
| `POST /api/identities/bulk` | CSV/Excel ingestion with optional `photo_url` |
| `GET /api/identities` | List generated identities + asset URLs |
| `POST /api/scan/verify` | Validate QR/NFC token, log attendance, broadcast |
| `WS /api/scan/live` | Live verification stream for dashboards |

### Pipeline

1. Data ingestion (form/photo/CSV)  
2. Face detection + crop + alignment (OpenCV + Pillow)  
3. Branding intelligence (ColorThief)  
4. Card rendering (Pillow glassmorphism template)  
5. Tokenization (JWT + random NFC hex) + QR image  
6. Export PNG/PDF/mobile wallet  
7. Real-time verification + attendance logging  

## Frontend (React + Vite)

### Setup

```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_BASE_URL` / `VITE_WS_BASE_URL` in `.env` if backend isn’t `http://localhost:8000`.

### Screens

- **Hero dashboard** – positioning, elevator pitch, taglines, neon metrics.
- **Single generator** – drag portrait → auto theme + downloads.
- **Bulk console** – Excel/CSV ingestion hints.
- **Live feed** – WebSocket stream of scans (“Print it. Scan it. Trust it.”).
- **Poster brief** – art direction copy for marketing collateral.
- **Scanner web app** – paste QR/NFC payload for instant verification demo.

## Poster / UI Art Direction

“Futuristic holographic smart ID cards, glowing QR, NFC symbol, blue-purple neon cyber-tech gradients, face detection frame, glassmorphism, premium minimal high-tech UI, glowing title ‘Smart Identity Generator’, modern clean typography, digital authentication theme.”

## Taglines

- Identity that protects itself.
- Print it. Scan it. Trust it.
- Identity meets intelligence.
- Smart IDs for smarter institutions.
- Identify. Verify. Simplify.
- A card that verifies itself.
- Your identity, now intelligent.

## Roadmap Ideas

- Plug in cloud vision APIs for even higher accuracy.
- Apple/Google wallet pass packaging.
- Attendance analytics + anomaly detection.
- Hardware NFC provisioning.

## License

MIT – customize freely for hackathons, POCs or production pilots.

