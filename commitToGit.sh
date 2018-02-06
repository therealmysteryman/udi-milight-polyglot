git add profile.zip
git commit -m "generated profile zip [skip ci]"
git branch tmp_dev
git checkout dev
git merge tmp_dev
git remote add origin-pages https://$GITHUB_TOKEN@github.com/therealmysteryman/udi-milight-polyglot 
git status
git push origin-pages dev 
