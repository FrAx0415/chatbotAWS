'''Benvenuto nell'app scenario RAG APP Pricing Calculator. 
In questo script Python è stato ipotizzato un traffico pari a 200 domande al giorno sul nostro chatbot. 
Vediamo quanto ci costa per tali domande.'''

# Calcolo dei token
Token_input = 1500
Token_output = 325
Token_totali = Token_input + Token_output

# Calcolo scenario con token e domande al giorno
Domande_del_cliente_algiorno = 100
token_giornalieri = Domande_del_cliente_algiorno * Token_totali  # Somma di input e output

# Costo del modello per generazione domande
costo_model_giornaliero = (token_giornalieri / 1000) * 0.00013  # USD al giorno
costo_model_mensile = costo_model_giornaliero * 30  # USD al mese
costo_model_annuale = costo_model_mensile * 12  # USD all'anno

# Costo embedding su Amazon Bedrock
costo_embedding_mensile = 3.2  # USD al mese
costo_embedding_annuale = costo_embedding_mensile * 12  # USD all'anno

# Costo Amazon OpenSearch Serverless
costo_opensearch_mensile = 0.1517 * 30  # USD al mese
costo_opensearch_annuale = costo_opensearch_mensile * 12  # USD all'anno

# Costo Amazon S3 (Standard Infrequent Access)
costo_s3_mensile = 0.07  # USD al mese
costo_s3_annuale = costo_s3_mensile * 12  # USD all'anno

# Costo API Gateway (REST API)
costo_api_gateway_mensile = 3.70  # USD al mese per un milione di richieste
costo_api_gateway_annuale = costo_api_gateway_mensile * 12  # USD all'anno

# Costo AWS Lambda
costo_lambda_computazione_mensile = 16.67  # USD al mese
costo_lambda_richieste_mensile = 0.20  # USD al mese
costo_lambda_totale_mensile = costo_lambda_computazione_mensile + costo_lambda_richieste_mensile
costo_lambda_totale_annuale = costo_lambda_totale_mensile * 12  # USD all'anno

# Calcolo del costo totale
costo_totale_mensile = (
    costo_model_mensile +
    costo_embedding_mensile +
    costo_opensearch_mensile +
    costo_s3_mensile +
    costo_api_gateway_mensile +
    costo_lambda_totale_mensile
)
costo_totale_annuale = costo_totale_mensile * 12  # USD all'anno

# Tasso di cambio da USD a EUR (esempio: 1 USD = 0.85 EUR)
tasso_di_cambio = 0.85

# Conversione dei costi in EUR
costo_totale_mensile_eur = costo_totale_mensile * tasso_di_cambio
costo_totale_annuale_eur = costo_totale_annuale * tasso_di_cambio

# Risultati
print("Il prezzo mensile di Amazon Bedrock è di: {:.2f} USD ({:.2f} EUR)".format(costo_totale_mensile, costo_totale_mensile_eur))
print("Il costo annuale di Amazon Bedrock invece è di: {:.2f} USD ({:.2f} EUR)".format(costo_totale_annuale, costo_totale_annuale_eur))

'''Amazon Q'''
indice = 1  # Un indice avrà massimo 200 megabyte di analisi, nel S3 vi sono 30 MB scartando le immagini.
numero_utenti = 10  # Dieci utenti
costo_utenti_mensile = 3 * numero_utenti  # USD al mese
costo_utenti_annuale = costo_utenti_mensile * 12  # USD all'anno

costo_query_mensile = ((indice * 0.14) * 24) * 30
costo_query_annuale = costo_query_mensile * 12  # USD all'anno

costo_totale_amazonq_mensile = costo_utenti_mensile + costo_query_mensile
costo_totale_amazonq_annuale = costo_totale_amazonq_mensile * 12

# Conversione in EUR
costo_totale_amazonq_mensile_eur = costo_totale_amazonq_mensile * tasso_di_cambio
costo_totale_amazonq_annuale_eur = costo_totale_amazonq_annuale * tasso_di_cambio

totale_differenza_annuale = costo_totale_amazonq_annuale_eur - costo_totale_annuale_eur

# Risultati Amazon Q
print("Il prezzo mensile di Amazon Q è di: {:.2f} USD ({:.2f} EUR)".format(costo_totale_amazonq_mensile, costo_totale_amazonq_mensile_eur))
print("Il costo annuale di Amazon Q è di: {:.2f} USD ({:.2f} EUR)".format(costo_totale_amazonq_annuale, costo_totale_amazonq_annuale_eur))
print("\nLa differenza di prezzo annuale è di: {:.2f} EUR".format(totale_differenza_annuale))
