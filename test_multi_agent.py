import asyncio
from agent.browser_agent import run_multi_item_task

async def main():
    items = ["phone charger", "bluetooth earbuds"]
    budget = 1000

    result = await run_multi_item_task(items, budget)
    print("\n--- MULTI-ITEM RESULT ---")
    print(result.final_result())

if __name__ == "__main__":
    asyncio.run(main())