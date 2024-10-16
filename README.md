# Introduction à la recommandation par Factorisation ou Complétion

## Description

L'objectif de ce dépôt est d'étudier les articles suivants:
- [Introduction aux méthodes](http://www.math.univ-toulouse.fr/~besse/Wikistat/pdf/st-scenar-explo7-nmf.pdf)
- [Factorisation par matrices non négatives NMF](http://wikistat.fr/pdf/st-m-explo-nmf.pdf)
- [Bibliothèque NMF](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.NMF.html)

## Organisation du dépôt

- Etude: Le document relatif à notre étude sont disponibles dans le dossier `pdf`: (Filtrage_collaboratof)[https://github.com/Qufst/Filtrage_collaboratif/tree/main/pdf]
- Source LaTeX: Le fichier LaTeX original utilisé pour générer le rapport se trouve dans le dossier `tex`
- Codes Python:  Les scripts Python utilisés dans notre étude sont disponibles dans le dossier `python`. On a décidé de séparer l'étude de la base de donnée réelle Netflix de notre éxemple construit à la main pour l'explication puisque la cross-validation sur la base de données Netflix a un temps de calcul de plusieurs heures.
De plus, la base de données Netflix étant trop grande pour github, pour la reproductibilité du code veuillez récupérer la base de données manuellement:[dataset](https://www.kaggle.com/datasets/rishitjavia/netflix-movie-rating-dataset), et modifier les paths.

On retrouve les dépendances du projet dans le fichier 'requirements.txt'. les prérequis incluent:
- `numpy`
- `pandas`
- `matplotlib`
- `scikit-learn` (pour `NMF`, `cosine_similarity`, `pairwise_distances`, `SimpleImputer`, `KFold`, `silhouette_score`, `mean_squared_error` et `TruncatedSVD`)
- `fancyimpute` (pour `SoftImpute`)
- `seaborn`
- `time`



## Compilation du rapport

Pour générer le rapport, un compilateur LaTeX est nécessaire. Vous pouvez utiliser un outil comme Overleaf pour la compilation en ligne.


Auteurs: [Lahjiouj Aicha](https://github.com/aichalhj), [Dias Pierre](https://github.com/pierre-ed-ds), [Festor Quentin](https://github.com/Qufst)