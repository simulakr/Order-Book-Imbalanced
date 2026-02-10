SYMBOL = "btcusdt"
DEPTH_LEVELS = 10 # Level-2 depth (top N levels)
OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

DEPTH_FILE = OUTPUT_DIR / "depth.jsonl"
TRADE_FILE = OUTPUT_DIR / "trades.jsonl"

# Binance Futures WebSocket endpoints
DEPTH_STREAM = f"wss://fstream.binance.com/ws/{SYMBOL}@depth{DEPTH_LEVELS}@100ms"
TRADE_STREAM = f"wss://fstream.binance.com/ws/{SYMBOL}@trade"
