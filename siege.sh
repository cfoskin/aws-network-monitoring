#colum foskin 20062042
#!/bin/bash
sudo apt-get install -y siege
siege -d10 -c500 cFoskin-elb-8649480.eu-west-1.elb.amazonaws.com >/dev/null;
