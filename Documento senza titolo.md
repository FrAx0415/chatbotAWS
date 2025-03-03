Retrieval Augmented Generation APP

Scenario:  
*Si necessita un chatbot per la interrogazione di documentazione privata. Le specifiche prese in considerazione sono:* 

* region eu-central-1  
* 10 utenti che fanno 10 domande a testa  
* 100mb di storage da interrogare 	(circa **3.751.835 token \-\> 4m**)  
* 100 domande al giorno		(circa **150.000** token input **32.500** token output)  
* 4 embedding mensili

Modelli usati da Amazon Bedrock: 	

* Titan Text Embeddings V2 per l’embedding  
* Llama 3.2 Instruct (1B) per la generazione delle domande

Totale giornaliero: 182.500 token circa

Costo di interrogazione al modello:  
Costo input	 \= 150000 / 1000 × 0.00013  	\= 	0.0195 USD  
Costo output	 \= 32500 / 1000 × 0.00013 	\=	0.0042 USD  
**Costo totale** 	\= 1.2 \+ 0.78 \= 1.98 1.2+0.78	\= 	**0.0237 USD**  
iCosto di Embedding su Amazon Bedrock:  
L’embedding va fatto ogni volta che di desidera aggiornare i dati sul chatbot

	**costo**  \= 4m x 0,2 \= **0,80$ al giorno**

DEF: Embedding (Capacità di trasformare parole in indici numerici) su S3

- Sui **0,20$ per un milione di Token**. Saranno circa necessari 4 milioni di token per fare un embedding unico su S3.

Costo Amazon Opensearch (Collection Serverless):

	**Tempo di utilizzo**:	100 x 8 \= 800 secondi    
800 / 3600 \= **0.2222 ore**  
**costo** 	\=		0.2222 x 0.683 \= **0.1517 USD al giorno**

DEF: Posto fisico su cui salvare i dati indicizzati.

- **Si paga 0.683 USD all’ora**. In particolare ecco i prezzi mostrati dal Pricing Calculator.

- 1 OCUs x 730 hours in a month x 0.339 USD \= 247.47 USD (Indexing cost)  
- 1 OCUs x 730 hours in a month x 0.339 USD \= 247.47 USD (Search and query cost)  
- 1 GB x 0.026 USD \= 0.03 USD (Managed storage cost)  
- 247.47 USD \+ 247.47 USD \+ 0.03 USD \= 494.97 USD (Amazon OpenSearch Serverless cost)  
- Amazon OpenSearch Serverless cost (monthly): 494.97 USD

Costo Amazon S3 (Standard Infrequent Access S3 plan):

- S3 Standard \- Infrequent Access (S3 Standard-IA) **cost (monthly): 0.07 USD**  
- S3 Standard \- Infrequent Access (S3 Standard-IA) **cost (upfront): 0.00 USD**

Costo API Gateway (REST API):  
il numero di richieste è di gran lunga 

**costo \=** 1,000,000 richieste x 0.0000037 \= **3.70 USD**

Costo Lambda Function:

**costo \= 0,55 USD al giorno**

- **Monthly compute charges: 16.67 USD**  
- Sono **0,55 USD al giorno**  
- 1,000,000 requests x 0.0000002 USD \= 0.20 USD (monthly request charges)

  Number of requests: 1 million per month \* 1000000 multiplier \= 1000000 per month  
- Amount of memory allocated: 128 MB x 0.0009765625 GB in a MB \= 0.125 GB  
- Amount of ephemeral storage allocated: 512 MB x 0.0009765625 GB in a MB \= 0.5 GB

  ##### **Pricing calculations**

  1,000,000 requests x 8,000 ms x 0.001 ms to sec conversion factor \= 8,000,000.00 total compute (seconds)  
  0.125 GB x 8,000,000.00 seconds \= 1,000,000.00 total compute (GB-s)  
  Tiered price for: 1,000,000.00 GB-s  
  1,000,000 GB-s x 0.0000166667 USD \= 16.67 USD  
  Total tier cost \= 16.6667 USD (monthly compute charges)  
  **Monthly compute charges: 16.67 USD**  
  1,000,000 requests x 0.0000002 USD \= 0.20 USD (monthly request charges)  
  **Monthly request charges: 0.20 USD**  
  0.50 GB \- 0.5 GB (no additional charge) \= 0.00 GB billable ephemeral storage per function  
  **Monthly ephemeral storage charges: 0 USD**  
  16.67 USD \+ 0.20 USD \= 16.87 USD  
  Lambda cost (monthly): 16.87 USD  
    
  