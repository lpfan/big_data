#
# Cookbook Name:: hbase
# Recipe:: hbase_config
#
# Copyright (c) 2015 The Authors, All Rights Reserved.


#include_recipe "hbase::hbase_install"


template '/home/hduser/.bashrc' do
    source 'default/hduser_bashrc.erb'
    owner 'hduser'
    group 'hduser'
end

execute 'source user profile' do
    user 'hduser'
    command 'source ~/.bashrc'
end

template '/usr/local/hbase/conf/hbase-site.xml' do
    source 'default/hbase-site.xml.erb'
end
