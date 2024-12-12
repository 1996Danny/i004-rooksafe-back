import requests
from requests.exceptions import RequestException
from .models import Cryptocurrency

class CoinGeckoService:
    BASE_URL = "https://api.coingecko.com/api/v3"

    def get_coin_data(self, coin_id: str) -> dict:
        """
        Fetch live data for a specific cryptocurrency.
        """
        url = f"{self.BASE_URL}/coins/{coin_id}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            raise ValueError(f"Failed to fetch data for coin {coin_id}: {e}")

    def get_historical_data(self, coin_id: str, days: int) -> dict:
        """
        Fetch historical data for a cryptocurrency.
        """
        if days <= 0:
            raise ValueError("Days must be a positive integer.")
        
        url = f"{self.BASE_URL}/coins/{coin_id}/market_chart"
        params = {"vs_currency": "usd", "days": days}
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            raise ValueError(f"Failed to fetch historical data for {coin_id}: {e}")

    def get_coins_list(self) -> list:
        """
        Fetch a list of available coins from CoinGecko.
        """
        url = f"{self.BASE_URL}/coins/list"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            raise ValueError(f"Failed to fetch coins list: {e}")

    def get_top_cryptos(self, vs_currency: str = "usd", per_page: int = 10, page: int = 1) -> list:
        """
        Fetch top cryptocurrencies by market cap.
        """
        url = f"{self.BASE_URL}/coins/markets"
        params = {
            "vs_currency": vs_currency,
            "order": "market_cap_desc",
            "per_page": per_page,
            "page": page,
            "sparkline": False,
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            raise ValueError(f"Failed to fetch top cryptocurrencies: {e}")

def fetch_crypto_data():
    """
    Fetch top cryptocurrencies and update the database.
    """
    service = CoinGeckoService()
    try:
        data = service.get_top_cryptos()

        for coin in data:
            Cryptocurrency.objects.update_or_create(
                symbol=coin['symbol'].upper(),
                defaults={
                    'name': coin['name'],
                    'price': coin['current_price'],
                    'change_1h': coin.get('price_change_percentage_1h_in_currency'),
                    'change_24h': coin.get('price_change_percentage_24h_in_currency'),
                    'change_7d': coin.get('price_change_percentage_7d_in_currency'),
                    'market_cap': coin['market_cap'],
                    'volume_24h': coin['total_volume'],
                    'icon_url': coin['image'],
                }
            )
    except ValueError as e:
        print(f"Error updating cryptocurrency data: {e}")