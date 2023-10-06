# task 101 :puppet script to do task 0
exec {'install_nginx':
  command  => 'sudo apt-get update ; sudo apt-get -y install nginx',
  provider => shell,
}

-> package {'nginx':
  ensure   => 'present',
  provider => 'apt'
}

-> exec {'create_multi_dirs':
  command  => 'sudo mkdir -p /data/web_static/releases/test/ ; sudo mkdir -p /data/web_static/shared/',
  provider => shell,
}

-> file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "this is just content for testing for web static with fabric project\n"
}

-> file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test'
}

-> exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/'
}

-> exec {'replace_config_with_sed':
  command  => 'sh -c \'sed -i "/server_name/a location /hbnb_static { alias /data/web_static/current/;}" /etc/nginx/sites-enabled/default\' ',
  provider => shell,
}

-> exec {'apply_new_config':
  command  => 'sudo service nginx restart',
  provider => shell,
}
