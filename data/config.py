from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
# IP = env.str("IP")  # Тоже str, но для айпи адреса хоста

AVAILABLE_WAKEUP_TIMESTAMPS = ("5-00", "5-30", "6-00")

