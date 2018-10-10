#!/bin/bash

function initial_setup {
	
	#Create base directories
	mkdir /u01
	mkdir /u02
}

function motd_setup {
		
	echo "** BUY USA - PROD **"  >> /etc/motd
	echo "** NGINIX, DJANGO, POSTGRESQL, PYTHON, JAVA **"  >> /etc/motd
}

function ssh_setup {

	#Setup SSH Configs
	rm /etc/ssh/sshd_config
	echo "Port 7876" >> /etc/ssh/sshd_config
	echo "Protocol 2" >> /etc/ssh/sshd_config
	echo "PermitRootLogin no" >> /etc/ssh/sshd_config
	echo "UsePrivilegeSeparation yes" >> /etc/ssh/sshd_config
	echo "AllowTcpForwarding no" >> /etc/ssh/sshd_config
	echo "X11Forwarding no" >> /etc/ssh/sshd_config
	echo "StrictModes yes" >> /etc/ssh/sshd_config
	echo "IgnoreRhosts yes" >> /etc/ssh/sshd_config
	echo "HostbasedAuthentication no" >> /etc/ssh/sshd_config
	echo "RhostsRSAAuthentication no" >> /etc/ssh/sshd_config
	echo "Banner /etc/motd" >> /etc/ssh/sshd_config
	echo "Subsystem       sftp    /usr/libexec/openssh/sftp-server" >> /etc/ssh/sshd_config
	echo "#Only key access" >> /etc/ssh/sshd_config
	echo "PasswordAuthentication no" >> /etc/ssh/sshd_config
	echo "ChallengeResponseAuthentication no" >> /etc/ssh/sshd_config
	echo "UsePAM no" >> /etc/ssh/sshd_config
	echo "PermitEmptyPasswords no" >> /etc/ssh/sshd_config
	echo "AllowUsers centos" >> /etc/ssh/sshd_config
	
	mkdir /home/centos/.ssh
	echo "ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAQEAj6/CWsnDDwB3GNub+07UdKyPMMkdPnmq2bo5FxNK18ysmocJGzWLgTy4vSM81w8jyA9MiIlB3fz+4AXqAesfuI0+w67Kd9VGNyggYDY85drlCySAh7jqpraLtmow6gn9osFWF04LoQLCSonHgnOPk+uQWBPc9p/HPmorfXr/azZYdEqFBPsx/HlmVRcpOv+Mtt0TRiAEouMOgAZ4b1Ko3lDlC/JuqftMEg+fFU7tuNxIwxcmrwOeYpWytBV92jnH7VnK7vINKnLt4cXqp+VZdfR0dUUKFpi/6UQB5nLM3JpDnXejuTU3ElgnCIELF6YCMPBzK+97mvDt1iInny+YyQ== rsa-key-20170402" >> /home/centos/.ssh/authorized_keys

	echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDSbg7tUod0HP4ggkLplwQjokpLCaLvcGROB3jafiuMbmOT16h+12ow+J6698fXayQNzF5H00NTzTDSgIw8BGL5LKuvoBLeyNFrKHd+Q68j4R47rtc7LmVo9Osve+ynnr7+8Y4gyqR+CYs4nlUX8jtZdMzaGKlsCT2AYhKqaglzS4WsN5XGrXYE0J/CP3b7LHHsOsDjLnyE8nUtdgRgG1+jU9TptR1mZEBOvrf920sRkkoX34aFJ+Vf0CAS+GBYieJuQcFrGYHH/Mw5MqZ0SKxY9WjmVycLyGI2cIcoZ/nB9O2Drpii5VH8raJtfHgmh7eF1tzhamTo2yaf3X7LVKpF centos@mox001
	" >> /home/centos/.ssh/authorized_keys

	chmod 700 /home/centos/.ssh
	chmod 640 /home/centos/.ssh/authorized_keys
	chown -R centos:centos /home/centos/.ssh/
}

