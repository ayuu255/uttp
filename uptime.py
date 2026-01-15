import asyncio
import aiohttp
from datetime import datetime

URL = "https://kstn32-8888.csb.app/terminals/1"  # change with your url

PING_INTERVAL = 5
COLD_START_TIMEOUT = 60     # its  important for Render and do not change it 
NORMAL_TIMEOUT = 10

async def ping(session, timeout):
    try:
        async with session.get(URL, timeout=timeout) as r:
            status = r.status

            if status in [200, 201]:
                print(f"[✅ UP] {datetime.now()} | {status}")
            elif status in [502, 503, 504]:
                print(f"[⏳ WAKING] {datetime.now()} | status {status}")
            else:
                print(f"[⚠️ RESPONSE] {datetime.now()} | {status}")

    except asyncio.TimeoutError:
        print(f"[⏱ TIMEOUT] {datetime.now()} — server still waking")

    except Exception as e:
        print(f"[❌ ERROR] {datetime.now()} — {e}")


async def main():
    timeout = aiohttp.ClientTimeout(total=COLD_START_TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout) as session:

        print("🚀 Advanced Uptime Monitor Started (Render-safe)")

        while True:
            await ping(session, timeout)
            await asyncio.sleep(PING_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
