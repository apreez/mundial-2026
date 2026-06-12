import streamlit as st
import json
import os
import hashlib
from datetime import datetime
from pathlib import Path
import requests

st.set_page_config(
    page_title="🏆 Apuesta Mundial 2026",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE  = "apuestas.json"
API_BASE   = "https://api.football-data.org/v4"

# ── Diccionario de banderas (nombres en español, inglés, TLA y variantes) ────
EQUIPOS = {
    "Argentina":"🇦🇷","Brazil":"🇧🇷","Brasil":"🇧🇷",
    "Mexico":"🇲🇽","México":"🇲🇽","MX":"🇲🇽",
    "United States":"🇺🇸","USA":"🇺🇸","Estados Unidos":"🇺🇸","US":"🇺🇸",
    "Canada":"🇨🇦","Canadá":"🇨🇦","CA":"🇨🇦",
    "Colombia":"🇨🇴","CO":"🇨🇴",
    "Uruguay":"🇺🇾","UY":"🇺🇾",
    "Ecuador":"🇪🇨","EC":"🇪🇨",
    "Chile":"🇨🇱","CL":"🇨🇱",
    "Peru":"🇵🇪","Perú":"🇵🇪","PE":"🇵🇪",
    "Venezuela":"🇻🇪","VE":"🇻🇪",
    "Bolivia":"🇧🇴","BO":"🇧🇴",
    "Paraguay":"🇵🇾","PY":"🇵🇾",
    "Panama":"🇵🇦","Panamá":"🇵🇦","PA":"🇵🇦",
    "Costa Rica":"🇨🇷","CR":"🇨🇷",
    "Honduras":"🇭🇳","HN":"🇭🇳",
    "Jamaica":"🇯🇲","JM":"🇯🇲",
    "France":"🇫🇷","Francia":"🇫🇷","FR":"🇫🇷",
    "Spain":"🇪🇸","España":"🇪🇸","ES":"🇪🇸",
    "England":"🏴󠁧󠁢󠁥󠁮󠁧󠁿","Inglaterra":"🏴󠁧󠁢󠁥󠁮󠁧󠁿","ENG":"🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Germany":"🇩🇪","Alemania":"🇩🇪","DE":"🇩🇪","GER":"🇩🇪",
    "Portugal":"🇵🇹","PT":"🇵🇹",
    "Netherlands":"🇳🇱","Países Bajos":"🇳🇱","NL":"🇳🇱",
    "Belgium":"🇧🇪","Bélgica":"🇧🇪","BE":"🇧🇪",
    "Italy":"🇮🇹","Italia":"🇮🇹","IT":"🇮🇹",
    "Croatia":"🇭🇷","Croacia":"🇭🇷","HR":"🇭🇷",
    "Switzerland":"🇨🇭","Suiza":"🇨🇭","CH":"🇨🇭",
    "Austria":"🇦🇹","AT":"🇦🇹",
    "Poland":"🇵🇱","Polonia":"🇵🇱","PL":"🇵🇱",
    "Denmark":"🇩🇰","Dinamarca":"🇩🇰","DK":"🇩🇰",
    "Serbia":"🇷🇸","RS":"🇷🇸",
    "Ukraine":"🇺🇦","Ucrania":"🇺🇦","UA":"🇺🇦",
    "Romania":"🇷🇴","Rumania":"🇷🇴","RO":"🇷🇴",
    "Slovakia":"🇸🇰","Eslovaquia":"🇸🇰","SK":"🇸🇰",
    "Turkey":"🇹🇷","Turkiye":"🇹🇷","Turquía":"🇹🇷","TR":"🇹🇷",
    "Greece":"🇬🇷","Grecia":"🇬🇷","GR":"🇬🇷",
    "Scotland":"🏴󠁧󠁢󠁳󠁣󠁴󠁿","Escocia":"🏴󠁧󠁢󠁳󠁣󠁴󠁿","SCO":"🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "Czech Republic":"🇨🇿","Czechia":"🇨🇿","República Checa":"🇨🇿","CZ":"🇨🇿",
    "Hungary":"🇭🇺","Hungría":"🇭🇺","HU":"🇭🇺",
    "Albania":"🇦🇱","AL":"🇦🇱",
    "Georgia":"🇬🇪","GE":"🇬🇪",
    "Slovenia":"🇸🇮","Eslovenia":"🇸🇮","SI":"🇸🇮",
    "Morocco":"🇲🇦","Marruecos":"🇲🇦","MA":"🇲🇦",
    "Senegal":"🇸🇳","SN":"🇸🇳",
    "Nigeria":"🇳🇬","NG":"🇳🇬",
    "Egypt":"🇪🇬","Egipto":"🇪🇬","EG":"🇪🇬",
    "Cameroon":"🇨🇲","Camerún":"🇨🇲","CM":"🇨🇲",
    "South Africa":"🇿🇦","Sudáfrica":"🇿🇦","ZA":"🇿🇦","RSA":"🇿🇦",
    "Ghana":"🇬🇭","GH":"🇬🇭",
    "Ivory Coast":"🇨🇮","Côte d'Ivoire":"🇨🇮","CI":"🇨🇮",
    "Algeria":"🇩🇿","Argelia":"🇩🇿","DZ":"🇩🇿",
    "Tunisia":"🇹🇳","Túnez":"🇹🇳","TN":"🇹🇳",
    "Mali":"🇲🇱","ML":"🇲🇱",
    "Congo DR":"🇨🇩","DR Congo":"🇨🇩","CD":"🇨🇩",
    "Tanzania":"🇹🇿","TZ":"🇹🇿",
    "Japan":"🇯🇵","Japón":"🇯🇵","JP":"🇯🇵",
    "South Korea":"🇰🇷","Korea Republic":"🇰🇷","Corea del Sur":"🇰🇷","KR":"🇰🇷",
    "Saudi Arabia":"🇸🇦","Arabia Saudita":"🇸🇦","SA":"🇸🇦","KSA":"🇸🇦",
    "Iran":"🇮🇷","IR":"🇮🇷",
    "Australia":"🇦🇺","AU":"🇦🇺",
    "New Zealand":"🇳🇿","Nueva Zelanda":"🇳🇿","NZ":"🇳🇿",
    "Qatar":"🇶🇦","QA":"🇶🇦",
    "China":"🇨🇳","CN":"🇨🇳",
    "Indonesia":"🇮🇩","ID":"🇮🇩",
    "Uzbekistan":"🇺🇿","Uzbekistán":"🇺🇿","UZ":"🇺🇿",
}

# Selector para el formulario de apuestas (solo español, sin duplicados)
EQUIPOS_SELECTOR = {
    "Argentina":"🇦🇷","Brasil":"🇧🇷","Francia":"🇫🇷","España":"🇪🇸","Inglaterra":"🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Alemania":"🇩🇪","Portugal":"🇵🇹","Países Bajos":"🇳🇱","Uruguay":"🇺🇾","Colombia":"🇨🇴",
    "México":"🇲🇽","Estados Unidos":"🇺🇸","Canadá":"🇨🇦","Marruecos":"🇲🇦","Senegal":"🇸🇳",
    "Japón":"🇯🇵","Corea del Sur":"🇰🇷","Australia":"🇦🇺","Ecuador":"🇪🇨","Chile":"🇨🇱",
    "Perú":"🇵🇪","Venezuela":"🇻🇪","Bolivia":"🇧🇴","Paraguay":"🇵🇾","Suiza":"🇨🇭",
    "Bélgica":"🇧🇪","Italia":"🇮🇹","Croacia":"🇭🇷","Turquía":"🇹🇷","Austria":"🇦🇹",
    "Polonia":"🇵🇱","Dinamarca":"🇩🇰","Serbia":"🇷🇸","Nigeria":"🇳🇬","Arabia Saudita":"🇸🇦",
    "Panamá":"🇵🇦","Costa Rica":"🇨🇷","República Checa":"🇨🇿","Sudáfrica":"🇿🇦",
}

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600;700&display=swap');
  :root{--verde:#00C853;--oro:#FFD600;--rojo:#E53935;--card:#161B22;--borde:#30363D;--texto:#E6EDF3;}
  html,body,[class*="css"]{font-family:'Inter',sans-serif;}
  .titulo-mundial{font-family:'Bebas Neue',sans-serif;font-size:3.2rem;letter-spacing:4px;
    background:linear-gradient(135deg,var(--oro) 0%,var(--verde) 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;text-align:center;margin-bottom:.2rem;}
  .subtitulo{text-align:center;color:#8B949E;font-size:.9rem;margin-bottom:2rem;letter-spacing:2px;text-transform:uppercase;}
  .apuesta-card{background:var(--card);border:1px solid var(--borde);border-radius:12px;
    padding:1.2rem 1.5rem;margin-bottom:.8rem;display:flex;align-items:center;justify-content:space-between;}
  .apuesta-card:hover{border-color:var(--oro);}
  .pos-badge{font-family:'Bebas Neue',sans-serif;font-size:1.8rem;width:2.2rem;text-align:center;}
  .pos-1{color:var(--oro);} .pos-2{color:#C0C0C0;} .pos-3{color:#CD7F32;}
  .monto-badge{background:linear-gradient(135deg,var(--verde),#00897B);color:#000;font-weight:700;
    font-size:.9rem;padding:.3rem .8rem;border-radius:20px;}
  .partido-card{background:var(--card);border:1px solid var(--borde);border-radius:12px;
    padding:1.2rem;margin-bottom:.8rem;text-align:center;}
  .score-big{font-family:'Bebas Neue',sans-serif;font-size:2.8rem;letter-spacing:6px;color:var(--texto);}
  .tarjeta-roja{display:inline-block;background:#E53935;width:14px;height:18px;border-radius:2px;margin:0 2px;}
  .tarjeta-amarilla{display:inline-block;background:#FDD835;width:14px;height:18px;border-radius:2px;margin:0 2px;}
  .estado-live{color:var(--rojo);font-weight:700;font-size:.75rem;animation:pulse 1.2s infinite;}
  .estado-fin{color:#8B949E;font-size:.75rem;}
  .estado-pronto{color:var(--verde);font-size:.75rem;}
  @keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
  .metric-box{background:var(--card);border:1px solid var(--borde);border-radius:10px;padding:1rem;text-align:center;}
  .metric-val{font-family:'Bebas Neue',sans-serif;font-size:2rem;color:var(--oro);}
  .metric-lbl{font-size:.78rem;color:#8B949E;text-transform:uppercase;letter-spacing:1px;}
  div[data-testid="stSidebar"]{background:var(--card)!important;}
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def cargar_apuestas():
    if Path(DATA_FILE).exists():
        with open(DATA_FILE,"r",encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_apuestas(data):
    with open(DATA_FILE,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

def hash_pass(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def verificar_password(nombre, pw, apuestas):
    if nombre not in apuestas:
        return False
    return apuestas[nombre]["password_hash"] == hash_pass(pw)

def bandera_pais(nombre):
    if not nombre or not isinstance(nombre, str):
        return "🏳️"
    # Exacto primero
    if nombre in EQUIPOS:
        return EQUIPOS[nombre]
    # Parcial case-insensitive
    nombre_l = nombre.lower().strip()
    for k, v in EQUIPOS.items():
        if k.lower() in nombre_l or nombre_l in k.lower():
            return v
    return "🏳️"

# ── API ───────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=180)
def obtener_partidos():
    api_key = st.secrets.get("FOOTBALL_API_KEY","") or st.session_state.get("api_key_tmp","")
    if not api_key:
        return []
    headers = {"X-Auth-Token": api_key}
    for comp in ["WC", "2000"]:
        try:
            r = requests.get(f"{API_BASE}/competitions/{comp}/matches", headers=headers, timeout=10)
            if r.status_code == 200:
                return r.json().get("matches", [])
        except Exception as e:
            st.warning(f"Error API: {e}")
    return []

def formatear_partido(m):
    ht = m.get("homeTeam", {})
    at = m.get("awayTeam", {})
    home = ht.get("name") or ht.get("shortName") or ht.get("tla") or "?"
    away = at.get("name") or at.get("shortName") or at.get("tla") or "?"
    # bandera: intentar con name y tla
    flag_h = bandera_pais(home)
    if flag_h == "🏳️":
        flag_h = bandera_pais(ht.get("tla",""))
    flag_a = bandera_pais(away)
    if flag_a == "🏳️":
        flag_a = bandera_pais(at.get("tla",""))

    score = m.get("score", {})
    full  = score.get("fullTime", {})
    pen_h = None; pen_a = None
    if score.get("penalties"):
        pen_h = score["penalties"].get("home")
        pen_a = score["penalties"].get("away")

    return {
        "home": home, "away": away,
        "flag_home": flag_h, "flag_away": flag_a,
        "goles_home": full.get("home"), "goles_away": full.get("away"),
        "penalties_home": pen_h, "penalties_away": pen_a,
        "status": m.get("status","SCHEDULED"),
        "fecha": m.get("utcDate","")[:10],
        "hora":  m.get("utcDate","")[11:16],
        "etapa": m.get("stage",""),
        "grupo": m.get("group","") or "",
        "cards_home_r":0,"cards_home_y":0,
        "cards_away_r":0,"cards_away_y":0,
        "id": m.get("id"),
    }

# ── Datos demo ────────────────────────────────────────────────────────────────
PARTIDOS_DEMO = [
    {"home":"Argentina","away":"México","flag_home":"🇦🇷","flag_away":"🇲🇽",
     "goles_home":2,"goles_away":0,"penalties_home":None,"penalties_away":None,
     "status":"FINISHED","fecha":"2026-06-15","hora":"18:00","etapa":"GROUP_STAGE","grupo":"Grupo A",
     "cards_home_r":0,"cards_home_y":1,"cards_away_r":1,"cards_away_y":2,"id":1},
    {"home":"Brasil","away":"España","flag_home":"🇧🇷","flag_away":"🇪🇸",
     "goles_home":1,"goles_away":1,"penalties_home":None,"penalties_away":None,
     "status":"FINISHED","fecha":"2026-06-16","hora":"21:00","etapa":"GROUP_STAGE","grupo":"Grupo B",
     "cards_home_r":0,"cards_home_y":3,"cards_away_r":0,"cards_away_y":2,"id":2},
    {"home":"Francia","away":"Alemania","flag_home":"🇫🇷","flag_away":"🇩🇪",
     "goles_home":None,"goles_away":None,"penalties_home":None,"penalties_away":None,
     "status":"SCHEDULED","fecha":"2026-06-17","hora":"20:00","etapa":"GROUP_STAGE","grupo":"Grupo C",
     "cards_home_r":0,"cards_home_y":0,"cards_away_r":0,"cards_away_y":0,"id":3},
]

def render_partido(p):
    status_map = {
        "FINISHED": ("<span class='estado-fin'>⚫ Finalizado</span>", True),
        "IN_PLAY":  ("<span class='estado-live'>🔴 EN VIVO</span>", True),
        "PAUSED":   ("<span class='estado-live'>🟡 Descanso</span>", True),
        "SCHEDULED":("<span class='estado-pronto'>🟢 Próximo</span>", False),
        "TIMED":    ("<span class='estado-pronto'>🟢 Próximo</span>", False),
    }
    estado_html, mostrar_score = status_map.get(p["status"], ("", False))

    if mostrar_score and p["goles_home"] is not None:
        score_html = f"<div class='score-big'>{p['goles_home']} – {p['goles_away']}</div>"
        if p.get("penalties_home") is not None:
            score_html += f"<div style='color:#8B949E;font-size:.8rem'>Penales: {p['penalties_home']} – {p['penalties_away']}</div>"
    else:
        score_html = f"<div style='font-size:.9rem;color:#8B949E'>{p['hora']} UTC</div>"

    def tarjetas_html(r, y):
        h = "".join(["<span class='tarjeta-roja'></span>"]*r + ["<span class='tarjeta-amarilla'></span>"]*y)
        return h or "—"

    grupo_txt = f"<span style='font-size:.7rem;color:#8B949E'>{p['grupo'] or p['etapa']}</span>" if (p.get('grupo') or p.get('etapa')) else ""

    st.markdown(f"""
    <div class='partido-card'>
      <div style='margin-bottom:.4rem'>{estado_html} &nbsp; {grupo_txt}</div>
      <div style='display:flex;align-items:center;justify-content:space-between'>
        <div style='text-align:right;flex:1'>
          <div style='font-size:2rem'>{p['flag_home']}</div>
          <div style='font-weight:600;font-size:.9rem'>{p['home']}</div>
          <div style='margin-top:4px'>{tarjetas_html(p['cards_home_r'],p['cards_home_y'])}</div>
        </div>
        <div style='flex:1;text-align:center'>{score_html}</div>
        <div style='text-align:left;flex:1'>
          <div style='font-size:2rem'>{p['flag_away']}</div>
          <div style='font-weight:600;font-size:.9rem'>{p['away']}</div>
          <div style='margin-top:4px'>{tarjetas_html(p['cards_away_r'],p['cards_away_y'])}</div>
        </div>
      </div>
      <div style='font-size:.75rem;color:#8B949E;margin-top:.5rem'>{p['fecha']}</div>
    </div>
    """, unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuración")
    api_key_input = st.text_input("🔑 API Key (football-data.org)", type="password",
                                   help="Regístrate gratis en football-data.org/client/login")
    if api_key_input:
        st.session_state["api_key_tmp"] = api_key_input

    modo_demo = not bool(st.secrets.get("FOOTBALL_API_KEY","") or st.session_state.get("api_key_tmp",""))
    if modo_demo:
        st.info("🎮 **Modo Demo** — datos de ejemplo.\nAgrega tu API Key para datos reales.")
    else:
        st.success("✅ API Key activa")
        if st.button("🔄 Actualizar datos"):
            obtener_partidos.clear()
            st.rerun()

    st.divider()
    apuestas_all = cargar_apuestas()
    total = sum(a.get("monto",0) for a in apuestas_all.values())
    st.markdown("### 🏦 Fondo del pozo")
    st.markdown(f"<div style='text-align:center'><span style='font-size:2.5rem;font-weight:700;color:#FFD600'>${total:,.0f}</span><br><span style='font-size:.8rem;color:#8B949E'>CLP en juego</span></div>", unsafe_allow_html=True)
    st.divider()
    st.markdown("### 👥 Participantes")
    for nombre, data in apuestas_all.items():
        equipo = data.get("equipo","?")
        flag   = EQUIPOS_SELECTOR.get(equipo, bandera_pais(equipo))
        st.markdown(f"**{flag} {nombre}** → {equipo}")

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("<div class='titulo-mundial'>⚽ APUESTA MUNDIAL 2026 ⚽</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitulo'>La apuesta amistosa del equipo · Verisure Chile</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🏆 Tabla de apuestas","📅 Partidos","➕ Registrar apuesta","✏️ Editar mi apuesta"])

# ── TAB 1: TABLA ──────────────────────────────────────────────────────────────
with tab1:
    apuestas = cargar_apuestas()
    if not apuestas:
        st.info("Aún no hay apuestas registradas. ¡Sé el primero en la pestaña **➕ Registrar**!")
    else:
        st.markdown("#### 🥇 Ranking de Apostadores")
        c1,c2,c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='metric-box'><div class='metric-val'>{len(apuestas)}</div><div class='metric-lbl'>Participantes</div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='metric-box'><div class='metric-val'>${total:,.0f}</div><div class='metric-lbl'>Pozo total (CLP)</div></div>", unsafe_allow_html=True)
        with c3:
            montos = [a.get("monto",0) for a in apuestas.values()]
            st.markdown(f"<div class='metric-box'><div class='metric-val'>${max(montos):,.0f}</div><div class='metric-lbl'>Apuesta máxima</div></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        ranking = sorted(apuestas.items(), key=lambda x: x[1].get("monto",0), reverse=True)
        medallas = {1:"🥇",2:"🥈",3:"🥉"}
        clases   = {1:"pos-1",2:"pos-2",3:"pos-3"}

        for i,(nombre,data) in enumerate(ranking,1):
            equipo = data.get("equipo","?")
            monto  = data.get("monto",0)
            flag   = EQUIPOS_SELECTOR.get(equipo, bandera_pais(equipo))
            nota   = data.get("nota","")
            medal  = medallas.get(i,f"#{i}")
            cls    = clases.get(i,"")
            st.markdown(f"""
            <div class='apuesta-card'>
              <span class='pos-badge {cls}'>{medal}</span>
              <span style='font-size:2.2rem;margin:0 .8rem'>{flag}</span>
              <div style='flex:1'>
                <div style='font-weight:700;font-size:1.05rem'>{nombre}</div>
                <div style='color:#8B949E;font-size:.85rem'>{equipo}{f" · {nota}" if nota else ""}</div>
              </div>
              <span class='monto-badge'>${monto:,.0f} CLP</span>
            </div>""", unsafe_allow_html=True)
        st.caption(f"Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# ── TAB 2: PARTIDOS ───────────────────────────────────────────────────────────
with tab2:
    if modo_demo:
        partidos_raw = PARTIDOS_DEMO
        st.caption("📌 Datos de ejemplo — conecta tu API Key para resultados reales del Mundial 2026")
    else:
        with st.spinner("Cargando partidos..."):
            raw = obtener_partidos()
            partidos_raw = [formatear_partido(m) for m in raw] if raw else PARTIDOS_DEMO

    col_f1,col_f2 = st.columns([2,3])
    with col_f1:
        filtro_estado = st.selectbox("Estado",["Todos","EN VIVO","Finalizados","Próximos"])
    with col_f2:
        grupos_disp = sorted(set(p.get("grupo","") for p in partidos_raw if p.get("grupo")))
        filtro_grupo = st.selectbox("Grupo / Etapa",["Todos"]+grupos_disp) if grupos_disp else "Todos"

    estado_map = {"EN VIVO":["IN_PLAY","PAUSED"],"Finalizados":["FINISHED"],"Próximos":["SCHEDULED","TIMED"]}
    pf = partidos_raw
    if filtro_estado != "Todos":
        pf = [p for p in pf if p["status"] in estado_map.get(filtro_estado,[])]
    if filtro_grupo != "Todos":
        pf = [p for p in pf if p.get("grupo")==filtro_grupo]

    st.markdown(f"**{len(pf)} partido(s)**")
    for p in pf:
        render_partido(p)

# ── TAB 3: REGISTRAR ──────────────────────────────────────────────────────────
with tab3:
    st.markdown("#### ➕ Nueva apuesta")
    apuestas_reg = cargar_apuestas()
    with st.form("form_registro"):
        nombre_nuevo = st.text_input("👤 Tu nombre", placeholder="Ej: Anibal")
        equipo_nuevo = st.selectbox("🏳️ Elige tu equipo campeón",
                                     sorted(EQUIPOS_SELECTOR.keys()),
                                     format_func=lambda x: f"{EQUIPOS_SELECTOR.get(x,'🏳️')} {x}")
        monto_nuevo  = st.number_input("💰 Monto de apuesta (CLP)",min_value=1000,max_value=5_000_000,value=10_000,step=1000)
        nota_nueva   = st.text_input("📝 Comentario opcional", placeholder="Ej: ¡Argentina campeón!")
        pass_nuevo   = st.text_input("🔒 Crea tu contraseña", type="password")
        pass_confirm = st.text_input("🔒 Confirma contraseña", type="password")
        submitted    = st.form_submit_button("✅ Registrar apuesta", use_container_width=True)

    if submitted:
        nombre_nuevo = nombre_nuevo.strip()
        if not nombre_nuevo:
            st.error("El nombre no puede estar vacío.")
        elif nombre_nuevo in apuestas_reg:
            st.error(f"**{nombre_nuevo}** ya tiene una apuesta. Ve a ✏️ Editar para modificarla.")
        elif not pass_nuevo:
            st.error("Debes crear una contraseña.")
        elif pass_nuevo != pass_confirm:
            st.error("Las contraseñas no coinciden.")
        else:
            apuestas_reg[nombre_nuevo] = {
                "equipo": equipo_nuevo, "monto": monto_nuevo, "nota": nota_nueva,
                "password_hash": hash_pass(pass_nuevo),
                "fecha_registro": datetime.now().strftime("%d/%m/%Y %H:%M"),
            }
            guardar_apuestas(apuestas_reg)
            flag = EQUIPOS_SELECTOR.get(equipo_nuevo,"🏳️")
            st.success(f"🎉 **{nombre_nuevo}** apostó **${monto_nuevo:,.0f} CLP** por {flag} **{equipo_nuevo}**. ¡Buena suerte!")
            st.balloons()

# ── TAB 4: EDITAR ─────────────────────────────────────────────────────────────
with tab4:
    st.markdown("#### ✏️ Modificar mi apuesta")
    apuestas_edit = cargar_apuestas()
    nombre_edit   = st.selectbox("👤 Selecciona tu nombre",["— elige —"]+sorted(apuestas_edit.keys()))

    if nombre_edit != "— elige —":
        pass_edit = st.text_input("🔒 Tu contraseña", type="password", key="pass_edit_input")
        if st.button("🔓 Verificar", key="btn_verificar"):
            if verificar_password(nombre_edit, pass_edit, apuestas_edit):
                st.session_state["edit_autorizado"] = nombre_edit
                st.success("✅ Contraseña correcta.")
            else:
                st.error("❌ Contraseña incorrecta.")

        if st.session_state.get("edit_autorizado") == nombre_edit:
            current = apuestas_edit[nombre_edit]
            opciones = sorted(EQUIPOS_SELECTOR.keys())
            idx_actual = opciones.index(current.get("equipo", opciones[0])) if current.get("equipo") in opciones else 0
            with st.form("form_edicion"):
                equipo_edit = st.selectbox("🏳️ Nuevo equipo campeón", opciones, index=idx_actual,
                                            format_func=lambda x: f"{EQUIPOS_SELECTOR.get(x,'🏳️')} {x}")
                monto_edit  = st.number_input("💰 Nuevo monto (CLP)",min_value=1000,max_value=5_000_000,
                                               value=int(current.get("monto",10000)),step=1000)
                nota_edit   = st.text_input("📝 Comentario", value=current.get("nota",""))
                pass_nueva  = st.text_input("🔑 Nueva contraseña (vacío = mantener actual)", type="password")
                save_btn    = st.form_submit_button("💾 Guardar cambios", use_container_width=True)

            if save_btn:
                apuestas_edit[nombre_edit].update({
                    "equipo": equipo_edit, "monto": monto_edit, "nota": nota_edit,
                    "ultima_edicion": datetime.now().strftime("%d/%m/%Y %H:%M"),
                })
                if pass_nueva:
                    apuestas_edit[nombre_edit]["password_hash"] = hash_pass(pass_nueva)
                guardar_apuestas(apuestas_edit)
                flag = EQUIPOS_SELECTOR.get(equipo_edit,"🏳️")
                st.success(f"✅ Actualizado: {flag} {equipo_edit} · ${monto_edit:,.0f} CLP")
                st.session_state["edit_autorizado"] = None
