import json
import boto3
import os

def lambda_handler(event, context):
    """
    Funzione AWS Lambda che integra Amazon Bedrock Knowledge Base con modelli di inferenza.
    Prende una query dall'utente, la usa per cercare informazioni nella knowledge base,
    e poi utilizza queste informazioni come contesto per generare una risposta con un modello LLM.
    
    Args:
        event (dict): L'evento trigger di AWS Lambda, che deve contenere una 'query'
        context (object): Oggetto di contesto fornito da AWS Lambda
        
    Returns:
        dict: Una risposta formattata che include la domanda, la risposta generata dal modello,
              e le fonti della knowledge base utilizzate
    """
    
    # Configura il client per Bedrock Agent Runtime che gestisce le operazioni sulla knowledge base
    # Questo è utilizzato per interrogare la knowledge base e ottenere documenti pertinenti
    bedrock_agent_runtime = boto3.client(
        service_name='bedrock-agent-runtime',
        region_name=os.environ.get('AWS_REGION', 'eu-central-1')  # Ottiene la regione dalle variabili d'ambiente o usa eu-central-1 come default
    )
    
    # Configura il client per Bedrock Runtime che gestisce l'inferenza del modello linguistico
    # Questo è utilizzato per interagire con il modello LLM (es. Claude)
    bedrock_runtime = boto3.client(
        service_name='bedrock-runtime',
        region_name=os.environ.get('AWS_REGION', 'eu-central-1')  # Ottiene la regione dalle variabili d'ambiente o usa eu-central-1 come default
    )
    
    # Recupera l'ID della knowledge base
    # Usiamo un ID hardcoded, ma può anche essere passato tramite l'evento
    knowledge_base_id = "KDOFABEGRN"
    if not knowledge_base_id and 'knowledgeBaseId' in event:
        knowledge_base_id = event['knowledgeBaseId']
    
    # Recupera l'ID del modello da utilizzare per l'inferenza
    # Default al modello Claude Instant, ma può essere sovrascritto dall'evento
    model_id = os.environ.get('MODEL_ID', "anthropic.claude-instant-v1")
    if 'modelId' in event:
        model_id = event['modelId']
    
    # Recupera la query (domanda) dall'evento
    # Questa è obbligatoria - se non è presente, restituiamo un errore
    query = ""
    if 'query' in event:
        query = event['query']
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('È necessario fornire una query nell\'evento')
        }
    
    try:
        # Effettua una richiesta alla knowledge base per recuperare informazioni pertinenti alla query
        # La query dell'utente viene inviata e si richiedono i 5 risultati più rilevanti
        retrieve_response = bedrock_agent_runtime.retrieve(
            knowledgeBaseId=knowledge_base_id,  # ID della knowledge base da interrogare
            retrievalQuery={
                'text': query  # La query dell'utente diventa il criterio di ricerca
            },
            retrievalConfiguration={
                'vectorSearchConfiguration': {
                    'numberOfResults': 5  # Recupera i 5 risultati più pertinenti
                }
            }
        )
        
        # Estrae i risultati dalla risposta della knowledge base
        results = retrieve_response.get('retrievalResults', [])  # Se 'retrievalResults' non esiste, restituisce una lista vuota
        
        # Formatta i risultati per l'input del modello
        # Unisce tutti i testi dei risultati per creare un unico contesto
        context_content = ""
        for result in results:
            if 'content' in result and 'text' in result['content']:
                context_content += result['content']['text'] + "\n\n"  # Aggiunge due newline per separare i vari contenuti
        
        print("CONTESTOOOOO: "+context_content)  # Stampa il contesto per debug

        # Prepara il prompt per il modello
        # Include il contesto recuperato dalla knowledge base e la query originale
        prompt = f"""
        Contesto:
        {context_content}
        
        Rispondimi in modo
        sintetico e preciso, quando mi rispondi voglio che mi dici all'inizio del messaggio : ciao cloud specialist!!
        domanda:
        {query}
        
        Per favore rispondi alla domanda basandoti solo sul contesto fornito.
        """
        
        # Parametri per la richiesta al modello utilizzando il client bedrock-runtime
        inference_params = {
            'modelId': model_id,  # ID del modello selezionato
            'body': json.dumps({  # Corpo della richiesta in formato JSON
                'anthropic_version': 'bedrock-2023-05-31',  # Versione dell'API Anthropic utilizzata
                'max_tokens': 1000,  # Numero massimo di token da generare nella risposta
                'messages': [  # Formato delle conversazioni per i modelli Claude
                    {
                        'role': 'user',  # Ruolo del messaggio (user = la richiesta viene dall'utente)
                        'content': prompt  # Il prompt completo che include contesto e query
                    }
                ]
            }),
            'contentType': 'application/json',  # Tipo di contenuto della richiesta
            'accept': 'application/json'  # Tipo di contenuto accettato per la risposta
        }
        
        # Effettua la chiamata al modello linguistico
        inference_response = bedrock_runtime.invoke_model(**inference_params)
        
        # Estrae e decodifica la risposta dal modello
        response_body = json.loads(inference_response['body'].read().decode('utf-8'))
        model_response = response_body['content'][0]['text']  # Estrae il testo della risposta
        
        # Restituisce una risposta formattata che include:
        # - La domanda originale
        # - La risposta generata dal modello
        # - Le fonti (URI S3) dei documenti utilizzati dalla knowledge base
        return {
            'statusCode': 200,
            'body': json.dumps({
                'question': query,  # La domanda originale
                'answer': model_response,  # La risposta generata dal modello
                'sources': [result.get('location', {}).get('s3Location', {}).get('uri', '') 
                           for result in results]  # Lista degli URI S3 delle fonti utilizzate
            })
        }
    
    except Exception as e:
        # Gestione degli errori
        # In caso di errore, restituisce un codice di stato 500 e il messaggio di errore
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }