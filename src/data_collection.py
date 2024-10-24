import requests
import pandas as pd
from datetime import datetime 

#define subgraph endpoint URL with API key
url = 'https://gateway.thegraph.com/api/3c93f56916d32c29dc6780920c95d19a/subgraphs/id/5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV'

# GraphQL query to fetch daily historical TVL for the ETH/USDC pair over the past 7 days
query = """
{
  poolDayDatas(
    first: 7,
    orderBy: date,
    orderDirection: desc,
    where: { pool: "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8" }
  ) {
    date
    tvlUSD
    volumeToken0
    volumeToken1
    volumeUSD
    token0Price
    token1Price
    feesUSD
  }
}
"""

def fetch_historical_data():
  headers = {'Content-Type': 'application/json'}
  try:
    response = requests.post(url, json={'query': query}, headers=headers)

    #print the response status and text for debugging
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")

    #check if the response is JSON-formatted
    if response.headers.get('Content-Type') == 'application/json':
      data = response.json()
      pool_day_data = data.get('data', {}).get('poolDayDatas', [])
      if pool_day_data:
        print("\nHistorical TVL (Last 7 Days):")
        for entry in pool_day_data:
          date = datetime.utcfromtimestamp(entry['date']).strftime('%Y-%m-%d')
          tvl_usd = float(entry['tvlUSD'])
          volume_token0 = float(entry['volumeToken0'])
          volume_token1 = float(entry['volumeToken1'])
          volume_usd = float(entry['volumeUSD'])
          eth_price_in_usdc = float(entry['token0Price'])
          usdc_price_in_eth = float(entry['token1Price'])
          fees_usd = float(entry['feesUSD'])
          
          
          print(f"Date: {date}, TVL in USD: ${tvl_usd:,.2f}, "
                          f"Volume USDC: {volume_token0:,.2f}, "
                          f"Volume ETH: {volume_token1:,.2f}, "
                          f"Volume in USD: ${volume_usd:,.2f}, "
                          f"ETH Price (in USDC): ${eth_price_in_usdc:.2f}, "
                          f"USDC Price (in ETH): {usdc_price_in_eth:.6f} ETH, "
                          f"Fees in USD: ${fees_usd:,.2f}")
      else:
        print("No historical data found for the ETH/USDC pool.")
    else:
      print("The response not in JSON format. Check for errors.")
  except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
  except Exception as err:
    print(f"Other error occured: {err}")
        
if __name__ == "__main__":
    fetch_historical_data()
