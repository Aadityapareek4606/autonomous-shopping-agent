from dotenv import load_dotenv
from browser_use import Agent, ChatGoogle

load_dotenv()

def get_llm():
    """Primary Gemini LLM for the agent."""
    return ChatGoogle(model="gemini-flash-lite-latest")

def get_fallback_llm():
    """Backup LLM used automatically if the primary model is overloaded (503/429 errors)."""
    return ChatGoogle(model="gemini-3.6-flash")

async def run_shopping_task(task: str):
    """
    Runs a browser automation task using browser-use + Gemini.
    Falls back to a lighter model automatically if the primary is overloaded.
    """
    llm = get_llm()
    fallback_llm = get_fallback_llm()
    agent = Agent(task=task, llm=llm, fallback_llm=fallback_llm)
    result = await agent.run()
    return result
async def run_multi_item_task(items: list[str], budget: float, currency: str = "INR"):
    """
    Searches for multiple items across Amazon.in and Flipkart,
    then recommends the best combination that fits within the total budget.
    """
    items_str = ", ".join(items)
    task = (
        f"You are a smart shopping assistant. The user wants to buy: {items_str}. "
        f"Total budget: {currency} {budget}. "
        f"CRITICAL RULE: You must ONLY record product names, prices, and ratings that you have "
        f"actually extracted from the live webpage using the extract action. "
        f"NEVER write product data into any file from memory or assumption. "
        f"If you have not called extract on a search results page yet, you have no data to record. "
        f"For each item: "
        f"1. Navigate to Amazon.in, search for the item, and use the extract action to pull the top 3 real results with exact prices and ratings from the page. "
        f"2. Navigate to Flipkart.com, search for the item, and use the extract action to pull the top 3 real results with exact prices and ratings from the page. "
        f"3. Only after extracting real data from both sites, compare them and pick the best option per item. "
        f"Choose a combination that together fits within the total budget while prioritizing good ratings and value. "
        f"For each recommended item, state: exact product name, exact price, and which site it's from — all taken directly from extracted data. "
        f"Then give the total combined price, and a short 1-2 sentence reason why this combination is the best choice within the budget."
        f"Finally, add a section titled 'FULL COMPARISON:' that lists ALL the options you found "
        f"for each item from both sites (not just the winners), each with name, price, rating, and site."
    )
    llm = get_llm()
    fallback_llm = get_fallback_llm()
    agent = Agent(task=task, llm=llm, fallback_llm=fallback_llm)
    result = await agent.run()
    return result