import argparse
import os

parser = argparse.ArgumentParser(description = "Perform Quering")

parser.add_argument('-q','--qrels_path', help ='qrels path',required = True)
parser.add_argument('-r','--results_path', help = 'results folder directory',required = True)

args= parser.parse_args()

if os.path.exists("run_results.sh"):
    os.remove("run_results.sh")

with open("run_results.sh", 'a') as results_file:
    results_file.write('#!/bin/sh \n')

files = os.listdir(args.results_path)

s = ""

for file in files:
    s += 'echo "results for %s"' %file
    s += "\n"
    s += "./trec_eval"+ " " + args.qrels_path+ " "+ args.results_path+"/"+file+"\n"
    
    s += "\n"

with open("run_results.sh", "a") as text_file:
    text_file.write(s)

print("file created")
print("Use 'chmod +x run_results.sh' to use it as executable")
print("Use ./run_results.sh")