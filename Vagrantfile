# -*- mode: ruby -*-
# vi: set ft=ruby :

# ninjaDVA Dashboard
#

Vagrant.configure("2") do |config|

    # deactivate the standard shared folder
    config.vm.synced_folder ".", "/vagrant", disabled:true

    # name and version of vm image
    config.vm.box = "debian/contrib-stretch64"
    config.vm.box_version = "9.1.0"

    #set hostname for vm
    config.vm.hostname = "dashboardvm"

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

    ########### copy files to vm

    # copy network interfaces definition and hosts file to vm
    config.vm.provision "file", source: "./interfaces", destination: "/home/vagrant/tmp_provision/interfaces"
    config.vm.provision "file", source: "./hosts", destination: "/home/vagrant/tmp_provision/hosts"

    # copy apache vm definition and server code to vm
    config.vm.provision "file", source: "./vmhost.conf", destination: "/home/vagrant/tmp_provision/vmhost.conf"
    config.vm.provision "file", source: "./www", destination: "/home/vagrant/tmp_provision/www"

    # move files to their destination
    config.vm.provision "shell", inline: <<~END
        cd /home/vagrant/tmp_provision/
        install -o root -g root interfaces /etc/network/interfaces
        install -o root -g root hosts /etc/hosts
        install -o root -g root  vmhost.conf /etc/apache2/sites-available/vmhost.conf
        cp -R www/* /var/www/
        chown -R root:root /var/www/
        rm -rf *
    END

    # shared folders
    Dir.mkdir("config") unless Dir.exists?("config")
    config.vm.synced_folder "./config", "/var/www/config", mount_options: ["dmode=777,fmode=666"]
    config.vm.synced_folder "./challenge-descriptions", "/var/www/challenge-descriptions"


    # reload the network configuration
    config.vm.provision "shell", inline: <<~END
    ifdown eth1
        ifup eth1
        ifup eth1:0
        ifup eth1:1
    END


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
end
