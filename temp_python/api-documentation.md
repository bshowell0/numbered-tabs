# API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently using basic authentication. Include API key in headers:
```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### Health Check
```http
GET /health
```
Returns server status and version information.

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Tab Management
```http
GET /tabs
POST /tabs
PUT /tabs/{id}
DELETE /tabs/{id}
```

**Example POST Request**:
```json
{
  "title": "New Tab",
  "url": "https://example.com",
  "position": 1
}
```

### Analytics
```http
GET /analytics/usage
GET /analytics/performance
```

Returns usage statistics and performance metrics.

### Configuration
```http
GET /config
PUT /config
```

Manage application configuration settings.

## Rate Limiting
- 100 requests per minute per API key
- 1000 requests per hour per IP address

## Error Responses
Standard HTTP status codes with JSON error messages:
```json
{
  "error": "Invalid request",
  "code": "INVALID_INPUT",
  "details": "Missing required field: title"
}
```
