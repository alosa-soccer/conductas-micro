import streamlit as st
import re
import pandas as pd
import os

def set_page(name):
    st.session_state["pagina_actual"] = name
    st.rerun()

# --- CONFIGURACIÓN Y ESTADO ---
st.set_page_config(page_title="Conductas Micro - Levante UD", layout="wide")

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# Inicializamos la página actual si no existe
if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = "Librería"

def check_login():
    st.container()
    with st.columns([1, 2, 1])[1]:  # Centra un poco el formulario
        st.title("🔐 Acceso Privado")
        st.subheader("Conductas Micro - Levante UD")
        
        with st.form("login_form"):
            usuario_input = st.text_input("Correo electrónico")
            password_input = st.text_input("Contraseña", type="password")
            boton_login = st.form_submit_button("Iniciar Sesión", use_container_width=True)
            
            if boton_login:
                # Accedemos a la sección [users] de tu secrets.toml
                usuarios_registrados = st.secrets["users"]
                
                if usuario_input in usuarios_registrados and usuarios_registrados[usuario_input] == password_input:
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("Usuario y/o contraseña incorrectos")

# Control de flujo: Si no está logueado, se muestra el form y se para la ejecución
if not st.session_state.autenticado:
    check_login()
    st.stop()

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
        width: 180px; /* Un poco más ancho para que quepan los 5 */
        height: 180px;
        flex-direction: row;
    }
    .carril-h {
        border: 1px solid rgba(255,255,255,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        font-size: 10px;
    }

    /* Proporciones de los carriles */
    .carril-ce { flex: 1.5; } /* Exteriores: tamaño intermedio */
    .carril-ci { flex: 1; }   /* Interiores: los más estrechos */
    .carril-cc { flex: 2.5; } /* Central: el más ancho */

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

def pag_libreria():
    st.title("Librería de Conductas")

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
            "Momento con o sin balón", "Rol funcional", "Sub-rol", 
            "Intención"]
        filtros_dict = {}

        # Generamos la rejilla 2x2
        for row in range(2):
            cols = st.columns(2)
            for col_idx in range(2):
                flat_idx = row * 2 + col_idx
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
                # --- SOLUCIÓN: Limpieza y normalización de la URL ---
                url_str = str(url).strip()
                
                # Si es un link corto (youtu.be), lo convertimos al formato largo estándar
                if "youtu.be/" in url_str:
                    video_id = url_str.split("youtu.be/")[1].split("?")[0]
                    url_str = f"https://www.youtube.com/watch?v={video_id}"
                
                # Intentamos reproducir el video
                st.video(url_str)
                
                # --- SOLUCIÓN: Botón de respaldo por si YouTube bloquea la inserción ---
                st.link_button("🌐 Ver directamente en YouTube", url_str, use_container_width=True)
                
                # El resto de tu código de Zona y Carril...
                zona_activa = str(datos_conducta.get('Zona', '')).upper()
                carril_activo = str(datos_conducta.get('Carril', '')).upper()

                es_ce = "CE" in carril_activo
                es_ci = "CI" in carril_activo
                es_cc = "CC" in carril_activo

                st.write("📍 **Ubicación de la conducta**")
                
                html_campos = f"""<div class="mini-campo-container">
    <div class="mini-campo campo-zonas">
        <div class="zona-v {'highlight-red' if 'Z4' in zona_activa else ''}">Z4</div>
        <div class="zona-v {'highlight-red' if 'Z3' in zona_activa else ''}">Z3</div>
        <div class="zona-v {'highlight-red' if 'Z2' in zona_activa else ''}">Z2</div>
        <div class="zona-v {'highlight-red' if 'Z1' in zona_activa else ''}">Z1</div>
    </div>
    <div class="mini-campo campo-carriles">
        <div class="carril-h carril-ce {'highlight-red' if es_ce else ''}">CE</div>
        <div class="carril-h carril-ci {'highlight-red' if es_ci else ''}">CI</div>
        <div class="carril-h carril-cc {'highlight-red' if es_cc else ''}">CC</div>
        <div class="carril-h carril-ci {'highlight-red' if es_ci else ''}">CI</div>
        <div class="carril-h carril-ce {'highlight-red' if es_ce else ''}">CE</div>
    </div>
</div>"""
                
                st.markdown(html_campos, unsafe_allow_html=True)

                # --- DESPLEGABLE DE INFORMACIÓN OPTIMIZADO ---
                st.write("") 
                with st.expander("ℹ️ Información"):
                    # 1. Campos generales
                    campos_principales = {
                        "Conducta": "Conducta",
                        "Rol funcional": "Rol funcional",
                        "Sub-rol": "Sub-rol",
                        "Intención": "Intención",
                        "CF/IF": "CF/IF",
                        "Rival poseedor": "Rival poseedor",
                        "D": "D",
                        "V": "V",
                        "S": "S",
                        "Recurso Técnico Individual": "Recurso Técnico Individual"
                    }

                    for label, col in campos_principales.items():
                        valor = datos_conducta.get(col, "-")
                        st.markdown(f"**{label}:** {valor}")

                    # 2. Sección de Errores Comunes con formato de lista
                    st.markdown("**Errores comunes:**")
                    
                    columna_objetivo = "Error típico"
                    col_impacto = "Impacto error"
                    valor_celda = datos_conducta.get(columna_objetivo, "")
                    valor_impacto = datos_conducta.get(col_impacto, "-")

                    # 2. Verificamos que no esté vacío o sea NaN
                    if pd.isna(valor_celda) or str(valor_celda).strip() == "" or valor_celda == "-":
                        st.markdown("• Sin errores registrados.")
                    else:
                        texto = str(valor_celda)
                        
                        match_e1 = re.search(r"E1:(.*?)(?=E2:|$)", texto, re.DOTALL)
                        match_e2 = re.search(r"E2:(.*)", texto, re.DOTALL)

                        # 4. Mostramos los resultados si existen
                        if match_e1:
                            e1_texto = match_e1.group(1).strip()
                            st.markdown(f"• **Error 1:** {e1_texto}")
                        
                        if match_e2:
                            e2_texto = match_e2.group(1).strip()
                            st.markdown(f"• **Error 2:** {e2_texto}")

                    if pd.isna(valor_impacto) or str(valor_impacto).strip() == "":
                        valor_impacto = "-"

                    st.markdown(f"**Impacto:** {valor_impacto}", unsafe_allow_html=True)
        

        else:
            st.info("Selecciona una conducta para reproducir.")

    # Debug final
    #with st.expander("🔍 Ver tabla de datos filtrados"):
        #st.dataframe(df_filtrado)

