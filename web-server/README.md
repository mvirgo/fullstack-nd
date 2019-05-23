# Linux Web Server Configuration Project

In this project, I used Amazon Lightsail to configure a secure Linux server, then deploy the Item Catalog website from the previous project to it.

### Server login information

**IP address:** 35.161.230.61
**Port:** 2200

### Deployed website

[35.161.230.61.xip.io](http://35.161.230.61.xip.io/)

Please note that this site may eventually be taken down in order to save on server costs.

### Software installed

(Linux with `sudo apt-get install`)
- apache2
- libapache2-mod-wsgi
- git
- postgresql 
- postgresql-contrib

(pip)
- flask
- sqlalchemy

### Configuration changes made

- add ports 2200 (a new SSH port, configured in coming step), 80 (HTTP) and 123 (NTP) to the accepted incoming ports on Amazon Lightsail settings
- use `sudo apt-get update` and `sudo apt-get upgrade` to install updated packages
- update `/etc/ssh/sshd_config` to use port 2200 instead of 22 (default for SSH)
- configured the `ufw` (firewall) to deny incoming by default, then allowed ports 2200, 80 and 123. Allowed all outgoing as well
- restarted the SSH service
- enabled `ufw`
- added a new user `grader`
- gave `grader` sudo permissions in the `sudoers.d` directory
- created a private key for the `grader` user (using `ssh-keygen` on my Macbook) 
- added the related public key into their `/.ssh/authorized_keys` file
- configured the timezone to UTC
- installed and configured PostgreSQL to not allow remote users, and added `catalog` postgres user
- cloned my Item Catalog project into `var/www` and renamed the folder to `views` for simplicity (matching the related Python file)
- added a configuration file `views.conf` into `/etc/apache2/sites-available/` and configured it accordingly
- updated `views.py` to have an absolute path for the related `.db` file
- Add a python path to `views.conf` so it could appropriately access where `sqlalchemy` was installed
- added the new ip address (deployed website above) to the Google OAuth credentials site for proper authentication usage on the Item Catalog

### Third-party resources used

The following blog and Stack Overflow posts helped me complete this project (in addition to the lessons in the classroom):

- https://www.jakowicz.com/flask-apache-wsgi/
- https://mudspringhiker.github.io/deploying-a-flask-web-app-on-lightsail-aws.html
- https://django.readthedocs.io/en/2.2.x/howto/deployment/wsgi/modwsgi.html
- https://www.godaddy.com/garage/how-to-install-postgresql-on-ubuntu-14-04/
- https://stackoverflow.com/questions/40391409/apache-mod-wsgi-python-doesnt-load-installed-modules

### Other

*Note*: Log-in is only possible with a separate private key not provided here. A separate private key has been provided to the reviewer of the project. For others to view the project, please visit the deployed website.