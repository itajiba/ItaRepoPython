##Installling and configuring a Ubuntu server VM with Confluent Kafka

### Installling the Ubuntu server VM

1. Create the VM. I need to modify the Boot Options from BIOS to UFI
2. Mount the Ubuntu ISO and start the VM
3. Follow the steps

### Installing and starting the **Confluent Platform** (which includes Apache Kafka and related tools) on an **Ubuntu Server**:

#### 🧰 Step 1: Install Java (required for Kafka)

Confluent Platform requires Java 11 or later.

```bash
sudo apt update
sudo apt install openjdk-11-jdk -y
```

Verify:
```bash
java -version
```

---

#### 🧰 Step 2: Add the Confluent APT repository

```bash
wget -qO - https://packages.confluent.io/deb/7.9/archive.key | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://packages.confluent.io/deb/7.9 stable main"
sudo apt update
```

> Replace `7.9` with the latest version if needed.

---

#### 🧰 Step 3: Install Confluent Platform (Community Edition)

```bash
sudo apt install confluent-community-2.13 -y
```

This installs:
- Apache Kafka
- Zookeeper
- Schema Registry
- Kafka REST Proxy
- Kafka Connect
- ksqlDB
- Control Center

---

#### 🧰 Step 4: Start the services

Start Zookeeper:
```bash
sudo systemctl start confluent-zookeeper
```

Start Kafka:
```bash
sudo systemctl start confluent-kafka
```

Start other services as needed:
```bash
sudo systemctl start confluent-schema-registry
sudo systemctl start confluent-kafka-rest
sudo systemctl start confluent-ksqldb
sudo systemctl start confluent-control-center
```

Enable them to start on boot:
```bash
sudo systemctl enable confluent-zookeeper
sudo systemctl enable confluent-kafka
```

---

#### 🧪 Step 5: Verify Kafka is running

Check Kafka status:
```bash
sudo systemctl status confluent-kafka
```

Test with:
```bash
kafka-topics --bootstrap-server localhost:9092 --list
```

---

#### 🧼 Optional: Create a topic

```bash
kafka-topics --bootstrap-server localhost:9092 --create --topic test-topic --partitions 1 --replication-factor 1
```

---


### Check if the Open JDK is installed correctly


#### ✅ **1. Check Java in PATH**
Run this command in your terminal:
```bash
which java
```

- If it returns a path like `/usr/bin/java`, Java is in your `PATH`.
- If it returns nothing, Java is either not installed or not added to the `PATH`.

---

#### ✅ **2. Check Java Version**
To confirm Java is working:
```bash
java -version
```

You should see output like:
```
openjdk version "11.0.22" 2024-04-16
OpenJDK Runtime Environment ...
```

---

#### ✅ **3. Check JAVA_HOME Environment Variable**
Sometimes applications like Kafka also rely on `JAVA_HOME`. Check it with:
```bash
echo $JAVA_HOME
```

If it's empty or incorrect, you can set it like this (example for OpenJDK 11):
```bash
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
```

To make this permanent, add those lines to your shell config file:

- For Bash: `~/.bashrc`
- For Zsh: `~/.zshrc`

Then reload the config:
```bash
source ~/.bashrc
```

--- 

### Check if the **Confluent Platform components** are installed on your system

#### 📦 **Method 1: Check Installed Packages (APT/YUM)**

##### On **Debian/Ubuntu**:
```bash
dpkg -l | grep confluent
```

##### On **RHEL/CentOS/Fedora**:
```bash
rpm -qa | grep confluent
```

This will list all installed Confluent components, such as:
- `confluent-kafka`
- `confluent-zookeeper`
- `confluent-control-center`
- `confluent-schema-registry`
- etc.

---

#### 📁 **Method 2: Check Systemd Services**
You can also check which Confluent services are available via systemd:
```bash
systemctl list-units --type=service | grep confluent
```

##### **APT Package Installation**

If you installed it using APT (Advanced Package Tool), the files are typically spread across standard Linux directories:

- Binaries: `/usr/bin/`
- Config files: `/etc/confluent/`
- Logs: `/var/log/confluent/`
- Data: `/var/lib/confluent/`

You can verify the installation path using:
```bash
dpkg -L confluent-community
```
---

### Check if **Confluent Platform services** are currently running on your Ubuntu server

#### ✅ **1. If You Installed via Systemd (APT installation)**

Run this command to list all Confluent-related services:

```bash
systemctl list-units --type=service | grep confluent
```

This will show services like:

- `confluent-kafka.service`
- `confluent-zookeeper.service`
- `confluent-schema-registry.service`
- `confluent-ksql.service`
- `confluent-control-center.service`
- `confluent-connect.service`
- `confluent-rest-proxy.service`

To check the status of a specific service:
```bash
systemctl status confluent-kafka
```

---

### If you have an issue to start the Confluent Control Center

#### ✅ 1. **Ensure the Replication Settings Are Correct**

Please confirm that your `/etc/confluent-control-center/control-center.properties` file includes **all three** of these lines:

```properties
confluent.controlcenter.internal.topics.replication=1
confluent.metrics.topic.replication=1
confluent.monitoring.interceptor.topic.replication=1
```

If any are missing, add them, save the file, and restart the service again.

---

#### 🔁 2. **Restart the Service Again**

After confirming the config file is correct:
```bash
sudo systemctl restart confluent-control-center
```

Then check the logs again:
```bash
journalctl -u confluent-control-center -f
```

---

#### 🧪 3. **Verify Kafka Broker Is Running**

The error also implies that Control Center can’t create topics because it can’t find enough brokers. Let’s make sure your Kafka broker is running:

```bash
sudo systemctl status confluent-kafka
```

If it’s not running, start it:
```bash
sudo systemctl start confluent-kafka
```

---

#### 🧰 4. **(Optional) Manually Create the License Topic**

If the automatic topic creation is still failing, you can try manually creating the required topic with a replication factor of 1:

```bash
kafka-topics --create \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 1 \
  --topic _confluent-controlcenter-license
```

Then restart Control Center again.

---

### If the Metrics are not showing in the Confluent Control-Center

---

#### ✅ To Enable Metrics Reporting for Control Center

You need to **uncomment and configure** the following lines in your `server.properties`:

```properties
metric.reporters=io.confluent.metrics.reporter.ConfluentMetricsReporter
confluent.metrics.reporter.bootstrap.servers=10.222.68.223:9092
confluent.metrics.reporter.topic.replicas=1
```

> Replace `10.222.68.223:9092` with your actual broker address if different.

---

#### 🔄 Steps to Apply the Changes

1. **Edit the file**:
   ```bash
   sudo nano /etc/kafka/server.properties
   ```

2. **Uncomment and update** the metrics reporter section as shown above.

3. **Restart the Kafka broker**:
   ```bash
   sudo systemctl restart confluent-kafka
   # or if using Kafka directly
   sudo systemctl restart kafka
   ```

4. **Verify the metrics topic is created**:
   ```bash
   kafka-topics --bootstrap-server 10.222.68.223:9092 --list | grep _confluent-metrics
   ```

---

#### 🧪 Optional: Check Metrics Are Flowing

You can check if metrics are being published by consuming from the topic:
```bash
kafka-console-consumer --bootstrap-server 10.222.68.223:9092 --topic _confluent-metrics --from-beginning
```

---

