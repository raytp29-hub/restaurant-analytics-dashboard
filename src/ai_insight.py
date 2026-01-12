from anthropic import Anthropic
from streamlit import json
from config import CLAUDE_API_KEY
import pandas as pd
import ollama
import json

def generate_insights(df):
    """
    Genera insights AI analizzando i dati dei ristoranti
    
    Args:
        df (pd.DataFrame): DataFrame con dati ristoranti filtrati
        
    Returns:
        str: Insights generati da Claude
    """
    
    stats = {
        'total_restaurants': len(df),
        'avg_rating': df['rating'].mean(),
        'categories': df['categories'].value_counts().to_dict(),
        'top_rated': df.nlargest(3, 'rating')[['name', 'rating', 'categories']].to_dict('records'),
        'rating_distribution': df['rating'].describe().to_dict()
    }
    
    
    
    prompt = f"""
        Sei un esperto di business intelligence nel settore food & beverage.

        Analizza questi dati sui ristoranti e genera 3-4 insights strategici concreti:

        STATISTICHE:
        - Totale ristoranti analizzati: {stats['total_restaurants']}
        - Rating medio: {stats['avg_rating']:.2f}
        - Distribuzione categorie: {stats['categories']}
        - Top 3 ristoranti: {stats['top_rated']}

        COMPITI:
        1. Identifica opportunità di mercato (gap, categorie sotto-rappresentate)
        2. Analizza trend rating per categoria
        3. Suggerisci strategie per nuovo business
        4. Evidenzia pattern interessanti

        Rispondi in italiano, in modo conciso e professionale (max 300 parole).
        """
        
    
    client = Anthropic(api_key=CLAUDE_API_KEY)
    
    message = client.messages.create(
        model="claude-4-sonnet-20250514",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    insights = message.content[0].text
    
    return insights




#OLLAMA SETUP
    
"""    response = ollama.chat(
        model="gemma3:latest",
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    """
    
    #insights = response["message"]["content"]
    
    
    

def generate_insights_data(df):
    """
    Genera dati strutturati per visualizzazioni AI-powered
    
    Args:
        df (pd.DataFrame): DataFrame con dati ristoranti filtrati
        
    Returns:
        dict: Dati strutturati per grafici
    """

    
    # 1. Prepara statistiche
    stats = {
        'total_restaurants': len(df),
        'avg_rating': round(df['rating'].mean(), 2),
        'categories': df['categories'].value_counts().to_dict(),
        'top_rated': df.nlargest(3, 'rating')[['name', 'rating', 'categories']].to_dict('records'),
    }
    
    # 2. Prompt per JSON strutturato
    prompt = f"""
Analizza questi dati sui ristoranti:
- Totale: {stats['total_restaurants']}
- Rating medio: {stats['avg_rating']}
- Categorie: {stats['categories']}
- Top 3: {stats['top_rated']}

Genera un'analisi strategica in formato JSON con questa struttura ESATTA:

{{
  "market_gaps": [
    {{"category": "nome categoria", "opportunity_score": numero 1-10, "reason": "spiegazione breve"}}
  ],
  "category_performance": [
    {{"category": "nome", "predicted_rating": numero, "market_saturation": "bassa/media/alta", "trend": "crescita/stabile/declino"}}
  ],
  "strategic_priorities": [
    {{"action": "azione concreta", "priority": numero 1-10, "roi_potential": "basso/medio/alto", "timeframe": "breve/medio/lungo"}}
  ],
  "risk_assessment": [
    {{"risk": "descrizione rischio", "severity": numero 1-10, "probability": "bassa/media/alta"}}
  ]
}}

IMPORTANTE: Rispondi SOLO con il JSON valido, senza markdown, senza testo aggiuntivo, senza ```json```.
"""
    
    # 3. Chiama Claude API
    client = Anthropic(api_key=CLAUDE_API_KEY)
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        temperature=0.3,  # Più deterministico per JSON
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # 4. Estrai e parsifica JSON
    response_text = message.content[0].text
    
    # Rimuovi eventuali markdown ```json``` se presenti
    response_text = response_text.replace('```json', '').replace('```', '').strip()
    
    try:
        data = json.loads(response_text)
        return data
    except json.JSONDecodeError as e:
        print(f"Errore parsing JSON: {e}")
        print(f"Risposta Claude: {response_text}")
        return None
    