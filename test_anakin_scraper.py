from agent.anakin_client import scrape_url_with_anakin

result = scrape_url_with_anakin("https://www.amazon.in/s?k=phone+charger")
print(result[:1000])