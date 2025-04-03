python3 -m venv venv
source venv/bin/activate    
pip install mkdocs mkdocs-material

pip freeze > requirements.txt

mkdocs new .
mkdocs serve


rm -rf .git




git init
git remote add origin https://github.com/waterinag/eqipa-docs.git
git add .
git commit -m "Clean initial commit"
git branch -M main
git push -f origin main  # <- force push to overwrite old content

