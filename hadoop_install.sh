#Download and install all required software
### Apache Hadoop v 2.7.1
```wget http://apache.ip-connect.vn.ua/hadoop/common/hadoop-2.7.1/hadoop-2.7.1.tar.gz```
### installation of Oracle Java JDK.
sudo apt-get -y update
sudo apt-get -y install python-software-properties
sudo add-apt-repository -y ppa:webupd8team/java
sudo apt-get -y update
sudo apt-get -y install oracle-java7-installer

### extracting hadoop
sudo tar -xzf hadoop-2.7.1.tar.gz -C /usr/local
sudo mv /usr/local/hadoop-2.7.1/ /usr/local/hadoop

### configuring system's env
vim ~/.bashrc
export JAVA_HOME=/usr
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$JAVA_HOME:$HADOOP_HOME/bin

### check
```hadoop version```

# Hadoop configuration
sudo vim /usr/local/hadoop/etc/hadoop/hadoop-env.sh
export JAVA_HOME="/usr/lib/jvm/java-7-oracle"
### Next edit configuration file. Proper configuration is given in this repo as an example
```code
sudo nano core-site.xml
sudo nano yarn-site.xml
sudo nano mapred-site.xml
sudo nano hdfs-site.xml
```

### Create data- and meta- folders
```code
cp
sudo mkdir -p /usr/local/hadoop/hadoop_data/hdfs/namenode
sudo mkdir -p /usr/local/hadoop/hadoop_data/hdfs/datanode
```
### next prepear the namenode
hadoop namenode -format

### to start hadoop
/usr/local/hadoop/sbin/start-dfs.sh &&  /usr/local/hadoop/sbin/start-yarn.sh
### check
jps
