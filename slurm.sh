#!/bin/sh 
#SBATCH --account=pinaki.sarder 
#SBATCH --job-name=NaglahPipeline
#SBATCH --output=NaglahPipeline_%j.log
#SBATCH --ntasks=1
#SBATCH --mem=40gb
#SBATCH --time=72:00:00
#SBATCH --partition=gpu
#SBATCH --gpus=geforce

date;hostname;pwd
 
module load conda

conda activate wsi

conda run python "./UnifiedFeatureExtraction/runNaglahPipeline.py" \
    --svsBase "/blue/pinaki.sarder/" \
    --fid "659eb008bd96faac30b68fff" \
    --layerName "tubules" \
    --outputdir "/orange/pinaki.sarder/" \
    --username "username" \
    --password "password" \
    --apiUrl "https://athena.rc.ufl.edu/api/v1" \
    --name "tubulePipeline" 