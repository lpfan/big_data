#
# Cookbook Name:: hbase
# Recipe:: hbase_install
#
# Copyright (c) 2015 The Authors, All Rights Reserved.

remote_file '/tmp/hbase.tar.gz' do
    source 'http://apache.ip-connect.vn.ua/hbase/stable/hbase-1.1.2-bin.tar.gz'
    owner 'hduser'
    group 'hadoop'
    mode '0755'
    action :create
end

execute 'untar hbase' do
    command 'mkdir /usr/local/hbase && tar xzf /tmp/hbase.tar.gz -C /usr/local/hadoop --strip-components=1'
end

execute 'chown hduser->hbase' do
    command 'chown -R hduser:hadoop /usr/local/hbase'
end
