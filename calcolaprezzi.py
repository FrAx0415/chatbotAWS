'''Benvenuto nell'app scenario RAG APP Pricing Calculator.
In questo script python è stato ipotizzato un traffico pari a 200 domande al giorno sul nostro chatbot. Vediamo quanto ci costa per tali domande.'''

# Calcolo dei token
Token_input = 1500
Token_output = 325
Token_totali = Token_input + Token_output

#Calcolo scenario con token e domande al giorno:

Domande_del_cliente_algiorno = 200
token_giornalieri = Domande_del_cliente_algiorno*Token_totali  #Somma di input e output


# Costo del modello per generazione domande
costo_model_giornaliero = (token_giornalieri / 1000) * 0.00013  # USD al giorno
costo_model_mensile = costo_model_giornaliero * 30  # USD al mese

# Costo embedding su Amazon Bedrock
costo_embedding_mensile = 3.2  # USD al mese

# Costo Amazon OpenSearch Serverless
costo_opensearch_mensile = 0.1517 * 30  # USD al mese

# Costo Amazon S3 (Standard Infrequent Access)
costo_s3_mensile = 0.07  # USD al mese

# Costo API Gateway (REST API)
costo_api_gateway_mensile = 3.70  # USD al mese PER UN MILIONE DI RICHIESTE

# Costo AWS Lambda
costo_lambda_computazione_mensile = 16.67  # USD al mese
costo_lambda_richieste_mensile = 0.20  # USD al mese
costo_lambda_totale_mensile = costo_lambda_computazione_mensile + costo_lambda_richieste_mensile

'''Nei costi della lambda
è escluso il free tier'''

# Calcolo del costo totale mensile
costo_totale_mensile = (
    costo_model_mensile +
    costo_embedding_mensile +
    costo_opensearch_mensile +
    costo_s3_mensile +
    costo_api_gateway_mensile +
    costo_lambda_totale_mensile
)

costo_annuale = costo_totale_mensile * 12
# Tasso di cambio da USD a EUR (esempio: 1 USD = 0.85 EUR)
tasso_di_cambio = 0.85

# Conversione dei costi in EUR
costo_totale_mensile_eur = costo_totale_mensile * tasso_di_cambio
costo_annuale_eur = costo_annuale * tasso_di_cambio
# Risultati
print("Il prezzo mensile della RAG App è di: " + str(costo_totale_mensile) + " USD (" + str(costo_totale_mensile_eur) + " EUR)")
print("Il costo annuale invece è di: " + str(costo_annuale) + " USD (" + str(costo_annuale_eur) + " EUR)")
