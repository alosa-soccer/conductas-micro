import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Conductas Micro", layout="wide")

# --- ESTILO CSS PARA EL CAMPO (Versión Porterías Garantizadas) ---
st.markdown("""
    <style>
    /* Contenedor principal del campo */
    [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] #campo-tactico) {
        background-color: #2e7d32 !important;
        position: relative !important; /* Necesario para posicionar las porterías */
        background-image: 
            /* Círculo central */
            radial-gradient(circle at 50% 50%, transparent 14%, rgba(255,255,255,0.4) 14.5%, transparent 15.5%),
            /* Línea de medio campo */
            linear-gradient(to bottom, transparent 49.5%, rgba(255,255,255,0.4) 50%, transparent 50.5%),
            /* Perímetro blanco */
            linear-gradient(to right, white 2px, transparent 2px),
            linear-gradient(to left, white 2px, transparent 2px),
            linear-gradient(to top, white 2px, transparent 2px),
            linear-gradient(to bottom, white 2px, transparent 2px) !important;
        background-size: 100% 100% !important;
        background-repeat: no-repeat !important;
        border-radius: 12px !important;
        padding: 45px 15px !important; /* Espacio para que las porterías respiren */
        border: 2px solid #1b5e20 !important;
        box-shadow: inset 0 0 30px rgba(0,0,0,0.2) !important;
    }

    /* Dibujo de la Portería Superior */
    [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] #campo-tactico)::before {
        content: "" !important;
        position: absolute !important;
        top: 0 !important;
        left: 35% !important;
        width: 30% !important;
        height: 15px !important;
        border-left: 2px solid white !important;
        border-right: 2px solid white !important;
        border-bottom: 2px solid white !important;
        z-index: 1 !important;
    }

    /* Dibujo de la Portería Inferior */
    [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] #campo-tactico)::after {
        content: "" !important;
        position: absolute !important;
        bottom: 0 !important;
        left: 35% !important;
        width: 30% !important;
        height: 15px !important;
        border-left: 2px solid white !important;
        border-right: 2px solid white !important;
        border-top: 2px solid white !important;
        z-index: 1 !important;
    }

    /* Estilo de los botones */
    [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] #campo-tactico) .stButton > button {
        background-color: white !important;
        color: #1e1e1e !important;
        border: 1px solid #ccc !important;
        font-weight: bold !important;
        height: 38px !important;
        z-index: 2 !important; /* Por encima de las líneas */
    }

    /* Botón seleccionado */
    [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] #campo-tactico) .stButton > button[kind="primary"] {
        background-color: #ff4b4b !important;
        color: white !important;
        border: 2px solid white !important;
    }
    /* Estilos para los Mini Campos de Zona y Carril */
    .mini-campo-container {
        display: flex;
        gap: 40px;
        justify-content: center;
        padding: 20px;
        background: #f8f9fa;
        border-radius: 12px;
        margin-top: 15px;
        border: 1px solid #ddd;
    }
    .mini-campo {
        background-color: #2e7d32;
        border: 2px solid white;
        display: flex;
        color: white;
        font-size: 12px;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    /* Campo de Zonas (Vertical) - Z4 ARRIBA, Z1 ABAJO */
    .campo-zonas {
        width: 160px;
        height: 180px;
        flex-direction: column; /* Cambiado de column-reverse a column */
    }
    .zona-v {
        flex: 1;
        border: 1px solid rgba(255,255,255,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
    }
    /* Campo de Carriles (Horizontal) */
    .campo-carriles {
        width: 160px;
        height: 180px;
        flex-direction: row;
    }
    .carril-h {
        border: 1px solid rgba(255,255,255,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
    }
    .carril-lat { flex: 1; } /* Izquierda y Derecha */
    .carril-cen { flex: 2; } /* Centro más grande */
    
    .highlight-red {
        background-color: #ff4b4b !important;
        color: white !important;
    } 
    </style>
""", unsafe_allow_html=True)

