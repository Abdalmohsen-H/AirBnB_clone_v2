#!/usr/bin/env bash
# Task0: Bash script to sets up Nginx web servers to deploy web_static later we will use fabric(python)
# -y means assume yes on all question or choices during executing command
#If an undesirable situation occurs then apt-get will abort.

# updates apt (Advanced Packaging Tool)
sudo apt-get update -y

#install nginx web server
sudo apt-get -y install nginx

# -p option in mkdir command stands for "parent.", it tells mkdir to create not
# only the specified directory but also any necessary parent directories that do not exist.
# but passed in path to mkdir, 5 lines below could be just 2 lines but I will leave them for now
sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

sudo touch /data/web_static/releases/test/index.html
echo "<html>
    <head>
    </head>
    <body>
        It's working!! A. Hesham
    </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

rm -rf /data/web_static/current
# -s symplic link , -f force create this new even if name already exist onpath then overwrite
sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current

# -R operate recursively, changing ownership not only for specified directory, but also of all files and subdirectories within it.
# to be owned by ubuntu/ubuntu user/group
sudo chown -R ubuntu:ubuntu /data/

# using sed command with (a), find line contain pattern "server_name" then append (a) after it the location with alias
# on nginx default config file, -i means change in place , / befor a, is just a delimeter have no meaning and could be replaced
# 0,/^\tserver_name/a -> 0 means first match , a for append
if ! grep -q 'location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default; then
    awk '/server_name/ && !flag {print; print "\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n}"; flag=1; next} 1' /etc/nginx/sites-enabled/default | sudo tee /etc/nginx/sites-enabled/default >/dev/null
fi

# restart nginx to apply new changes in config
sudo service nginx restart

# Exit mode
exit
