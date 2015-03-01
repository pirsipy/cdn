# -*- mode: ruby -*-
project = 'pirsipy-cdn'
box     = 'pirsipy/cdn'
memory  = '512'

VAGRANTFILE_API_VERSION = '2'

$script = <<SCRIPT
sudo service supervisord restart
SCRIPT

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = box

  config.vm.network 'forwarded_port', guest: 8080, host: 8080
  config.vm.synced_folder '.', '/vagrant', disabled: true
  config.vm.synced_folder '.', '/home/webmaster/app', id: 'app', owner: 'webmaster', group: 'webmaster'

  config.vm.provider 'virtualbox' do |vb|
    vb.customize ['modifyvm', :id, '--name', project, '--memory', memory]
  end

  config.vm.provision 'shell', inline: $script, run: 'always'

end
