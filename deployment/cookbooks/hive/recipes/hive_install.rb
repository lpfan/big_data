#
# Cookbook Name:: hive
# Recipe:: hive_install
#
# Copyright (c) 2015 The Authors, All Rights Reserved.


remote_file '/tmp/hive.tar.gz' do
    source 'http://apache.volia.net/hive/hive-1.2.1/apache-hive-1.2.1-bin.tar.gz'
    owner 'hduser'
    group 'hadoop'
    action :create
end

directory '/usr/local/hive' do
    owner 'hduser'
    group 'hadoop'
end

execute 'hive archive' do
    command 'tar xzf /tmp/hive.tar.gz -C /usr/local/hive --strip-components=1'
end
