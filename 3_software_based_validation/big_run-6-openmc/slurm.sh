#!/usr/local_rwth/bin/bash     

###
### Christopher Fichtlscherer
###

#SBATCH --job-name=drm
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --ntasks=1
#SBATCH --time=24:00:00
#SBATCH --mem=6000M
#SBATCH --output=drm.out
#SBATCH --account=p0020230

(module load HDF5/1.14.0-serial.lua && module load GCC/11.3.0.lua && module load Python/3.9.6 && python3.9 run.py)