function sudoers_setup {

	#Setup sudoers
	rm -rf /etc/sudoers.d
	mkdir /etc/sudoers.d
	echo "centos        ALL=(ALL)       ALL" >> /etc/sudoers.d/centos_sudo
	echo " " >> /etc/sudoers.d/centos_sudo
	
	#Apache
	echo "Cmnd_Alias APACHE = /usr/bin/systemctl stop httpd.service, /usr/bin/systemctl start httpd.service, /usr/bin/systemctl restart httpd.service, /usr/bin/systemctl status httpd.service" >> /etc/sudoers.d/centos_sudo
	echo "centos      ALL=(ALL)       NOPASSWD: APACHE" >> /etc/sudoers.d/centos_sudo
	echo "Defaults!APACHE !requiretty" >> /etc/sudoers.d/centos_sudo
	echo " " >> /etc/sudoers.d/centos_sudo
	
	#Gunicorn System D
	echo "Cmnd_Alias BUYUSA = /usr/bin/systemctl stop buyusa.service, /usr/bin/systemctl start buyusa.service, /usr/bin/systemctl restart buyusa.service, /usr/bin/systemctl status buyusa.service" >> /etc/sudoers.d/centos_sudo
	echo "centos      ALL=(ALL)       NOPASSWD: WUTSTORY" >> /etc/sudoers.d/centos_sudo
	echo "Defaults!WUTSTORY !requiretty" >> /etc/sudoers.d/centos_sudo
	echo " " >> /etc/sudoers.d/centos_sudo
}

function firewall_setup {

#Firewall
cat > /root/firewall_setup.sh <<EOF 
#!/bin/bash
iptables -F
iptables -t nat -F

#SSH rate limit and log drop
iptables -A INPUT -p tcp -m tcp --dport 7876 -m state --state NEW -m recent --set --name SSH --rsource
iptables -A INPUT -p tcp -m tcp --dport 7876 -m recent --rcheck --seconds 30 --hitcount 25 --rttl --name SSH --rsource -j REJECT --reject-with tcp-reset
iptables -A INPUT -p tcp -m tcp --dport 7876 -m recent --rcheck --seconds 30 --hitcount 15 --rttl --name SSH --rsource -j LOG --log-prefix 'SSH brute force '
iptables -A INPUT -p tcp -m tcp --dport 7876 -m recent --update --seconds 30 --hitcount 15 --rttl --name SSH --rsource -j REJECT --reject-with tcp-reset
iptables -A INPUT -p tcp -m tcp --dport 7876 -j ACCEPT

#Postgresql
iptables -I INPUT -p tcp -s 72.252.192.144 --dport 5432 -j ACCEPT
iptables -I INPUT -p tcp -s 104.168.154.22 --dport 5432 -j ACCEPT

#Enable For DDOS Protection
#iptables -A INPUT -p tcp --dport 80 -m limit --limit 20/minute --limit-burst 100 -j ACCEPT

#Other ports
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -P INPUT DROP
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT
/sbin/service iptables save
iptables -L -v
EOF

#Restart SSH and run firewall
service sshd restart
sh /root/firewall_setup.sh

}

function standard_tools_install {
	
	#install htop
	yum -y update
	yum -y install epel-release
	#wget http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm	
	#rpm -ivh epel-release-latest-7.noarch.rpm
	yum -y install wget htop nano sudo net-tools screen mlocate
}

function python_install {

	#Install python 3.5.2
	yum -y groupinstall "Development tools"
	yum -y install zlib-devel bzip2-devel sqlite sqlite-devel openssl-devel gcc
	mkdir /u02/python35
	cd /u02/python35
	wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
	tar -xvf Python-3.5.2.tgz
	cd Python-3.5.2
	#./configure --enable-shared --prefix=/u02/python35
	./configure --prefix=/u02/python35
	make altinstall
	#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/u02/python35/lib #Need this for Python3.5 to work with --enable-shared and for virtual env
	#echo export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/u02/python35/lib >> /home/centos/.bash_profile	
	
	/u02/python35/bin/pip3.5 install --upgrade pip
}

