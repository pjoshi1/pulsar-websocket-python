
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


docker compose down
docker compose up -d
```