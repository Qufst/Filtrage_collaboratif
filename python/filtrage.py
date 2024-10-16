#%% NMF sur une petite base de données construite à la main
import numpy as np
import pandas as pd
from sklearn.decomposition import NMF
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import pairwise_distances
from sklearn.metrics import silhouette_score
from fancyimpute import SoftImpute
from sklearn.decomposition import TruncatedSVD
import time as time  

#%% Création d'un dataframe à partir des données d'introduction

data = {
    'Users': [
        'User 1', 'User 2', 'User 3', 'User 4',
        'User 5', 'User 6', 'User 7'
    ],
    'The Walking Dead': [3, 3, 1, np.nan, np.nan, 3, 2],
    'The Witcher': [3, np.nan, 2, np.nan, 3, 1, 3],
    'Dark': [np.nan, np.nan, np.nan, 5, 4, np.nan, 4],
    'Gossip Girl': [2, 3, 5, 3, np.nan, 4, np.nan],
    'The Crown': [3, 1, 2, 2, np.nan, np.nan, 4]
}

df = pd.DataFrame(data)
#Remplacer les valeurs manquantes par 0

Xbase = df.values[:, 1:].astype(float)
print(Xbase)
X = np.nan_to_num(Xbase, nan=0.0)
nan_mask = np.isnan(Xbase) # Masque des valeurs manquantes
print(X)

#%%
# On applique la factorisation de matrice non négative

model=NMF(n_components=2, init='random', random_state=0)
W=model.fit_transform(X)
H=model.components_
X_nmf = np.dot (W , H )
print (" Matrice X reconstruite : \n", X_nmf )

# On calucule l'erreur de reconstruction

erreur_nmf= np.sqrt(np.mean((X-X_nmf)**2))
print("Erreur de reconstruction : ",erreur_nmf)

#%%

# On affiche les matrices W et H

print("Matrice W : \n", W)
print("Matrice H : \n", H)

#%%
# Calculer la matrice de consensus avec distances cosinus
consensus_matrix = 1 - pairwise_distances(W, metric='cosine')

# Créer un DataFrame pour la matrice de consensus
df_consensus = pd.DataFrame(consensus_matrix, index=df['Users'], columns=df['Users'])

# Visualisation de la matrice de consensus
plt.figure(figsize=(10, 8))
sns.heatmap(df_consensus, annot=False, cmap='cividis', cbar=True)
plt.title('Matrice de Consensus ')
plt.xlabel('Utilisateurs')
plt.ylabel('Utilisateurs')
plt.show()
#%%
#Les 3 graphes residus variance et silhouette pour les données jouet
from sklearn.metrics import silhouette_score


ranks = range(2, 6)  
residuals = []
evar_scores = []
silhouette_scores = []

for r in ranks:
    model = NMF(n_components=r, init='random', random_state=0)
    W = model.fit_transform(X)
    H = model.components_
    X_nmf = np.dot(W, H)
    
    # Calcul de l'erreur de reconstruction
    residual = np.sqrt(np.mean((X - X_nmf) ** 2))
    residuals.append(residual)

    # Calcul de la variance expliquée
    evar = 1 - (np.sum((X - X_nmf) ** 2) / np.sum(X ** 2))
    evar_scores.append(evar)
    
    # Calcul du score de silhouette
    if r > 1:  # Le score de silhouette nécessite au moins 2 clusters
        silhouette_avg = silhouette_score(X, W.argmax(axis=1))
        silhouette_scores.append(silhouette_avg)
    else:
        silhouette_scores.append(0)
    

# Affichage des résultats
plt.figure(figsize=(20, 6))

# Graphique pour les résidus
plt.subplot(1, 3, 1)
plt.plot(ranks, residuals, marker='o', linestyle='-', color='b', label='Résidus')
plt.xlabel('Rang')
plt.ylabel('Erreur de reconstruction (RMSE)')
plt.title('Évolution des résidus')
plt.grid(True)

# Graphique pour la variance expliquée
plt.subplot(1, 3, 2)
plt.plot(ranks, evar_scores, marker='o', linestyle='-', color='c', label='Variance expliquée')
plt.xlabel('Rang')
plt.ylabel('Variance expliquée')
plt.title('Évolution de la variance expliquée')
plt.grid(True)


# Graphique pour le score de silhouette
plt.subplot(1, 3, 3)
plt.plot(ranks, silhouette_scores, marker='^', linestyle='-', color='y', label='Score de silhouette')
plt.xlabel('Rang')
plt.ylabel('Score de silhouette')
plt.title('Évolution du score de silhouette')
plt.grid(True)


plt.tight_layout()
plt.show()
#%%
# NMF pour n_components=2
model = NMF(n_components=2, init='random', random_state=0)
W = model.fit_transform(X)
H = model.components_



