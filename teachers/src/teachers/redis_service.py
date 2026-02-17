import json
import asyncio
import os
from typing import Callable, Optional
import redis.asyncio as redis


class RedisService:
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.pubsub: Optional[redis.client.PubSub] = None
        self.is_connected = False
        
        self.host = os.getenv('REDIS_HOST', 'localhost')
        self.port = int(os.getenv('REDIS_PORT', 6379))
        self.password = os.getenv('REDIS_PASSWORD', None)
        
    async def connect(self):
        """Connect to Redis server"""
        try:
            self.redis_client = await redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password if self.password else None,
                decode_responses=True,
                socket_connect_timeout=5
            )
            
            await self.redis_client.ping()
            self.is_connected = True
            print(f"✅ Redis connected successfully to {self.host}:{self.port}")
            
        except Exception as e:
            print(f"❌ Failed to connect to Redis: {e}")
            self.is_connected = False
            raise
    
    async def disconnect(self):
        """Disconnect from Redis server"""
        try:
            if self.pubsub:
                await self.pubsub.unsubscribe()
                await self.pubsub.close()
            
            if self.redis_client:
                await self.redis_client.close()
            
            self.is_connected = False
            print("Redis disconnected")
            
        except Exception as e:
            print(f"Error disconnecting from Redis: {e}")
    
    async def publish(self, channel: str, message: dict):
        """
        Publish a message to a Redis channel
        
        Args:
            channel: Channel name
            message: Message dictionary (will be JSON serialized)
        """
        if not self.is_connected:
            raise Exception("Redis is not connected")
        
        try:
            message_str = json.dumps(message)
            num_subscribers = await self.redis_client.publish(channel, message_str)
            
            # Only log completion messages
            if message.get('done'):
                print(f"✅ Response completed for chat {message.get('chatId', 'unknown')}")
            
        except Exception as e:
            print(f"❌ Publish error: {e}")
            raise
    
    async def subscribe_and_listen(self, channel: str, callback: Callable, ready_event: Optional[asyncio.Event] = None):
        """
        Subscribe to a Redis channel and listen for messages
        
        Args:
            channel: Channel name
            callback: Async callback function to handle messages
            ready_event: Optional asyncio.Event to signal when subscription is ready
        """
        if not self.is_connected:
            raise Exception("Redis is not connected")
        
        try:
            self.pubsub = self.redis_client.pubsub()
            await self.pubsub.subscribe(channel)
            
            # Listen for messages
            async for message in self.pubsub.listen():
                if message['type'] == 'message':
                    try:
                        data = json.loads(message['data'])
                        chat_id = data.get('chatId', 'unknown')
                        print(f"📥 Processing request for chat {chat_id}")
                        
                        # Call the callback function
                        await callback(data)
                        
                    except json.JSONDecodeError as e:
                        print(f"❌ Invalid message format: {e}")
                    except Exception as e:
                        print(f"❌ Error processing message: {e}")
                elif message['type'] == 'subscribe':
                    # Signal that subscription is ready
                    if ready_event:
                        ready_event.set()
                        
        except Exception as e:
            print(f"❌ Subscription error: {e}")
            raise
    
    def check_connection(self) -> bool:
        """Check if Redis is connected"""
        return self.is_connected


# Singleton instance
redis_service = RedisService()
