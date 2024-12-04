
import os
import numpy as np
import pandas as pd
from itertools import combinations
import sys

os.chdir("..")

# Load user and model data and find alignment

# A distinguishability matrix showing which recordings were judged as same/different from one another by model.
def model_matrix(df,rec_num):

	matrix = [ [0]*6 for i in range(6)]
	
	for (g1, g2) in combinations(range(6), 2):
	    matrix[g1][g2] = df.loc[df['Unnamed: 0'] == "V"+str(g1)+"-V"+str(g2)][rec_num].values[0]
	    matrix[g2][g1] = df.loc[df['Unnamed: 0'] == "V"+str(g1)+"-V"+str(g2)][rec_num].values[0]

	for i in range(0,6):
	     matrix[i][i] = 'Indistinguishable'

	return np.array(matrix)

# A distinguishability matrix showing which recordings were judged as same/different from one another by model.
def user_matrix(user_ratings):

	matrix = [ [0]*6 for i in range(6)]

	for (g1, g2) in combinations(range(6), 2):
	    if user_ratings[g1] == user_ratings[g2]:
	        matrix[g1][g2] = "Indistinguishable"
	        matrix[g2][g1] = "Indistinguishable"
	    else:
	        matrix[g1][g2] = "Distinguishable"
	        matrix[g2][g1] = "Distinguishable"

	for i in range(0,6):
	     matrix[i][i] = 'Indistinguishable'
	
	return np.array(matrix)

def alignment(rec_num):

	user_ratings = ["HT","S","S","M","S","S"]

	df = pd.read_csv("data/stats_rbf_kernel_1000.csv")

	user_df = pd.DataFrame(user_matrix(user_ratings), columns=["V0","V1","V2","V3","V4","V5"])
	model_df = pd.DataFrame(model_matrix(df,rec_num), columns=["V0","V1","V2","V3","V4","V5"])

	print("User's judgements of sameness")
	print(user_df)
	print("------------------------------")

	print("Models's judgements of sameness")
	print(model_df)
	print("------------------------------")

	comparison = model_df == user_df

	print("Comparing User's and model's judgements")
	print(comparison)
	
	true_count = comparison.sum().sum()

	print("Numeric alignment is => ", str(true_count/user_df.size))

alignment("R3")

# if sys.argv[1] == "R1" or sys.argv[1] == "R2" or sys.argv[1] == "R3":
# 	alignment(sys.argv[1])
# else:
# 	print("Provide the correct recording number: R1,R2 or R3")
