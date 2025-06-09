# Boys Project MySQL Database Setup with XAMPP

## Prerequisites

1. **XAMPP Installation**
   - Download and install XAMPP from https://www.apachefriends.org/
   - Make sure MySQL service is included

2. **Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Setup Steps

### 1. Start XAMPP Services
1. Open XAMPP Control Panel
2. Start **Apache** service
3. Start **MySQL** service
4. Verify both services are running (green status)

### 2. Access phpMyAdmin (Optional)
1. Open browser and go to `http://localhost/phpmyadmin`
2. Login with:
   - Username: `root`
   - Password: (leave empty)

### 3. Run Database Setup
```bash
# Install dependencies
pip install mysql-connector-python pandas

# Test database connection and import data
python test_database_connection.py
```

### 4. Verify Database Setup
The script will:
- Create `boysproject` database
- Import all tables from `boysproject.sql`
- Display product statistics
- Show sample data

## Database Schema Overview

### Main Tables
- **products**: Main product information
- **product_options**: Available options for products (motor type, size, etc.)
- **product_option_values**: Specific values for each option
- **customers**: Customer information
- **contact_messages**: Customer support messages
- **chat_conversations**: Live chat conversations

### Product Relationships
```
products (1) → (many) product_options
product_options (1) → (many) product_option_values
```

## Sample Products in Database

1. **Mounting Upsize All** (Mounting & Body)
   - Universal mounting solution
   - Stock: 3,901 units
   - Options: Motor type, Size (3cm-9cm)

2. **Mounting Vario** (Mounting & Body)
   - Specialized for Vario series
   - Stock: 3,006 units
   - High ratings: 4.8/5.0

3. **Turbo SE Experience 60W** (Lampu)
   - High-performance LED lamp
   - Stock: 90 units
   - Options: Quantity (Single/Pair)

## Usage Examples

### Basic Database Connection
```python
from database_connector import BoysProjectDatabase

db = BoysProjectDatabase()
if db.connect():
    products = db.get_all_products()
    print(f"Found {len(products)} products")
    db.disconnect()
```

### Get Products by Category
```python
lampu_products = db.get_products_by_category('Lampu')
mounting_products = db.get_products_by_category('Mounting & Body')
```

### Search Products
```python
results = db.search_products('mounting aerox')
```

### Get Product with Options
```python
product_detail = db.get_product_with_options(1)
print(f"Product: {product_detail['name']}")
for option in product_detail['options']:
    print(f"Option: {option['display_name']}")
```

## ML Model Integration

### Connect with Intent Classification
```python
from ml_database_integration import MLDatabaseIntegration

ml_db = MLDatabaseIntegration()
if ml_db.connect_database():
    response = ml_db.get_intent_response('harga', 'Berapa harga mounting?')
    print(response)
```

### Available Intents
- `harga` - Price inquiries
- `daftar` - Product listings
- `stok_produk` - Stock information
- `kategori_lighting` - Lighting products
- `kategori_mounting_body` - Mounting products
- `jam_operasional` - Operating hours
- `garansi` - Warranty information
- `booking_pemasangan` - Installation booking
- `pengiriman` - Shipping information
- `tipe_motor_matic` - Compatible motorcycles

## Troubleshooting

### Connection Issues
1. **Error: Access denied**
   - Check XAMPP MySQL is running
   - Verify username/password (default: root/empty)

2. **Error: Database doesn't exist**
   - Run `test_database_connection.py` to create database
   - Check SQL file path is correct

3. **Error: Module not found**
   ```bash
   pip install mysql-connector-python
   ```

### Performance Tips
1. Use connection pooling for production
2. Cache frequently accessed data
3. Index important columns for faster queries

## Next Steps

1. **Integrate with Chatbot**
   - Use `MLDatabaseIntegration` class
   - Connect intent classification with database responses

2. **Add Real-time Updates**
   - Implement stock monitoring
   - Set up product change notifications

3. **Extend Functionality**
   - Add order processing
   - Implement customer management
   - Create admin dashboard

## Contact

For questions about the database setup or Boys Project:
- WhatsApp: 08211990442
- Shopee: shopee.co.id/boyprojectsasli 