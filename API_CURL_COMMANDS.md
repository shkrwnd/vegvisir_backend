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

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "student@example.com",
    "full_name": "John Doe",
    "student_id": "STU12345",
    "major": "Computer Science",
    "class_year": "2025",
    "role": "student",
    "created_at": "2025-11-15T14:14:34.235054Z",
    "updated_at": "2025-11-15T14:14:34.235054Z"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
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

**Response:**
```json
{
  "id": 1,
  "email": "student@example.com",
  "full_name": "John Doe",
  "student_id": "STU12345",
  "major": "Computer Science",
  "class_year": "2025",
  "role": "student",
  "created_at": "2025-11-15T14:14:34.235054Z",
  "updated_at": "2025-11-15T14:27:59.053040Z"
}
```

### 4. Forgot Password
```bash
curl -X POST "http://localhost:8000/api/v1/auth/forgot-password" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com"
  }'
```

**Response:**
```json
{
  "message": "If the email exists, a password reset link has been sent.",
  "reset_token": "abc123xyz789..." 
}
```

**Note:** In production, the reset token would be sent via email. In development, it's returned in the response.

### 5. Reset Password
```bash
curl -X POST "http://localhost:8000/api/v1/auth/reset-password" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "RESET_TOKEN_FROM_FORGOT_PASSWORD",
    "new_password": "newpassword123"
  }'
```

**Response:**
```json
{
  "message": "Password has been reset successfully"
}
```

**Note:** The reset token expires after 1 hour. After resetting, the token is invalidated.

---

## Transaction Endpoints

**Note:** Transactions are automatically created when payments are completed. They are read-only records and cannot be manually created, updated, or deleted.

### 6. Get All Transactions
```bash
curl -X GET "http://localhost:8000/api/v1/transactions/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "amount": 50.00,
    "category": "dining",
    "payment_method": "card",
    "description": "Campus Dining Hall - Dinner",
    "transaction_date": "2025-11-15T18:30:00Z",
    "created_at": "2025-11-15T18:30:15.123456Z"
  },
  {
    "id": 2,
    "user_id": 1,
    "amount": 25.50,
    "category": "entertainment",
    "payment_method": "card",
    "description": "Movie Ticket",
    "transaction_date": "2025-11-14T20:00:00Z",
    "created_at": "2025-11-14T20:00:10.654321Z"
  }
]
```

### 7. Get Transactions with Filters
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

### 8. Get Transaction by ID
```bash
curl -X GET "http://localhost:8000/api/v1/transactions/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "amount": 50.00,
  "category": "dining",
  "payment_method": "card",
  "description": "Campus Dining Hall - Dinner",
  "transaction_date": "2025-11-15T18:30:00Z",
  "created_at": "2025-11-15T18:30:15.123456Z"
}
```

### 9. Get Spending Analytics
```bash
# Get analytics for last 30 days (default)
curl -X GET "http://localhost:8000/api/v1/transactions/analytics" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Get analytics for specific date range
curl -X GET "http://localhost:8000/api/v1/transactions/analytics?start_date=2025-11-01T00:00:00&end_date=2025-11-30T23:59:59" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "total_spent": 125.50,
  "transaction_count": 5,
  "average_transaction": 25.10,
  "by_category": {
    "dining": 75.00,
    "entertainment": 25.50,
    "services": 25.00
  },
  "by_payment_method": {
    "card": 100.00,
    "cash": 25.50
  },
  "period": {
    "start_date": "2025-11-01T00:00:00Z",
    "end_date": "2025-11-30T23:59:59Z"
  }
}
```

---

## Budget Endpoints

### 10. Get All Budgets
```bash
curl -X GET "http://localhost:8000/api/v1/budgets/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "category": "dining",
    "limit_amount": 500.00,
    "period": "monthly",
    "start_date": "2025-11-01",
    "end_date": "2025-11-30",
    "created_at": "2025-11-01T00:00:00Z",
    "updated_at": "2025-11-01T00:00:00Z"
  }
]
```

