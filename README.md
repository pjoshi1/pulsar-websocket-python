
---

## 🐳 Running Pulsar Standalone

Start Pulsar:

```bash
docker compose up -d
```
verify props works

```bash
docker exec -it pulsar-standalone \
  grep -E "webSocketMaxTextFrameSize|maxMessageSize" conf/standalone.conf

```
you should see

```bash
webSocketMaxTextFrameSize=10485760
maxMessageSize=8388608
```

create python env and run client

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r client/requirements.txt

source .venv/bin/activate
python client/pulsar-ws-client.py
```

output for python consumer/producer

```bash
Connecting producer to: ws://localhost:8080/ws/v2/producer/persistent/public/default/file-topic
[PRODUCER] Sent file #1 (102400 bytes ≈ 100.0 KB)
[PRODUCER] Sent file #2 (524288 bytes ≈ 512.0 KB)
[PRODUCER] Sent file #3 (1048576 bytes ≈ 1024.0 KB)
[PRODUCER] Sent file #4 (2097152 bytes ≈ 2048.0 KB)
[PRODUCER] Sent file #5 (5242880 bytes ≈ 5120.0 KB)
[PRODUCER] Done sending all messages.

Connecting consumer to: ws://localhost:8080/ws/v2/consumer/persistent/public/default/file-topic/file-sub-earliest?subscriptionInitialPosition=Earliest
[CONSUMER] Received file #1: 102400 bytes ≈ 100.0 KB
[CONSUMER] Received file #2: 524288 bytes ≈ 512.0 KB
[CONSUMER] Received file #3: 1048576 bytes ≈ 1024.0 KB
[CONSUMER] Received file #4: 2097152 bytes ≈ 2048.0 KB
[CONSUMER] Received file #5: 5242880 bytes ≈ 5120.0 KB
[CONSUMER] Done. Total messages processed: 5
```


take docker compose down/up
```bash

docker compose down
docker compose up -d
```