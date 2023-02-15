from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
import time
import asyncio
from asgiref.sync import sync_to_async
from .models import Quiz
from channels.db import database_sync_to_async



class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send_notification()
    
  
    
    async def send_notification(self):
        while True:
            await asyncio.sleep(30)  # sleep for 30 seconds
            async for quiz in Quiz.objects.filter(is_available=True):
                await self.send(text_data=json.dumps({
                    'type': 'notification',
                    'message': f"{quiz.title} is available now",
                    'quiz_id': quiz.id,
                    'time limit': quiz.time_limit
                }))


    async def disconnect(self, close_code):
        await self.send(text_data=json.dumps({
            "type": "disconnected",
            "message": f"Disconnected from the server with code {close_code}"
        }))
        await self.close()