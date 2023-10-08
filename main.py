import logging
import asyncio
import sqlite3
from pyrogram import Client, filters
from pyrogram.types import Message
import random
from pyrogram import enums

# Initialize the Pyrogram client
api_id = "2208722"
api_hash = "1d6e03d89eab1c53223d40fc154999e0"
bot_token = '6500096001:AAFaq3tmm-eG0K85uNr8lUkmYQfKihaZQ-E'

bot = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Initialize the SQLite database
db = sqlite3.connect("user_scores.db")
cursor = db.cursor()

# Create a table to store user scores if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_scores (
        user_id INTEGER PRIMARY KEY,
        score INTEGER
    )
''')
db.commit()

# Sample riddles with one-word answers
riddles = [
    {"question": "I have banks, but I'm not a financial institution. What am I?", "answer": "River"},
    {"question": "I melt when you light me, but what am I?", "answer": "Candle"},
    {"question": "What can you see, but never touch or catch?", "answer": "Footsteps"},
    {"question": "I have keys but open no locks. What am I?", "answer": "Keyboard"},
    {"question": "I have hands, but I can't clap. What am I?", "answer": "Clock"},
    {"question": "I am something you can hear, but not touch or see. What am I?", "answer": "Silence"},
    {"question": "I whistle, but I'm not a person. What am I?", "answer": "Teapot"},
    {"question": "I'm white, oval, and I break easily. What am I?", "answer": "Egg"},
    {"question": "I have layers and make you cry, but I'm not a person. What am I?", "answer": "Onion"},
    {"question": "I open doors, but I'm not a doorman. What am I?", "answer": "Key"},
    {"question": "I'm something you use to dry yourself, but I'm not a hairdryer. What am I?", "answer": "Towel"},
    {"question": "I go up and down, but I'm not an elevator. What am I?", "answer": "Stairs"},
    {"question": "I'm invisible, and you need me to stay alive. What am I?", "answer": "Breath"},
    {"question": "I'm hot and give off light, but I'm not the sun. What am I?", "answer": "Fire"},
    {"question": "I'm quiet and often secret. What am I?", "answer": "Whisper"},
    {"question": "I'm soft and absorbent, but I'm not a towel. What am I?", "answer": "Sponge"},
    {"question": "I'm a final resting place, but I'm not a bedroom. What am I?", "answer": "Grave"},
    {"question": "I'm round and have value. What am I?", "answer": "Coin"},
    {"question": "I'm cold and melt in the heat. What am I?", "answer": "Ice"},
    {"question": "I mark the end of the day. What am I?", "answer": "Sunset"},
    {"question": "I'm tall, and my light guides ships. What am I?", "answer": "Lighthouse"},
    {"question": "I reflect your image. What am I?", "answer": "Mirror"},
    {"question": "I fall from the sky to water the earth. What am I?", "answer": "Rain"},
    {"question": "I'm always with you but never in front of you. What am I?", "answer": "Shadow"},
    {"question": "I'm a mystery to solve. What am I?", "answer": "Riddle"},
    {"question": "I'm used to write or draw. What am I?", "answer": "Pencil"},
    {"question": "I come in various colors and are used for coloring. What am I?", "answer": "Crayon"},
    {"question": "I'm sharp and used for shaving. What am I?", "answer": "Razor"},
    {"question": "I'm sweet and often made into candy. What am I?", "answer": "Chocolate"},
    {"question": "I'm the sound of happiness. What am I?", "answer": "Laughter"},
    {"question": "I measure temperature. What am I?", "answer": "Thermometer"},
    {"question": "I'm made by bees and sweet to taste. What am I?", "answer": "Honey"},
    {"question": "I'm used for talking to people far away. What am I?", "answer": "Telephone"},
    {"question": "I come in many colors and are often given as a gift. What am I?", "answer": "Flower"},
    {"question": "I'm black and white and have stripes. What am I?", "answer": "Zebra"},
    {"question": "I'm heavy and keep a boat in place. What am I?", "answer": "Anchor"},
    {"question": "I'm a place with many books. What am I?", "answer": "Library"},
    {"question": "I'm used on a chalkboard and come in various colors. What am I?", "answer": "Chalk"},
    {"question": "I'm a smart and playful sea creature. What am I?", "answer": "Dolphin"},
    {"question": "I show locations and directions. What am I?", "answer": "Map"},
    {"question": "I have a pouch to carry my baby. What am I?", "answer": "Kangaroo"},
    {"question": "I'm a precious stone and sparkle in the light. What am I?", "answer": "Diamond"},
    {"question": "I'm a large cat and often called the 'king of the jungle.' What am I?", "answer": "Lion"},
    {"question": "I'm a bird that can't fly and waddle when I walk. What am I?", "answer": "Penguin"},
    {"question": "I have many colors and appear after the rain. What am I?", "answer": "Rainbow"},
    {"question": "I start as a caterpillar and then become beautiful. What am I?", "answer": "Butterfly"},
    {"question": "I'm used for eating and speaking. What am I?", "answer": "Mouth"},
    {"question": "I'm used to buy things. What am I?", "answer": "Money"},
    {"question": "I'm used to enter and exit a room. What am I?", "answer": "Door"},
    {"question": "I'm a tall animal with a long neck. What am I?", "answer": "Giraffe"},
    {"question": "I'm something you can turn, but I'm not a door. What am I?", "answer": "Steering wheel"},
    {"question": "I'm used to play music. What am I?", "answer": "Guitar"},
    {"question": "I'm a green vegetable and make you cry when you cut me. What am I?", "answer": "Green pepper"},
    {"question": "I'm used to clean teeth. What am I?", "answer": "Toothbrush"},
    {"question": "I'm a bird with beautiful colors and can talk. What am I?", "answer": "Parrot"},
    {"question": "I'm a vegetable that's long and orange. What am I?", "answer": "Carrot"},
    {"question": "I'm something you can play and bounce on. What am I?", "answer": "Ball"},
    {"question": "I have a mane and like to run. What am I?", "answer": "Horse"},
    {"question": "I'm used to measure time. What am I?", "answer": "Watch"},
    {"question": "I have a horn on my head and love to charge. What am I?", "answer": "Rhino"},
    {"question": "I'm small and live in a hole. What am I?", "answer": "Mouse"},
    {"question": "I'm used to protect your head. What am I?", "answer": "Helmet"},
    {"question": "I'm a big cat and like to swim. What am I?", "answer": "Tiger"},
    {"question": "I'm a sea creature and have eight legs. What am I?", "answer": "Octopus"},
    {"question": "I'm used to keep books together. What am I?", "answer": "Bookend"},
    {"question": "I'm a red vegetable and often used to make ketchup. What am I?", "answer": "Tomato"},
    {"question": "I'm a bird that's often found near water. What am I?", "answer": "Duck"},
    {"question": "I'm a pink bird with long legs. What am I?", "answer": "Flamingo"},
    {"question": "I'm cold and found in a freezer. What am I?", "answer": "Ice cream"},
    {"question": "I have a horn and like to charge. What am I?", "answer": "Bull"},
    {"question": "I'm a large animal that likes to take baths. What am I?", "answer": "Elephant"},
    {"question": "I'm made of glass and hold drinks. What am I?", "answer": "Cup"},
    {"question": "I'm round and have a hole in the middle. What am I?", "answer": "Doughnut"},
    {"question": "I'm white and cold and can be shaped into sculptures. What am I?", "answer": "Snow"},
    {"question": "I'm a type of vehicle that runs on tracks. What am I?", "answer": "Train"},
    {"question": "I'm a musical instrument and have black and white keys. What am I?", "answer": "Piano"},
    {"question": "I'm a large animal with a hump. What am I?", "answer": "Camel"},
    {"question": "I'm a small insect and work in a colony. What am I?", "answer": "Ant"},
    {"question": "I'm a fruit that comes in many varieties. What am I?", "answer": "Apple"},
    {"question": "I'm a big bird that can't fly. What am I?", "answer": "Ostrich"},
    {"question": "I'm a fruit and often used to make wine. What am I?", "answer": "Grapes"},
    {"question": "I'm a sea creature with eight arms. What am I?", "answer": "Octopus"},
    {"question": "I'm a large fish and known as a predator. What am I?", "answer": "Shark"},
    {"question": "I'm a green vegetable and good for your health. What am I?", "answer": "Broccoli"},
    {"question": "I'm a yellow fruit and very sour. What am I?", "answer": "Lemon"},
    {"question": "I'm flown in the sky and attached to a string. What am I?", "answer": "Kite"},
    {"question": "I'm a small rodent and often found near computers. What am I?", "answer": "Mouse"},
    {"question": "I'm a bird that can't fly but swims well. What am I?", "answer": "Penguin"},
    {"question": "I'm worn on the wrist as jewelry. What am I?", "answer": "Bracelet"},
    {"question": "I'm white and cold and can be sculpted into figures. What am I?", "answer": "Snow"},
    {"question": "I'm a type of bird and known for being wise. What am I?", "answer": "Owl"},
    {"question": "I'm a type of fruit and come in red, green, and yellow varieties. What am I?", "answer": "Apple"},
    {"question": "I'm a small creature that can crawl and have many legs. What am I?", "answer": "Spider"},
    {"question": "I'm an amphibian and can jump very high. What am I?", "answer": "Frog"},
    {"question": "I'm a cold dessert and come in various flavors. What am I?", "answer": "Ice cream"},
    {"question": "I'm a large bird that can't fly. What am I?", "answer": "Ostrich"},
    {"question": "I'm a fruit that's often used to make juice. What am I?", "answer": "Orange"},
    {"question": "I'm black and white and live in the cold. What am I?", "answer": "Penguin"},
    {"question": "I'm a type of fish and my name sounds like a musical instrument. What am I?", "answer": "Bass"},
    {"question": "I'm a fruit that's shaped like a pear and often called 'forbidden.' What am I?", "answer": "Apple"},
    {"question": "I'm used to make calls and fit in your pocket. What am I?", "answer": "Phone"},
    {"question": "I'm a type of clothing and worn on your feet. What am I?", "answer": "Shoe"},
    {"question": "I'm used to travel on the road. What am I?", "answer": "Car"},
    {"question": "I'm used to see things from a distance. What am I?", "answer": "Telescope"},
    {"question": "I'm a type of food and often made with cheese and toppings. What am I?", "answer": "Pizza"},
    {"question": "I'm a type of dog and known for herding sheep. What am I?", "answer": "Collie"},
    {"question": "I'm a type of tree and produce acorns. What am I?", "answer": "Oak"},
    {"question": "I'm a type of bird and known for being a symbol of peace. What am I?", "answer": "Dove"},
    {"question": "I'm a small creature that likes to hop and eat flies. What am I?", "answer": "Frog"},
    {"question": "I'm a type of animal and live in a hive. What am I?", "answer": "Bee"},
    {"question": "I'm a large animal and known for having a horn. What am I?", "answer": "Rhino"},
    {"question": "I'm a type of fruit and often called a 'citrus.' What am I?", "answer": "Orange"},
    {"question": "I'm a type of bird and known for my beautiful feathers. What am I?", "answer": "Peacock"},
    {"question": "I'm a type of vehicle and used to travel on water. What am I?", "answer": "Boat"},
    {"question": "I'm a type of food and used to sweeten coffee or tea. What am I?", "answer": "Sugar"},
    {"question": "I'm a type of animal and often used in stories about big bad wolves. What am I?", "answer": "Wolf"},
    {"question": "I'm a type of food and made from dough and tomato sauce. What am I?", "answer": "Pizza"},
    {"question": "I'm a type of bird and known for my long neck. What am I?", "answer": "Giraffe"},
    {"question": "I'm a type of plant and grow in water. What am I?", "answer": "Lily"},
    {"question": "I'm a type of cat and like to climb trees. What am I?", "answer": "Leopard"},
    {"question": "I'm a type of animal and often have large, curved horns. What am I?", "answer": "Bull"},
    {"question": "I'm a type of vehicle and often used by police. What am I?", "answer": "Car"},
    {"question": "I'm a type of dog and known for my spotted coat. What am I?", "answer": "Dalmatian"},
    {"question": "I'm a type of reptile and known for my colorful scales. What am I?", "answer": "Snake"},
    {"question": "I'm a type of clothing and used to cover your head. What am I?", "answer": "Hat"},
    {"question": "I'm a type of tree and known for my colorful leaves in the fall. What am I?", "answer": "Maple"},
    {"question": "I'm a type of bird and known for my long legs. What am I?", "answer": "Crane"},
    {"question": "I'm a type of vehicle and used for carrying heavy loads. What am I?", "answer": "Truck"},
    {"question": "I'm a type of animal and known for hopping. What am I?", "answer": "Kangaroo"},
    {"question": "I'm a type of food and often served at parties. What am I?", "answer": "Cake"},
    {"question": "I'm a type of fish and often found in a can. What am I?", "answer": "Tuna"},
    {"question": "I'm a type of flower and known for my red color. What am I?", "answer": "Rose"},
    {"question": "I'm a type of bird and known for my beautiful songs. What am I?", "answer": "Nightingale"},
    {"question": "I'm a type of fruit and often used to make pie. What am I?", "answer": "Apple"},
    {"question": "I'm a type of vehicle and used for delivering mail. What am I?", "answer": "Mail truck"},
    {"question": "I'm a type of vegetable and often used in salads. What am I?", "answer": "Lettuce"},
    {"question": "I'm a type of bird and known for my colorful feathers. What am I?", "answer": "Parrot"},
    {"question": "I'm a type of food and often made with cheese and tomato sauce. What am I?", "answer": "Pizza"},
    {"question": "I'm a type of animal and often found in zoos. What am I?", "answer": "Lion"},
    {"question": "I'm a type of clothing and often worn at bedtime. What am I?", "answer": "Pajamas"},
    {"question": "I'm a type of vehicle and used to fly in the sky. What am I?", "answer": "Airplane"},
    {"question": "I'm a type of animal and known for my trunk. What am I?", "answer": "Elephant"},
    {"question": "I'm a type of food and often used to make sandwiches. What am I?", "answer": "Bread"},
    {"question": "I'm a type of vehicle and often found on farms. What am I?", "answer": "Tractor"},
    {"question": "I'm a type of bird and known for my long beak. What am I?", "answer": "Pelican"},
    {"question": "I'm a type of animal and known for my stripes. What am I?", "answer": "Zebra"},
    {"question": "I'm a type of fruit and often used in smoothies. What am I?", "answer": "Banana"},
    {"question": "I'm a type of vehicle and used to ride on two wheels. What am I?", "answer": "Bicycle"},
    {"question": "I'm a type of animal and often used to pull a sled. What am I?", "answer": "Dog"},
    {"question": "I'm a type of clothing and used to keep your feet warm. What am I?", "answer": "Sock"},
    {"question": "I'm a type of tree and often used to make furniture. What am I?", "answer": "Oak"},
    {"question": "I'm a type of food and often used for making pies. What am I?", "answer": "Apple"},
    {"question": "I'm a type of bird and known for my loud call. What am I?", "answer": "Crow"},
    {"question": "I'm a type of animal and known for my long neck. What am I?", "answer": "Giraffe"},
    {"question": "I'm a type of plant and known for my thorns. What am I?", "answer": "Rose"},
    {"question": "I'm a type of vehicle and used to carry people to school. What am I?", "answer": "Bus"},
    {"question": "I'm a type of bird and known for my beautiful tail feathers. What am I?", "answer": "Peacock"},
    {"question": "I'm a type of animal and known for my spots. What am I?", "answer": "Leopard"},
    {"question": "I'm a type of clothing and used to keep you warm in the winter. What am I?", "answer": "Coat"},
    {"question": "I'm a type of fish and often used in sushi. What am I?", "answer": "Tuna"},
    {"question": "I'm a type of tree and often found in the desert. What am I?", "answer": "Cactus"},
    {"question": "I'm a type of vehicle and used to travel on snow. What am I?", "answer": "Sled"},
    {"question": "I'm a type of animal and known for my long ears. What am I?", "answer": "Rabbit"},
    {"question": "I'm a type of clothing and used to protect your eyes from the sun. What am I?", "answer": "Sunglasses"},
    {"question": "I'm a type of bird and known for my beautiful song. What am I?", "answer": "Nightingale"},
    {"question": "I'm a type of animal and known for my long tongue. What am I?", "answer": "Chameleon"},
    {"question": "I'm a type of food and often served with ketchup. What am I?", "answer": "French fries"},
    {"question": "I'm a type of animal and often used to guard a house. What am I?", "answer": "Dog"},
    {"question": "I'm a type of tree and known for my colorful leaves in the fall. What am I?", "answer": "Maple"},
    {"question": "I'm a type of vehicle and used to carry heavy loads. What am I?", "answer": "Truck"},
    {"question": "I'm a type of bird and known for my beautiful feathers. What am I?", "answer": "Parrot"},
    {"question": "I'm a type of food and often made with cheese and tomato sauce. What am I?", "answer": "Pizza"},
    {"question": "I'm a type of animal and often found in zoos. What am I?", "answer": "Lion"},
    {"question": "I'm a type of clothing and often worn at bedtime. What am I?", "answer": "Pajamas"},
    {"question": "I'm a type of vehicle and used to fly in the sky. What am I?", "answer": "Airplane"},
    {"question": "I'm a type of animal and known for my trunk. What am I?", "answer": "Elephant"},
    {"question": "I'm a type of food and often used to make sandwiches. What am I?", "answer": "Bread"},
    {"question": "I'm a type of vehicle and often found on farms. What am I?", "answer": "Tractor"},
    {"question": "I'm a type of bird and known for my long beak. What am I?", "answer": "Pelican"},
    {"question": "I'm a type of animal and known for my stripes. What am I?", "answer": "Zebra"},
    {"question": "I'm a type of fruit and often used in smoothies. What am I?", "answer": "Banana"},
    {"question": "I'm a type of vehicle and used to ride on two wheels. What am I?", "answer": "Bicycle"},
    {"question": "I'm a type of animal and often used to pull a sled. What am I?", "answer": "Dog"},
    {"question": "I'm a type of clothing and used to keep your feet warm. What am I?", "answer": "Sock"},
    {"question": "I'm a type of tree and often used to make furniture. What am I?", "answer": "Oak"},
    {"question": "I'm a type of food and often used for making pies. What am I?", "answer": "Apple"},
    {"question": "I'm a type of bird and known for my loud call. What am I?", "answer": "Crow"},
    {"question": "I'm a type of animal and known for my long neck. What am I?", "answer": "Giraffe"},
    {"question": "I'm a type of plant and known for my thorns. What am I?", "answer": "Rose"},
    {"question": "I'm a type of vehicle and used to carry people to school. What am I?", "answer": "Bus"},
    {"question": "I'm a type of bird and known for my beautiful tail feathers. What am I?", "answer": "Peacock"},
    {"question": "I'm a type of animal and known for my spots. What am I?", "answer": "Leopard"},
    {"question": "I'm a type of clothing and used to keep you warm in the winter. What am I?", "answer": "Coat"},
    {"question": "I'm a type of fish and often used in sushi. What am I?", "answer": "Tuna"},
    {"question": "I'm a type of tree and often found in the desert. What am I?", "answer": "Cactus"},
    {"question": "I'm a type of vehicle and used to travel on snow. What am I?", "answer": "Sled"},
    {"question": "I'm a type of animal and known for my long ears. What am I?", "answer": "Rabbit"},
    {"question": "I'm a type of clothing and used to protect your eyes from the sun. What am I?", "answer": "Sunglasses"},
    {"question": "I'm a type of bird and known for my beautiful song. What am I?", "answer": "Nightingale"},
    {"question": "I'm a type of animal and known for my long tongue. What am I?", "answer": "Chameleon"},
    {"question": "I'm a type of food and often served with ketchup. What am I?", "answer": "French fries"},
    {"question": "I'm a type of animal and often used to guard a house. What am I?", "answer": "Dog"},
    {"question": "I'm a type of tree and known for my colorful leaves in the fall. What am I?", "answer": "Maple"},
    {"question": "I'm a type of vehicle and used to carry heavy loads. What am I?", "answer": "Truck"},
    {"question": "I'm a type of bird and known for my beautiful feathers. What am I?", "answer": "Parrot"},
    {"question": "I'm a type of food and often made with cheese and tomato sauce. What am I?", "answer": "Pizza"},
    {"question": "I'm a type of animal and often found in zoos. What am I?", "answer": "Lion"},
    {"question": "I'm a type of clothing and often worn at bedtime. What am I?", "answer": "Pajamas"},
    {"question": "I'm a type of vehicle and used to fly in the sky. What am I?", "answer": "Airplane"},
    {"question": "I'm a type of animal and known for my trunk. What am I?", "answer": "Elephant"},
    {"question": "I'm a type of food and often used to make sandwiches. What am I?", "answer": "Bread"},
    {"question": "I'm a type of vehicle and often found on farms. What am I?", "answer": "Tractor"},
    {"question": "I'm a type of bird and known for my long beak. What am I?", "answer": "Pelican"},
    {"question": "I'm a type of animal and known for my stripes. What am I?", "answer": "Zebra"},
    {"question": "I'm a type of fruit and often used in smoothies. What am I?", "answer": "Banana"},
    {"question": "I'm a type of vehicle and used to ride on two wheels. What am I?", "answer": "Bicycle"},
    {"question": "I'm a type of animal and often used to pull a sled. What am I?", "answer": "Dog"},
    {"question": "I'm a type of clothing and used to keep your feet warm. What am I?", "answer": "Sock"},
    {"question": "I'm a type of tree and often used to make furniture. What am I?", "answer": "Oak"},
    {"question": "I'm a type of food and often used for making pies. What am I?", "answer": "Apple"},
    {"question": "I'm a type of bird and known for my loud call. What am I?", "answer": "Crow"},
    {"question": "I'm a type of animal and known for my long neck. What am I?", "answer": "Giraffe"},
    {"question": "I'm a type of plant and known for my thorns. What am I?", "answer": "Rose"},
    {"question": "I'm a type of vehicle and used to carry people to school. What am I?", "answer": "Bus"},
    {"question": "I'm a type of bird and known for my beautiful tail feathers. What am I?", "answer": "Peacock"},
    {"question": "I'm a type of animal and known for my spots. What am I?", "answer": "Leopard"},
    {"question": "I'm a type of clothing and used to keep you warm in the winter. What am I?", "answer": "Coat"},
    {"question": "I'm a type of fish and often used in sushi. What am I?", "answer": "Tuna"},
    {"question": "I'm a type of tree and often found in the desert. What am I?", "answer": "Cactus"},
    {"question": "I'm a type of vehicle and used to travel on snow. What am I?", "answer": "Sled"},
    {"question": "I'm a type of animal and known for my long ears. What am I?", "answer": "Rabbit"},
    {"question": "I'm a type of clothing and used to protect your eyes from the sun. What am I?", "answer": "Sunglasses"},
    {"question": "I'm a type of bird and known for my beautiful song. What am I?", "answer": "Nightingale"},
    {"question": "I'm a type of animal and known for my long tongue. What am I?", "answer": "Chameleon"},
    {"question": "I'm a type of food and often served with ketchup. What am I?", "answer": "French fries"},
    {"question": "I'm a type of animal and often used to guard a house. What am I?", "answer": "Dog"}
]

# Access the riddles like this:
# riddle = riddles[0]
# print("Question:", riddle["question"])
# print("Answer:", riddle["answer"])


# Store the current riddle and user state
current_riddle = None
user_states = {}

# User states
STATE_IDLE = 0
STATE_WAITING_FOR_RIDDLE = 1

# Function to send a new riddle
async def send_riddle(chat_id, user_id):
    global current_riddle
    riddle = random.choice(riddles)
    current_riddle = riddle

    try:
        await bot.send_message(chat_id, f"Your total score: {get_user_score(user_id)}")
        await bot.send_message(chat_id, f" Riddle: **{riddle['question']}**\n\nYou have 2 minutes to answer.")
        user_states[chat_id] = {"riddle": riddle, "user_id": user_id}  # Set riddle state

        # Schedule sending the correct answer after 2 minutes
        await asyncio.sleep(120)
        if user_states.get(chat_id):
            riddle_data = user_states[chat_id]
            await bot.send_message(chat_id, f"The correct answer was: **{riddle_data['riddle']['answer']}**")
            del user_states[chat_id]  # Clear the riddle state
    except Exception as e:
        logging.error(f"Error sending riddle: {e}")

# Handle /start command to welcome the user
@bot.on_message(filters.command("start"))
async def start_command(_, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_name = message.from_user.first_name  # Get user's first name
    welcome_message = f"Welcome, {user_name}!\nTo get a riddle, use the /riddle command."
    await bot.send_message(chat_id, welcome_message)

# Handle /score command
@bot.on_message(filters.command("score"))
async def score_command(_, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_name = message.from_user.first_name  # Get user's first name
    total_score = get_user_score(user_id)
    score_message = f"{user_name},\nYour total score: {total_score}"
    await bot.send_message(chat_id, score_message)

# Handle /new command
@bot.on_message(filters.command("riddle"))
async def new_riddle(_, message: Message):
    chat_id = message.chat.id

    if user_states.get(chat_id):
        # If there's an ongoing riddle, respond with a message
        await bot.send_message(chat_id, "There is already an ongoing riddle!")
    else:
        user_id = message.from_user.id
        await send_riddle(chat_id, user_id)

# Handle /about command
@bot.on_message(filters.command("about"))
async def about_command(_, message: Message):
    chat_id = message.chat.id

    about_message = (
        "🤖 **About This Bot** 🤖\n\n"
        "This is the Riddle Bot, designed to entertain you with challenging riddles!\n\n"
        "🔍 **Features**:\n"
        "- Get a new riddle using /riddle command.\n"
        "- Check your score using /score command.\n\n"
        "💡 **How to Play**:\n"
        "1. Use /new to get a riddle.\n"
        "2. Send your answer to the riddle as a text message.\n"
        "3. If you answer correctly, you'll earn a point!\n\n"
        "📝 **Note**:\n"
        "- Riddles are updated regularly, so keep playing to test your wit.\n\n"
        "Enjoy the riddles and challenge your friends! 🎉\n\n"
        "Dev : @mustBePro\n"
        "Use /about for help !"
    )

    await bot.send_message(chat_id, about_message, parse_mode=enums.ParseMode.MARKDOWN)

# Handle user answers
@bot.on_message(filters.text)
async def check_answer(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name  # Get user's first name
    user_answer = message.text.lower()

    if user_states.get(chat_id) and user_states[chat_id]["riddle"]:
        riddle = user_states[chat_id]["riddle"]
        if user_answer == riddle["answer"].lower():
            # Update user score
            increment_user_score(user_id)
            del user_states[chat_id]  # Clear the riddle state
            score_message = f"Correct answer by {user_name}!\nYour total score: {get_user_score(user_id)}"
            await bot.send_message(chat_id, score_message)

# Function to get the user's score from the database
def get_user_score(user_id):
    cursor.execute("SELECT score FROM user_scores WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        return 0

# Function to increment the user's score
def increment_user_score(user_id):
    current_score = get_user_score(user_id)
    cursor.execute("REPLACE INTO user_scores (user_id, score) VALUES (?, ?)", (user_id, current_score + 1))
    db.commit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    bot.run()
