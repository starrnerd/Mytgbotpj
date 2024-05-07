import telebot
from telebot import types

# Replace 'YOUR_TOKEN' with your actual Telegram Bot API token
bot = telebot.TeleBot('6532690795:AAE-X6aaEjrfBtShhxtd8TC-RZFW0Ae8HaI')

# Dictionary to store products (product_id: product_name)
products = {
    1: "Product 1",
    2: "Product 2",
    3: "Product 3",
}

# Dictionary to store user shopping carts (user_id: [product_ids])
user_carts = {}

# Command handler for the start command
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_carts[user_id] = []  # Initialize an empty cart for the user
    welcome_message = "Welcome to the Shopping Bot! Here are the available commands:\n\n"
    welcome_message += "/products - View available products\n"
    welcome_message += "/cart - View your shopping cart\n"
    bot.send_message(user_id, welcome_message)

# Command handler for listing products
@bot.message_handler(commands=['products'])
def list_products(message):
    user_id = message.chat.id
    product_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for product_id, product_name in products.items():
        product_button = types.KeyboardButton(product_name)
        product_markup.add(product_button)
    bot.send_message(user_id, "Here are the available products:", reply_markup=product_markup)

# Message handler for viewing product details
@bot.message_handler(func=lambda message: message.text in products.values())
def view_product_details(message):
    user_id = message.chat.id
    product_name = message.text
    # Replace this with code to retrieve product details from a database
    product_details = f"Details for {product_name}:\nPrice: $10\nDescription: Lorem ipsum dolor sit amet."
    bot.send_message(user_id, product_details)

# Message handler for adding a product to the cart
@bot.message_handler(func=lambda message: message.text in products.values())
def add_to_cart(message):
    user_id = message.chat.id
    product_name = message.text
    product_id = [key for key, value in products.items() if value == product_name][0]
    user_carts[user_id].append(product_id)
    bot.send_message(user_id, f"{product_name} added to your cart.")

# Command handler for viewing the shopping cart
@bot.message_handler(commands=['cart'])
def view_cart(message):
    user_id = message.chat.id
    if user_carts[user_id]:
        cart_contents = "Your shopping cart:\n"
        for product_id in user_carts[user_id]:
            cart_contents += f"- {products[product_id]}\n"
    else:
        cart_contents = "Your shopping cart is empty."
    bot.send_message(user_id, cart_contents)

# Start the bot
bot.polling()
