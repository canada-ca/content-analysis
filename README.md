# Consultation Content Analysis (pilot)

OpenNorth’s exploration of preprocessing and content analysis of comments from public consultation datasets using Python. These steps are intended to be applied to data in CSV format from public consultations. Note that responses to questions can only be processed one at a time.

generate --> describe --> preprocessing --> analyze


---
# Analyse du contenu des consultations no (pilote)

Exploration, réalisée par NordOuvert en langage Python, du prétraitement et de l’analyse du contenu des commentaires contenus dans les ensembles de données tirées des consultations publiques. Ces étapes doivent être appliquées en format CSV (valeurs séparées par des virgules) aux données des consultations publiques. Veuillez prendre note que les réponses aux questions de recherche ne peuvent être traitées qu’une seule à la fois.

générer --> décrire --> prétraiter --> analyse

---

Preprocessing: 

•	Manual formatting: Ensure that the input dataset is in CSV format. Each row in the CSV should reflect an independent data entry and each column should be an associated metadata or attribute field. The first row should contain column headers. 

•	Make note of the CSV columns (starting at 0) that correspond to the ID field, Comment field (only select one response column at a time if the dataset contains multiple), Participant Information field, Event field, and Date field. Refer to instructions in the “generate_csv” script if any of this information is missing. 

•	Change necessary variables in the “generate_csv” script to create a new CSV file that is of appropriate structure 

•	Change the necessary variables in the “describe_csv” script to create a new text file with basic descriptions of the dataset

Analysis: 

In progress

