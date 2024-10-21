import requests

#define subgraph endpoint URL with API key
url = 'https://gateway.thegraph.com/api/3c93f56916d32c29dc6780920c95d19a/subgraphs/id/5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV'

# GraphQL query to fetch TVL for the ETH/USDC pair
query = """
{
  pools(where: { id: "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8" }) {
    id
    token0 {
      symbol
    }
    token1 {
      symbol
    }
    totalValueLockedUSD
    totalValueLockedETH
  }
}
"""

def fetch_tvl():
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json={'query': query}, headers=headers)

        #print the response status and text for debugging
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")

        #check if the response is JSON-formatted
        if response.headers.get('Content-Type') == 'application/json':
            data = response.json()
            pools = data.get('data', {}).get('pools', [])
            if pools:
                pool = pools[0]
                print(f"ETH/USDC Pool TVL in USD: ${pool['totalValueLockedUSD']}")
                print(f"ETH/USDC Pool TVL in ETH: {pool['totalValueLockedETH']} ETH")
            else:
                print("No data found for the ETH/USDC pool")
        else:
            print("The response is not in JSON format")
    except request.exceptions.HTTPError as http_error:
        printf("HTTP error occured: {http_error}")
    except Exception as error:
        print(f"Other error occured: {error}")
        
if __name__ == "__main__":
    fetch_tvl()
