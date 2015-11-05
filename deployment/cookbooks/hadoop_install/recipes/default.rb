#
# Cookbook Name:: hadoop_install
# Recipe:: default
#
# Copyright (c) 2015 The Authors, All Rights Reserved.


execute 'apt-get update' do
    command 'apt-get update'
end

package 'ssh'
package 'default-jdk'
package 'rsync'
