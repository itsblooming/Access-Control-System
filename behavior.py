import time
from pynput import mouse, keyboard
from database import get_user_id
import sqlite3

def measure_typing_speed():
    sample_text = "The quick brown fox jumps over the lazy dog."
    input(f"Type the following and press Enter:\n{sample_text}\nPress Enter to start...")

    start_time = time.time()
    hold_times = []
    flight_times = []
    prev_release_time = None
    key_press_times = {}

    def on_press(key):
        key_press_times[key] = time.time()

    def on_release(key):
        nonlocal prev_release_time
        release_time = time.time()
        if key in key_press_times:
            hold_times.append(release_time - key_press_times[key])
        if prev_release_time is not None:
            flight_times.append(release_time - prev_release_time)
        prev_release_time = release_time

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    user_input = input("Now type: ")
    listener.stop()

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Проверка деления на ноль
    if elapsed_time == 0:
        elapsed_time = 1  # Предотвращаем деление на ноль

    typing_speed = len(user_input) / elapsed_time

    avg_hold_time = sum(hold_times) / len(hold_times) if hold_times else 0
    avg_flight_time = sum(flight_times) / len(flight_times) if flight_times else 0

    return typing_speed, avg_hold_time, avg_flight_time


def measure_mouse_movement():
    start_time = time.time()
    prev_x, prev_y = None, None
    distance = 0

    def on_move(x, y):
        nonlocal prev_x, prev_y, distance
        if prev_x is not None and prev_y is not None:
            distance += ((x - prev_x) ** 2 + (y - prev_y) ** 2) ** 0.5
        prev_x, prev_y = x, y

    with mouse.Listener(on_move=on_move) as listener:
        time.sleep(5)
        listener.stop()

    return distance

def record_user_behavior(username):
    user_id = get_user_id(username)
    if user_id:
        typing_speed, hold_time, flight_time = measure_typing_speed()
        mouse_movement = measure_mouse_movement()
        with sqlite3.connect("users.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO behavior_data (user_id, typing_speed, mouse_movement, hold_time, flight_time) 
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, typing_speed, mouse_movement, hold_time, flight_time))
            conn.commit()
    else:
        print("User not found!")