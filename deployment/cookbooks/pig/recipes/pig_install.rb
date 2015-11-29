#
# Cookbook Name:: pig
# Recipe:: pig_install
#
# Copyright (c) 2015 The Authors, All Rights Reserved.


remote_file '/tmp/pig.tar.gz' do
    source 'http://apache.ip-connect.vn.ua/pig/pig-0.15.0/pig-0.15.0.tar.gz'
    owner 'hduser'
    group 'hadoop'
end

execute 'untar pig' do
    command 'mkdir /usr/local/pig && tar xzf /tmp/pig.tar.gz -C /usr/local/pig --strip-components=1'
end

execute 'chown pig dir' do
    command 'chown -R hduser+rab:hadoop /usr/local/pig'
end
