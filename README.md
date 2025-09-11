
# MusicalTimeMachine

# 🎶 Musical Time Machine

A Flask-based mini project that integrates with the Spotify API to generate custom playlists.  
Users can log in with their Spotify account and create playlists based on:

- 📅 **Time Travel** (Billboard Hot 100 by date, extended with language support)
- 🎭 **Mood** (happy, sad, chill, party)
- 🌍 **Language** (English, Hindi, Tamil, Malayalam, etc.)
- 🎶 **Genre** (Pop, Rock, Jazz, Classical, EDM, Hip-Hop)
- 🔄 **Recently Played** (based on user’s listening history)

---

## 🚀 Features
- Spotify OAuth login for multiple users
- Billboard scraping for historical English top songs
- Extended support for regional languages using Spotify search
- Automatic playlist creation in user’s Spotify account
- Secure logout option

---

## 🛠️ Tech Stack
- **Backend**: Flask (Python)
- **Spotify Integration**: Spotipy
- **Frontend**: HTML, CSS (Jinja templates)
- **Web Scraping**: BeautifulSoup

---

## ⚙️ Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/musical-time-machine.git
   cd musical-time-machine