function apache_install {
	#Apache
	yum -y install httpd httpd-devel
}

function set_owners_groups {
	#Set owners and groups
	chown -R centos:centos /u01
	chown -R centos:centos /u02
}

function certbot_https_install {

	#Certbot installation for SSL
	yum -y install python-certbot-apache
	echo "rsa-key-size = 4096" >> /root/cli.ini
	echo "" >> /root/cli.ini
	echo "email = inringame@gmail.com" >> /root/cli.ini
	echo "" >> /root/cli.ini
	echo "domains = buyusa.support, www.buyusa.support" >> /root/cli.ini
	echo "" >> /root/cli.ini
	echo "authenticator = standalone" >> /root/cli.ini
	echo "" >> /root/cli.ini
	echo "preferred-challenges = http-01" >> /root/cli.ini

	certbot certonly -n --agree-tos -c /root/cli.ini	
	
	#Installing cron for renewing cert
	echo "30 03 01 */2 * certbot renew >> /tmp/certbot_renew.log " >> /var/spool/cron/root
	chmod 600 /var/spool/cron/root
}

function post_install {
	updatedb
	service crond start
	chkconfig crond on
	systemctl enable crond.service
}

function postgresql_install {

	yum -y install https://download.postgresql.org/pub/repos/yum/9.6/redhat/rhel-7-x86_64/pgdg-redhat96-9.6-3.noarch.rpm
	yum -y groupinstall "PostgreSQL Database Server 9.6 PGDG"
	#yum -y install postgresql96-server postgresql96-contrib
	#service postgresql-9.6 initdb
	/usr/pgsql-9.6/bin/postgresql96-setup initdb
	chkconfig postgresql-9.6 on service postgresql-9.6 start	

	mv /var/lib/pgsql/9.6/data/pg_hba.conf /var/lib/pgsql/9.6/data/pg_hba.conf.bkup
	cat > /var/lib/pgsql/9.6/data/pg_hba.conf <<EOF	
local   all             all                                     peer
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
host    all             all             72.252.38.228/32  		md5
host    all             all             172.31.91.3/32  		md5
# IPv6 local connections:
host    all             all             ::1/128                 md5
EOF


	mv /var/lib/pgsql/9.6/data/postgresql.conf /var/lib/pgsql/9.6/data/postgresql.conf.bkup
	cat > /var/lib/pgsql/9.6/data/postgresql.conf <<EOF
listen_addresses = '*'
shared_buffers = 128MB
dynamic_shared_memory_type = posix

# logging
log_destination = 'stderr'
logging_collector = on
log_directory = 'pg_log'
log_filename = 'postgresql-%a.log'
log_truncate_on_rotation = on
log_rotation_age = 1d
log_rotation_size = 0
log_line_prefix = '< %m > '
log_timezone = 'UTC'
datestyle = 'iso, mdy'
timezone = 'UTC'
lc_messages = 'C'
lc_monetary = 'C'
lc_numeric = 'C'
lc_time = 'C'

# default configuration for text search
default_text_search_config = 'pg_catalog.english'
EOF

service postgresql-9.6 start
sudo -u postgres psql -c "create user buyusauser password 'buyusa@79'"
sudo -u postgres psql -c "CREATE DATABASE buyusa OWNER buyusauser;"
#sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE "buyusa" to buyusauser;"

systemctl enable postgresql-9.6.service

adduser buyusauser

}

function java_install {
	
	yum -y install java-1.8.0-openjdk.x86_64 #Short fix so grammar checker can find java 0__0
	#Install Java
	mkdir /u02/oracle_java
	cd /u02/oracle_java
	wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u121-b13/e9e7ea248e2c4826b92b3f075a80e441/jdk-8u121-linux-x64.tar.gz
	tar -xvf jdk-8u121-linux-x64.tar.gz
	export JAVA_HOME=/u02/oracle_java/jdk1.8.0_121
	export PATH=$PATH:/u02/oracle_java/jdk1.8.0_121/bin
	
	echo "PATH=$PATH:/u02/oracle_java/jdk1.8.0_121/bin:/usr/local/git/bin;export PATH;export JAVA_HOME=/u02/oracle_java/jdk1.8.0_121" >> /home/centos/.bash_profile
	echo "PATH=$PATH:/u02/oracle_java/jdk1.8.0_121/bin:/usr/local/git/bin;export PATH;export JAVA_HOME=/u02/oracle_java/jdk1.8.0_121" >> /etc/profile.d/java_oracle.sh
}