@st.cache_data
def cargar_layout_doc():
    nombre_archivo = "documentación.xlsx" # Asegúrate de que el nombre coincida exactamente
    if not os.path.exists(nombre_archivo):
        return pd.DataFrame()
    try:
        # Leemos la hoja "columnas"
        return pd.read_excel(nombre_archivo, sheet_name="columnas")
    except Exception as e:
        st.error(f"Error al leer la hoja 'columnas': {e}")
        return pd.DataFrame()
    
@st.cache_data
def cargar_contexto_doc():
    nombre_archivo = "documentación.xlsx"
    if not os.path.exists(nombre_archivo):
        return pd.DataFrame()
    try:
        # Leemos la hoja "contexto"
        return pd.read_excel(nombre_archivo, sheet_name="contexto")
    except Exception as e:
        st.error(f"Error al leer la hoja 'contexto': {e}")
        return pd.DataFrame()

@st.cache_data
def cargar_recursos_tecnicos():
    nombre_archivo = "documentación.xlsx"
    if not os.path.exists(nombre_archivo):
        return pd.DataFrame()
    try:
        # Leemos la hoja "rtci"
        return pd.read_excel(nombre_archivo, sheet_name="rtci")
    except Exception as e:
        st.error(f"Error al leer la hoja 'rtci': {e}")
        return pd.DataFrame()
    
@st.cache_data
def cargar_elementos_doc():
    nombre_archivo = "documentación.xlsx"
    if not os.path.exists(nombre_archivo):
        return pd.DataFrame()
    try:
        # Leemos la hoja "elementos conformadores"
        return pd.read_excel(nombre_archivo, sheet_name="elementos conformadores")
    except Exception as e:
        st.error(f"Error al leer la hoja 'elementos conformadores': {e}")
        return pd.DataFrame()
    
