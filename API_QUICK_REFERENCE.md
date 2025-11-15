# Vendor API - Quick Reference

## Base URL
```
http://localhost:8000/api/v1
```

## Endpoints

### 1. Get All Vendors
```http
GET /vendors/
```

**Query Parameters:**
- `category` (optional): Filter by category - "dining", "retail", "service", "entertainment"
- `active_only` (optional, default: true): Show only active vendors
- `skip` (optional, default: 0): Pagination offset
- `limit` (optional, default: 100): Max results per page

**Examples:**
```bash
# Get all active vendors
curl http://localhost:8000/api/v1/vendors/

# Get only dining vendors
curl http://localhost:8000/api/v1/vendors/?category=dining

# Get all vendors including inactive
curl http://localhost:8000/api/v1/vendors/?active_only=false

# Pagination
curl http://localhost:8000/api/v1/vendors/?skip=0&limit=10
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Stonsby Commons",
    "category": "dining",
    "description": "Attached to Woodward Hall, Stonsby Commons is the main residential dining hall on campus, and is open to any student with a meal plan. Accepts meal plan flex dollars only.",
    "location": "91 Bleeker Street",
    "logo_url": null,
    "accepts_raider_card": true,
    "is_active": true,
    "created_at": "2025-11-15T21:23:54.242215Z",
    "updated_at": "2025-11-15T21:23:54.242215Z"
  }
]
```

---

### 2. Get Single Vendor
```http
GET /vendors/{vendor_id}
```

**Example:**
```bash
curl http://localhost:8000/api/v1/vendors/1
```

**Response:**
```json
{
  "id": 1,
  "name": "Stonsby Commons",
  "category": "dining",
  "description": "Attached to Woodward Hall...",
  "location": "91 Bleeker Street",
  "logo_url": null,
  "accepts_raider_card": true,
  "is_active": true,
  "created_at": "2025-11-15T21:23:54.242215Z",
  "updated_at": "2025-11-15T21:23:54.242215Z"
}
```

---

### 3. Create Payment with Vendor
```http
POST /payments/
```

**Headers:**
```
Authorization: Bearer {your_jwt_token}
Content-Type: application/json
```

**Body:**
```json
{
  "payment_type": "dining",
  "amount": 12.50,
  "description": "Lunch at Stonsby Commons",
  "vendor_id": 1
}
```

**Example:**
```bash
# Get token first
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=zem14@rutgers.edu&password=ziad1234" | \
  python -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# Create payment
curl -X POST http://localhost:8000/api/v1/payments/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "payment_type": "dining",
    "amount": 12.50,
    "description": "Lunch at Stonsby Commons",
    "vendor_id": 1
  }'
```

**Response:**
```json
{
  "id": 1,
  "user_id": 2,
  "vendor_id": 1,
  "payment_type": "dining",
  "amount": 12.50,
  "description": "Lunch at Stonsby Commons",
  "status": "pending",
  "created_at": "2025-11-15T22:00:00Z",
  "updated_at": "2025-11-15T22:00:00Z"
}
```

---

## Available Vendors

### Dining (5 vendors)
1. **Stonsby Commons** - 91 Bleeker Street
2. **JBJ Soul Kitchen** - 350 Dr MLK Jr Blvd (PRCC)
3. **Robeson Food Court** - 350 Dr MLK Jr Blvd (PRCC)
4. **Starbucks (PRCC)** - 350 Dr MLK Jr Blvd (PRCC)
5. **Starbucks (RBS)** - 1 Washington Place (RBS)

### Retail (1 vendor)
3. **On the RU-N** - 350 Dr MLK Jr Blvd (PRCC) - Convenience store

### Not Accepting Raider Card
7. **Barnes & Noble University Bookstore Newark** - 42 Halsey Street
   - Note: Only accepts real money, not meal plan

---

## Payment Types

Valid values for `payment_type`:
- `"dining"` - Food and beverages
- `"retail"` - Retail purchases
- `"service"` - Campus services
- `"event"` - Campus events
- `"club"` - Student club activities
- `"other"` - Other payments

---

## Categories

Valid vendor categories:
- `"dining"` - Restaurants, cafeterias, food courts
- `"retail"` - Stores, bookstores, convenience
- `"service"` - Printing, laundry, campus services
- `"entertainment"` - Movies, recreation, events

---

## Error Responses

### 404 Not Found
```json
{
  "detail": "Vendor with ID 999 not found"
}
```

### 400 Bad Request
```json
{
  "detail": "Vendor with name 'Stonsby Commons' already exists"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

---

## Testing Tips

### Quick Test Script
```bash
# Test vendors endpoint
curl http://localhost:8000/api/v1/vendors/ | python -m json.tool

# Filter by category
curl "http://localhost:8000/api/v1/vendors/?category=dining" | python -m json.tool

# Get specific vendor
curl http://localhost:8000/api/v1/vendors/1 | python -m json.tool
```

### Login and Create Payment
```bash
# 1. Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=your@email.com&password=yourpassword"

# 2. Copy the access_token from response

# 3. Create payment (replace YOUR_TOKEN)
curl -X POST http://localhost:8000/api/v1/payments/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "payment_type": "dining",
    "amount": 15.00,
    "description": "Lunch",
    "vendor_id": 1
  }'
```

---

## Need Help?

- **Full API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Migration Guide**: See MIGRATION_GUIDE.md
- **Implementation Details**: See VENDOR_IMPLEMENTATION_SUMMARY.md
