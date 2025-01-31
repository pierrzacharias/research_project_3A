################################################################################
# Same script as implementation_KKR
# but we use multiprocessing to compute faster 
################################################################################
import os
#os.chdir("C:/Users/pierre gauthier/Documents/3A/Projet_3A/Methode_Kernel_Ridge_Regression")
os.chdir("C:/Users/pierr/Documents/3A/projet/Projet_3A/Methode_Kernel_Ridge_Regression")
################################################################################
# roccad@gmail.com
 
<<<<<<< HEAD
import numpy as np
##import multiprocessing
##from scipy import sparse as sp
from sklearn import model_selection
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import learning_curve
from sklearn.kernel_ridge import KernelRidge
from sklearn import metrics 
import matplotlib.pyplot as plt
import pickle
from math import sqrt
from math import log2
from matplotlib import ticker, cm 
import time
=======
#import numpy as np
###import multiprocessing
###from scipy import sparse as sp
#from sklearn import model_selection
#from sklearn.svm import SVR
#from sklearn.model_selection import GridSearchCV
#from sklearn.model_selection import learning_curve
#from sklearn.kernel_ridge import KernelRidge
#from sklearn import metrics 
#import matplotlib.pyplot as plt
#import pickle
#from math import sqrt
#from math import log2
#from matplotlib import ticker, cm 
#import time
>>>>>>> 097f4e1538a04c6831c82b6aa557684d62d3fe31

################################################################################
plt.close()
#start_time = time.time()

# ######################## lecture des donnees #################################

matrice_coulomb = open('matrice_coulomb.txt', 'rb')
matrice_coulomb_depickler = pickle.Unpickler(matrice_coulomb)
energie_atomisation = open('energie_atomisation.txt','rb')
energie_atomisation_depickler = pickle.Unpickler(energie_atomisation)
number_of_non_H_atoms = open('number_of_non_H_atoms.txt', 'rb')
number_of_non_H_atoms_depickler = pickle.Unpickler(number_of_non_H_atoms)

X_dataset, Y_dataset= [matrice_coulomb_depickler.load()], [energie_atomisation_depickler.load()]
H_atoms = [number_of_non_H_atoms_depickler.load()]

continuer = True
while continuer == True:
    try:
        X_dataset.append(matrice_coulomb_depickler.load())
        Y_dataset.append(energie_atomisation_depickler.load())
        H_atoms.append(number_of_non_H_atoms_depickler.load())
    except:
        continuer = False    

matrice_coulomb.close()
energie_atomisation.close()
number_of_non_H_atoms.close()
X_dataset = np.asarray(X_dataset)
Y_dataset = np.asarray(Y_dataset)
H_atoms = np.asarray(H_atoms)
# ##################### selection trainnig set et Hold-out set #################

# plt.hist(H_atoms)
# on trie les liste si > ou < a 4 non-H-atoms par molecule
# toute les molecule <4 non H-atoms sont dans le trainning set
inds = H_atoms.argsort()
X_under_4_H = [X_dataset[i] for i in inds if H_atoms[i] < 5]
Y_under_4_H = [Y_dataset[i] for i in inds if H_atoms[i] < 5]
X_above_4_H = [X_dataset[i] for i in inds if H_atoms[i] > 4]
Y_above_4_H = [Y_dataset[i] for i in inds if H_atoms[i] > 4]

# on coupe de maniere aleatoire entre une basse de train (taille 1000) et une base de test
X_train, X_validation, Y_train,Y_validation = model_selection.train_test_split(
    X_above_4_H, Y_above_4_H, train_size= len(X_dataset) - 1000 + len(X_under_4_H),random_state=100) 

# on coupe le base de train en une base de train (900) pour les hyperparametre et une base test (taille 100) pour valider le choix des hyperparametres
X_training_set, X_hold_out_set, Y_training_set,Y_hold_out_set = model_selection.train_test_split(X_train,Y_train,train_size = len(X_train) - 100)  

# on ajoute les molecule <5-non-H-atoms dans la base de train pour avoir taille = 900 
X_training_set = np.concatenate((X_under_4_H,X_training_set),axis=0)
Y_training_set = np.concatenate((Y_under_4_H,Y_training_set),axis =0)   

#print('temps construction dataset= ',time.time() - start_time)
print('dataset genere')
################################################################################
# ###################### entrainement du modele ################################
################################################################################

# #################### choix des hyperparametres ###############################
# on entraine sur trainning_set et on predit sur hold_out_set
# recherche du parametre optimal 
# alpha = (2*C)^-1, C = 1/2*alpha
# dans article sigma de 5 a 18 --> gamma = 1/sigma**2 gamma in [.003,0.04]
# lambda de -40 a -5
# gamma = 1/sigma**2 

