FROM python:3.5
ADD dist/qube_placeholder*.whl .
ADD requirements.txt .
RUN pip install -r requirements.txt
RUN pip install qube_placeholder*.whl 

# install Consul CLI tool
RUN apt-get update && apt-get install -y jq unzip
RUN wget https://releases.hashicorp.com/consul/0.7.1/consul_0.7.1_linux_amd64.zip
RUN unzip consul_0.7.1_linux_amd64.zip -d /usr/local/bin/

ADD scripts/startup.sh .
CMD ["./startup.sh"]  