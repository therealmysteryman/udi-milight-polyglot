git add profile.zip
git commit -m "generated profile zip [skip ci]"
git checkout -b tmp_dev
git checkout dev
git merge my-tmp_dev-work
git remote add origin-pages https://$GITHUB_TOKEN@github.com/therealmysteryman/udi-milight-polyglot 
git status
git push origin-pages dev 
