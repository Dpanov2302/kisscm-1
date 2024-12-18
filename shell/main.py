import yaml
import os


def load_config(config_path):
    """Загружает конфигурацию из YAML-файла."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Конфигурационный файл {config_path} не найден.")

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    if 'user' not in config or 'vfs_path' not in config:
        raise ValueError("Конфигурационный файл должен содержать параметры 'user' и 'vfs_path'.")

    return config


if __name__ == "__main__":
    CONFIG_PATH = "config.yaml"

    try:
        config = load_config(CONFIG_PATH)
        print(f"Конфигурация загружена: {config}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Ошибка загрузки конфигурации: {e}")
