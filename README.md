# Energy_MLOPS

## All The Command Write In Bash Terminal

## Front Page
![](img/Screenshot%20(50).png)

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
```bash
git add . && git commit -m "First Commit" && git branch -M main
```
```bash
git remote add origin https://github.com/mayurborkar/Energy_MLOPS.git && git push origin main
```
## 5. Write down the params.yaml File As Your Configuration File

## 6. Create Python File Including Reading Data To Model Building Inside src Folder

## 7. Side By Side Fill Up The dvc.yaml File With The Stage Name & Execute The Below Command. No Need To Executive Separate Command For src Python File
```bash
dvc repro
```
## 8. TO Check The Difference In Score You Can See It By Below Command
```bash
dvc metrics diff
```
## 9. To Check THe Metrics You Can Used
```bash
dvc metrics show
```
## 10. Tox Can Create The Virtual Env For Testing Purpose. So Create The Tox File 
```bash
touch tox.ini
```
## 11. Then Create The tests Folder and Create The File Inside That
```bash
mkdir tests
```
```bash
touch tests/conftest.py tests/test_config.py tests/__init__.py
```
## 12. After Write It Down Test Code In test_config.py File Execute Below Command
```bash
tox
```
## 13. If You Update Requirements File You Can Execute Below Command
```bash
tox -r
```
## 14. To Execute The Setup.py File
```bash
pip install -e .
```
## 15. To Create The Package of You src File For That
```bash
python setup.py sdist bdist_wheel
```
