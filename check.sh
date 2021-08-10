#! /bin/bash


echo "Provide the name of the project"
read name_proj
echo "Provide the name of the script"
read name
echo "Provide the description of the project"
read descr
echo "## $name_proj" > README.md
echo >> README.md
echo "$descr" >> README.md
echo >> README.md
echo "Project contains $(wc -l $name | cut -c -3) lines of code" >> README.md
