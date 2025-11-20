import base64
import json
import os
import time
import json
import websocket
from json.decoder import JSONDecodeError



# -------------------------
# Config
# -------------------------

ENABLE_TLS = False
SCHEME = "wss" if ENABLE_TLS else "ws"

PULSAR_HTTP_WS_HOST = "localhost"
PULSAR_HTTP_WS_PORT = 8080

TOPIC_NAME = "file-topic"
# SUBSCRIPTION_NAME = "file-sub"

PRODUCER_URL = (
    f"{SCHEME}://{PULSAR_HTTP_WS_HOST}:{PULSAR_HTTP_WS_PORT}"
    f"/ws/v2/producer/persistent/public/default/{TOPIC_NAME}"
)
SUBSCRIPTION_NAME = "file-sub-earliest"

CONSUMER_URL = (
    f"{SCHEME}://{PULSAR_HTTP_WS_HOST}:{PULSAR_HTTP_WS_PORT}"
    f"/ws/v2/consumer/persistent/public/default/{TOPIC_NAME}/{SUBSCRIPTION_NAME}"
    "?subscriptionInitialPosition=Earliest"
)
# File sizes to send (bytes)
FILE_SIZES = [
    100 * 1024,         # 100 KB
    512 * 1024,         # 512 KB
    1 * 1024 * 1024,    # 1 MB
    2 * 1024 * 1024,    # 2 MB
    5 * 1024 * 1024     # 5 MB
]


# -------------------------
# Helpers
# -------------------------

def make_fake_file_bytes(size_bytes: int) -> bytes:
    """
    Create pseudo file content of given size.
    Using os.urandom so it's real binary, but you can replace this
    with open(..., 'rb').read() for real files.
    """
    return os.urandom(size_bytes)


def encode_payload(data: bytes) -> str:
    """Base64-encode bytes -> UTF-8 string for the WebSocket JSON payload."""
    return base64.b64encode(data).decode("utf-8")


def decode_payload(payload_b64: str) -> bytes:
    """Base64-decode string -> original bytes."""
    return base64.b64decode(payload_b64.encode("utf-8"))


# -------------------------
# Producer
# -------------------------

# ... keep your other imports / constants ...


def produce_files():
    print(f"Connecting producer to: {PRODUCER_URL}")
    ws = websocket.create_connection(PRODUCER_URL)

    try:
        for idx, size in enumerate(FILE_SIZES, start=1):
            data = make_fake_file_bytes(size)
            payload_str = encode_payload(data)

            message = {
                "payload": payload_str,
                "properties": {
                    "original_size_bytes": str(size),
                    "file_index": str(idx),
                },
                "context": str(idx),
            }

            # Send JSON text frame; don't wait for ACK
            ws.send(json.dumps(message))

            print(
                f"[PRODUCER] Sent file #{idx} "
                f"({size} bytes ≈ {size / 1024:.1f} KB)"
            )

        print("[PRODUCER] Done sending all messages.")
    finally:
        ws.close()

# -------------------------
# Consumer
# -------------------------

def consume_files(expected_count: int):
    print(f"\nConnecting consumer to: {CONSUMER_URL}")
    ws = websocket.create_connection(CONSUMER_URL)

    received = 0

    try:
        while received < expected_count:
            msg_raw = ws.recv()
            if not msg_raw:
                print("[CONSUMER] No more messages, exiting.")
                break

            msg = json.loads(msg_raw)

            # Decode the payload
            data = decode_payload(msg["payload"])
            size_bytes = len(data)
            size_kb = size_bytes / 1024.0

            properties = msg.get("properties", {})
            file_index = properties.get("file_index", "?")

            print(
                f"[CONSUMER] Received file #{file_index}: "
                f"{size_bytes} bytes ≈ {size_kb:.1f} KB"
            )

            # Acknowledge successful processing so Pulsar can mark the message consumed
            ack_payload = {"messageId": msg["messageId"]}
            ws.send(json.dumps(ack_payload))

            received += 1

        print(f"[CONSUMER] Done. Total messages processed: {received}")
    finally:
        ws.close()


# -------------------------
# Main
# -------------------------

if __name__ == "__main__":
    # Give Pulsar a bit of time to be ready after container start
    print("Waiting 3 seconds for Pulsar to be fully up (if just started)...")
    time.sleep(3)

    # 1) Produce a batch of "files"
    produce_files()

    # 2) Consume them and print their sizes
    consume_files(expected_count=len(FILE_SIZES))
