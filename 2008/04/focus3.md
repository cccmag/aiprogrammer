# Hadoop 叢集架設與設定

## 安裝前準備

### 系統需求

硬體需求（以 10 節點叢集為例）：

| 角色 | CPU | 記憶體 | 硬碟 | 數量 |
|------|-----|--------|------|------|
| NameNode | 4 核 | 8GB | 500GB | 1 |
| DataNode | 2 核 | 4GB | 1TB | 9+ |
| 客戶端 | 2 核 | 2GB | 100GB | 任意 |

### 軟體需求

- Java 6 或更高版本
- SSH（用於叢集通訊）
- Linux 作業系統（建議 Ubuntu 或 CentOS）

## 安裝步驟

### 1. 安裝 Java

```bash
# Ubuntu
sudo apt-get install openjdk-6-jdk

# 驗證 Java 安裝
java -version
```

### 2. 建立 Hadoop 使用者

```bash
sudo addgroup hadoop
sudo adduser --ingroup hadoop hduser
sudo ssh-keygen -t rsa -P ""
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```

### 3. 下載並解壓 Hadoop

```bash
wget http://archive.apache.org/dist/hadoop/core/hadoop-0.18.0/hadoop-0.18.0.tar.gz
tar -xzf hadoop-0.18.0.tar.gz
sudo mv hadoop-0.18.0 /usr/local/hadoop
sudo chown -R hduser:hadoop /usr/local/hadoop
```

## 設定 Hadoop

### 設定環境變數

在 `~/.bashrc` 中加入：

```bash
export HADOOP_HOME=/usr/local/hadoop
export JAVA_HOME=/usr/lib/jvm/java-6-openjdk
export PATH=$PATH:$HADOOP_HOME/bin
```

### 設定 hadoop-env.sh

```bash
export JAVA_HOME=/usr/lib/jvm/java-6-openjdk
export HADOOP_HOME=/usr/local/hadoop
export HADOOP_LOG_DIR=/var/log/hadoop
export HADOOP_OPTS=-Djava.net.preferIPv4Stack=true
```

### 設定 core-site.xml

```xml
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>fs.default.name</name>
        <value>hdfs://namenode:9000</value>
        <description>HDFS 名稱節點 URI</description>
    </property>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/var/tmp/hadoop-${user.name}</value>
        <description>臨時目錄</description>
    </property>
</configuration>
```

### 設定 hdfs-site.xml

```xml
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>3</value>
        <description>預設區塊複製數</description>
    </property>
    <property>
        <name>dfs.block.size</name>
        <value>134217728</value>
        <description>區塊大小 128MB</description>
    </property>
    <property>
        <name>dfs.name.dir</name>
        <value>/usr/local/hadoop/hdfs/name</value>
        <description>NameNode 元數據目錄</description>
    </property>
    <property>
        <name>dfs.data.dir</name>
        <value>/usr/local/hadoop/hdfs/data</value>
        <description>DataNode 資料目錄</description>
    </property>
</configuration>
```

### 設定 mapred-site.xml

```xml
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>mapred.job.tracker</name>
        <value>jobtracker:9001</value>
        <description>JobTracker 位址</description>
    </property>
    <property>
        <name>mapred.tasktracker.map.tasks.maximum</name>
        <value>4</value>
        <description>每節點最大 Map 任務數</description>
    </property>
    <property>
        <name>mapred.tasktracker.reduce.tasks.maximum</name>
        <value>2</value>
        <description>每節點最大 Reduce 任務數</description>
    </property>
</configuration>
```

## 格式化 HDFS

```bash
# 格式化名稱節點（首次使用）
hadoop namenode -format

# 確認格式化成功
ls -la /usr/local/hadoop/hdfs/name/
```

## 啟動叢集

### 啟動 Hadoop

```bash
# 啟動 HDFS
start-dfs.sh

# 啟動 MapReduce
start-mapred.sh

# 檢視行程
jps
```

### 驗證安裝

```bash
# 檢視叢集狀態
hadoop dfsadmin -report

# 檢視 Web 介面
# NameNode: http://namenode:50070
# JobTracker: http://jobtracker:50030
```

## 叢集設定

### 設定 masters 和 slaves

在 `conf/masters` 中：

```
namenode
```

在 `conf/slaves` 中：

```
datanode1
datanode2
datanode3
...
```

### SSH 無密碼登入

確保 NameNode 可以無密碼 SSH 到所有 DataNode：

```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub hduser@datanode1
ssh-copy-id -i ~/.ssh/id_rsa.pub hduser@datanode2
```

## 常見問題排除

### 連接拒絕

檢查防火牆設定：

```bash
sudo iptables -L
sudo service iptables stop
```

### 資料節點無法連接

檢查網路設定和 hosts 檔案：

```bash
cat /etc/hosts
# 確保所有節點 IP 正確對應
```

### 磁碟空間不足

清理並監控：

```bash
hadoop dfsadmin -report
hadoop dfs -du -h /
```

## 效能調校

### 記憶體設定

在 `hadoop-env.sh` 中：

```bash
export HADOOP_HEAPSIZE=2000
export HADOOP_OPTS="-server -Xmx2048m -Xms2048m"
```

### JVM 設定

為 Map 和 Reduce 任務設定 JVM 選項：

```bash
export HADOOP_OPTS="-server -XX:+UseParallelGC"
```

### MapReduce 記憶體

在 `mapred-site.xml` 中：

```xml
<property>
    <name>mapred.child.java.opts</name>
    <value>-Xmx512m</value>
</property>
```

## 監控與管理

### Web 介面

- **NameNode**：http://namenode:50070
- **DataNode**：http://datanode:50075
- **JobTracker**：http://jobtracker:50030
- **TaskTracker**：http://tasktracker:50060

### 常用管理命令

```bash
# 平衡叢集
hadoop balancer

# 安全模式
hadoop dfsadmin -safemode enter|leave|get

# 刷新節點
hadoop dfsadmin -refreshNodes

# 升級叢集
hadoop dfsadmin -finalize
```

## 結論

Hadoop 叢集的架設需要仔細規劃和配置。正確的設定可以充分發揮叢集的效能，而良好的監控和維護則能確保叢集穩定運行。

---

**延伸閱讀**

- [MapReduce 分散式運算](focus1.md)
- [HDFS 分散式檔案系統](focus2.md)
- [Hadoop+installation+guide](https://www.google.com/search?q=Hadoop+0.18+installation+guide)