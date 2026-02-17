import asyncio
from queue import Queue
import threading
from teachers.redis_service import redis_service
from teachers.lite_harness import run_lite_mode
from teachers.crew import Teachers


async def process_aiml_request(request_data: dict):
    """
    Process an AIML request from Redis and stream the response back
    
    Args:
        request_data: Dictionary containing chatId, question, mode, etc.
    """
    try:
        chat_id = request_data.get('chatId')
        question = request_data.get('question')
        mode = request_data.get('mode', 'lite')
        current_year = request_data.get('current_year', 2026)
        
        if not chat_id or not question:
            print("❌ Invalid request: missing chatId or question")
            await redis_service.publish(
                f"aiml:responses:{chat_id}",
                {
                    "chatId": chat_id,
                    "token": "",
                    "done": True,
                    "error": "Missing chatId or question"
                }
            )
            return
        
        print(f"🔄 Processing request for chat {chat_id}: {question[:50]}...")
        
        response_channel = f"aiml:responses:{chat_id}"
        
        inputs = {
            'topic': question,
            'current_year': str(current_year)
        }
        
        if mode.lower() == "lite":
            await process_lite_mode(chat_id, inputs, response_channel)
        else:
            await process_pro_mode(chat_id, inputs, response_channel)
            
    except Exception as e:
        print(f"❌ Error processing request: {e}")
        # Send error to Node.js
        if chat_id:
            await redis_service.publish(
                f"aiml:responses:{chat_id}",
                {
                    "chatId": chat_id,
                    "token": "",
                    "done": True,
                    "error": str(e)
                }
            )


async def process_lite_mode(chat_id: str, inputs: dict, response_channel: str):
    """
    Process request in Lite Mode with streaming
    
    Args:
        chat_id: Chat session ID
        inputs: Input dictionary for the crew
        response_channel: Redis channel to publish responses
    """
    try:
        token_queue = Queue()
        
        def run_loop():
            run_lite_mode(inputs, token_queue)
        
        thread = threading.Thread(target=run_loop, daemon=True)
        thread.start()
        
        while True:
            token = await asyncio.to_thread(token_queue.get)
            
            if token is None:
                print(f"✅ Lite mode streaming complete for chat {chat_id}")
                await redis_service.publish(
                    response_channel,
                    {
                        "chatId": chat_id,
                        "token": "",
                        "done": True
                    }
                )
                break
            
            await redis_service.publish(
                response_channel,
                {
                    "chatId": chat_id,
                    "token": token,
                    "done": False
                }
            )
        
        # Wait for thread to complete
        thread.join(timeout=1)
        
    except Exception as e:
        print(f"❌ Error in Lite mode processing: {e}")
        await redis_service.publish(
            response_channel,
            {
                "chatId": chat_id,
                "token": "",
                "done": True,
                "error": str(e)
            }
        )


async def process_pro_mode(chat_id: str, inputs: dict, response_channel: str):
    """
    Process request in Pro Mode (non-streaming for now)
    
    Args:
        chat_id: Chat session ID
        inputs: Input dictionary for the crew
        response_channel: Redis channel to publish responses
    """
    try:
        def run_crew():
            r = Teachers().crewcall()
            result = r.kickoff(inputs=inputs)
            return result.raw
        
        # Execute in thread pool
        result = await asyncio.to_thread(run_crew)
        
        # Send complete result as one message
        await redis_service.publish(
            response_channel,
            {
                "chatId": chat_id,
                "token": result,
                "done": False
            }
        )
        
        # Send completion signal
        await redis_service.publish(
            response_channel,
            {
                "chatId": chat_id,
                "token": "",
                "done": True
            }
        )
        
        print(f"✅ Pro mode processing complete for chat {chat_id}")
        
    except Exception as e:
        print(f"❌ Error in Pro mode processing: {e}")
        await redis_service.publish(
            response_channel,
            {
                "chatId": chat_id,
                "token": "",
                "done": True,
                "error": str(e)
            }
        )