@st.cache_data
def cargar_organizacion_elementos():
    nombre_archivo = "documentación.xlsx"
    if not os.path.exists(nombre_archivo):
        return pd.DataFrame()
    try:
        # Leemos la hoja "ec organizacion"
        return pd.read_excel(nombre_archivo, sheet_name="ec organizacion")
    except Exception as e:
        st.error(f"Error al leer la hoja 'ec organizacion': {e}")
        return pd.DataFrame()

def pag_data_layout():
    st.markdown("Estructura y definición de los datos utilizados en el proyecto.")
    
    df_layout = cargar_layout_doc()
    
    if df_layout.empty:
        st.warning("No se pudo cargar la información de 'documentación.xlsx'.")
        return

    # Recorremos cada fila del Excel
    for _, row in df_layout.iterrows():
        # Usamos el valor de 'Columna' como titular
        st.header(f"📍 {row['Columna']}")
        
        # Mostramos las preguntas y respuestas
        st.markdown(f"**¿Qué es?**")
        st.write(row["¿Qué es?"])
        
        st.markdown(f"**¿Para qué sirve?**")
        st.write(row["¿Para qué sirve?"])
        
        st.markdown(f"**¿Cómo se redacta?**")
        st.write(row["¿Cómo se redacta?"])
        
        # El ejemplo lo ponemos en un cuadro azul para que destaque
        if pd.notna(row["Ejemplo"]):
            st.info(f"**Ejemplo:** {row['Ejemplo']}")
        
        st.divider() # Línea de separación entre filas

def pag_contexto():
    st.title("🌍 Contexto")
    
    # Explicación inicial
    st.markdown("""
    En la siguiente página veremos el contexto en el que se produce la conducta micro. 
    En él podemos distinguir los siguientes conceptos:
    """)
    
    df_contexto = cargar_contexto_doc()
    
    if df_contexto.empty:
        st.warning("No se pudo cargar la información de la hoja 'contexto'.")
        return

    # Recorremos cada fila del Excel de contexto
    for _, row in df_contexto.iterrows():
        # Título: Valor de la columna 'Bloque'
        st.header(f"📌 {row['Bloque']}")
        
        # Cuerpo de la información
        st.markdown("**¿Qué es?**")
        st.write(row["¿Qué es?"])
        
        st.markdown("**¿Para qué sirve en el proyecto?**")
        st.write(row["¿Para qué sirve en el proyecto?"])
        
        st.markdown("**¿Cómo se redacta?**")
        st.write(row["¿Cómo se redacta?"])
        
        # Ejemplo resaltado
        if pd.notna(row["Ejemplo"]):
            st.success(f"**Ejemplo:** {row['Ejemplo']}")
        
        st.divider()

def pag_elementos():
    st.title("🧩 Elementos Conformadores")
    st.markdown("A continuación se detallan los elementos que conforman y estructuran las conductas micro:")
    
    # --- PARTE 1: Elementos Conformadores (Lo que ya tenías) ---
    df_elementos = cargar_elementos_doc()
    
    if not df_elementos.empty:
        for _, row in df_elementos.iterrows():
            st.header(f"🔸 {row['Elemento conformador']}")
            st.markdown(f"**¿Qué es?** \n{row['¿Qué es?']}")
            st.markdown(f"**¿Qué suele explicar?** \n{row['¿Qué suele explicar?']}")
            st.markdown(f"**Tipos frecuentes:** \n{row['Tipos frecuentes']}")
            if pd.notna(row["Ejemplo"]):
                st.info(f"**Ejemplo:** {row['Ejemplo']}")
            st.divider()
    
    # --- PARTE 2: Organización de Elementos Conformadores (NUEVA SECCIÓN) ---
    st.write("") # Espacio
    st.title("🧩 Organización de Elementos Conformadores")
    st.markdown("Estructura organizativa de los componentes detallados anteriormente:")
    
    df_org = cargar_organizacion_elementos()
    
    if df_org.empty:
        st.warning("No se pudo cargar la información de la hoja 'ec organizacion'.")
        return

    for _, row in df_org.iterrows():
        # Título: Valor de la columna 'Componente'
        st.header(f"🔸 {row['Componente']}")
        
        # Estructura de preguntas y respuestas
        st.markdown(f"**¿Qué es?**")
        st.write(row["¿Qué es?"])
        
        st.markdown(f"**¿Qué pregunta responde?**")
        st.write(row["¿Qué pregunta responde?"])
        
        st.markdown(f"**¿Qué incluye habitualmente?**")
        st.write(row["¿Qué incluye habitualmente?"])
        
        # Sección de advertencia (Lo que no debe hacer) en color rojo/naranja
        st.warning(f"**⚠️ ¿Qué no debe hacer?** \n{row['¿Qué no debe hacer?']}")
        
        st.markdown(f"**¿Cómo se redacta?**")
        st.write(row["¿Cómo se redacta?"])
        
        # Ejemplo resaltado
        if pd.notna(row["Ejemplo"]):
            st.success(f"**Ejemplo:** {row['Ejemplo']}")
        
        st.divider()

