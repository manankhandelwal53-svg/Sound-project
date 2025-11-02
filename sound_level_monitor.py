import os
import random
import time
import ctypes
import sounddevice as sd
import numpy as np

# ===============================================================
# CONFIGURATION
# ===============================================================

# 👇 Your wallpaper base path
BASE_PATH = r"D:\emotion\wallpapers"

# Folder mapping
WALLPAPER_PATHS = {
    "quiet": os.path.join(BASE_PATH, "quiet"),
    "moderate": os.path.join(BASE_PATH, "moderate"),
    "loud": os.path.join(BASE_PATH, "loud"),
    "very_loud": os.path.join(BASE_PATH, "very_loud")
}

# Thresholds (in decibels)
THRESHOLDS_DB = {
    "quiet": (-100, -40),
    "moderate": (-40, -20),
    "loud": (-20, -10),
    "very_loud": (-10, 10)
}

# Time between checks (seconds)
CHECK_INTERVAL = 2


# ===============================================================
# FUNCTIONS
# ===============================================================

def get_volume_db(duration=0.5):
    """Capture short sound sample and return its decibel value."""
    try:
        audio = sd.rec(int(duration * 44100), samplerate=44100, channels=1, dtype='float64')
        sd.wait()
        rms = np.sqrt(np.mean(audio ** 2))
        if rms <= 1e-10:
            rms = 1e-10
        db = 20 * np.log10(rms)
        return db
    except Exception as e:
        print(f"[Error capturing audio] {e}")
        return -100


def classify_sound_level(db_value):
    """Classify sound into quiet/moderate/loud/very_loud."""
    for level, (low, high) in THRESHOLDS_DB.items():
        if low <= db_value < high:
            return level
    return "quiet"


def set_wallpaper(image_path):
    """Change the Windows wallpaper using full path."""
    try:
        abs_path = os.path.abspath(image_path)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)
        # Force a desktop refresh for reliability
        ctypes.windll.user32.UpdatePerUserSystemParameters(1)
        print(f"✅ Wallpaper changed: {abs_path}\n")
    except Exception as e:
        print(f"[Wallpaper error] {e}")


def get_random_wallpaper(level):
    """Get a random wallpaper from the respective folder."""
    folder = WALLPAPER_PATHS[level]
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not files:
        print(f"⚠️ No wallpapers found in {folder}")
        return None
    return os.path.join(folder, random.choice(files))


# ===============================================================
# MAIN LOOP
# ===============================================================
def main():
    print("🎧 Sound-reactive wallpaper system started...")
    print("Listening for sound changes... (Ctrl+C to stop)\n")

    last_level = None

    while True:
        db = get_volume_db()
        level = classify_sound_level(db)

        print(f"Current Volume: {db:.2f} dB → Level: {level}")

        if level != last_level:
            print(f"🔊 Sound level changed: {last_level} → {level}")
            wallpaper_path = get_random_wallpaper(level)
            if wallpaper_path:
                set_wallpaper(wallpaper_path)
            last_level = level

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
