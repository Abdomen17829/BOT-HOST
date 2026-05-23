<div align="center">

# SityStar AI Commander

[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)](https://t.me/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)](https://python.org)
[![AI Powered](https://img.shields.io/badge/AI-Powered-purple?logo=openai)](https://ai.com)
[![Bilingual](https://img.shields.io/badge/Language-EN%20%7C%20AR-orange.svg)](README.md)

</div>

---

## 🚀 Overview

**SityStar AI Commander** is a powerful Telegram bot that simplifies website deployment and SEO optimization. Deploy static websites to cloud platforms (Netlify/Vercel) directly from Telegram with AI-powered SEO analysis.

### Key Features

- **Instant Deployment**: Upload `.zip`, `.rar`, `.7z`, `.tar.gz`, or `.html` files directly via Telegram
- **AI-Powered SEO**: Automatic SEO analysis and optimization using Gemini, OpenAI, or OpenRouter
- **Multi-Cloud Hosting**: Deploy to Netlify or Vercel with your personal tokens
- **Database Flexibility**: Choose from Supabase, MongoDB, or Firebase for project storage
- **Bilingual Support**: Full English and Arabic localization
- **Encrypted Security**: AES-256 encryption for all stored credentials

---

## 📋 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Commands](#commands)
- [Supported Formats](#supported-formats)
- [Deployment Platforms](#deployment-platforms)
- [Database Providers](#database-providers)
- [AI Providers](#ai-providers)

---

## 🛠️ Installation

### Prerequisites

- Python 3.10 or higher
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- (Optional) Supabase, MongoDB, or Firebase credentials
- (Optional) Netlify or Vercel access token

### Setup

```bash
# Clone the repository
git clone https://github.com/Abdomen17829/BOT-HOST.git
cd BOT-HOST

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
touch .env && nano .env
# Edit .env with your credentials
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather | Yes |
| `SUPABASE_URL` | Supabase project URL | No |
| `SUPABASE_KEY` | Supabase API key | No |
| `GEMINI_API_KEY` | Google Gemini API key | No |
| `NETLIFY_ACCESS_TOKEN` | Netlify personal access token | No |
| `ENCRYPTION_KEY` | Auto-generated if not provided | No |

### Running the Bot

```bash
python bot.py
```

---

## 🎯 Usage

### Quick Start

1. Start a chat with your bot on Telegram
2. Send `/start` to begin
3. Choose your language (English or Arabic)
4. Configure your AI provider, database, and hosting in Settings
5. Send a `.zip` file or GitHub repo link to deploy

### Main Menu Options

| Button | Description |
|--------|-------------|
| 🚀 Deploy New Site | Upload and deploy a website |
| 📁 My Projects | View your deployed projects |
| ⚙️ Settings | Configure AI, Database, Hosting |
| ❓ Help | Show available commands |

---

## 📜 Commands

| Command | Description |
|---------|-------------|
| `/start` | Launch the main menu |
| `/deploy` | Start deployment process |
| `/projects` | View your deployed projects |
| `/settings` | Open configuration settings |
| `/status` | Check connection status |
| `/help` | Display help message |

---

## 📦 Supported Formats

- **Archive Files**: `.zip`, `.rar`, `.7z`, `.tar.gz`
- **Web Files**: `.html` (single file)
- **Repositories**: GitHub repository links

---

## ☁️ Deployment Platforms

### Netlify

- Deploy via File Digest API
- SHA1-based file verification
- Automatic site creation

### Vercel

- Full deployment support
- Custom project names
- Instant preview URLs

---

## 🗄️ Database Providers

- **Supabase**: PostgreSQL-based backend
- **MongoDB**: NoSQL database support
- **Firebase**: Google Firebase integration

---

## 🤖 AI Providers

| Provider | API Key Prefix | Features |
|----------|---------------|----------|
| OpenRouter | `sk-or-...` | Access to multiple models |
| OpenAI | `sk-...` | GPT models |
| Gemini | `AIza...` | Google's Gemini models |

---

## 🔐 Security

- All API keys and credentials are encrypted with AES-256 before storage
- No sensitive data is logged
- End-to-end encryption for database records

---

## 🌍 Language Support

| Language | Status |
|----------|--------|
| English | ✅ Complete |
| Arabic | ✅ Complete |

---

## 📊 Project Structure

```
├── bot.py                    # Main entry point
├── config.py                 # Configuration loader
├── requirements.txt          # Python dependencies
├── handlers/
│   ├── start.py             # Start command handler
│   ├── settings.py          # Settings configuration
│   ├── upload.py            # File upload handler
│   └── dashboard.py         # Projects dashboard
├── services/
│   ├── database.py          # Database operations
│   ├── dynamic_hosting.py   # Netlify/Vercel deployment
│   ├── ai_factory.py        # AI provider factory
│   ├── seo_engine.py        # SEO analysis
│   └── dynamic_db.py        # Dynamic database switching
└── utils/
    └── locales.py           # Localization strings
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📧 Contact

<div align="center">

[![Telegram](https://img.shields.io/badge/Telegram-@SityStar-2CA5E0?logo=telegram&logoColor=white)](https://t.me/SityStar)
[![Email](https://img.shields.io/badge/Email-contact@sitystar.com-red?logo=gmail&logoColor=white)](mailto:contact@sitystar.com)
[![Website](https://img.shields.io/badge/Website-sitystar.com-blue?logo=google-chrome&logoColor=white)](https://sitystar.com)

</div>

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ by Abdelrahman**

</div>
