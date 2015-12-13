#
# Cookbook Name:: tweetray
# Recipe:: default
#
# Copyright (c) 2015 The Authors, All Rights Reserved.
package "ssh"
package "default-jdk"
package "rsync"
package "python-dev"
package "gcc"
package "rabbitmq-server"
package "mongodb"
package "python-virtualenv"

include_recipe "tweetray::hadoop_install"
include_recipe "tweetray::hadoop_config"
include_recipe "tweetray::mongodb_config"
include_recipe "tweetray::spark"
include_recipe "tweetray::start_app"
