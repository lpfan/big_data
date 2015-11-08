#
# Cookbook Name:: hadoop_install
# Recipe:: hadoop_install
#
# Copyright (c) 2015 The Authors, All Rights Reserved.


execute 'apt-get update' do
    command 'apt-get update'
end

package 'ssh'
package 'default-jdk'
package 'rsync'

user 'hduser' do
    comment 'Create dedicated hadoop user'
    shell '/bin/bash'
    password '$1$oxcUPjfZ$CzejJ8/BfQFR/vPnLtazS/'
    home '/home/hduser'
    supports :manage_home => true
end 

group 'hadoop' do
    action :create
    members 'hduser'
    append true
end

remote_file '/tmp/hadoop.tar.gz' do
    source 'http://apache.ip-connect.vn.ua/hadoop/common/hadoop-2.7.1/hadoop-2.7.1.tar.gz'
    owner 'hduser'
    group 'hadoop'
    mode '0755'
    action :create
end

execute 'untar hadoop' do
    command 'mkdir /usr/local/hadoop && tar xzf /tmp/hadoop.tar.gz -C /usr/local/hadoop --strip-components=1'
end
