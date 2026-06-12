# ⚽ Apuesta Mundial 2026 — Verisure Chile

App de apuesta amistosa para el equipo, con resultados en tiempo real del Mundial FIFA 2026.

## ✨ Funcionalidades

- 🏳️ Cada participante elige su equipo campeón con bandera
- 💰 Registro de monto apostado con pozo acumulado
- 📅 Partidos en vivo con marcador, tarjetas 🟨🟥 y penales
- 🔒 Contraseña individual para editar apuesta
- 🎨 Modo demo sin API Key (datos de ejemplo)

---

## 🚀 Deploy en Streamlit Cloud (gratis)

### 1. Sube el código a GitHub

```bash
git init
git add .
git commit -m "feat: apuesta mundial 2026"
git remote add origin https://github.com/TU_USUARIO/mundial-apuestas.git
git push -u origin main
```

### 2. Despliega en Streamlit Cloud

1. Ve a [share.streamlit.io](https://share.streamlit.io) e inicia sesión con GitHub
2. Clic en **"New app"**
3. Selecciona tu repo `mundial-apuestas`, rama `main`, archivo `app.py`
4. En **"Advanced settings → Secrets"**, pega:

```toml
FOOTBALL_API_KEY = "tu_key_real_aqui"
```

5. Clic en **Deploy** — listo en ~2 minutos ✅

---

## 🔑 Obtener API Key gratuita (football-data.org)

1. Regístrate en [football-data.org/client/login](https://www.football-data.org/client/login)
2. Recibirás la API Key por email
3. El tier gratuito incluye:
   - ✅ Resultados del Mundial FIFA 2026
   - ✅ Marcadores en tiempo real (delay ~1 min)
   - ✅ Alineaciones y eventos (goles, tarjetas)
   - ⚠️  Sin penales detallados en tier gratuito (sí marca si hubo penales)

---

## 🖥️ Ejecución local

```bash
pip install -r requirements.txt

# Agrega tu API Key en .streamlit/secrets.toml
streamlit run app.py
```

---

## 📁 Estructura del proyecto

```
mundial-apuestas/
├── app.py                    # App principal Streamlit
├── requirements.txt          # Dependencias Python
├── apuestas.json             # Datos de apuestas (se crea automáticamente)
├── .streamlit/
│   ├── config.toml           # Tema oscuro
│   └── secrets.toml          # ⚠️ NO subir a Git
├── .gitignore
└── README.md
```

---

## 🛠️ Notas técnicas

- Los datos de partidos se actualizan cada **3 minutos** (cache automático)
- `apuestas.json` se almacena localmente; en Streamlit Cloud persiste entre reinicios normales pero se borra con redeploys. Para persistencia robusta, considera migrar a **Supabase** (ya tienes experiencia).
- Las contraseñas se guardan como **SHA-256 hash** (nunca en texto plano)

---

*Hecho con ❤️ para el equipo CI&C — Verisure Chile*
