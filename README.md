## Pulsar WebSocket Python Demo

Purpose: **Verify that Apache Pulsar's WebSocket interface can send and consume messages larger than 1 MB (tested up to 5 MB) by ensuring the standalone config allows sufficiently large WebSocket text frames and message sizes.**

What it does:
1. Starts a local Apache Pulsar standalone via Docker.
2. Produces random binary blobs ("files") of preset sizes to a topic via the WebSocket producer endpoint.
3. Consumes them from the earliest position via the WebSocket consumer endpoint, base64‑decodes payloads, prints sizes, and acknowledges each `messageId`.

Payload bytes are base64 encoded inside a JSON frame (`{"payload": "..."}`) because Pulsar's WS API expects text frames. Sizes used: 100KB, 512KB, 1MB, 2MB, 5MB (the >1MB sizes demonstrate the verification goal).

### Quick start
```bash
# 1. Start Pulsar standalone
docker compose up -d

# 2. (Optional) Verify large frame settings
docker exec -it pulsar-standalone grep -E 'webSocketMaxTextFrameSize|maxMessageSize' conf/standalone.conf

# 3. Python env & deps
python3 -m venv .venv
source .venv/bin/activate
pip install -r client/requirements.txt

# 4. Run producer + consumer (single script runs both sequentially)
python client/pulsar-ws-client.py
```

### Sample output
```text
Connecting producer to: ws://localhost:8080/ws/v2/producer/persistent/public/default/file-topic
[PRODUCER] Sent file #1 (102400 bytes ≈ 100.0 KB)
...
[PRODUCER] Sent file #5 (5242880 bytes ≈ 5120.0 KB)
Connecting consumer to: ws://localhost:8080/ws/v2/consumer/persistent/public/default/file-topic/file-sub-earliest?subscriptionInitialPosition=Earliest
[CONSUMER] Received file #1: 102400 bytes ≈ 100.0 KB
...
[CONSUMER] Received file #5: 5242880 bytes ≈ 5120.0 KB
[CONSUMER] Done. Total messages processed: 5
```

### Cleanup
```bash
docker compose down
```

That's it. The script shows how to move binary data through Pulsar using its WebSocket API with simple base64 wrapping.
