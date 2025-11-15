# Smart Campus Wallet API - cURL Commands

Base URL: `http://localhost:8000`

## Authentication Endpoints

### 1. Register a New User
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "password123",
    "full_name": "John Doe",
    "student_id": "STU12345",
    "major": "Computer Science",
    "class_year": "2025"
  }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=student@example.com&password=password123"
```

**Response:** Save the `access_token` for authenticated requests
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Get Current User Info
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Transaction Endpoints

**Note:** Transactions are automatically created when payments are completed. They are read-only records and cannot be manually created, updated, or deleted.

### 4. Get All Transactions
```bash
curl -X GET "http://localhost:8000/api/v1/transactions/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. Get Transactions with Filters
```bash
# Filter by category
curl -X GET "http://localhost:8000/api/v1/transactions/?category=dining" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Filter by date range
curl -X GET "http://localhost:8000/api/v1/transactions/?start_date=2025-01-01T00:00:00&end_date=2025-12-31T23:59:59" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Combined filters
curl -X GET "http://localhost:8000/api/v1/transactions/?category=dining&skip=0&limit=20" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Available categories:** `dining`, `books`, `transportation`, `entertainment`, `services`, `other`

### 6. Get Transaction by ID
```bash
curl -X GET "http://localhost:8000/api/v1/transactions/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 7. Get Spending Analytics
```bash
# Get analytics for last 30 days (default)
curl -X GET "http://localhost:8000/api/v1/transactions/analytics" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Get analytics for specific date range
curl -X GET "http://localhost:8000/api/v1/transactions/analytics?start_date=2025-11-01T00:00:00&end_date=2025-11-30T23:59:59" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Budget Endpoints

### 11. Get All Budgets
```bash
curl -X GET "http://localhost:8000/api/v1/budgets/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 12. Create Budget
```bash
curl -X POST "http://localhost:8000/api/v1/budgets/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "dining",
    "limit_amount": 500.00,
    "period": "monthly",
    "start_date": "2025-11-01",
    "end_date": "2025-11-30"
  }'
```

**Available periods:** `weekly`, `monthly`

### 13. Get Budget by ID
```bash
curl -X GET "http://localhost:8000/api/v1/budgets/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 14. Get Budget Tracking
```bash
curl -X GET "http://localhost:8000/api/v1/budgets/1/tracking" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 15. Get All Budgets with Tracking
```bash
curl -X GET "http://localhost:8000/api/v1/budgets/tracking" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 16. Update Budget
```bash
curl -X PUT "http://localhost:8000/api/v1/budgets/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "limit_amount": 600.00
  }'
```

### 17. Delete Budget
```bash
curl -X DELETE "http://localhost:8000/api/v1/budgets/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Payment Endpoints

### 18. Get All Payments
```bash
curl -X GET "http://localhost:8000/api/v1/payments/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 19. Get Payments with Filters
```bash
# Filter by status
curl -X GET "http://localhost:8000/api/v1/payments/?status=pending" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Filter by payment type
curl -X GET "http://localhost:8000/api/v1/payments/?payment_type=event" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Combined filters
curl -X GET "http://localhost:8000/api/v1/payments/?status=completed&payment_type=club" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Available statuses:** `pending`, `completed`, `failed`, `cancelled`
**Available payment types:** `event`, `club`, `dining`, `printing`, `service`, `other`

### 20. Create Payment
```bash
curl -X POST "http://localhost:8000/api/v1/payments/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "payment_type": "event",
    "amount": 50.00,
    "description": "HackFest 2025 Registration"
  }'
```

### 21. Get Payment by ID
```bash
curl -X GET "http://localhost:8000/api/v1/payments/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 22. Complete Payment
```bash
curl -X POST "http://localhost:8000/api/v1/payments/1/complete" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Note:** Completing a payment automatically creates a transaction record. The transaction will appear in the transactions list after the payment is completed.

**Important:** Payments cannot be updated or deleted once created. They are immutable records. Only the status can be changed by completing the payment.

---

## Health Check

### 25. Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

---

## Example Workflow

### Complete Example: Register → Login → Create Payment → Complete Payment → Get Transactions → Get Analytics

```bash
# 1. Register
REGISTER_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "full_name": "Test User",
    "student_id": "TEST001"
  }')

echo "Registration: $REGISTER_RESPONSE"

# 2. Login
LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpass123")

TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
echo "Token: $TOKEN"

# 3. Create Payment
PAYMENT_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/payments/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "payment_type": "dining",
    "amount": 15.75,
    "description": "Campus Dining Hall - Dinner"
  }')

PAYMENT_ID=$(echo $PAYMENT_RESPONSE | grep -o '"id":[0-9]*' | cut -d':' -f2)
echo "Payment ID: $PAYMENT_ID"

# 4. Complete Payment (this automatically creates a transaction)
curl -X POST "http://localhost:8000/api/v1/payments/$PAYMENT_ID/complete" \
  -H "Authorization: Bearer $TOKEN"

# 5. Get Transactions (should now include the transaction from completed payment)
curl -X GET "http://localhost:8000/api/v1/transactions/" \
  -H "Authorization: Bearer $TOKEN"

# 6. Get Analytics
curl -X GET "http://localhost:8000/api/v1/transactions/analytics" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Notes

- Replace `YOUR_ACCESS_TOKEN` with the actual token received from the login endpoint
- All authenticated endpoints require the `Authorization: Bearer <token>` header
- Date formats: Use ISO 8601 format (e.g., `2025-11-15T12:30:00` for datetime, `2025-11-15` for date)
- Enum values are case-sensitive and must match exactly (e.g., `dining`, not `Dining`)
- The `skip` and `limit` parameters are used for pagination
- All amounts should be positive numbers
- **Transactions are read-only**: They are automatically created when payments are completed. You cannot manually create, update, or delete transactions.
- **Payments are immutable**: Once created, payments cannot be updated or deleted. Only the status can be changed by completing the payment.
- **Payment Flow**: Create a payment → Complete the payment → Transaction is automatically created

