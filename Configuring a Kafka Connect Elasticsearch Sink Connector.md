To configure a **Kafka Connect Elasticsearch Sink Connector** on a **Ubuntu server** where **Kafka was installed via APT**, follow these steps:

---

## ✅ Prerequisites

1. **Kafka installed via APT** (usually in `/usr/share/kafka`)
2. **Elasticsearch running** (locally or remotely)
3. **Java installed** (Kafka requires Java)
4. **Kafka Connect** is available (comes with Kafka)

---

## 🔌 Step-by-Step: Install and Configure Elasticsearch Connector

### 1. **Install the Elasticsearch Sink Connector**

If you're using **Confluent Hub**, install the connector like this:

```bash
confluent-hub install confluentinc/kafka-connect-elasticsearch:latest
```

If `confluent-hub` is not installed, you can install it:

```bash
wget -qO- https://packages.confluent.io/tools/confluent-hub-client-latest.tar.gz | tar xvz
sudo mv confluent-hub-client /usr/local/bin/confluent-hub
```

Then re-run the install command.

> If you're not using Confluent, you can manually download the connector JAR and place it in Kafka's `libs` or `plugins` directory.

---

### 2. **Create a Connector Configuration File**

Create a file like `elasticsearch-sink.json`:

```json
{
  "name": "elasticsearch-sink-connector",
  "config": {
    "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
    "tasks.max": "1",
    "topics": "your-kafka-topic",
    "connection.url": "http://localhost:9200",
    "type.name": "_doc",
    "key.ignore": "true",
    "schema.ignore": "true"
  }
}
```

Replace:
- `"your-kafka-topic"` with your actual topic name
- `"http://localhost:9200"` with your Elasticsearch endpoint

---

### 3. **Start Kafka Connect**

If you're using the default Kafka installation:

```bash
/usr/share/kafka/bin/connect-standalone.sh \
  /usr/share/kafka/config/connect-standalone.properties \
  elasticsearch-sink.json
```

Or for distributed mode:

```bash
/usr/share/kafka/bin/connect-distributed.sh \
  /usr/share/kafka/config/connect-distributed.properties
```

Then POST the config:

```bash
curl -X POST -H "Content-Type: application/json" \
  --data @elasticsearch-sink.json \
  http://localhost:8083/connectors
```

---

### 4. **Verify the Connector**

Check status:

```bash
curl http://localhost:8083/connectors/elasticsearch-sink-connector/status
```

---

