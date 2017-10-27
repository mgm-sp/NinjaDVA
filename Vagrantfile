# -*- mode: ruby -*-
# vi: set ft=ruby :

# ninjaDVA Dashboard
#
# Requirements:
# Please execute `vagrant plugin install vagrant-triggers`
# if you start the vm the first time and get an error

Vagrant.configure("2") do |config|

    # set username and ssh key for vagrant
    config.ssh.username="root"
    config.ssh.private_key_path = "./vagrant_key"

    # command that will be executed except of "sudo %c"
    # box will run under root thus we don't need sudo
    config.ssh.sudo_command='%c'

    # deactivate the standard shared folder
    config.vm.synced_folder ".", "/vagrant", disabled:true

    # name and url of vm image
    config.vm.box = "debian-minimal-64"
    config.vm.box_url = "http://vagrant-repo.mgm-edv.de/debian-minimal-64.json"
    config.vm.box_check_update = false #TODO: this is a debug statement for home office ... remove this later
    
    # add a interface to the vm that is in the same internal networke like the gateway
    #config.vm.network "private_network", type: "dhcp", virtualbox__intnet: "broken"
    config.vm.network "private_network", auto_config: false, virtualbox__intnet: "broken"

    # define commands that will be executed on the vm after the vm is
    # up and running. This is the right place for software installation.
    config.vm.provision "shell", inline: <<~END
        apt-get -y update
	    apt-get -y remove isc-dhcp-client
        apt-get -y install apache2 ruby ruby-dev ruby-sqlite3 sqlite3 inotify-tools dhcpcd5 psmisc atool
	    killall dhclient
        gem install argon2
        cd /tmp
        wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
        aunpack phantomjs-2.1.1-linux-x86_64.tar.bz2
        rm -rf /usr/share/phantom*
        mv phantomjs-2.1.1-linux-x86_64 /usr/share/
        ln -sf /usr/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/phantomjs
    END

    # copy network interfaces definition and hosts file to vm
    config.vm.provision "file", source: "./interfaces", destination: "/etc/network/interfaces"
    config.vm.provision "file", source: "./hosts", destination: "/etc/hosts"

    # reload the network configuration
    config.vm.provision "shell", inline: <<~END
	ifdown eth1
        ifup eth1
        ifup eth1:0
        ifup eth1:1
    END


    # copy apache vm definition and server code to vm
    config.vm.provision "file", source: "./vmhost.conf", destination: "/etc/apache2/sites-available/vmhost.conf"
    config.vm.provision "file", source: "./www", destination: "/var/www"

    Dir.mkdir("config") unless Dir.exists?("config")
    config.vm.synced_folder "./config", "/var/www/config", mount_options: ["dmode=777,fmode=666"]
    config.vm.synced_folder "./challenge-descriptions", "/var/www/challenge-descriptions"

    # define commands that will be executed after the code was copied to
    # the vm. This is the place where your server configuration can take place
    config.vm.provision "shell", inline: <<~END
        chown www-data:www-data /var/www/clonecloud
        service apache2 stop
        a2enconf serve-cgi-bin
        a2dismod mpm_event
        a2enmod mpm_prefork
        a2enmod cgi
        a2enmod headers
        a2enmod rewrite
	a2enmod auth_digest
        a2ensite vmhost
        a2dissite 000-default
        service apache2 start
    END
        # install -d -o www-data -g www-data -m 777 /var/www/config
end

# xvfb-run --server-args="-screen 0 640x480x16" phantomjs
