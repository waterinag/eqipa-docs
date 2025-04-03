python3 -m venv venv
source venv/bin/activate    
pip install mkdocs mkdocs-material

pip freeze > requirements.txt

mkdocs new .
mkdocs serve


rm -rf .git



# Initialize Git Repo
git init
git remote add origin https://github.com/waterinag/eqipa-docs.git
git add .
git commit -m "first commit"
git branch -M main
git push -f origin main 

# Deploy to GitHub Pages
mkdocs gh-deploy


https://waterinag.github.io/eqipa-docs/
