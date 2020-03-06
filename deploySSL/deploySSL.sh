#!/bin/bash

arg=$1

if [ ${#arg} == 0 ];
then
	echo -e "archive of certificate is necessary.\nexample:\n\t./deplySSL.sh domain.zip"
	exit
fi


apacheSSL="/etc/apache2/site-available/default-ssl.conf"
ngnixSSL=""
tomcatSSL=""

# 如果使用expr需要注意，由于REGEX中隐含了"^"，所以使得匹配时都是从string首字符开始的。
domain=$(echo $arg | grep -Eo ".*\.(com|org|net|cn|jp|me)")

apache2()
{
	if [ ! -d ~/ca ];
	then
		mkdir ~/ca
	fi
	
	if [ `command -v unzip` ];
	then
		unzip $arg ~/ca
	else
		apt install unzip
		unzip $arg ~/ca
	fi
	
	if [ ! -d /etc/apache2/ca ];
	then
		mkdir /etc/apache2/ca
	fi
	
	cp ~/ca/Apache/* /etc/apache2/ca
	rm -rf ~/ca
	ln -s $apacheSSL /etc/apache2/site-enbaled/ssl.conf
	sed -i 's/ssl.*\.pem$/apache2\/ca\/2_'$domain'.crt/g' $apacheSSL
	sed -i 's/ssl.*\.key/apache2\/ca\/3_'$domain'.key/g' $apacheSSL
	sed -i 's/#SSL.*server-ca.crt/SSLCertificateChainFile \/etc\/apache2\/ca\/1_root_bundle.crt/g' $apacheSSL`
	a2enmod ssl
	systemctl restart apache2
	echo "set up successfully."
	exit
	
}


ngnix()
{
	echo "achieve in future"
}


tomcat()
{
	echo "achieve in future"
}


echo "which server do you whant to deploy?"
echo -e "1.apache2\n2.Nginx\n3.Tomcat"


while :
do
	read -p "your option: " opt
	case $opt in
		1)
			if [  `command -v apache2` ];
			then
				echo "apache2 satisfied."
			else
				`apt install apache2`
			fi
			apache2
			break
			;;
		2)
			if [ `command -v ngnix` ];
			then
				echo "Ngnix satisfied."
			else
				`apt install ngnix`
			fi
			ngnix
			break
			;;
		3)
			if [ `command -v tomcat` ];
			then
				echo "Tomcat satisfied."
			else
				`apt install tomcat`
			fi
			tomcat
			break
			;;
		*)
			echo "invalid option, try again"
			;;
	esac		

done