# --- CARGA DE DATOS ---
@st.cache_data
def cargar_datos():
    # USAMOS RUTA RELATIVA: El archivo debe estar en la misma carpeta que este script
    nombre_archivo = "./conductas_micro.xlsx"
    
    # Verificamos si el archivo existe para dar un error amigable
    if not os.path.exists(nombre_archivo):
        st.error(f"❌ No se encontró el archivo '{nombre_archivo}' en el repositorio.")
        return pd.DataFrame()

    hojas = ["P1", "P2-P3", "P4-P5", "P6", "P7-P11", "P8", "P10", "P9"]
    lista_df = []
    
    for hoja in hojas:
        try:
            # Quitamos la ruta de C:\... y usamos solo el nombre
            df_temp = pd.read_excel(nombre_archivo, sheet_name=hoja)
            lista_df.append(df_temp)
        except Exception as e:
            st.warning(f"No se pudo leer la hoja {hoja}: {e}")
            
    if not lista_df:
        return pd.DataFrame()
        
    return pd.concat(lista_df, ignore_index=True)

df_base = cargar_datos()

# Estado para la posición seleccionada
if 'posicion_filtro' not in st.session_state:
    st.session_state.posicion_filtro = None

# --- DISEÑO DE INTERFAZ ---
st.subheader("Filtros globales")

col_campo, col_filtros = st.columns([1.3, 2], gap="large")


with col_campo:
    st.write("📍 **Demarcación**")
    
    # Este contenedor es el que recibirá el fondo verde
    with st.container():
        # El marcador debe estar aquí dentro para que el CSS funcione
        st.markdown('<div id="campo-tactico" style="height:0px;"></div>', unsafe_allow_html=True)
        
        # Fila 1: P11 - P9 - P7 (Ataque)
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: 
            if st.button("P11", use_container_width=True, key="p11", type="primary" if st.session_state.posicion_filtro == "P7-P11" else "secondary"):
                st.session_state.posicion_filtro = "P7-P11"
                st.rerun()
        with c3:
            if st.button("P9", use_container_width=True, key="p9", type="primary" if st.session_state.posicion_filtro == "P9" else "secondary"):
                st.session_state.posicion_filtro = "P9"
                st.rerun()
        with c5:
            if st.button("P7", use_container_width=True, key="p7", type="primary" if st.session_state.posicion_filtro == "P7-P11" else "secondary"):
                st.session_state.posicion_filtro = "P7-P11"
                st.rerun()

        # Fila 2: P8 - P10 (Interiores)
        st.write("") 
        c1, c2, c3, c4, c5 = st.columns(5)
        with c2:
            if st.button("P8", use_container_width=True, key="p8", type="primary" if st.session_state.posicion_filtro == "P8" else "secondary"):
                st.session_state.posicion_filtro = "P8"
                st.rerun()
        with c4:
            if st.button("P10", use_container_width=True, key="p10", type="primary" if st.session_state.posicion_filtro == "P10" else "secondary"):
                st.session_state.posicion_filtro = "P10"
                st.rerun()

        # Fila 3: P6 (Pivote)
        c1, c2, c3, c4, c5 = st.columns(5)
        with c3:
            if st.button("P6", use_container_width=True, key="p6", type="primary" if st.session_state.posicion_filtro == "P6" else "secondary"):
                st.session_state.posicion_filtro = "P6"
                st.rerun()

        # Fila 4: P3 - P4 - P5 - P2 (Defensa)
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            if st.button("P3", use_container_width=True, key="p3", type="primary" if st.session_state.posicion_filtro == "P2-P3" else "secondary"):
                st.session_state.posicion_filtro = "P2-P3"
                st.rerun()
        with c2:
            if st.button("P4", use_container_width=True, key="p4", type="primary" if st.session_state.posicion_filtro == "P4-P5" else "secondary"):
                st.session_state.posicion_filtro = "P4-P5"
                st.rerun()
        with c4:
            if st.button("P5", use_container_width=True, key="p5", type="primary" if st.session_state.posicion_filtro == "P4-P5" else "secondary"):
                st.session_state.posicion_filtro = "P4-P5"
                st.rerun()
        with c5:
            if st.button("P2", use_container_width=True, key="p2", type="primary" if st.session_state.posicion_filtro == "P2-P3" else "secondary"):
                st.session_state.posicion_filtro = "P2-P3"
                st.rerun()

        # Fila 5: P1 (Portero)
        st.write("") 
        c1, c2, c3, c4, c5 = st.columns(5)
        with c3:
            if st.button("P1", use_container_width=True, key="p1", type="primary" if st.session_state.posicion_filtro == "P1" else "secondary"):
                st.session_state.posicion_filtro = "P1"
                st.rerun()

    # Botón de limpiar FUERA del contenedor (recupera el fondo blanco)
    st.write("")
    if st.button("Limpiar Posición 🔄", use_container_width=True):
        st.session_state.posicion_filtro = None
        st.rerun()


