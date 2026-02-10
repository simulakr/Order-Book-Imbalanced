import asyncio
import json
import websockets
from datetime import datetime
from pathlib import Path

# =========================
# CONFIG
# =========================
SYMBOL = "btcusdt"
DEPTH_LEVELS = 10  # Level-2 depth (top N levels)
OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

DEPTH_FILE = OUTPUT_DIR / "depth.jsonl"
TRADE_FILE = OUTPUT_DIR / "trades.jsonl"

# Binance Futures WebSocket endpoints
DEPTH_STREAM = f"wss://fstream.binance.com/ws/{SYMBOL}@depth{DEPTH_LEVELS}@100ms"
TRADE_STREAM = f"wss://fstream.binance.com/ws/{SYMBOL}@trade"


# =========================
# UTILS
# =========================

def now_ts():
    return datetime.utcnow().isoformat()


async def write_jsonl(file_path: Path, data: dict):
    """Append JSON line asynchronously."""
    line = json.dumps(data, separators=(",", ":"))
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: file_path.open("a").write(line + "\n"))


# =========================
# DEPTH COLLECTOR
# =========================

async def collect_depth():
    while True:
        try:
            async with websockets.connect(DEPTH_STREAM, ping_interval=20) as ws:
                print("Connected to depth stream")

                async for msg in ws:
                    data = json.loads(msg)

                    record = {
                        "ts": now_ts(),
                        "event_time": data.get("E"),
                        "bids": data.get("b", []),
                        "asks": data.get("a", []),
                    }

                    await write_jsonl(DEPTH_FILE, record)

        except Exception as e:
            print("Depth stream error:", e)
            await asyncio.sleep(5)


# =========================
# TRADE COLLECTOR
# =========================

async def collect_trades():
    while True:
        try:
            async with websockets.connect(TRADE_STREAM, ping_interval=20) as ws:
                print("Connected to trade stream")

                async for msg in ws:
                    data = json.loads(msg)

                    record = {
                        "ts": now_ts(),
                        "event_time": data.get("E"),
                        "price": data.get("p"),
                        "qty": data.get("q"),
                        "is_buyer_maker": data.get("m"),
                    }

                    await write_jsonl(TRADE_FILE, record)

        except Exception as e:
            print("Trade stream error:", e)
            await asyncio.sleep(5)


# =========================
# MAIN
# =========================

async def main():
    print("Starting Binance Level-2 + Trade collector...")

    await asyncio.gather(
        collect_depth(),
        collect_trades(),
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped by user")
