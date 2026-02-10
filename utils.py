def now_ts():
    return datetime.utcnow().isoformat()

async def write_jsonl(file_path: Path, data: dict):
    """Append JSON line asynchronously."""
    line = json.dumps(data, separators=(",", ":"))
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: file_path.open("a").write(line + "\n"))
