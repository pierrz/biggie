import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import aiohttp


async def donwload_aio(urls: Iterable[str]) -> List[Tuple[str, bytes]]:
    async def download(url: str) -> Tuple[str, bytes]:
        print(f"Start downloading {url}")
        async with aiohttp.ClientSession() as s:
            resp = await s.get(url)
            data = await resp.json()
        results = data["data"].pop("results")
        print(f"Done downloading {url}")
        return results

    return await asyncio.gather(*[download(url) for url in urls])


async def write_aio(json_data: Iterable[any], output_dir):
    async def write(idx: int, page: Dict):
        print(f"Start writing page {idx}")
        path = Path(output_dir, f"page-{idx}_{datetime.utcnow().isoformat()}.json")
        with open(path, "w", encoding="utf8") as output_file:
            json.dump(page, output_file)
        print(f"Done writting page {idx}")

    await asyncio.gather(*[write(idx, page) for idx, page in enumerate(json_data)])
