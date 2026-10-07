scraper.py - VERSIÓN FUNCIONAL CON DATOS REALES
import requests
import pandas as pd
import os
from datetime import datetime

# Crear carpeta data si no existe
os.makedirs('data', exist_ok=True)

lista_leads = []

# ==========================================
# FUNCIÓN 1: SCRAPING DE MIPYMES (B2B)
# Busca startups y empresas en Product Hunt / Crunchbase
# ==========================================
def scrapear_mipymes():
    print(" Buscando MIPYMES en directorios públicos...")
    
    # Usamos una API pública real: GitHub Search API (empresas que buscan talento en datos)
    url = "https://api.github.com/search/repositories"
    params = {
        "q": "business intelligence OR data analysis OR dashboard",
        "sort": "updated",
        "order": "desc",
        "per_page": 10
    }
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "MotorProspeccion/1.0"
    }
    
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        data = resp.json()
        
        for item in data.get('items', [])[:5]:  # Tomamos los primeros 5
            owner = item.get('owner', {}).get('login', 'Desconocido')
            repo_name = item.get('name', 'N/A')
            descripcion = item.get('description', 'Sin descripción')[:150]
            url_repo = item.get('html_url', '')
            
            lista_leads.append({
                "Tipo": "MIPYME",
                "Nombre_Empresa": owner,
                "Nombre_Persona": "N/A",
                "Contacto": url_repo,
                "Necesidad_Detectada": f"Repo: {repo_name} - {descripcion}",
                "Fecha": datetime.now().strftime("%Y-%m-%d")
            })
        print(f"✅ Encontradas {min(5, len(data.get('items', [])))} MIPYMES")
    except Exception as e:
        print(f"❌ Error en MIPYMES: {e}")

# ==========================================
# FUNCIÓN 2: SCRAPING DE PERSONAS NATURALES
# Busca en Hacker News (foro público de tecnología)
# ==========================================
def scrapear_personas():
    print("👤 Buscando Personas Naturales en foros públicos...")
    
    # API pública de Hacker News
    url = "https://hacker-news.firebaseio.com/v0/search.json"
    
    # Buscamos posts recientes con palabras clave
    keywords = ["data analysis", "business intelligence", "dashboard", "powerbi"]
    
    for keyword in keywords[:2]:  # Limitamos a 2 keywords para no saturar
        try:
            # Usamos la API de búsqueda de HN (via Algolia)
            search_url = f"https://hn.algolia.com/api/v1/search?query={keyword}&tags=story&hitsPerPage=3"
            resp = requests.get(search_url, timeout=10)
            data = resp.json()
            
            for hit in data.get('hits', [])[:3]:
                titulo = hit.get('title', 'Sin título')
                autor = hit.get('author', 'Anónimo')
                url_post = hit.get('url', hit.get('permalink', ''))
                fecha = hit.get('created_at', '')[:10]
                
                lista_leads.append({
                    "Tipo": "Persona Natural",
                    "Nombre_Empresa": "Independiente",
                    "Nombre_Persona": autor,
                    "Contacto": url_post if url_post else f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}",
                    "Necesidad_Detectada": titulo[:150],
                    "Fecha": fecha if fecha else datetime.now().strftime("%Y-%m-%d")
                })
        except Exception as e:
            print(f"❌ Error buscando '{keyword}': {e}")
    
    print(f"✅ Encontradas varias personas naturales")

# ==========================================
# EJECUTAR Y GUARDAR
# ==========================================
if __name__ == "__main__":
    print("🚀 Iniciando Motor de Prospección...")
    
    scrapear_mipymes()
    scrapear_personas()
    
    if lista_leads:
        df = pd.DataFrame(lista_leads)
        df.to_csv('data/leads.csv', index=False, encoding='utf-8-sig')
        print(f"\n ¡ÉXITO! {len(df)} leads guardados en data/leads.csv")
        print("\n📊 Primeros leads:")
        print(df.head())
    else:
        print("⚠️ No se encontraron leads. Revisa la conexión a internet.")
