#colum foskin 20062042
#!/bin/bash
x=0
while true
do curl --silent cFoskin-elb-8649480.eu-west-1.elb.amazonaws.com?$x >/dev/null;
x=$((x+1))
done