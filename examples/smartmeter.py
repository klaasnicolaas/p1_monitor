# pylint: disable=W0621
"""Asynchronous Python client for the P1 Monitor API."""

import asyncio

from p1monitor import P1Monitor


async def main() -> None:
    """Show example on getting P1 Monitor data."""
    async with P1Monitor(host="example") as client:
        smartmeter = await client.smartmeter()
        print(smartmeter)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
