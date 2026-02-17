# AIML Service - Redis Pub/Sub Integration

This service uses **Redis pub/sub** for communication with the Node.js backend instead of direct WebSocket connections.

## 🏗️ Architecture

```
Node.js Backend → Redis (aiml:requests) → FastAPI AIML Service
FastAPI AIML Service → Redis (aiml:responses:{chatId}) → Node.js Backend
```

## 📋 Prerequisites

1. **Python 3.10+**
2. **Redis Server** (running locally or remotely)
3. **UV package manager** (recommended) or pip

## 🚀 Setup Instructions

### 1. Install Redis

#### Option A: Using Docker (Recommended for Windows)
```bash
docker run -d -p 6379:6379 --name redis-server redis:latest
```

#### Option B: Using WSL (Windows Subsystem for Linux)
```bash
# In WSL terminal
sudo apt update
sudo apt install redis-server
sudo service redis-server start
```

#### Option C: Redis Cloud (Free Tier)
Sign up at https://redis.com/try-free/ and get connection details

### 2. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your Redis configuration:
```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=  # Leave empty if no password

# Add your other API keys
GOOGLE_API_KEY=your_api_key_here
```

### 3. Install Python Dependencies

#### Using UV (Recommended)
```bash
uv sync
```

#### Using pip
```bash
pip install -e .
```

This will install:
- `redis>=5.0.0` - Async Redis client
- `fastapi` - Web framework
- `crewai` - AI orchestration
- All other dependencies

### 4. Run the Service

#### Using Uvicorn
```bash
uvicorn teachers.app:app --host 0.0.0.0 --port 8000 --reload
```

#### Using Python directly
```bash
python -m uvicorn teachers.app:app --host 0.0.0.0 --port 8000
```

## 📡 Redis Channels

### Incoming Requests (Subscribe)
**Channel:** `aiml:requests`

**Message Format:**
```json
{
  "chatId": "507f1f77bcf86cd799439011",
  "question": "What is photosynthesis?",
  "mode": "lite",
  "current_year": 2026,
  "timestamp": "2026-02-17T18:10:00Z"
}
```

### Outgoing Responses (Publish)
**Channel:** `aiml:responses:{chatId}`

**Streaming Token:**
```json
{
  "chatId": "507f1f77bcf86cd799439011",
  "token": "Photosynthesis is...",
  "done": false,
  "timestamp": "2026-02-17T18:10:01Z"
}
```

**Completion Signal:**
```json
{
  "chatId": "507f1f77bcf86cd799439011",
  "token": "",
  "done": true,
  "timestamp": "2026-02-17T18:10:05Z"
}
```

**Error Message:**
```json
{
  "chatId": "507f1f77bcf86cd799439011",
  "token": "",
  "done": true,
  "error": "Error message here"
}
```

## 🧪 Testing

### Test Redis Connection
```bash
redis-cli ping
# Should return: PONG
```

### Test the Service
```bash
# Check health endpoint
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "redis_connected": true
}
```

### Test with Redis CLI
```bash
# Subscribe to responses (in one terminal)
redis-cli
SUBSCRIBE aiml:responses:test123

# Publish a request (in another terminal)
redis-cli
PUBLISH aiml:requests '{"chatId":"test123","question":"Hello","mode":"lite","current_year":2026}'
```

## 📁 New Files Added

1. **`src/teachers/redis_service.py`**
   - Redis connection management
   - Async pub/sub implementation
   - Message serialization/deserialization

2. **`src/teachers/request_handler.py`**
   - Processes incoming requests from Redis
   - Handles lite/pro mode execution
   - Streams responses back via Redis

3. **`src/teachers/app.py`** (Modified)
   - Removed WebSocket endpoint
   - Added Redis startup/shutdown events
   - Background task for listening to requests

## 🔧 Troubleshooting

### Redis Connection Failed
```
❌ Failed to connect to Redis: Error connecting to localhost:6379
```
**Solution:** Make sure Redis is running:
```bash
# Check if Redis is running
redis-cli ping

# Start Redis (Docker)
docker start redis-server

# Start Redis (WSL)
sudo service redis-server start
```

### Import Errors
```
ModuleNotFoundError: No module named 'redis'
```
**Solution:** Reinstall dependencies:
```bash
uv sync
# or
pip install redis>=5.0.0
```

### No Messages Received
**Solution:** Check that both services are using the same Redis instance and channels:
1. Verify REDIS_HOST and REDIS_PORT in both `.env` files
2. Check logs for subscription confirmation: `👂 Subscribed to channel: aiml:requests`

## 🔄 Migration from WebSocket

### What Changed:
- ❌ Removed: `/ws` WebSocket endpoint
- ✅ Added: Redis pub/sub communication
- ✅ Added: Startup/shutdown event handlers
- ✅ Added: Background task for request listening
- ✅ Kept: `/query` HTTP endpoint for backward compatibility

### Benefits:
- ✅ Decoupled services (no direct connection needed)
- ✅ Better reliability and error handling
- ✅ Easier to scale (multiple workers)
- ✅ Message queuing and persistence
- ✅ Simpler debugging and monitoring

## 📊 Monitoring

### View Redis Activity
```bash
# Monitor all Redis commands
redis-cli monitor

# Check active connections
redis-cli client list

# View pub/sub channels
redis-cli pubsub channels
```

## 🤝 Integration with Node.js Backend

The Node.js backend should:
1. Publish to `aiml:requests` when user sends a message
2. Subscribe to `aiml:responses:{chatId}` for that specific chat
3. Stream tokens to frontend as they arrive
4. Unsubscribe when streaming is complete

See the Node.js backend README for setup instructions.

## 📝 License

ISC
