git add profile.zip
git commit -m "generated profile zip [skip ci]"
git remote add origin-pages https://$GITHUB_TOKEN@github.com/therealmysteryman/udi-milight-polyglot > /dev/null 2>&1
git push --quiet --set-upstream origin-pages dev 
