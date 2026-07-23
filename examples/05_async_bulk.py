"""Async client: fan out one call per instance concurrently."""
import asyncio

from vmos import AsyncVMOSClient


async def main() -> None:
    async with AsyncVMOSClient() as client:
        pads = await client.phone.user_pad_list()
        codes = [p["padCode"] for p in pads]
        print(f"{len(codes)} instances")

        # Query properties for every pad concurrently
        results = await asyncio.gather(
            *(client.instance.pad_properties(pad_code=c) for c in codes),
            return_exceptions=True,
        )
        for code, res in zip(codes, results):
            print(code, "->", "error" if isinstance(res, Exception) else "ok")


asyncio.run(main())