# Calculer les scores d'appréciation (reconstruire la matrice)
X_reconstructed = np.dot(W, H)

# Identifier le genre recommandé pour chaque utilisateur
recommended_genres = []
for i in range(X_reconstructed.shape[0]):
    if np.any(nan_mask[i]):  # Si l'utilisateur a au moins un NaN
        # On prend l'indice du genre avec la valeur maximale dans X_svd pour les NaN d'origine
        recommended_index = np.argmax(X_reconstructed[i, nan_mask[i]])
        recommended_genre = df.columns[1:][nan_mask[i]][recommended_index]
        recommended_score = X_reconstructed[i, nan_mask[i]][recommended_index]
    else:
        recommended_genre = 'Aucune recommandation'  # Si pas de NaN, pas de recommandation
        recommended_score = None
    recommended_genres.append((recommended_genre, recommended_score))

# Créer un DataFrame avec les résultats
result_dfNMF = pd.DataFrame({
    'Utilisateur': df['Users'],
    'Nouvelle série recommandé': [rec[0] for rec in recommended_genres],
    'Score d\'appréciation': [rec[1] for rec in recommended_genres]
})
print(result_dfNMF)
#%%
# SVD

# Effectuer la décomposition SVD
U, Sigma, Vt = np.linalg.svd(X)

# Sigma est un vecteur, on doit le transformer en matrice diagonale
Sigma_diag = np.diag(Sigma)

# Redimensionnement si nécessaire (U est (7,7), Sigma_diag est (5,5), Vt est (5,5))
X_svd = U[:, :Sigma_diag.shape[0]] @ Sigma_diag @ Vt

# Afficher la matrice reconstruite
print(X_svd)

# Calculer l'erreur de reconstruction
erreur_svd = np.sqrt(np.mean((X - X_svd) ** 2))
print("Erreur de reconstruction : ", erreur_svd)

recommended_genres = []
for i in range(X_svd.shape[0]):
    if np.any(nan_mask[i]):  # Si l'utilisateur a au moins un NaN
        # On prend l'indice du genre avec la valeur maximale dans X_svd pour les NaN d'origine
        recommended_index = np.argmax(X_svd[i, nan_mask[i]])
        recommended_genre = df.columns[1:][nan_mask[i]][recommended_index]
        recommended_score = X_svd[i, nan_mask[i]][recommended_index]
    else:
        recommended_genre = 'Aucune recommandation'  # Si pas de NaN, pas de recommandation
        recommended_score = None
    recommended_genres.append((recommended_genre, recommended_score))

# Créer un DataFrame avec les résultats
result_dfSVD = pd.DataFrame({
    'Utilisateur': df['Users'],
    'Nouvelle série recommandé': [rec[0] for rec in recommended_genres],
    'Score d\'appréciation': [rec[1] for rec in recommended_genres]
})
print(result_dfSVD)



#%%
# Complétion de la matrice


# Appliquer SoftImpute pour imputer les valeurs manquantes
X_chap = SoftImpute(max_iters=100, verbose=0).fit_transform(Xbase)

print(X_chap)
n_components = 2  # Choisir le nombre de composants, vous pouvez ajuster ce chiffre
model2 = NMF(n_components=n_components, init='random', random_state=0)
W2 = model2.fit_transform(X_chap)
H2 = model2.components_

# Calculer les scores d'appréciation (reconstruire la matrice)
X_reconstructed2 = np.dot(W2, H2)
print(X_reconstructed2)
# erreur de reconstruction
erreur_nmf2 = np.sqrt(np.mean((X_chap - X_reconstructed2) ** 2))
print("Erreur de reconstruction : ", erreur_nmf2)

# Identifier le genre recommandé pour chaque utilisateur
recommended_genres2 = []
for i in range(X_reconstructed2.shape[0]):
    if np.any(nan_mask[i]):  # Si l'utilisateur a au moins un NaN
        # On prend l'indice du genre avec la valeur maximale dans X_svd pour les NaN d'origine
        recommended_index = np.argmax(X_reconstructed2[i, nan_mask[i]])
        recommended_genre = df.columns[1:][nan_mask[i]][recommended_index]
        recommended_score = X_reconstructed2[i, nan_mask[i]][recommended_index]
    else:
        recommended_genre = 'Aucune recommandation'  # Si pas de NaN, pas de recommandation
        recommended_score = None
    recommended_genres2.append((recommended_genre, recommended_score))

# Créer un DataFrame avec les résultats
result_dfcomp = pd.DataFrame({
    'Utilisateur': df['Users'],
    'Nouvelle série recommandé': [rec[0] for rec in recommended_genres2],
    'Score d\'appréciation': [rec[1] for rec in recommended_genres2]
})
print(result_dfcomp)


# %%
