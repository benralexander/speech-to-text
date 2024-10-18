import os
from pathlib import Path
import subprocess
import threading
import time

import httpx
# import keyboard

CHUNK = 2**12
AUDIO_RECORD_CMD = [
    "ffmpeg",
    "-hide_banner",
    # "-loglevel",
    # "quiet",
    "-f",
    "alsa",
    "-i",
    "default",
    "-f",
    "wav",
]
COPY_TO_CLIPBOARD_CMD = "wl-copy"
USER = "nixos"
TIMEOUT = httpx.Timeout(None)
KEYBIND = "ctrl+x"
REQUEST_KWARGS = {
    "language": "en",
    "response_format": "text",
    "vad_filter": True,
}

class openai_cmd:
    def __init__(self):
        openai_base=os.getenv("OPENAI_BASE_URL")
        self.client = httpx.Client(base_url=openai_base, timeout=TIMEOUT)
        self.is_running = threading.Event()

    def perform(self,cmd):
        if cmd=="transcribe":
            audio_file = open("audio.wav", "rb")
            transcript = self.client.audio.transcriptions.create(
            model="Systran/faster-distil-whisper-large-v3", file=audio_file
        )
        print(transcript.text)


        print('CALLL LOCAL OPENAI')
        process = subprocess.Popen(
            [*AUDIO_RECORD_CMD, "-y", str(file.name)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            user=USER,
            env=dict(os.environ),
        )

        process.kill()
        stdout, stderr = process.communicate()
        if stdout or stderr:
            print(f"stdout: {stdout}")
            print(f"stderr: {stderr}")


    try:
        with file.open("rb") as fd:
            start = time.perf_counter()
            res = client.post(
                OPENAI_BASE_URL + TRANSCRIBE_PATH,
                files={"file": fd},
                data=REQUEST_KWARGS,
            )
        end = time.perf_counter()
        print(f"Transcription took {end - start} seconds")
        transcription = res.text
        # keyboard.type(transcription)
        print(transcription)
        subprocess.run([COPY_TO_CLIPBOARD_CMD], input=transcription.encode(), check=True)
    except httpx.ConnectError as e:
        print(f"Couldn't connect to server: {e}")