with col_filtros:
    # --- CUADRÍCULA DE FILTROS 3x3 ---
    columnas_filtros = [
        "Rol funcional", "Momento con o sin balón", "Sub-rol", 
        "Intención", "Contexto", "Zona", 
        "Carril", "Relación balón", "Referencia"
    ]
    filtros_dict = {}

    # Generamos la rejilla 3x3
    for row in range(3):
        cols = st.columns(3)
        for col_idx in range(3):
            flat_idx = row * 3 + col_idx
            if flat_idx < len(columnas_filtros):
                col_name = columnas_filtros[flat_idx]
                with cols[col_idx]:
                    opciones = sorted(df_base[col_name].dropna().unique().tolist())
                    filtros_dict[col_name] = st.multiselect(col_name, options=opciones, key=f"f_{col_name}")

# --- FILTRADO LÓGICO ---
df_filtrado = df_base.copy()

# Aplicar filtro de posición si existe
if st.session_state.posicion_filtro:
    df_filtrado = df_filtrado[df_filtrado['Demarcación'] == st.session_state.posicion_filtro]

# Aplicar el resto de filtros
for col, seleccion in filtros_dict.items():
    if seleccion:
        df_filtrado = df_filtrado[df_filtrado[col].isin(seleccion)]

# --- LISTADO Y VIDEO ---
st.divider()
col_lista, col_video = st.columns([1, 2])

with col_lista:
    st.subheader(f"Conductas ({len(df_filtrado)})")
    if df_filtrado.empty:
        st.info("No hay coincidencias.")
    else:
        for conducta in df_filtrado['Conducta'].unique():
            if st.button(conducta, key=f"btn_{conducta}", use_container_width=True):
                st.session_state.conducta_activa = conducta

with col_video:
    if 'conducta_activa' in st.session_state and st.session_state.conducta_activa in df_filtrado['Conducta'].values:
        conducta_sel = st.session_state.conducta_activa
        st.subheader(f"Visualizando: {conducta_sel}")
        datos_conducta = df_filtrado[df_filtrado['Conducta'] == conducta_sel].iloc[0]
        
        tipo_clip = st.radio("Tipo de clip:", ["Clip OK", "Clip Error", "Clip Tarea"], horizontal=True)
        url = datos_conducta[tipo_clip]
        
        if pd.isna(url) or str(url).strip() == "":
            st.error(f"⚠️ El clip seleccionado no tiene URL.")
        else:
            st.video(url)
        
            zona_activa = str(datos_conducta.get('Zona', '')).upper()
            carril_activo = str(datos_conducta.get('Carril', '')).upper()

            st.write("📍 **Ubicación de la conducta**")
            
            # Nota: Usamos HTML directo sin indentación extra para evitar que Markdown lo escape
            html_campos = f"""<div class="mini-campo-container">
<div class="mini-campo campo-zonas">
<div class="zona-v {'highlight-red' if 'Z4' in zona_activa else ''}">Z4</div>
<div class="zona-v {'highlight-red' if 'Z3' in zona_activa else ''}">Z3</div>
<div class="zona-v {'highlight-red' if 'Z2' in zona_activa else ''}">Z2</div>
<div class="zona-v {'highlight-red' if 'Z1' in zona_activa else ''}">Z1</div>
</div>
<div class="mini-campo campo-carriles">
<div class="carril-h carril-lat {'highlight-red' if carril_activo == 'I' else ''}">I</div>
<div class="carril-h carril-cen {'highlight-red' if carril_activo == 'C' else ''}">C</div>
<div class="carril-h carril-lat {'highlight-red' if carril_activo == 'D' else ''}">D</div>
</div>
</div>"""
            
            st.markdown(html_campos, unsafe_allow_html=True)

    else:
        st.info("Selecciona una conducta para reproducir.")

# Debug final
with st.expander("🔍 Ver tabla de datos filtrados"):
    st.dataframe(df_filtrado)