# 📖 API Documentation: {project_name}

## Base URL

`http://localhost:8000`

## Core Endpoints

### 🟢 GET `/health`

- **Description:** Basic health check.
- **Response:** `{{"status": "ok"}}`

### 🔵 POST `/api/v1/resource`

- **Description:** Create a new resource.
- **Payload:**

```json
{{
  "name": "example",
  "data": {{}}
}}
```

## Security

- [ ] JWT Authentication
- [ ] OAuth2 Flow
- [ ] API Key enforcement (Sentinel)

## Error Codes

| Code | Meaning |
| :--- | :--- |
| **200** | Success |
| **401** | Unauthorized |
| **404** | Not Found |
| **500** | Fatal Engine Error |
