import json
import yfinance as yf
from channels.generic.websocket import AsyncWebsocketConsumer

# class StockPriceConsumer(AsyncWebsocketConsumer):
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
#         data = json.loads(text_data)
#         action = data.get('action', None)

#         if action == "subscribe":
#             # Enviar confirmación al cliente
#             await self.send(json.dumps({"message": f"Subscribed to {self.stock_symbol} updates"}))

#     async def send_stock_update(self, event):
#         # Enviar actualización de precio al cliente
#         price_data = event['data']
#         await self.send(text_data=json.dumps(price_data))
import asyncio
from yahoo_fin import stock_info
class StockPriceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Manejar la conexión WebSocket.
        """
        self.stock_symbol = self.scope['url_route']['kwargs']['stock_symbol']
        self.group_name = f"stock_{self.stock_symbol}"

        # Unir al grupo de comunicación
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

        # Iniciar el envío de precios en tiempo real
        self.running = True
        asyncio.create_task(self.send_stock_prices())

    async def disconnect(self, close_code):
        """
        Manejar la desconexión WebSocket.
        """
        self.running = False  # Detener las actualizaciones
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Recibir mensajes del cliente.
        """
        data = json.loads(text_data)
        action = data.get('action', None)

        if action == "subscribe":
            # Confirmar suscripción al cliente
            await self.send(json.dumps({"message": f"Subscribed to {self.stock_symbol} updates"}))
        elif action == "unsubscribe":
            # Confirmar desuscripción al cliente
            self.running = False
            await self.send(json.dumps({"message": "Unsubscribed from updates"}))

    async def send_stock_prices(self):
        """
        Enviar precios actualizados al cliente cada segundo.
        """
        while self.running:
            try:
                # Obtener el precio del stock
                price = stock_info.get_live_price(self.stock_symbol)
                await self.send(json.dumps({
                    'symbol': self.stock_symbol,
                    'price': round(price, 2),
                }))
                await asyncio.sleep(1)  # Actualizar cada segundo
            except Exception as e:
                # Manejar errores de obtención de datos
                await self.send(json.dumps({'error': f'Error fetching price: {str(e)}'}))
                self.running = False
                break

    async def send_stock_update(self, event):
        """
        Método utilizado para enviar actualizaciones desde el channel layer.
        """
        price_data = event['data']
        await self.send(text_data=json.dumps(price_data))