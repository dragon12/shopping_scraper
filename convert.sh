#!/bin/bash

PROJ=$1
MODULE=$2

if [ "$PROJ" == "" ] || [ "$MODULE" == "" ]; then
    echo "Must specify project and module names"
fi

for f in `find . -name *NAME*`; do
   mv $f `echo $f | sed -e "s/NAME/$PROJ/"`
done

for f in `find . -name *myfile*`; do
   mv $f `echo $f | sed -e "s/myfile/$MODULE/"`
done

sed -i -e "s/NAME/$PROJ/" setup.py
find $PROJ tests -type f -exec sed -i -e "s/NAME/$PROJ/" {} \;
find $PROJ tests -type f -exec sed -i -e "s/myfile/$MODULE/" {} \;

git add tests/$PROJ $PROJ
git commit -a -m "Initial setup"

