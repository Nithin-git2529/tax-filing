# Tax Filing Demo (Educational)

A minimal demo showing a simplified tax workflow:
- Upload/read W-2-like data (sample CSV)
- Compute **estimated** tax with basic brackets (demo only)
- Simple UI + Flask API

> ⚠️ Not tax advice. Brackets/logic simplified for learning.

## Quick Start

### Backend
```bash
cd api
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python app.py
