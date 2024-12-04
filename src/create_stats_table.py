# Run PERMANOVA for each unique pair of groups

from itertools import combinations
from sklearn.metrics.pairwise import rbf_kernel, linear_kernel
import numpy as np
import pandas as pd

def compute_mmd(X, Y, ker, gamm=0.5):
    """Compute MMD statistic between two sets of embeddings using an RBF kernel."""

    if(ker=="linear_kernel"):
        XX = linear_kernel(X, X)
        YY = linear_kernel(Y, Y)
        XY = linear_kernel(X, Y)
    else:
        XX = rbf_kernel(X, X, gamma=gamm)
        YY = rbf_kernel(Y, Y, gamma=gamm)
        XY = rbf_kernel(X, Y, gamma=gamm)
    mmd_stat = XX.mean() + YY.mean() - 2 * XY.mean()
    return mmd_stat

def permutation_test_mmd(X, Y, kernel, num_permutations=100, gamma=0.5):
    """Perform permutation test for MMD between two sets of embeddings."""
    observed_mmd = compute_mmd(X, Y, kernel, gamma)
    combined = np.vstack([X, Y])
    n_X = len(X)
    mmd_permuted = []
    
    for _ in range(num_permutations):
        np.random.shuffle(combined)
        X_permuted = combined[:n_X]
        Y_permuted = combined[n_X:]
        mmd_stat = compute_mmd(X_permuted, Y_permuted, kernel, gamma)
        mmd_permuted.append(mmd_stat)
    
    p_value = np.mean(np.array(mmd_permuted) >= observed_mmd)
    return observed_mmd, p_value


def pairwise_test(paths):

    stats_table = {}
    stats_table["R1"] = {}
    stats_table["R2"] = {}
    stats_table["R3"] = {}

    for p1 in paths:
        
        var_path = p1 + "/R" + str(paths.index(p1)+1) + "-V"
        for (g1, g2) in combinations(range(6), 2):

            rec = "R" + str(paths.index(p1)+1)
            key = "V"+str(g1)+"-V"+str(g2)
            embedding1 = np.load(var_path + str(g1) + ".npy")
            embedding2 = np.load(var_path + str(g2) + ".npy")
           
            pairwise_distances = np.linalg.norm(embedding1[:, np.newaxis] - embedding2, axis=2)
            gamma = 1 / np.median(pairwise_distances) # Set gamma to inverse of median distance

            stats, p = permutation_test_mmd(embedding1[0],embedding2[0],"rbf_kernel", 1000, gamma)

            if p < 0.05:
                stats_table[rec][key] = "Distinguishable"
            else:
                stats_table[rec][key] = "Indistinguishable"

    df = pd.DataFrame(stats_table,columns = ['R1', 'R2', 'R3'])

    df.to_csv("stats_rbf_kernel_1000.csv")