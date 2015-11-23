#!/bin/bash
x=0
while true
do curl cFoskin-elb-8649480.eu-west-1.elb.amazonaws.com?$x;
x=$((x+1))
done