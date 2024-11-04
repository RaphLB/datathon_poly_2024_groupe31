**Analyse des Rapports Financiers : Explications des Fonctionnalités**


Les rapports financiers, et plus spécifiquement les états financiers, offrent aux investisseurs et aux analystes une vue détaillée de la situation actuelle d'une entreprise. Comme seuls les rapports annuels font l'objet de vérifications officielles, notre solution se concentre sur cette source fiable d'information pour répondre aux besoins des analystes. Notre outil propose quatre fonctionnalités principales :


1. **Résumé automatique** : fournit une synthèse concise des informations essentielles.
2. **Analyse de sentiment** : identifie le ton (optimiste, neutre, pessimiste) des messages de la direction.
3. **Extraction d’informations clés** : extrait les éléments principaux, en particulier des tableaux financiers.
4. **Calcul de ratios financiers** : facilite l'évaluation des performances par des ratios standards.


Notre solution est propulsée par une IA Générative (Claude 3 Haiku) et traite des rapports en anglais et en français.


### Le dossier comprends 5 script python : 


1. **Main** : Ce script joue le rôle de point d’entrée pour le programme. Il relie tous les autres scripts et coordonne l’interaction avec l’utilisateur. C’est lui qui gère le flux global de l’application et les choix de l’utilisateur pour activer l’une ou l’autre des fonctionnalités : résumé automatique, analyse de sentiment, extraction d’informations clés, ou calcul de ratios financiers.


2. **Extract_data** : Ce script est dédié au traitement initial des rapports financiers en format PDF. Il convertit le contenu du PDF en texte brut, ce qui permet ensuite d’en extraire les informations pour des analyses plus approfondies.


3. **Analyse_csv** : Après la conversion du PDF en texte, ce script prend en charge l'analyse de ce texte pour isoler les informations pertinentes. Il extrait, nettoie et organise les données en format CSV, facilitant ainsi le traitement ultérieur des informations.


4. **LLM_options** : Ce script gère les interactions avec le modèle de langage Claude 3 Haiku. Il envoie des prompts spécifiques et reçoit les réponses formatées selon les besoins. Ce script prend en charge les trois premières options (résumé automatique, analyse de sentiment, et extraction d’informations clés) en communiquant les données pertinentes et en interprétant les retours du modèle pour l'utilisateur.


5. **Ratio** : Ce script s’occupe de la quatrième fonctionnalité, le calcul des ratios financiers. Il utilise les données extraites pour calculer différents ratios financiers importants, tels que le bénéfice net, les dividendes par action, les actifs et passifs totaux et courants, le ratio de liquidité, entre autres. Il permet également de comparer ces ratios à des moyennes sectorielles si celles-ci sont disponibles.


Ensemble, ces cinq scripts créent un outil d’analyse financière complet qui assiste l’utilisateur dans l'extraction, le résumé, l’analyse de sentiment et les calculs de ratios financiers, le tout en utilisant une IA pour automatiser et optimiser le traitement des rapports annuels.




### Fonctionnalités détaillées


#### Résumé automatique
Lorsque l’utilisateur sélectionne cette option, le fichier PDF est converti en texte, puis envoyé à Claude 3 Haiku pour obtenir un résumé structuré contenant les informations clés souhaitées (nom de la compagnie, date, secteur, points financiers clés, risques, opportunités et conclusion).


#### Analyse de sentiment
Cette analyse porte principalement sur le message de la direction. Après conversion du PDF en texte, seules les premières pages sont conservées pour aider l'IA à détecter et résumer le message de la direction. L’IA évalue ensuite le ton général du message.


#### Extraction d’informations clés
Dans cette étape, Claude 3 Haiku aide l’utilisateur à identifier rapidement des mots-clés pour extraire les informations essentielles des tableaux financiers, générant un fichier CSV qui consolide ces données. L'IA analyse ensuite le contenu pour fournir une interprétation des données.


#### Calcul de ratios financiers
Cette fonctionnalité propose une analyse détaillée de l'évolution des caractéristiques financières importantes : bénéfices nets, dividendes par action, actifs et passifs totaux, ratio d’endettement, actifs et passifs courants, ratio de liquidité courante, bénéfices non distribués et dividendes versés. Le script extrait et nettoie les données pertinentes en supprimant les doublons et valeurs manquantes, puis les transforme pour un affichage graphique.


Chaque fonction inclut un argument **domain** (facultatif) qui, s'il est précisé, permet de comparer la performance de l’entreprise avec la moyenne sectorielle (industriel, services, télécoms) sur une période donnée. Cependant, cette comparaison reste indicative en raison de l’échantillon restreint de rapports disponibles.


### Détails du traitement des ratios
Le processus suit un schéma commun pour chaque fonction :


- **Identification de la colonne** : la colonne la plus proche du terme "idéal" est sélectionnée pour assurer la précision des données.
- **Nettoyage des valeurs** : la fonction `clean_strings` transforme les données en entiers et gère les cas où des parenthèses indiquent des valeurs négatives.
- **Gestion des NaN** : les lignes contenant exclusivement des valeurs "NaN" sont ignorées.
  
**Fonctions spécifiques** :
- `evolution_benefice_net(domain)`: évolution du bénéfice net et comparaison avec le secteur.
- `evolution_div_action(domain)`: évolution du dividende par action.
- `show_actifs_passifs_totaux(domain)`: évolution des actifs et passifs totaux, avec calcul du ratio d’endettement.
- `show_actifs_passifs_current(domain)`: évolution des actifs et passifs courants et du ratio de liquidité courante.
- `evolution_rnd(domain)`: évolution des bénéfices non répartis.
- `evolution_div_versé(domain)`: total des dividendes versés par année.


En combinant analyse horizontale (dans le temps) et comparaison sectorielle, notre solution facilite une évaluation rapide des ratios financiers d’une entreprise.


--- 


Cette structure permettra à vos lecteurs de naviguer plus facilement entre les sections et d’avoir une compréhension immédiate de chaque fonctionnalité, tout en rendant le texte fluide et professionnel.
