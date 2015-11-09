#
# Cookbook Name:: hadoop
# Recipe:: hadoop_start
#
# Copyright (c) 2015 The Authors, All Rights Reserved.


execute 'apply needed permissions for hduser' do
    command 'chown -R hduser:hadoop /usr/local/hadoop'
end

execute 'start NameNode and DataNode daemon' do
    user 'hduser'
    command '/usr/local/hadoop/sbin/start-dfs.sh'
end

execute 'start yarn' do
    user 'hduser'
    command '/usr/local/hadoop/sbin/start-yarn.sh'
end
