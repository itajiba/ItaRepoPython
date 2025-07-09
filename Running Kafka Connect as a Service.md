To run **Kafka Connect in Standalone mode as a service** on a **Ubuntu server**, you can create a **systemd service unit**. Here's a step-by-step guide:

---

### ✅ 1. **Create a Systemd Service File**

Create a new service file for Kafka Connect:

```bash
sudo nano /etc/systemd/system/kafka-connect-standalone.service
```

Paste the following content, adjusting paths as needed:

```ini
[Unit]
Description=Kafka Connect Standalone Service
After=network.target

[Service]
Type=simple
User=kafka
ExecStart=/opt/kafka/bin/connect-standalone.sh /opt/kafka/config/connect-standalone.properties /opt/kafka/config/my-connector.properties
Restart=on-abnormal

[Install]
WantedBy=multi-user.target
```

- Replace `/opt/kafka/` with your Kafka installation path.
- Replace `kafka` with the appropriate user (e.g., `ubuntu` or a dedicated `kafka` user).
- Ensure the paths to the `connect-standalone.properties` and connector config are correct.

---

### ✅ 2. **Reload Systemd and Enable the Service**

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable kafka-connect-standalone
```

---

### ✅ 3. **Start the Service**

```bash
sudo systemctl start kafka-connect-standalone
```

---

### ✅ 4. **Check Logs and Status**

```bash
sudo systemctl status kafka-connect-standalone
sudo journalctl -u kafka-connect-standalone -f
```

---

Would you like help generating a sample `connect-standalone.properties` or connector config file?