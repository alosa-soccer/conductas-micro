import streamlit as st
import pandas as pd
import os

# --- 1. CONFIGURACIÓN Y ESTADO ---
st.set_page_config(page_title="Conductas Micro - Levante UD", layout="wide")

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = "Librería"

# --- 2. SISTEMA DE LOGIN ---
def check_login():
    with st.columns([1, 2, 1])[1]:
        st.title("🔐 Acceso Privado")
        st.subheader("Conductas Micro - Levante UD")
        with st.form("login_form"):
            usuario_input = st.text_input("Correo electrónico")
            password_input = st.text_input("Contraseña", type="password")
            boton_login = st.form_submit_button("Iniciar Sesión", use_container_width=True)
            if boton_login:
                usuarios_registrados = st.secrets["users"]
                if usuario_input in usuarios_registrados and usuarios_registrados[usuario_input] == password_input:
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("Usuario y/o contraseña incorrectos")

if not st.session_state.autenticado:
    check_login()
    st.stop()

# --- 3. ESTILO CSS (Global) ---
st.markdown("""
    <style>
    /* Tu CSS del campo de fútbol */
    [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] #campo-tactico) {
        background-color: #2e7d32 !important;
        position: relative !important;
        background-image: 
            radial-gradient(circle at 50% 50%, transparent 14%, rgba(255,255,255,0.4) 14.5%, transparent 15.5%),
            linear-gradient(to bottom, transparent 49.5%, rgba(255,255,255,0.4) 50%, transparent 50.5%),
            linear-gradient(to right, white 2px, transparent 2px),
            linear-gradient(to left, white 2px, transparent 2px),
            linear-gradient(to top, white 2px, transparent 2px),
            linear-gradient(to bottom, white 2px, transparent 2px) !important;
        background-size: 100% 100% !important;
        border-radius: 12px !important;
        padding: 45px 15px !important;
        border: 2px solid #1b5e20 !important;
    }
    /* Estilos de botones de posición */
    [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] #campo-tactico) .stButton > button {
        background-color: white !important;
        color: #1e1e1e !important;
        font-weight: bold !important;
        z-index: 2 !important;
    }
    [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] #campo-tactico) .stButton > button[kind="primary"] {
        background-color: #ff4b4b !important;
        color: white !important;
    }
    /* Mini campos */
    .mini-campo-container { display: flex; gap: 40px; justify-content: center; padding: 20px; background: #f8f9fa; border-radius: 12px; border: 1px solid #ddd; }
    .mini-campo { background-color: #2e7d32; border: 2px solid white; display: flex; color: white; font-size: 12px; font-weight: bold; text-align: center; }
    .campo-zonas { width: 160px; height: 180px; flex-direction: column; }
    .zona-v { flex: 1; border: 1px solid rgba(255,255,255,0.3); display: flex; align-items: center; justify-content: center; width: 100%; }
    .campo-carriles { width: 160px; height: 180px; flex-direction: row; }
    .carril-h { border: 1px solid rgba(255,255,255,0.3); display: flex; align-items: center; justify-content: center; height: 100%; }
    .carril-lat { flex: 1; } .carril-cen { flex: 2; }
    .highlight-red { background-color: #ff4b4b !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. CARGA DE DATOS ---
@st.cache_data
def cargar_datos():
    nombre_archivo = "./conductas_micro.xlsx"
    if not os.path.exists(nombre_archivo):
        return pd.DataFrame()
    hojas = ["P1", "P2-P3", "P4-P5", "P6", "P7-P11", "P8", "P10", "P9"]
    lista_df = []
    for hoja in hojas:
        try:
            df_temp = pd.read_excel(nombre_archivo, sheet_name=hoja)
            lista_df.append(df_temp)
        except: continue
    return pd.concat(lista_df, ignore_index=True) if lista_df else pd.DataFrame()

df_base = cargar_datos()

# --- 5. FUNCIÓN LIBRERÍA (Tu código original) ---
def pag_libreria():
    st.subheader("📍 Librería Táctica")
    if 'posicion_filtro' not in st.session_state:
        st.session_state.posicion_filtro = None

    col_campo, col_filtros = st.columns([1.3, 2], gap="large")

    with col_campo:
        st.write("📍 **Demarcación**")
        with st.container():
            st.markdown('<div id="campo-tactico" style="height:0px;"></div>', unsafe_allow_html=True)
            # Filas de botones (P11 a P1)
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1: 
                if st.button("P11", key="p11", type="primary" if st.session_state.posicion_filtro == "P7-P11" else "secondary"):
                    st.session_state.posicion_filtro = "P7-P11"; st.rerun()
            with c3:
                if st.button("P9", key="p9", type="primary" if st.session_state.posicion_filtro == "P9" else "secondary"):
                    st.session_state.posicion_filtro = "P9"; st.rerun()
            with c5:
                if st.button("P7", key="p7", type="primary" if st.session_state.posicion_filtro == "P7-P11" else "secondary"):
                    st.session_state.posicion_filtro = "P7-P11"; st.rerun()
            
            st.write("")
            c1, c2, c3, c4, c5 = st.columns(5)
            with c2:
                if st.button("P8", key="p8", type="primary" if st.session_state.posicion_filtro == "P8" else "secondary"):
                    st.session_state.posicion_filtro = "P8"; st.rerun()
            with c4:
                if st.button("P10", key="p10", type="primary" if st.session_state.posicion_filtro == "P10" else "secondary"):
                    st.session_state.posicion_filtro = "P10"; st.rerun()

            c1, c2, c3, c4, c5 = st.columns(5)
            with c3:
                if st.button("P6", key="p6", type="primary" if st.session_state.posicion_filtro == "P6" else "secondary"):
                    st.session_state.posicion_filtro = "P6"; st.rerun()

            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                if st.button("P3", key="p3", type="primary" if st.session_state.posicion_filtro == "P2-P3" else "secondary"):
                    st.session_state.posicion_filtro = "P2-P3"; st.rerun()
            with c2:
                if st.button("P4", key="p4", type="primary" if st.session_state.posicion_filtro == "P4-P5" else "secondary"):
                    st.session_state.posicion_filtro = "P4-P5"; st.rerun()
            with c4:
                if st.button("P5", key="p5", type="primary" if st.session_state.posicion_filtro == "P4-P5" else "secondary"):
                    st.session_state.posicion_filtro = "P4-P5"; st.rerun()
            with c5:
                if st.button("P2", key="p2", type="primary" if st.session_state.posicion_filtro == "P2-P3" else "secondary"):
                    st.session_state.posicion_filtro = "P2-P3"; st.rerun()

            st.write("")
            c1, c2, c3, c4, c5 = st.columns(5)
            with c3:
                if st.button("P1", key="p1", type="primary" if st.session_state.posicion_filtro == "P1" else "secondary"):
                    st.session_state.posicion_filtro = "P1"; st.rerun()

        if st.button("Limpiar Posición 🔄", use_container_width=True):
            st.session_state.posicion_filtro = None; st.rerun()

    with col_filtros:
        columnas_filtros = ["Rol funcional", "Momento con o sin balón", "Sub-rol", "Intención", "Contexto", "Zona", "Carril", "Relación balón", "Referencia"]
        filtros_dict = {}
        for row in range(3):
            cols = st.columns(3)
            for col_idx in range(3):
                idx = row * 3 + col_idx
                if idx < len(columnas_filtros):
                    col_n = columnas_filtros[idx]
                    opc = sorted(df_base[col_n].dropna().unique().tolist())
                    filtros_dict[col_n] = cols[col_idx].multiselect(col_n, options=opc, key=f"f_{col_n}")

    # Filtrado
    df_f = df_base.copy()
    if st.session_state.posicion_filtro:
        df_f = df_f[df_f['Demarcación'] == st.session_state.posicion_filtro]
    for c, s in filtros_dict.items():
        if s: df_f = df_f[df_f[c].isin(s)]

    # Lista y Video
    st.divider()
    cl, cv = st.columns([1, 2])
    with cl:
        st.subheader(f"Conductas ({len(df_f)})")
        for cond in df_f['Conducta'].unique():
            if st.button(cond, key=f"btn_{cond}", use_container_width=True):
                st.session_state.conducta_activa = cond
    
    with cv:
        if 'conducta_activa' in st.session_state and st.session_state.conducta_activa in df_f['Conducta'].values:
            datos = df_f[df_f['Conducta'] == st.session_state.conducta_activa].iloc[0]
            st.subheader(f"Video: {st.session_state.conducta_activa}")
            t_clip = st.radio("Tipo:", ["Clip OK", "Clip Error", "Clip Tarea"], horizontal=True)
            url = datos[t_clip]
            if pd.isna(url): st.error("No hay URL")
            else: 
                st.video(url)
                # Mini campos de zona/carril
                z_act = str(datos.get('Zona', '')).upper()
                c_act = str(datos.get('Carril', '')).upper()
                html = f"""<div class="mini-campo-container">
                    <div class="mini-campo campo-zonas">
                        <div class="zona-v {'highlight-red' if 'Z4' in z_act else ''}">Z4</div>
                        <div class="zona-v {'highlight-red' if 'Z3' in z_act else ''}">Z3</div>
                        <div class="zona-v {'highlight-red' if 'Z2' in z_act else ''}">Z2</div>
                        <div class="zona-v {'highlight-red' if 'Z1' in z_act else ''}">Z1</div>
                    </div>
                    <div class="mini-campo campo-carriles">
                        <div class="carril-h carril-lat {'highlight-red' if c_act == 'I' else ''}">I</div>
                        <div class="carril-h carril-cen {'highlight-red' if c_act == 'C' else ''}">C</div>
                        <div class="carril-h carril-lat {'highlight-red' if c_act == 'D' else ''}">D</div>
                    </div></div>"""
                st.markdown(html, unsafe_allow_html=True)

# --- 6. BARRA LATERAL UNIFICADA ---
with st.sidebar:
    try:
        st.image("Levante_Union_Deportiva_Logo.png", use_container_width=True)
    except:
        st.error("Logo no encontrado")
    
    st.divider()
    
    with st.expander("⚽ Conductas Micro", expanded=(st.session_state.pagina_actual == "Librería")):
        if st.button("📊 Librería", use_container_width=True):
            st.session_state.pagina_actual = "Librería"
            st.rerun()

    with st.expander("📚 Documentación", expanded=(st.session_state.pagina_actual != "Librería")):
        opciones_doc = ["Data Layout", "Contexto", "Elementos Conformadores", "Recursos Técnico-Coordinativos Individuales"]
        indice_def = opciones_doc.index(st.session_state.pagina_actual) if st.session_state.pagina_actual in opciones_doc else 0
        seleccion = st.radio("Secciones:", opciones_doc, index=indice_def, key="radio_docs")
        
        if seleccion != st.session_state.pagina_actual and st.session_state.pagina_actual != "Librería":
            st.session_state.pagina_actual = seleccion
            st.rerun()

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.autenticado = False; st.rerun()

# --- 7. RENDERIZADO FINAL (Aquí es donde se llama a la función) ---
if st.session_state.pagina_actual == "Librería":
    pag_libreria()  # <--- ESTA ES LA CLAVE: Aquí se ejecuta tu código
else:
    st.title(f"📖 {st.session_state.pagina_actual}")
    st.info("Esta sección está en desarrollo.")