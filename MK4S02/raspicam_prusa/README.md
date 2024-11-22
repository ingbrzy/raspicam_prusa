sudo nano /etc/rc.local

sudo chmod -v +x /etc/rc.local

sudo systemctl enable rc-local.service

sudo systemctl is-enabled rc-local.service

sudo systemctl status rc-local.service

systemctl status rc.local.service
