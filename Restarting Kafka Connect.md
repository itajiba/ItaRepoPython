To restart **Kafka Connect** installed via **APT** on Ubuntu, you’ll typically use **systemd**, since Kafka services are managed as system services.

---

## 🔁 Restart Kafka Connect

### 1. **For Standalone Mode**
If you're running Kafka Connect manually (e.g., with `connect-standalone.sh`), you’ll need to stop and re-run the command manually.

Example:
```bash
# Stop the current process (Ctrl+C if running in foreground)
# Then restart it:
connect-standalone /etc/kafka/connect-standalone.properties your-connector-config.json
```

---

### 2. **For Distributed Mode (as a systemd service)**

If Kafka Connect is running as a systemd service, try:

```bash
sudo systemctl restart kafka-connect
```

If that fails with a "Unit not found" error, check available services:

```bash
systemctl list-units --type=service | grep kafka
```

You might see something like:
- `confluent-kafka-connect.service`
- `kafka-connect-distributed.service`

Then restart the correct one:
```bash
sudo systemctl restart kafka-connect-distributed
```

---

### ✅ Confirm It’s Running

```bash
sudo systemctl status kafka-connect
```

Or check the REST API (default port is `8083`):
```bash
curl http://localhost:8083/
```

---

Would you like help identifying which mode your Kafka Connect is running in or checking the logs?