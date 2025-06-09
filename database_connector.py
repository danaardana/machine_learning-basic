import mysql.connector
from mysql.connector import Error
import pandas as pd
from typing import List, Dict, Optional, Tuple
import json
from datetime import datetime

class BoysProjectDatabase:
    """
    Database connector for Boys Project MySQL database in XAMPP
    Handles connection and operations for products, product_options, and product_option_values tables
    """
    
    def __init__(self, host='localhost', user='root', password='', database='boysproject'):
        """
        Initialize database connection with XAMPP default configuration
        
        Args:
            host: MySQL host (default: localhost)
            user: MySQL user (default: root)
            password: MySQL password (default: empty)
            database: Database name (default: boysproject)
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print(f"✅ Successfully connected to MySQL database: {self.database}")
                return True
                
        except Error as e:
            print(f"❌ Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("🔌 MySQL connection closed")
    
    def create_database(self):
        """Create database if it doesn't exist"""
        try:
            # Connect without specifying database
            temp_connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            temp_cursor = temp_connection.cursor()
            
            # Create database
            temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✅ Database '{self.database}' created or already exists")
            
            temp_cursor.close()
            temp_connection.close()
            
        except Error as e:
            print(f"❌ Error creating database: {e}")
    
    def import_sql_file(self, sql_file_path: str):
        """
        Import SQL file to create tables and insert data
        
        Args:
            sql_file_path: Path to the SQL file
        """
        try:
            with open(sql_file_path, 'r', encoding='utf-8') as file:
                sql_content = file.read()
            
            # Split SQL commands
            sql_commands = sql_content.split(';')
            
            successful_commands = 0
            for command in sql_commands:
                command = command.strip()
                if command and not command.startswith('--') and command.upper() not in ['START TRANSACTION', 'COMMIT']:
                    try:
                        self.cursor.execute(command)
                        successful_commands += 1
                    except Error as e:
                        if "already exists" not in str(e).lower():
                            print(f"⚠️  Warning executing command: {e}")
            
            self.connection.commit()
            print(f"✅ SQL file imported successfully! Executed {successful_commands} commands")
            
        except FileNotFoundError:
            print(f"❌ SQL file not found: {sql_file_path}")
        except Error as e:
            print(f"❌ Error importing SQL file: {e}")
    
    def get_all_products(self) -> List[Dict]:
        """Get all products with their details"""
        try:
            query = """
            SELECT 
                id, name, category, image, description, 
                stock, sold, ratings, average_rating, 
                is_active, created_at, updated_at
            FROM products 
            WHERE is_active = 1
            ORDER BY name
            """
            self.cursor.execute(query)
            products = self.cursor.fetchall()
            print(f"📦 Retrieved {len(products)} products")
            return products
            
        except Error as e:
            print(f"❌ Error fetching products: {e}")
            return []
    
    def get_product_with_options(self, product_id: int) -> Dict:
        """
        Get product with all its options and option values
        
        Args:
            product_id: Product ID
            
        Returns:
            Dictionary containing product info with options
        """
        try:
            # Get product info
            product_query = """
            SELECT * FROM products WHERE id = %s AND is_active = 1
            """
            self.cursor.execute(product_query, (product_id,))
            product = self.cursor.fetchone()
            
            if not product:
                return {}
            
            # Get product options
            options_query = """
            SELECT * FROM product_options 
            WHERE product_id = %s 
            ORDER BY sort_order, option_name
            """
            self.cursor.execute(options_query, (product_id,))
            options = self.cursor.fetchall()
            
            # Get option values for each option
            for option in options:
                values_query = """
                SELECT * FROM product_option_values 
                WHERE product_option_id = %s AND is_available = 1
                ORDER BY sort_order, display_value
                """
                self.cursor.execute(values_query, (option['id'],))
                option['values'] = self.cursor.fetchall()
            
            product['options'] = options
            return product
            
        except Error as e:
            print(f"❌ Error fetching product with options: {e}")
            return {}
    
    def get_products_by_category(self, category: str) -> List[Dict]:
        """
        Get products by category
        
        Args:
            category: Product category (e.g., 'Lampu', 'Mounting & Body')
            
        Returns:
            List of products in the category
        """
        try:
            query = """
            SELECT * FROM products 
            WHERE category = %s AND is_active = 1
            ORDER BY name
            """
            self.cursor.execute(query, (category,))
            products = self.cursor.fetchall()
            print(f"🏷️  Retrieved {len(products)} products in category: {category}")
            return products
            
        except Error as e:
            print(f"❌ Error fetching products by category: {e}")
            return []
    
    def search_products(self, search_term: str) -> List[Dict]:
        """
        Search products by name or description
        
        Args:
            search_term: Search term
            
        Returns:
            List of matching products
        """
        try:
            query = """
            SELECT * FROM products 
            WHERE (name LIKE %s OR description LIKE %s) 
            AND is_active = 1
            ORDER BY name
            """
            search_pattern = f"%{search_term}%"
            self.cursor.execute(query, (search_pattern, search_pattern))
            products = self.cursor.fetchall()
            print(f"🔍 Found {len(products)} products matching: {search_term}")
            return products
            
        except Error as e:
            print(f"❌ Error searching products: {e}")
            return []
    
    def get_product_categories(self) -> List[str]:
        """Get all unique product categories"""
        try:
            query = """
            SELECT DISTINCT category FROM products 
            WHERE is_active = 1
            ORDER BY category
            """
            self.cursor.execute(query)
            categories = [row['category'] for row in self.cursor.fetchall()]
            print(f"📋 Retrieved {len(categories)} categories")
            return categories
            
        except Error as e:
            print(f"❌ Error fetching categories: {e}")
            return []
    
    def get_stock_info(self, product_id: int) -> Dict:
        """
        Get stock information for a product
        
        Args:
            product_id: Product ID
            
        Returns:
            Dictionary with stock information
        """
        try:
            query = """
            SELECT name, stock, sold, average_rating, ratings
            FROM products 
            WHERE id = %s AND is_active = 1
            """
            self.cursor.execute(query, (product_id,))
            result = self.cursor.fetchone()
            
            if result:
                return {
                    'product_name': result['name'],
                    'stock': result['stock'],
                    'sold': result['sold'],
                    'average_rating': float(result['average_rating']),
                    'total_ratings': result['ratings'],
                    'availability': 'In Stock' if result['stock'] > 0 else 'Out of Stock'
                }
            return {}
            
        except Error as e:
            print(f"❌ Error fetching stock info: {e}")
            return {}
    
    def get_database_stats(self) -> Dict:
        """Get database statistics"""
        try:
            stats = {}
            
            # Product stats
            self.cursor.execute("SELECT COUNT(*) as total FROM products WHERE is_active = 1")
            stats['total_products'] = self.cursor.fetchone()['total']
            
            # Category stats
            self.cursor.execute("SELECT COUNT(DISTINCT category) as total FROM products WHERE is_active = 1")
            stats['total_categories'] = self.cursor.fetchone()['total']
            
            # Stock stats
            self.cursor.execute("SELECT SUM(stock) as total FROM products WHERE is_active = 1")
            stats['total_stock'] = self.cursor.fetchone()['total'] or 0
            
            # Sales stats
            self.cursor.execute("SELECT SUM(sold) as total FROM products WHERE is_active = 1")
            stats['total_sold'] = self.cursor.fetchone()['total'] or 0
            
            # Option stats
            self.cursor.execute("SELECT COUNT(*) as total FROM product_options")
            stats['total_options'] = self.cursor.fetchone()['total']
            
            self.cursor.execute("SELECT COUNT(*) as total FROM product_option_values WHERE is_available = 1")
            stats['total_option_values'] = self.cursor.fetchone()['total']
            
            return stats
            
        except Error as e:
            print(f"❌ Error fetching database stats: {e}")
            return {}
    
    def update_stock(self, product_id: int, new_stock: int) -> bool:
        """
        Update product stock
        
        Args:
            product_id: Product ID
            new_stock: New stock quantity
            
        Returns:
            True if successful, False otherwise
        """
        try:
            query = """
            UPDATE products 
            SET stock = %s, updated_at = %s 
            WHERE id = %s AND is_active = 1
            """
            self.cursor.execute(query, (new_stock, datetime.now(), product_id))
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                print(f"✅ Stock updated for product ID {product_id}: {new_stock}")
                return True
            else:
                print(f"⚠️  No product found with ID {product_id}")
                return False
                
        except Error as e:
            print(f"❌ Error updating stock: {e}")
            return False

