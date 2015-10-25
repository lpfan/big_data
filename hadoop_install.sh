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

### next prepear the namende
hadoop namenode -format



### to start hadoop
/usr/local/hadoop/sbin/start-dfs.sh &&  /usr/local/hadoop/sbin/start-yarn.sh
