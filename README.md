# Hallo Batam AI — Django Backend

**A separate backend implementation for a tourism-focused conversational assistant.**

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) ![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white) ![REST](https://img.shields.io/badge/REST_API-Django_REST_Framework-555555)

## Overview

This repository contains a Django REST Framework backend, tourism knowledge files and ingestion utilities. Its dependency list includes OpenAI, Google Gen AI, LangChain Community, ChromaDB and FastEmbed.

This is a related backend implementation; the current [Hallo Batam AI frontend](https://github.com/fahmifaldi61-tech/wisatabatam) is configured to use a Supabase chat endpoint.

## API

| Route | Purpose |
| --- | --- |
| `/api/chat/` | Chat API view |
| `/admin/` | Django administration |

## Repository structure

| Path | Purpose |
| --- | --- |
| `api/` | Chat API application |
| `backend_pariwisata/` | Django project configuration |
| `data_wisata/` | Tourism knowledge source |
| `ingest.py` | Ingestion utility |
| `isi_data.py` | Data preparation utility |
| `requirements.txt` | Python dependencies |
| `Procfile` | Gunicorn startup configuration |

## Local setup

```bash
git clone https://github.com/fahmifaldi61-tech/wisatabatam-backend..git
cd wisatabatam-backend.
python -m venv .venv
```

Activate the environment (Windows PowerShell: `.venv\Scripts\Activate.ps1`; macOS/Linux: `source .venv/bin/activate`), then:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Review the settings and configure required service credentials locally before using AI features. Keep credentials out of Git. External service availability and full runtime compatibility have not been verified.

## Related projects

[Frontend repository](https://github.com/fahmifaldi61-tech/wisatabatam) · [Developer portfolio](https://github.com/fahmifaldi61-tech/wisatabatam/blob/main/PORTFOLIO.md)