def main():
    """Main function to demonstrate database connectivity"""
    # Initialize database connector
    db = BoysProjectDatabase()
    
    # Create database if needed
    db.create_database()
    
    # Connect to database
    if db.connect():
        try:
            # Import SQL file
            print("\n🔄 Importing SQL file...")
            db.import_sql_file('boysproject.sql')
            
            # Get database statistics
            print("\n📊 Database Statistics:")
            stats = db.get_database_stats()
            for key, value in stats.items():
                print(f"   {key.replace('_', ' ').title()}: {value}")
            
            # Show all products
            print("\n📦 All Products:")
            products = db.get_all_products()
            for product in products:
                print(f"   - {product['name']} ({product['category']}) - Stock: {product['stock']}")
            
            # Show product categories
            print("\n📋 Product Categories:")
            categories = db.get_product_categories()
            for category in categories:
                print(f"   - {category}")
            
            # Example: Get product with options
            if products:
                print(f"\n🔍 Product Details with Options (ID: {products[0]['id']}):")
                product_detail = db.get_product_with_options(products[0]['id'])
                print(f"   Product: {product_detail['name']}")
                print(f"   Description: {product_detail['description']}")
                if 'options' in product_detail:
                    for option in product_detail['options']:
                        print(f"   Option: {option['display_name']}")
                        for value in option['values']:
                            print(f"     - {value['display_value']}")
            
        finally:
            # Always disconnect
            db.disconnect()
    
    else:
        print("❌ Failed to connect to database. Make sure XAMPP MySQL is running!")

if __name__ == "__main__":
    main() 