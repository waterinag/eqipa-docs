# Initialize mkdocs
python3 -m venv venv
source venv/bin/activate    
pip install mkdocs mkdocs-material

pip freeze > requirements.txt

mkdocs new .
mkdocs serve
http://127.0.0.1:8000/eqipa-docs/

# Building site: When finished editing, build a static site from Markdown files:
mkdocs build


# Remove git files from the folder
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








# Update MkDocs Site After Changes
git add .
git commit -m "updated"
git push origin main

# Redeploy the site:
mkdocs gh-deploy





# If gdal not works in Windows then try
set GDAL_DATA=%CONDA_PREFIX%\Library\share\gdal
set PROJ_LIB=%CONDA_PREFIX%\Library\share\proj
