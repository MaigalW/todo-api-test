# INSTRUCTIONS FOR DEPLOYING API IN AWS EC2 (FastAPI + MongoDB)

## What i needed

- AWS account (i used free tier)
- Access to EC2
- Llave SSH generada y descargada ('.pem')

## What type of instance i used (EC2)

- Instance type: 't3.micro'
- OS: Ubuntu 24.04 LTS
- Storage: 8 GB
- Security group:
  - Ports 22 (SSH) and 8000 (FastAPI API)

### How i connected to the instance

- Downloaded the .pem with the keys
- Changed file permissions:
    chmod 400 todo-keys.pem
- Connected to the instance
    ssh -i "todo-keys.pem" ubuntu@<INSTANCE_IP>

### Once inside the instance

- Install docker
sudo snap install docker
- Install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

-Pull from github
git clone https://github.com/MaigalW/todo-api-test.git
cd todo-api-test

-Create own .env using .env.example

-Execute docker-compose
sudo docker-compose up -d --build

-THE API IS SUCCESSFULLY DEPLOYED