param_grid={"alpha": [np.linspace(-30, -1, 20)]}
def RMSE(y_true, y_pred): return sqrt(metrics.mean_squared_error(y_true, y_pred))
def R2(y_true, y_pred): return 1 - (metrics.r2_score(y_true, y_pred))
def MAE(y_true, y_pred): return metrics.mean_absolute_error(y_true, y_pred)
scoring_dict = {'RMSE' : metrics.make_scorer(RMSE),
                'MAE' : 'neg_mean_absolute_error',
                'R2': 'r2'}


#scoring = 'neg_mean_squared_error' # MSE ** 2
#scoring = 'r2' # R ** 2
#scoring ='neg_mean_absolute_error' # MAE
#"gamma": np.linspace(.001,0.1, 20)})
# https://scikit-learn.org/stable/modules/grid_search.html#exhaustive-grid-search
#kr_opti = GridSearchCV(KernelRidge(kernel='rbf', gamma=0.5), cv=5,
                       #param_grid={"alpha": [np.linspace(1, 5, 10)]}, 
                       #scoring = scoring,
                       #scoring = scoring_dict,
                       #refit = 'MSE',
                       #verbose = True,
                       #return_train_score=True)
#kr_opti.fit(X_hold_out_set,Y_hold_out_set)
#print("score KRR OTIMISEE %.3f" % kr_opti.score(X_hold_out_set,Y_hold_out_set) )
#results = kr_opti.cv_results_
#print("results", results)

# les valeur optimale dans l'article sont notre_gamma = 1/(2* gamma_article **2)
# gamma optimal article 724 recher dans [5,18]
# notre_gamma optimal serait -19 a chercher dans [-11,-40]

<<<<<<< HEAD
# lambda optimal dans l'article est 10**(-6.5), -21 en base 2,a cherher dans :5 -40, -5
alpha_grid_log2 = np.arange(-30,-10,0.5)
alpha_grid = [2.**alpha_grid_log2[i] for i in range(len(alpha_grid_log2))]
gamma_grid_log2 = np.arange(-30,-10,0.5)
=======
# lambda optimal dans l'article est 10**(-6.5), -21 en base 2,a chercher dans :5 -40, -5
alpha_grid_log2 = np.arange(-40,-5,0.5)
alpha_grid = [2.**alpha_grid_log2[i] for i in range(len(alpha_grid_log2))]
gamma_grid_log2 = np.arange(-30,-5,1)
>>>>>>> 097f4e1538a04c6831c82b6aa557684d62d3fe31
#gamma_grid_log2 = [-15]
gamma_grid = [2.**gamma_grid_log2[i] for i in range(len(gamma_grid_log2))]


# stockage des score pour les differentes mesure
RMSE_SCORE = []
MAE_SCORE = []
R2_SCORE = []
#start_time = time.time()
min_RMSE = 1e6
i = 0
for alpha in alpha_grid: 
    #for gamma in gamma_grid:
        #gamma = 1e-4
<<<<<<< HEAD
        Y_kr_pred = KernelRidge(kernel='rbf', gamma = gamma, alpha = alpha).fit(X_training_set,Y_training_set).predict(X_training_set)     
        RMSE_SCORE.append(RMSE(Y_training_set,Y_kr_pred))
        R2_SCORE.append(R2(Y_training_set,Y_kr_pred))
        MAE_SCORE.append(MAE(Y_training_set,Y_kr_pred))
        if RMSE_SCORE[-1] < min_RMSE: 
            alpha_min, gamma_min = alpha, gamma
            min_RMSE = RMSE_SCORE[-1]
        print(i,'iteration sur',len(gamma_grid)*len(alpha_grid))
        i += 1
=======
    Y_kr_pred = KernelRidge(kernel='linear',alpha = alpha).fit(X_training_set,Y_training_set).predict(X_training_set)     
    RMSE_SCORE.append(RMSE(Y_training_set,Y_kr_pred))
    R2_SCORE.append(R2(Y_training_set,Y_kr_pred))
    MAE_SCORE.append(MAE(Y_training_set,Y_kr_pred))
    if RMSE_SCORE[-1] < min_RMSE: 
        alpha_min, gamma_min = alpha, gamma
        min_RMSE = RMSE_SCORE[-1]
    print(i,'iteration sur',2400)
    i += 1
>>>>>>> 097f4e1538a04c6831c82b6aa557684d62d3fe31

