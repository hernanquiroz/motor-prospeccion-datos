import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
os.makedirs('data', exist_ok=True)

lista_leads = []

# ==========================================
# FUNCIÓN 1: SCRAPING DE MIPYMES (B2B)
# ==========================================
def scrapear_mipymes():
    print("🏢 Buscando MIPYMES...")
    # URL de ejemplo (Debes cambiarla por un directorio real, ej. Cámara de Comercio)
    url = "https://www.directorioempresarialfake.com/tecnologia" 
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Simulación de extracción (Cambia las clases CSS por las reales)
        tarjetas = soup.find_all('div', class_='empresa-card') 
        for t in tarjetas:
            nombre = t.find('h3').text.strip() if t.find('h3') else "N/A"
            web = t.find('a')['href'] if t.find('a') else "N/A"
            
            lista_leads.append({
                "Tipo": "MIPYME",
                "Nombre_Empresa": nombre,
                "Nombre_Persona": "N/A",
                "Contacto": web,
                "Necesidad_Detectada": "Requiere análisis de datos / BI",
                "Fecha": datetime.now().strftime("%Y-%m-%d")
            })
    except Exception as e:
        print(f"Error en MIPYMES: {e}")

# ==========================================
# FUNCIÓN 2: SCRAPING DE PERSONAS NATURALES (B2C/FREELANCE)
# ==========================================
def scrapear_personas():
    print("👤 Buscando Personas Naturales (Freelancers/Independientes)...")
    # URL de ejemplo (Podría ser el feed público de Workana, Reddit, o foros)
    url = "https://www.forofreelancefake.com/busco-experto-datos"
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Simulación de extracción (Cambia las clases CSS por las reales)
        posts = soup.find_all('div', class_='post-servicio')
        for p in posts:
            usuario = p.find('span', class_='usuario').text.strip() if p.find('span', class_='usuario') else "Anónimo"
            mensaje = p.find('p', class_='descripcion').text.strip() if p.find('p', class_='descripcion') else "Sin detalle"
            enlace_post = p.find('a')['href'] if p.find('a') else "N/A"
            
            # Solo guardamos si menciona palabras clave de datos
            palabras_clave = ['datos', 'excel', 'powerbi', 'dashboard', 'análisis']
            if any(word in mensaje.lower() for word in palabras_clave):
                lista_leads.append({
                    "Tipo": "Persona Natural",
                    "Nombre_Empresa": "Independiente",
                    "Nombre_Persona": usuario,
                    "Contacto": enlace_post,
                    "Necesidad_Detectada": mensaje[:100] + "...", # Primeros 100 chars
                    "Fecha": datetime.now().strftime("%Y-%m-%d")
                })
    except Exception as e:
        print(f"Error en Personas: {e}")

# --- EJECUTAR Y GUARDAR ---
if __name__ == "__main__":
    scrapear_mipymes()
    scrapear_personas()
    
    if lista_leads:
        df = pd.DataFrame(lista_leads)
        df.to_csv('data/leads.csv', index=False, encoding='utf-8-sig')
        print(f"✅ Éxito. {len(df)} leads guardados.")
    else:
        print("⚠️ No se encontraron leads. Revisa las URLs y clases CSS.")
