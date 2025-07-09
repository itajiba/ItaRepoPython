The error message:

```
{"error_code":404,"message":"No status found for connector elasticsearch-sink-connector"}
```

means that the connector **has not been created or registered** with Kafka Connect.

---

### ✅ Here's how to proceed:

#### **1. Confirm Kafka Connect is Running**
Make sure the Kafka Connect service is up and running on your Ubuntu server:

```bash
systemctl status confluent-kafka-connect
```

Or if you're running it manually:

```bash
ps aux | grep connect
```

---

#### **2. Register the Connector**
If it’s not registered yet, you need to POST the JSON config to the Kafka Connect REST API:

```bash
curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "elasticsearch-sink-connector",
    "config": {
      "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
      "tasks.max": "1",
      "topics": "customer1topic80",
      "connection.url": "http://10.222.68.115:9200",
      "type.name": "_doc",
      "key.ignore": "true",
      "schema.ignore": "true"
    }
  }'
```

> Replace `localhost:8083` with the actual IP/hostname of your Kafka Connect REST endpoint if it's different.

---

#### **3. Confirm Registration**
After posting, check the connector list:

```bash
curl http://localhost:8083/connectors
```

You should see `elasticsearch-sink-connector` in the list.

---

Would you like help crafting or posting the JSON config from your machine? Or checking if Kafka Connect is running properly?