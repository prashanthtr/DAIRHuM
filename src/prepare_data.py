
import os

from save_embeddings import store_embeddings
from create_stats_table import pairwise_test

os.chdir("..")

# Analyze recordings to store embeddings

# Replace this with the directory path you want to inspect
main_folder = "data/"

subfolders = [f.path for f in os.scandir(main_folder+"recordings/") if f.is_dir()]

print("Storing embeddings.. ")

for subfolder in subfolders:

	instr1 = "Mridangam"
	instr2 = "Kanjira"
	instr3 = "Track"

	recording_num = subfolder.split("/")[-1]

	read_path = os.path.join(subfolder,instr1)
	out_path = os.path.join(main_folder,"embeddings",recording_num,instr1)

	store_embeddings(read_path,out_path)

	read_path = os.path.join(subfolder,instr2)
	out_path = os.path.join(main_folder,"embeddings",recording_num,instr2)

	store_embeddings(read_path,out_path)

	read_path = os.path.join(subfolder,instr3)
	print(read_path)
	out_path = os.path.join(main_folder,"embeddings",recording_num,instr3)

	store_embeddings(read_path,out_path)

paths = []

for subfolder in subfolders:
	
	recording_num = subfolder.split("/")[-1]
	path = os.path.join(main_folder,"embeddings",recording_num,instr3)
	paths.append(path)

print("Storing model judgements.. ")

pairwise_test(paths)