### 11. Create Budget
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

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "category": "dining",
  "limit_amount": 500.00,
  "period": "monthly",
  "start_date": "2025-11-01",
  "end_date": "2025-11-30",
  "created_at": "2025-11-01T00:00:00Z",
  "updated_at": "2025-11-01T00:00:00Z"
}
```

**Available periods:** `weekly`, `monthly`

### 12. Get Budget by ID
```bash
curl -X GET "http://localhost:8000/api/v1/budgets/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "category": "dining",
  "limit_amount": 500.00,
  "period": "monthly",
  "start_date": "2025-11-01",
  "end_date": "2025-11-30",
  "created_at": "2025-11-01T00:00:00Z",
  "updated_at": "2025-11-01T00:00:00Z"
}
```

### 13. Get Budget Tracking
```bash
curl -X GET "http://localhost:8000/api/v1/budgets/1/tracking" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "category": "dining",
  "limit_amount": 500.00,
  "period": "monthly",
  "start_date": "2025-11-01",
  "end_date": "2025-11-30",
  "created_at": "2025-11-01T00:00:00Z",
  "updated_at": "2025-11-01T00:00:00Z",
  "current_spending": 125.50,
  "remaining_amount": 374.50,
  "percentage_used": 25.1,
  "status": "under"
}
```

**Status values:** `under` (spending < limit), `at_limit` (spending = limit), `over` (spending > limit)

### 14. Get All Budgets with Tracking
```bash
curl -X GET "http://localhost:8000/api/v1/budgets/tracking" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "category": "dining",
    "limit_amount": 500.00,
    "period": "monthly",
    "start_date": "2025-11-01",
    "end_date": "2025-11-30",
    "created_at": "2025-11-01T00:00:00Z",
    "updated_at": "2025-11-01T00:00:00Z",
    "current_spending": 125.50,
    "remaining_amount": 374.50,
    "percentage_used": 25.1,
    "status": "under"
  }
]
```

### 15. Update Budget
```bash
curl -X PUT "http://localhost:8000/api/v1/budgets/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "limit_amount": 600.00
  }'
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "category": "dining",
  "limit_amount": 600.00,
  "period": "monthly",
  "start_date": "2025-11-01",
  "end_date": "2025-11-30",
  "created_at": "2025-11-01T00:00:00Z",
  "updated_at": "2025-11-15T14:30:00Z"
}
```

### 16. Delete Budget
```bash
curl -X DELETE "http://localhost:8000/api/v1/budgets/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
- **Status Code:** `204 No Content`
- **Body:** Empty (no response body)

**Note:** The delete endpoint returns a 204 status code with no response body, which is the standard REST API behavior for successful deletions.

---

## Payment Endpoints

### 17. Get All Payments
```bash
curl -X GET "http://localhost:8000/api/v1/payments/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "payment_type": "event",
    "amount": 50.00,
    "status": "pending",
    "description": "HackFest 2025 Registration",
    "created_at": "2025-11-15T10:00:00Z",
    "updated_at": "2025-11-15T10:00:00Z"
  },
  {
    "id": 2,
    "user_id": 1,
    "payment_type": "dining",
    "amount": 15.75,
    "status": "completed",
    "description": "Campus Dining Hall - Dinner",
    "created_at": "2025-11-15T18:00:00Z",
    "updated_at": "2025-11-15T18:30:15Z"
  }
]
```

### 18. Get Payments with Filters
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

