# Introduction à la recommandation par Factorisation ou Complétion

## Description

L'objectif de ce dépôt est d'étudier les articles suivants:
- [Introduction aux méthodes](http://www.math.univ-toulouse.fr/~besse/Wikistat/pdf/st-scenar-explo7-nmf.pdf)
- [Factorisation__par_matrices_non_négatives_NMF](http://wikistat.fr/pdf/st-m-explo-nmf.pdf)
- [Codes](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.NMF.html)

## Organisation du dépôt

- Etude: Les documents relatifs à notre étude sont disponibles dans le dossier `pdf`
- Source LaTeX: Le fichier LaTeX original utilisé pour générer le rapport se trouve dans le dossier `tex`
- Codes Python:  Les scripts Python utilisés dans notre étude sont disponibles dans le dossier `python`

On retrouve les dépendances du projet dans le fichier 'requirements.txt'. les prérequis incluent:
- `numpy`
- `pandas`
- `matplotlib`
- `scikit-learn` (pour `NMF` et `TruncatedSVD`)
- `fancyimpute` (pour `SoftImpute`)

## Compilation du rapport

Pour générer le rapport, un compilateur LaTeX est nécessaire. Vous pouvez utiliser un outil comme Overleaf pour la compilation en ligne.


Auteurs: [Lahjiouj Aicha](https://github.com/aichalhj), [Dias Pierre](https://github.com/pierre-ed-ds), [Festor Quentin](https://github.com/Qufst)