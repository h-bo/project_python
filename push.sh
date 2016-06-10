git add *
echo -n "enter your commit message:"
read message
git commit -m ${message}
git push -u origin master