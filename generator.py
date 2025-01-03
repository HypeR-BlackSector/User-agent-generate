import requests
from bs4 import BeautifulSoup
import random
import uuid

# Список версий Android
android_versions = ["8.0", "9.0", "10", "11", "12", "13", "14"]

# Минимальная версия Android для установки Telegram
min_android_version = 4.1

# Список браузеров с возможными версиями
browsers = {
    "Chrome": ["91.0.4472.124", "92.0.4515.131", "93.0.4577.82", "94.0.4606.81", "95.0.4638.50"],
    "Firefox": ["89.0", "90.0", "91.0", "92.0", "93.0"],
    "Opera": ["75.0.3969.143", "76.0.4017.177", "77.0.4053.118", "78.0.4093.192"],
    "Samsung Browser": ["14.0", "15.0", "16.0"],
    "Safari": ["14.0", "15.0", "16.0"],
    "UC Browser": ["12.0", "13.0", "14.0"],
    "Microsoft Edge": ["91.0", "92.0", "93.0"],
    "Brave": ["1.32.113", "1.33.74"],
    "Vivaldi": ["4.1.2369", "4.2.2702"]
}

# Список рендеринг движков
render_engines = ["AppleWebKit", "Blink", "Gecko", "Presto"]

# Дополнительные заголовки для уникальности
accept_languages = ["en-US", "ru-RU", "de-DE", "fr-FR", "es-ES"]
accept_encodings = ["gzip", "deflate", "br", "identity"]
connections = ["keep-alive", "close"]

# Список архитектур
architectures = ["arm64", "armeabi-v7a", "x86_64"]

# Функция для получения списка моделей Android с сайта
def get_android_models():
    url = 'https://www.gsmarena.com/makers.php3'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    models = []
    for maker in soup.find_all('div', {'class': 'makers'}):
        for link in maker.find_all('a'):
            if 'android' in link.get('href', '').lower():
                models.append(link.text.strip())
    return models

# Функция для проверки, поддерживает ли модель Telegram
def supports_telegram(version):
    version_numbers = [int(x) for x in version.split('.')]
    min_version_numbers = [int(x) for x in str(min_android_version).split('.')]
    
    if version_numbers[0] > min_version_numbers[0]:
        return True
    elif version_numbers[0] == min_version_numbers[0] and version_numbers[1] >= min_version_numbers[1]:
        return True
    return False

# Получаем список моделей Android
android_models = get_android_models()

# Функция для генерации уникальных User-Agent строк
def generate_user_agents(android_versions, android_models, browsers, render_engines, count):
    user_agents = set()  # Используем множество для хранения уникальных строк

    # Генерация Android User-Agents
    while len(user_agents) < count:
        model = random.choice(android_models)
        version = random.choice(android_versions)

        # Проверка на поддержку Telegram
        if not supports_telegram(float(version)):
            continue  # Пропускаем модели, которые не поддерживают Telegram

        # Выбираем случайный браузер и его версию
        browser_name = random.choice(list(browsers.keys()))
        browser_version = random.choice(browsers[browser_name])

        # Выбираем случайный рендеринг движок
        render_engine = random.choice(render_engines)

        # Дополнительные случайные параметры
        language = random.choice(accept_languages)
        encoding = random.choice(accept_encodings)
        connection = random.choice(connections)
        architecture = random.choice(architectures)
        device_id = uuid.uuid4()

        # Формируем User-Agent
        user_agent = (f"Mozilla/5.0 (Linux; Android {version}; {model} Build/XYZ; {architecture}) "
                      f"{render_engine}/537.36 (KHTML, like Gecko) {browser_name}/{browser_version} "
                      f"Mobile Safari/537.36 Accept-Language: {language} Accept-Encoding: {encoding} "
                      f"Connection: {connection} Device-ID: {device_id}")

        # Проверяем уникальность и добавляем в множество
        if user_agent not in user_agents:
            user_agents.add(user_agent)

    # Возвращаем все уникальные User-Agent'ы
    return list(user_agents)

# Запрос количества User-Agent'ов
count = int(input("Введите количество User-Agent'ов для генерации: "))

# Генерация указанного количества уникальных User-Agent'ов для Android, поддерживающих Telegram
generated_user_agents = generate_user_agents(
    android_versions=["8.0", "9.0", "10", "11", "12", "13", "14"],
    android_models=android_models,
    browsers=browsers,
    render_engines=render_engines,
    count=count
)

# Запись результата в файл с пробелами между User-Agent'ами
file_name = f'android_user_agents_with_telegram_support_{count}.txt'
with open(file_name, 'w') as file:
    for agent in generated_user_agents:
        file.write(agent + '\n\n')  # Каждую строку с новой строки и пробелом между ними

print(f"{len(generated_user_agents)} уникальных Android User-Agent'ов, поддерживающих Telegram, были успешно сгенерированы и сохранены в файл {file_name}.")