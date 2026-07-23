"""Async client: fan out one call per instance concurrently."""
import asyncio

from vmos import AsyncVMOSClient


async def main() -> None:
    async with AsyncVMOSClient() as client:
        page = await client.instance.pad_detail(rows=50)
        records = page.get("page", {}).get("records", []) if isinstance(page, dict) else []
        codes = [r["padCode"] for r in records]
        print(f"{len(codes)} instances")

        # Query properties for every pad concurrently
        results = await asyncio.gather(
            *(client.instance.pad_properties(pad_code=c) for c in codes),
            return_exceptions=True,
        )
        for code, res in zip(codes, results):
            print(code, "->", "error" if isinstance(res, Exception) else "ok")


asyncio.run(main())