### 19. Create Payment
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

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "payment_type": "event",
  "amount": 50.00,
  "status": "pending",
  "description": "HackFest 2025 Registration",
  "created_at": "2025-11-15T10:00:00Z",
  "updated_at": "2025-11-15T10:00:00Z"
}
```

### 20. Get Payment by ID
```bash
curl -X GET "http://localhost:8000/api/v1/payments/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "payment_type": "event",
  "amount": 50.00,
  "status": "pending",
  "description": "HackFest 2025 Registration",
  "created_at": "2025-11-15T10:00:00Z",
  "updated_at": "2025-11-15T10:00:00Z"
}
```

### 21. Complete Payment
```bash
curl -X POST "http://localhost:8000/api/v1/payments/1/complete" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "payment_type": "event",
  "amount": 50.00,
  "status": "completed",
  "description": "HackFest 2025 Registration",
  "created_at": "2025-11-15T10:00:00Z",
  "updated_at": "2025-11-15T18:30:15Z"
}
```

**Note:** Completing a payment automatically creates a transaction record. The transaction will appear in the transactions list after the payment is completed.

**Important:** Payments cannot be updated or deleted once created. They are immutable records. Only the status can be changed by completing the payment.

---

## Card Endpoints

### 22. Get All Cards
```bash
curl -X GET "http://localhost:8000/api/v1/cards/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "card_number": "1234",
    "cardholder_name": "John Doe",
    "expiry_date": "2026-12-31",
    "card_type": "debit",
    "bank_name": "Chase Bank",
    "is_default": true,
    "created_at": "2025-11-15T17:54:54.407242Z",
    "updated_at": "2025-11-15T17:54:54.407242Z"
  },
  {
    "id": 2,
    "user_id": 1,
    "card_number": "5678",
    "cardholder_name": "John Doe",
    "expiry_date": "2027-06-30",
    "card_type": "credit",
    "bank_name": "Bank of America",
    "is_default": false,
    "created_at": "2025-11-15T17:54:56.712962Z",
    "updated_at": "2025-11-15T17:54:56.712962Z"
  }
]
```

### 23. Create Card
```bash
curl -X POST "http://localhost:8000/api/v1/cards/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "card_number": "1234",
    "cardholder_name": "John Doe",
    "expiry_date": "2026-12-31",
    "card_type": "debit",
    "bank_name": "Chase Bank",
    "is_default": true
  }'
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "card_number": "1234",
  "cardholder_name": "John Doe",
  "expiry_date": "2026-12-31",
  "card_type": "debit",
  "bank_name": "Chase Bank",
  "is_default": true,
  "created_at": "2025-11-15T17:54:54.407242Z",
  "updated_at": "2025-11-15T17:54:54.407242Z"
}
```

**Note:** 
- `card_number` must be exactly 4 digits (last 4 digits of the card)
- `card_type` must be either `debit` or `credit`
- `expiry_date` format: `YYYY-MM-DD`
- Setting `is_default` to `true` will automatically unset other default cards for the user
- `bank_name` is optional

### 24. Get Card by ID
```bash
curl -X GET "http://localhost:8000/api/v1/cards/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "card_number": "1234",
  "cardholder_name": "John Doe",
  "expiry_date": "2026-12-31",
  "card_type": "debit",
  "bank_name": "Chase Bank",
  "is_default": true,
  "created_at": "2025-11-15T17:54:54.407242Z",
  "updated_at": "2025-11-15T17:54:54.407242Z"
}
```

### 25. Update Card
```bash
curl -X PUT "http://localhost:8000/api/v1/cards/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cardholder_name": "John D. Doe",
    "bank_name": "Updated Bank Name",
    "is_default": false
  }'
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "card_number": "1234",
  "cardholder_name": "John D. Doe",
  "expiry_date": "2026-12-31",
  "card_type": "debit",
  "bank_name": "Updated Bank Name",
  "is_default": false,
  "created_at": "2025-11-15T17:54:54.407242Z",
  "updated_at": "2025-11-15T18:00:00.123456Z"
}
```

**Note:** Only provided fields will be updated. You cannot update `card_number` or `card_type` after creation. Setting `is_default` to `true` will automatically unset other default cards.

### 26. Delete Card
```bash
curl -X DELETE "http://localhost:8000/api/v1/cards/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
- **Status Code:** `204 No Content`
- **Body:** Empty (no response body)

**Note:** The delete endpoint returns a 204 status code with no response body, which is the standard REST API behavior for successful deletions.

---

## Health Check

### 27. Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected"
}
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
- **Cards**: Users can manage multiple debit/credit cards. Only one card can be set as default at a time. Card number is stored as last 4 digits only for security.

