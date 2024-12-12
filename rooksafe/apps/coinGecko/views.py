from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .services import CoinGeckoService

service = CoinGeckoService()

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def fetch_quotes(request):
    """
    Fetch live data for a cryptocurrency.
    """
    coin_id = request.GET.get("coin_id")
    if not coin_id:
        return JsonResponse({"error": "Coin ID is required."}, status=400)
    try:
        coin_data = service.get_coin_data(coin_id)
        return JsonResponse({"status": "success", "data": coin_data}, status=200)
    except ValueError as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def fetch_historical_data(request):
    """
    Fetch historical data for a cryptocurrency.
    """
    coin_id = request.GET.get("coin_id")
    days = int(request.GET.get("days", 30))  # Default to 30 days

    if not coin_id:
        return JsonResponse({"error": "Coin ID is required."}, status=400)

    try:
        historical_data = service.get_historical_data(coin_id, days)
        return JsonResponse({"status": "success", "data": historical_data}, status=200)
    except ValueError as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_symbols(request):
    """
    Fetch a list of available cryptocurrencies.
    """
    try:
        coins = service.get_coins_list()
        return JsonResponse({"status": "success", "data": coins}, status=200)
    except ValueError as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)