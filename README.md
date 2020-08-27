# Clone

```
git clone https://github.com/datkk06/webhook-netbox.git
```

# 1. Manual

- Install python 3.6 and dependencies

```sh
yum groupinstall "Development Tools" -y
yum install https://centos7.iuscommunity.org/ius-release.rpm -y
yum install python-devel -y
yum install python36-devel -y
yum install python36 -y
yum install python-pip -y
yum install python36u-pip -y
pip3.6 install virtualenv==16.7.9
```

- Move source into /opt

```sh
mv <path>/webhook-netbox/ /opt
```

- Create venv

```sh
cd /opt/webhook-netbox
virtualenv env -p python3.6
source env/bin/activate
```

- Install requirement

```sh
pip install -r requirements.txt
```

- Open file config

```sh
vi /opt/webhook-netbox/config.py
```

- Edit parameter

```sh
SLACK_TOKEN
SLACK_CHANNEL
TELEGRAM_TOKEN
TELEGRAM_CHAT_ID
```

- Create Systemd

```sh
vi /etc/systemd/system/webhook-netbox.service
```

- With

```sh
[Unit]
Description=Webhook Netbox
After=network.target

[Service]
PermissionsStartOnly=True
User=root
Group=root
ExecStart=/opt/webhook-netbox/env/bin/python /opt/webhook-netbox/webhook.py --serve-in-foreground

[Install]
WantedBy=multi-user.target
```

- Start

```sh
systemctl daemon-reload
systemctl start webhook-netbox
systemctl status webhook-netbox
```
# 2. Docker

- Move source into /opt

```sh
mv <path>/webhook-netbox/ /opt
cd /opt/webhook-netbox/
```

- Create images

```sh
docker build -t webhook-netbox .
```

- Run container

```sh
docker run -itd -p 5000:5000 --name webhook-netbox webhook-netbox
```
