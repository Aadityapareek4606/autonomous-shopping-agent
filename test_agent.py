import asyncio
from agent.browser_agent import run_shopping_task

async def main():
    task = "Go to Amazon.com, search for 'wireless earbuds under $30', and list the names and prices of the top 3 results."
    result = await run_shopping_task(task)
    print("\n--- AGENT FINAL ANSWER ---")
    print(result.final_result())

if __name__ == "__main__":
    asyncio.run(main())