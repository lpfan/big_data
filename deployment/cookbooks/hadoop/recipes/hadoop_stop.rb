#
# Cookbook Name:: hadoop
# Recipe:: hadoop_stop
#
# Copyright (c) 2015 The Authors, All Rights Reserved.


execute 'stop NameNode and DataNode daemon' do
    user 'hduser'
    command '/usr/local/hadoop/sbin/stop-dfs.sh'
end

execute 'stop yarn' do
    user 'hduser'
    command '/usr/local/hadoop/sbin/stop-yarn.sh'
end
