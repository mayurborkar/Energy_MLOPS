# Energy_MLOPS

## All The Command Write In Bash Terminal

## 1. Create Conda Env In Current Local Disk
```bash
conda create --prefix ./env python=3.7 -y
```
## 2. To Activate Conda 
```bash
conda activate ./env
```
## 3. Create template.py & Requirements.txt File
```bash
touch template.py
```
```bash
touch requirements.txt
```
## 4. Initialize The Git and DVC & Add Data
```bash
git init
```
```bash
dvc init
```
```bash
dvc add data_given/EnergyData.csv
```