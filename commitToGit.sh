git add profile.zip
git commit -m "generated profile zip [skip ci]"
git remote add origin-pages https://$GITHUB_TOKEN@github.com/therealmysteryman/udi-milight-polyglot 
git push --set-upstream origin-pages dev 