def pag_recursos_tecnicos():
    st.title("⚡ Recursos Técnico-Coordinativos Individuales")
    
    # Texto introductorio solicitado
    st.markdown("A continuación se describen los diferentes tipos de Recursos Técnicos-Coordinativos Individuales:")
    
    df_rtci = cargar_recursos_tecnicos()
    
    if df_rtci.empty:
        st.warning("No se pudo cargar la información de la hoja 'rtci'.")
        return

    # Recorremos cada fila
    for _, row in df_rtci.iterrows():
        # Título: Valor de la columna 'Tipo de RTCI'
        st.header(f"🔹 {row['Tipo de RTCI']}")
        
        # Cuerpo de la información
        st.markdown("**¿Cuándo aplica?**")
        st.write(row["¿Cuándo aplica?"])
        
        st.markdown("**¿Qué incluye?**")
        st.write(row["¿Qué incluye?"])
        
        # El Checklist lo mostramos con un formato especial
        st.markdown("**Checklist:**")
        st.info(row["Checklist"])
        
        # Ejemplo resaltado
        if pd.notna(row["Ejemplo"]):
            st.markdown(f"**Ejemplo:** {row['Ejemplo']}")
        
        st.divider()       

def render_sidebar():
    with st.sidebar:
        # Escudo centrado y más pequeño
        if os.path.exists("Levante_Union_Deportiva_Logo.png"):
            col_izq, col_logo, col_der = st.sidebar.columns([1, 2, 1])
            with col_logo:
                st.image("Levante_Union_Deportiva_Logo.png", use_container_width=True)
        
        st.divider()

        # 1) Sección Conductas
        with st.sidebar.expander("⚽ Conductas Micro", expanded=True):
            if st.button("📊 Librería", use_container_width=True, key="btn_lib"):
                set_page("Librería")

        # 2) Sección Documentación
        with st.sidebar.expander("📚 Documentación", expanded=True):
            if st.button("Data Layout", use_container_width=True):
                set_page("Data Layout")
            if st.button("Contexto", use_container_width=True):
                set_page("Contexto")
            if st.button("Elementos Conformadores", use_container_width=True):
                set_page("Elementos Conformadores")
            if st.button("Recursos Técnicos", use_container_width=True):
                set_page("Recursos Técnico-Coordinativos Individuales")

        st.sidebar.markdown("---")
        if st.sidebar.button("Cerrar Sesión", use_container_width=True):
            st.session_state.autenticado = False
            st.rerun()

# Ejecutamos la barra lateral
render_sidebar()

# Control de qué página se muestra
pagina = st.session_state.get("pagina_actual", "Librería")

if pagina == "Librería":
    pag_libreria()
elif pagina == "Data Layout":
    st.title("📊 Data Layout")
    pag_data_layout()
elif pagina == "Contexto":
    pag_contexto()
elif pagina == "Elementos Conformadores":
    pag_elementos()
elif pagina == "Recursos Técnico-Coordinativos Individuales":
    pag_recursos_tecnicos()