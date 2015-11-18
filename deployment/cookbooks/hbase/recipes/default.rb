#
# Cookbook Name:: hbase
# Recipe:: default
#
# Copyright (c) 2015 The Authors, All Rights Reserved.

include_recipe "hadoop::hadoop_install"
include_recipe "hadoop::hadoop_config"
include_recipe "hbase::hbase_intsall"
include_recipe "hbase::hbase_config"