function gunicorn_systemd {

cat > /etc/systemd/system/buyusa.service <<EOF
[Unit]
Description = Buyusa Gunicorn Server
After = network.target

[Service]
PIDFile = /run/buyusa/buyusa.pid
User = centos
Group = centos
WorkingDirectory = /u01/buyusa/www
ExecStart = /u01/buyusa/www/env/bin/gunicorn buyusa.wsgi -b 127.0.0.1:8000 --timeout 60 -w 9 --access-logfile /u01/buyusa/logs/gunicorn_access.log --error-logfile /u01/buyusa/logs/gunicorn.log -n buyusa -u centos -g centos

[Install]
WantedBy = multi-user.target
EOF

systemctl daemon-reload
systemctl enable buyusa.service

}

function nginx_install {

yum -y install nginx
mkdir /etc/nginx/sites-enabled/
mkdir /etc/nginx/cert/
openssl dhparam 2048 -out /etc/nginx/cert/dhparam.pem

cat > /etc/nginx/sites-enabled/buyusa.support.conf <<EOF
server {
       listen         80;
       server_name    buyusa.support;
       return         301 https://www.$server_name$request_uri;
}

server {
       listen         80;
       server_name    www.buyusa.support;
       return         301 https://www.$server_name$request_uri;
}

server {
  listen 443 ssl http2;
  listen [::]:443 ssl http2;
  server_name  www.buyusa.support;

  ssl    on;
  ssl_certificate    /etc/letsencrypt/live/buyusa.support/fullchain.pem;
  ssl_certificate_key    /etc/letsencrypt/live/buyusa.support/privkey.pem;

  ssl_session_cache shared:SSL:20m;
  ssl_session_timeout 60m;

  ssl_prefer_server_ciphers on;
  ssl_ciphers ECDH+AESGCM:ECDH+AES256:ECDH+AES128:DH+3DES:!ADH:!AECDH:!MD5;

  ssl_dhparam /etc/nginx/cert/dhparam.pem;

  ssl_protocols TLSv1 TLSv1.1 TLSv1.2;

  add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;


  location /static {
        alias /u01/buyusa/www/staticfiles;     # your Django project's static files
    }
	
  location /media {
        alias /u01/buyusa/media;     # your Django project's media files
		client_max_body_size 200M;
    }

  location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
		client_body_temp_path /tmp/nginx 1 2;
		client_max_body_size 200M;
        #proxy_send_timeout 90s;
        #proxy_read_timeout 90s;
        #proxy_connect_timeout 75s;
    }

  #error_page   500 502 503 504  /50x.html;
  #location = /50x.html {
  #  root   html;
  #}
}
EOF

sed -i "21i include /etc/nginx/sites-enabled/*.conf;" /etc/nginx/nginx.conf
systemctl enable nginx
mkdir -P /u01/buyusa/www/staticfiles
chown -R centos:centos /u01/buyusa/www/staticfiles
chcon -Rt httpd_sys_content_t /u01/buyusa/www/staticfiles
chcon -Rt httpd_sys_content_t /u01/buyusa/media
chwon -R centos:centos /var/lib/nginx/tmp
service nginx start

}


#Install script for MOX 003
echo -n "Buyusa Server Setup Script 0____0"
echo ""
echo ""

initial_setup
motd_setup
#ssh_setup
#sudoers_setup
#firewall_setup
standard_tools_install
python_install
java_install
#apache_install
set_owners_groups
certbot_https_install
#postgresql_install
gunicorn_systemd
nginx_install
post_install

