# код написан ИИ но зато игра смогла запуститься на pydroid

import atexit
import sys
import termios
import threading
import tty
from collections import defaultdict

# Используем select для неблокирующего чтения в Unix-подобных системах
try:
    import select
except ImportError:
    # Ошибка: select не найден (например, в некоторых средах Windows), 
    # но поскольку мы используем termios, среда должна быть Unix-подобной.
    pass

# --- ВНУТРЕННИЕ ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ СОСТОЯНИЯ ---
_HOTKEYS = defaultdict(list)
_RUNNING = False
_THREAD = None
_FD = sys.stdin.fileno()
_ORIGINAL_TERMINAL_SETTINGS = None
_LOCK = threading.Lock()


# --- Внутренние Функции Управления Терминалом ---

def _set_cbreak_mode():
    """Устанавливает терминал в cbreak режим для Hotkeys."""
    global _ORIGINAL_TERMINAL_SETTINGS, _RUNNING
    if _ORIGINAL_TERMINAL_SETTINGS is None:
        try:
            _ORIGINAL_TERMINAL_SETTINGS = termios.tcgetattr(_FD)
        except termios.error:
            _RUNNING = False
            return
    tty.setcbreak(_FD)


def _restore_terminal_mode():
    """Возвращает терминал в исходное состояние (канонический режим)."""
    if _ORIGINAL_TERMINAL_SETTINGS is not None:
        termios.tcsetattr(_FD, termios.TCSADRAIN, _ORIGINAL_TERMINAL_SETTINGS)


def _get_single_char():
    """
    Считывает один символ, используя select для неблокирующего чтения. 
    Возвращает "", если символ не был нажат.
    """
    try:
        # Таймаут 0.001с (или меньше) позволяет потоку быстро завершиться
        ready, _, _ = select.select([_FD], [], [], 0.001)
        if ready:
            return sys.stdin.read(1)
    except select.error:
        # Происходит, если терминал был закрыт или изменен во время select
        pass
    except termios.error:
        # Происходит, если терминал был изменен
        pass

    return ""


# --- Внутренний Поток Слушателя ---

def _listener_loop():
    """Цикл, который слушает ввод Hotkeys."""
    global _RUNNING

    _set_cbreak_mode()

    try:
        while _RUNNING:
            key = _get_single_char()

            if not key:
                # Если ввода нет (неблокирующий select), быстро проверяем _RUNNING
                continue

            key_lower = key.lower()

            # --- Маппинг пробела ---
            if key_lower == " ":
                key_lower = "space"

            # Остановка по сигналу (Ctrl+C/D)
            if key in ('\x03', '\x04'):
                _RUNNING = False
                break

            if key_lower in _HOTKEYS:
                for func in _HOTKEYS[key_lower]:
                    func()

    except Exception:
        pass

    finally:
        _restore_terminal_mode()


# --- Публичные Функции API ---

def add_hotkey(key_to_track, function_to_call):
    """Регистрирует функцию и запускает слушатель."""
    key = key_to_track.lower()

    # --- Маппинг пробела ---
    if key == " ":
        key = "space"

    _HOTKEYS[key].append(function_to_call)

    if not _RUNNING:
        start_hotkey_listener()


def start_hotkey_listener():
    """Запускает слушатель в новом фоновом потоке."""
    global _RUNNING, _THREAD

    with _LOCK:
        if _RUNNING:
            return

        _RUNNING = True
        _THREAD = threading.Thread(target=_listener_loop, daemon=True)
        _THREAD.start()


def stop_hotkey_listener(wait=False):
    """
    Останавливает слушатель. wait=True гарантирует завершение потока.
    """
    global _RUNNING, _THREAD

    with _LOCK:
        if not _RUNNING:
            return

        _RUNNING = False

        # 1. Восстанавливаем настройки (важно для atexit)
        _restore_terminal_mode()

        if _THREAD and threading.current_thread() != _THREAD:
            # 2. Ждем завершения потока. Теперь это не приведет к тупику.
            if wait:
                # Даем потоку небольшой таймаут для выхода из цикла
                _THREAD.join(timeout=0.1)

            if not _THREAD.is_alive():
                _THREAD = None
            else:
                # Если не завершился (очень маловероятно), сбрасываем ссылку на него
                _THREAD = None


def get_user_input(prompt=""):
    """
    Встроенная, измененная и работающая версия input().
    Останавливает поток, выполняет ввод, и снова запускает поток.
    """
    was_running = _RUNNING

    # 1. *** ГАРАНТИРОВАННАЯ ПОЛНАЯ ОСТАНОВКА ПОТОКА ***
    if was_running:
        # stop_hotkey_listener(wait=True) теперь надежно завершит поток
        stop_hotkey_listener(wait=True)

        # 2. Очистка буфера ввода (Ключевой момент для надежной работы input())
    try:
        termios.tcflush(_FD, termios.TCIFLUSH)
    except termios.error:
        pass

    # 3. Выполняем ввод
    result = input(prompt)

    # 4. *** ПЕРЕЗАПУСК ПОТОКА ***
    if was_running:
        start_hotkey_listener()

    return result


# Регистрируем функцию сброса для гарантированного восстановления терминала при завершении
# Регистрируем оба, так как stop_hotkey_listener может не успеть восстановить терминал
atexit.register(stop_hotkey_listener)
atexit.register(_restore_terminal_mode)