print('alpha min, gamma min=',alpha_min,gamma_min,'minimum RMSE sur training',min(RMSE_SCORE))
#print('temps de calcul sur la grille = ',time.time() - start_time)
# calcul erreur sur set taille 100 pour validation
Y_kr_pred = KernelRidge(kernel='rbf', gamma = gamma_min, alpha = alpha_min).fit(X_training_set,Y_training_set).predict(X_training_set)     
print('erreur sur set validation de taille 100',RMSE(Y_training_set,Y_kr_pred))
#print('temps recherche hyperparametres',time.time() - start_time)


# remplissage sur la grille a partir des scores calcules


X_mesh, Y_mesh = np.meshgrid(gamma_grid_log2, alpha_grid_log2)    
Z_mesh_RMSE = np.zeros(X_mesh.shape)
k = 0
for i in range(Z_mesh_RMSE.shape[0]):
    for j in range(Z_mesh_RMSE.shape[1]):
        Z_mesh_RMSE[i][j] = RMSE_SCORE[k]
        k += 1 
#print('temps remplissage grille = ',time.time() - start_time)

fig, ax = plt.subplots()  

#ax.set_ylim(log2(min(alpha_grid))-200,log2(max(alpha_grid))+200)
#ax.set_xlim(log2(min(gamma_grid))-200,log2(max(gamma_grid))+200)

cp = ax.contourf(X_mesh, Y_mesh, Z_mesh_RMSE)
ax.contour(cp)
ax.clabel(cp, inline=True, fontsize=10)    
ax.grid(c='k', ls='-', alpha=0.7)
ax.set_xlabel(r'$\gamma$')
ax.set_ylabel(r'$\alpha$')
fig.colorbar(cp)
plt.show()   

# affichage p color

fig1, ax1 = plt.subplots()  
cs = ax1.pcolor(X_mesh, Y_mesh, Z_mesh_RMSE, edgecolors='k', linewidths=1)
fig.colorbar(cs)
plt.show()
# ######################## performance modele ##################################

kr_final = KernelRidge(kernel='Laplacian', gamma = gamma_min, alpha = alpha_min)
kr_final.fit(np.concatenate((X_hold_out_set,X_training_set)),

             np.concatenate((Y_hold_out_set,Y_training_set)))     
Y_kr_pred_final = kr_final.predict(X_validation)
print('score final RMSE =',RMSE(Y_validation,Y_kr_pred_final))
#print('temps execution = ',time.time() - start_time)

<<<<<<< HEAD
matrice_RMSE= open("Resultat_RMSE_RBF_2_30_10.txt","wb")
=======
matrice_RMSE= open("Resultat_RMSE_linear.txt","wb")
>>>>>>> 097f4e1538a04c6831c82b6aa557684d62d3fe31
matrice_RMSE_pickler = pickle.Pickler(matrice_RMSE)
for i in range(len(RMSE_SCORE)):
    matrice_RMSE_pickler.dump(RMSE_SCORE[i])
matrice_RMSE.close()
<<<<<<< HEAD
matrice_R2 = open("Resultat_R2_RBF_2_30_10.txt","wb")
=======
matrice_R2 = open("Resultat_R2_linear.txt","wb")
>>>>>>> 097f4e1538a04c6831c82b6aa557684d62d3fe31
matrice_R2_pickler = pickle.Pickler(matrice_R2)
for i in range(len(R2_SCORE)):
    matrice_R2_pickler.dump(R2_SCORE[i])
matrice_R2.close()
<<<<<<< HEAD
matrice_MAE = open("Resultat_MAE_RBF_2_30_10.txt","wb")
=======
matrice_MAE = open("Resultat_MAE_linear.txt","wb")
>>>>>>> 097f4e1538a04c6831c82b6aa557684d62d3fe31
matrice_MAE_pickler = pickle.Pickler(matrice_MAE)
for i in range(len(MAE_SCORE)):
    matrice_MAE_pickler.dump(MAE_SCORE[i])
matrice_MAE.close()


################################################################################
#resultats pour RBF
#alpha_grid_log2 = np.arange(-30,-10,0.5)
#gamma_grid_log2 = np.arange(-30,-10,0.5)
#score final RMSE = 10.335641860418134 [-13,-29]
#score final MAE = 11.050325445167802 [-11.5,29]
#score final R2 = 0.9977 [-13,-29]

#resultats pour Laplacian
#dans l'article alpha = 10**(-12) = -40 gamma = 10**(3.6)  = -12 
#alpha_grid_log2 = np.arange(-40,-20,0.5)
#gamma_grid_log2 = np.arange(-30,-5,1)
