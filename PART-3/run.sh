#!/bin/sh
python build.py P1-packages/BigSample

python query.py -i output -q P2files/queryfile.txt -r results -rt a -d 2 -tc 1

echo "followed by results for baseline"
echo "\n"

echo "\n"


python query.py -i output -q P2files/queryfile.txt -r results -rt a -d 2 -tc 2


python query.py -i output -q P2files/queryfile.txt -r results -rt a -d 2 -tc 3


python query.py -i output -q P2files/queryfile.txt -r results -rt a -d 3 -tc 1


python query.py -i output -q P2files/queryfile.txt -r results -rt a -d 3 -tc 2


python query.py -i output -q P2files/queryfile.txt -r results -rt a -d 3 -tc 3


python query.py -i output -q P2files/queryfile.txt -r results -rt a -d 4 -tc 1


python query.py -i output -q P2files/queryfile.txt -r results -rt a -d 4 -tc 2


python query.py -i output -q P2files/queryfile.txt -r results -rt a -d 4 -tc 3


python query.py -i output -q P2files/queryfile.txt -r results -rt a -d 5 -tc 1


python query.py -i output -q P2files/queryfile.txt -r results -rt a -d 5 -tc 2


python query.py -i output -q P2files/queryfile.txt -r results -rt a -d 5 -tc 3


python query.py -i output -q P2files/queryfile.txt -r results -rt a -d 10 -tc 1


python query.py -i output -q P2files/queryfile.txt -r results -rt a -d 10 -tc 2


python query.py -i output -q P2files/queryfile.txt -r results -rt a -d 10 -tc 3




python query.py -i output -q P2files/queryfile.txt -r results -rt b -qp 10
echo "followed by results for baseline"
echo "\n"

echo "\n"

python query.py -i output -q P2files/queryfile.txt -r results -rt b -qp 20


python query.py -i output -q P2files/queryfile.txt -r results -rt b -qp 30


python query.py -i output -q P2files/queryfile.txt -r results -rt b -qp 40


python query.py -i output -q P2files/queryfile.txt -r results -rt b -qp 50

python query.py -i output -q P2files/queryfile.txt -r results -rt b -qp 60



python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 2 -tc 1 -qp 10
echo "followed by results for baseline"
echo "\n"
echo "\n"


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 2 -tc 2 -qp 10


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 2 -tc 3 -qp 10


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 3 -tc 1 -qp 10


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 3 -tc 2 -qp 10


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 3 -tc 3 -qp 10


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 4 -tc 1 -qp 10


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 4 -tc 2 -qp 10


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 4 -tc 3 -qp 10




python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 2 -tc 1 -qp 20


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 2 -tc 2 -qp 20


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 2 -tc 3 -qp 20


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 3 -tc 1 -qp 20


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 3 -tc 2 -qp 20


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 3 -tc 3 -qp 20


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 4 -tc 1 -qp 20


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 4 -tc 2 -qp 20


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 4 -tc 3 -qp 20



python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 2 -tc 1 -qp 30

python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 2 -tc 2 -qp 30


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 2 -tc 3 -qp 30


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 3 -tc 1 -qp 30


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 3 -tc 2 -qp 30


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 3 -tc 3 -qp 30


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 4 -tc 1 -qp 30


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 4 -tc 2 -qp 30

python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 4 -tc 3 -qp 30




python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 2 -tc 1 -qp 40

python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 2 -tc 2 -qp 40


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 2 -tc 3 -qp 40


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 3 -tc 1 -qp 40


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 3 -tc 2 -qp 40


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 3 -tc 3 -qp 40


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 4 -tc 1 -qp 40


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 4 -tc 2 -qp 40


python query.py -i output -q P2files/queryfile.txt -r results -rt c -d 4 -tc 3 -qp 40





