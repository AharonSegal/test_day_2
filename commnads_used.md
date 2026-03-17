git init
python -m venv venv
source venv/Scripts/activate
python.exe -m pip install --upgrade pip

pip install -r requirements.txt
pip install geopandas
pip install mysql-connector-python
pip install pandas
pip install matplotlib

uvicorn app.main:app --reload

pip freeze > requirements.txt
git add .  
git commit -m "initial commit"
git push -u origin main

branches
git checkout -b intel
git checkout -b attack
git checkout -b damage

