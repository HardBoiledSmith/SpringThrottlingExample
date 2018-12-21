# SpringThrottlingExample

Example for rate limit throttling in Spring MVC 

## Required

1. Java 8 (with JDK)
1. Maven 3
1. IntelliJ IDEA 2018+

## Start Vagrant

1. `cd _provisioning`
1. `vagrant up`
1. Vagrant box `SpringThrottlingExample` reboots after provisioning was successful

## Install WAS (SpringThrottlingExample.war)

1. after reboot, copy `SpringThrottlingExample.war` to `/home/ec2-user/`
1. connect ssh `ssh root@[IP_ADDRESS]`
1. `sudo su`
1. `mv /home/ec2-user/SpringThrottlingExample.war /var/lib/tomcat8/webapps/`
1. `service tomcat8 restart`
1. open `http://[IP_ADDRESS]:8080/SpringThrottlingExample`