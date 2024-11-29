import requests
from typing import List, Dict
import time

class BundleBearAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.chains = ['all', 'ethereum', 'optimism', 'arbitrum', 'base', 'polygon', 'avalanche', 'bsc']
        self.endpoints = [
            '/overview',
            '/bundler',
            '/paymaster',
            '/account_deployer',
            '/apps',
            '/wallet'
        ]

    def make_request(self, endpoint: str, chain: str, timeframe: str = 'week') -> Dict:
        """Make a request to a specific endpoint for a given chain."""
        url = f"{self.base_url}{endpoint}?chain={chain}&timeframe={timeframe}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return {
                'endpoint': endpoint,
                'chain': chain,
                'status': response.status_code,
                'data': response.json()
            }
        except requests.exceptions.RequestException as e:
            return {
                'endpoint': endpoint,
                'chain': chain,
                'status': getattr(e.response, 'status_code', None),
                'error': str(e)
            }

    def fetch_all_data(self):
        """Fetch data from all endpoints for all chains."""
        for chain in self.chains:
            print(f"\nFetching data for chain: {chain}")
            for endpoint in self.endpoints:
                print(f"  Calling endpoint: {endpoint}")
                result = self.make_request(endpoint, chain)
                
                # Add a small delay to avoid overwhelming the API
                time.sleep(0.5)
                
                # Print status and data
                if result.get('error'):
                    print(f"    Error: {result['error']}")
                else:
                    print(f"    Status: {result['status']}")
                    # print(f"    Data: {result['data']}")

def main():
    # Initialize the API client
    api = BundleBearAPI('https://bundlebear-api.onrender.com')
    
    # Fetch all data
    print("Starting data collection...")
    api.fetch_all_data()

if __name__ == "__main__":
    main()