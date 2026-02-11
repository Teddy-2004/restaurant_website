# 📡 API Documentation

The restaurant website includes a RESTful API for programmatic access to data.

## Base URL

```
http://localhost:5000/api
```

Production: `https://your-domain.com/api`

## Authentication

Most endpoints are public and don't require authentication. Rate limiting is applied.

## Rate Limiting

- **Default**: 200 requests per day, 50 per hour
- **API endpoints**: Specific limits per endpoint
- Rate limit headers included in responses

## Endpoints

### Menu Items

#### Get All Menu Items

```http
GET /api/menu
```

**Query Parameters:**
- `category_id` (integer, optional): Filter by category ID
- `featured` (boolean, optional): Show only featured items

**Example Request:**
```bash
curl http://localhost:5000/api/menu?category_id=1
```

**Example Response:**
```json
{
  "success": true,
  "count": 5,
  "items": [
    {
      "id": 1,
      "name": "Mediterranean Mezze Platter",
      "description": "Hummus, baba ganoush, falafel...",
      "price": 14.99,
      "category": "Appetizers",
      "image_url": "/static/uploads/menu/abc123.jpg",
      "is_available": true,
      "is_featured": true,
      "allergens": ["gluten", "sesame"]
    }
  ]
}
```

#### Get Single Menu Item

```http
GET /api/menu/:id
```

**Example Request:**
```bash
curl http://localhost:5000/api/menu/1
```

**Example Response:**
```json
{
  "success": true,
  "item": {
    "id": 1,
    "name": "Mediterranean Mezze Platter",
    "description": "Hummus, baba ganoush, falafel, olives, and warm pita",
    "price": 14.99,
    "category": "Appetizers",
    "image_url": "/static/uploads/menu/abc123.jpg",
    "is_available": true,
    "is_featured": true,
    "allergens": ["gluten", "sesame"]
  }
}
```

---

### Categories

#### Get All Categories

```http
GET /api/categories
```

**Example Response:**
```json
{
  "success": true,
  "categories": [
    {
      "id": 1,
      "name": "Appetizers",
      "slug": "appetizers",
      "description": "Start your meal with our delicious starters",
      "item_count": 5
    }
  ]
}
```

---

### Reviews

#### Get Reviews

```http
GET /api/reviews
```

**Query Parameters:**
- `limit` (integer, optional): Maximum number of reviews (default: 10, max: 50)

**Example Response:**
```json
{
  "success": true,
  "count": 10,
  "average_rating": 4.7,
  "reviews": [
    {
      "id": 1,
      "customer_name": "Sarah Johnson",
      "rating": 5,
      "comment": "Absolutely amazing!",
      "created_at": "2024-02-10T12:00:00"
    }
  ]
}
```

---

### Events

#### Get Events

```http
GET /api/events
```

**Query Parameters:**
- `upcoming` (boolean, optional): Show only upcoming events (default: true)

**Example Response:**
```json
{
  "success": true,
  "count": 2,
  "events": [
    {
      "id": 1,
      "title": "Wine Tasting Night",
      "description": "Join us for an evening of fine wines...",
      "event_date": "2024-03-15T19:00:00",
      "image_url": "/static/uploads/events/wine.jpg",
      "is_active": true
    }
  ]
}
```

---

### Reservations

#### Check Availability

```http
POST /api/reservations/check
```

**Request Body:**
```json
{
  "date": "2024-03-15",
  "time": "19:00",
  "party_size": 4
}
```

**Example Response:**
```json
{
  "success": true,
  "available": true,
  "message": "Time slot available",
  "reservations_count": 2,
  "max_capacity": 5
}
```

**Rate Limit**: 30 requests per minute

---

### Search

#### Search Menu Items

```http
GET /api/search?q=chicken
```

**Query Parameters:**
- `q` (string, required): Search query (minimum 2 characters)

**Example Response:**
```json
{
  "success": true,
  "query": "chicken",
  "count": 3,
  "results": [
    {
      "id": 6,
      "name": "Chicken Souvlaki",
      "description": "Marinated chicken skewers...",
      "price": 19.99,
      "category": "Main Courses",
      "image_url": "/static/uploads/menu/chicken.jpg",
      "is_available": true,
      "is_featured": false,
      "allergens": []
    }
  ]
}
```

**Rate Limit**: 60 requests per minute

---

### Statistics

#### Get Public Stats

```http
GET /api/stats
```

**Example Response:**
```json
{
  "success": true,
  "stats": {
    "total_reviews": 47,
    "average_rating": 4.7,
    "total_menu_items": 25,
    "upcoming_events": 3
  }
}
```

**Rate Limit**: 30 requests per minute

---

## Error Responses

### 400 Bad Request

```json
{
  "success": false,
  "message": "Missing required fields"
}
```

### 404 Not Found

```json
{
  "success": false,
  "message": "Resource not found"
}
```

### 429 Too Many Requests

```json
{
  "success": false,
  "message": "Rate limit exceeded. Please try again later."
}
```

### 500 Internal Server Error

```json
{
  "success": false,
  "message": "Internal server error"
}
```

---

## Usage Examples

### JavaScript (Fetch API)

```javascript
// Get menu items
fetch('http://localhost:5000/api/menu?category_id=1')
  .then(response => response.json())
  .then(data => {
    console.log('Menu items:', data.items);
  })
  .catch(error => console.error('Error:', error));

// Check reservation availability
fetch('http://localhost:5000/api/reservations/check', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    date: '2024-03-15',
    time: '19:00',
    party_size: 4
  })
})
  .then(response => response.json())
  .then(data => {
    console.log('Availability:', data.available);
  });
```

### Python (Requests)

```python
import requests

# Get menu items
response = requests.get('http://localhost:5000/api/menu')
data = response.json()
print(f"Found {data['count']} items")

# Search menu
response = requests.get('http://localhost:5000/api/search', params={'q': 'chicken'})
results = response.json()
for item in results['results']:
    print(f"{item['name']}: ${item['price']}")

# Check availability
response = requests.post(
    'http://localhost:5000/api/reservations/check',
    json={
        'date': '2024-03-15',
        'time': '19:00',
        'party_size': 4
    }
)
availability = response.json()
print(f"Available: {availability['available']}")
```

### cURL

```bash
# Get all menu items
curl http://localhost:5000/api/menu

# Get featured items only
curl "http://localhost:5000/api/menu?featured=true"

# Search
curl "http://localhost:5000/api/search?q=lamb"

# Check availability
curl -X POST http://localhost:5000/api/reservations/check \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2024-03-15",
    "time": "19:00",
    "party_size": 4
  }'

# Get statistics
curl http://localhost:5000/api/stats
```

---

## Rate Limit Headers

All API responses include rate limit headers:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

---

## Best Practices

1. **Cache responses** when appropriate to reduce API calls
2. **Handle rate limits** gracefully with exponential backoff
3. **Validate data** before sending POST requests
4. **Use query parameters** for filtering instead of fetching all data
5. **Check HTTP status codes** for proper error handling

---

## CORS

CORS is enabled for all origins in development. In production, configure allowed origins in `config.py`:

```python
CORS_ORIGINS = ['https://your-frontend-domain.com']
```

---

## Support

For API issues or feature requests, please open an issue on GitHub.
