#
# Cookbook Name:: hadoop_install
# Recipe:: hadoop_config
#
# Copyright (c) 2015 The Authors, All Rights Reserved.


template '/home/hduser/.bashrc' do
    source 'hadoop_config/hduser_bashrc.erb'
    owner 'hduser'
    group 'hduser'
end

template '/usr/local/hadoop/etc/hadoop/hadoop-env.sh' do
    source 'hadoop_config/hadoop-env.sh.erb'
end

execute 'create hadoop tmp folder' do
    command 'mkdir -p /media/hadoop/tmp && chown -R hduser:hadoop /hadoop'
end

template '/usr/local/hadoop/etc/hadoop/core-site.xml' do
    source 'hadoop_config/core-site.xml.erb'
end

template '/usr/local/hadoop/etc/hadoop/mapred-site.xml' do
    source 'hadoop_config/mapred-site.xml.erb'
end

template '/usr/local/hadoop/etc/hadoop/hds-site.xml' do
    source 'hadoop_config/hdfs-site.xml.erb'
end

execute 'create local directories for Namenode and Datanode' do
    command 'mkdir -p /media/hadoop/meta/dfs/namenode && mkdir -p /media/hadoop/data/dfs/datanode'
end

execute 'apply needed permissions for hduser' do
    command 'chown -R hduser:hadoop /media/hadoop'
end

execute 'apply needed permissions for hduser' do
    command 'chown -R hduser:hadoop /usr/local/hadoop'
end

execute 'format hdfs node' do
    command 'hdfs namenode -format'
end
