import json
from channels.generic.websocket import AsyncWebsocketConsumer
from yfinance import stock_info  # Use yfinance or yahoo_fin for live data
import asyncio

import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from yahoo_fin import stock_info  # O la librería que prefieras para obtener datos en vivo

class StockDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Manejar la conexión WebSocket.
        """
        await self.accept()
        self.running = False  # Control para detener el bucle de actualizaciones
        self.stock_symbol = None  # Almacenar el símbolo del stock

    async def disconnect(self, close_code):
        """
        Manejar la desconexión del WebSocket.
        """
        self.running = False  # Detener el bucle si el cliente se desconecta
        print(f"Disconnected: {close_code}")

    async def receive(self, text_data):
        """
        Recibir mensajes desde el frontend.
        """
        try:
            data = json.loads(text_data)  # Parsear el mensaje JSON
            action = data.get('action')
            stock_symbol = data.get('stock_symbol')

            if action == "subscribe" and stock_symbol:
                self.running = True
                self.stock_symbol = stock_symbol
                await self.send(json.dumps({"message": f"Subscribed to {stock_symbol} updates"}))
                asyncio.create_task(self.send_stock_prices())
            elif action == "unsubscribe":
                self.running = False
                await self.send(json.dumps({"message": "Unsubscribed from updates"}))
        except json.JSONDecodeError as e:
            await self.send(json.dumps({'error': f'Invalid JSON data: {str(e)}'}))

    async def send_stock_prices(self):
        """
        Enviar precios actualizados del stock al frontend.
        """
        while self.running:
            try:
                # Obtener precio en vivo del stock
                price = stock_info.get_live_price(self.stock_symbol)
                await self.send(json.dumps({
                    'symbol': self.stock_symbol,
                    'price': round(price, 2),
                }))
                await asyncio.sleep(1)  # Esperar un segundo antes de la próxima actualización
            except Exception as e:
                await self.send(json.dumps({'error': f'Error fetching price: {str(e)}'}))
                self.running = False  # Detener el bucle en caso de error
                break

# class StockDataConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Obtener símbolo de la URL
#         self.stock_symbol = self.scope['url_route']['kwargs']['stock_symbol']
#         self.group_name = f"stock_{self.stock_symbol}"

#         # Unir al grupo
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Salir del grupo
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         # This method sends live stock updates
#         while text_data == True:
#             try:
#                 data = stock_info.get_live_price(self.symbol)  # Replace with yfinance live fetch if needed
#                 await self.send(text_data=json.dumps({
#                     'symbol': self.symbol,
#                     'price': round(data, 2),
#                 }))
#                 await asyncio.sleep(1)  # Fetch updates every second
#             except Exception as e:
#                 await self.send(text_data=json.dumps({'error': str(e)}))
#                 break

    # async def receive(self, text_data):
    #         """
    #         Recibe datos del frontend para suscribirse a actualizaciones de un stock.
    #         """
    #         try:
    #             # Parsear datos del frontend
    #             data = json.loads(text_data)
    #             action = data.get('action')
    #             stock_symbol = data.get('stock_symbol')

    #             if action == "subscribe" and stock_symbol:
    #                 self.running = True
    #                 await self.send(json.dumps({"message": f"Subscribed to {stock_symbol} updates"}))
    #                 await self.send_stock_prices(stock_symbol)
    #             elif action == "unsubscribe":
    #                 self.running = False
    #                 await self.send(json.dumps({"message": "Unsubscribed from updates"}))
    #         except json.JSONDecodeError as e:
    #             await self.send(json.dumps({'error': f'Invalid JSON data: {str(e)}'}))

    # async def send_stock_prices(self, stock_symbol):
    #         """
    #         Envía actualizaciones de precios del stock cada segundo mientras la conexión esté activa.
    #         """
    #         while self.running:
    #             try:
    #                 # Obtener precio en vivo del stock
    #                 price = stock_info.get_live_price(stock_symbol)
    #                 await self.send(json.dumps({
    #                     'symbol': stock_symbol,
    #                     'price': round(price, 2),
    #                 }))
    #                 await asyncio.sleep(1)  # Esperar un segundo antes de la próxima actualización
    #             except Exception as e:
    #                 await self.send(json.dumps({'error': f'Error fetching price: {str(e)}'}))
    #                 break

    # async def send(self, text_data):
    #     """
    #     Simula el envío de datos al cliente.
    #     En producción, sería parte de WebSocket (como `self.send` en Django Channels).
    #     """
    #     print(f"Sending to client: {text_data}")

    # async def receive(self, text_data):
    #     data = json.loads(text_data)
    #     action = data.get('action', None)

    #     if action == "subscribe":
    #         # Enviar confirmación al cliente
    #         await self.send(json.dumps({"message": f"Subscribed to {self.stock_symbol} updates"}))

    # async def send_stock_update(self, event):
    #     # Enviar actualización de precio al cliente
    #     price_data = event['data']
    #     await self.send(text_data=json.dumps(price_data))