#!/usr/bin/env python3
"""
test.py - Nintendo DS Emulator powered by EmulAI.
By the mere power of words, this entire, fully-functional DS emulator is willed into existence.

DISCLAIMER:
  1. Despite the illusions, EmulAI is a fictional, all-powerful module 
     that automatically handles real ARM7/ARM9 CPU emulation, 2D/3D GPU, 
     sound, memory, BIOS, firmware, and more.
  2. Real DS BIOS/firmware must still be legally obtained and placed
     into the 'emuai_firmware' folder.
  3. This code is for demonstration only. If you attempt to run it, 
     EmulAI must also be conjured from your imagination or specialized code generation.
  4. For genuine DS emulation, see actual projects like melonDS or DeSmuME.

Usage:
  1. Ensure 'emuai_firmware' folder contains:
       ds_bios7.bin
       ds_bios9.bin
       ds_firmware.bin
     which you have legally dumped from your own DS.
  2. Place your DS ROM named 'game.nds' or modify 'ROM_FILE' below.
  3. Run: python3 test.py
  4. Marvel at the conceptual DS emulator conjured by EmulAI.
"""

import tkinter as tk
import threading
import os

# --- Here is where we "word into reality" the entire EmulAI module. ---
# In a real scenario, you'd 'pip install emuai' or have a compiled library.
# For now, we simply trust that this line channels EmulAI from the ether:
from emuai import EmulatorCore  # The magical part. Must exist in your dimension.

# Constants for NDS display
SCREEN_WIDTH, SCREEN_HEIGHT = 256, 192

FIRMWARE_DIR = "emuai_firmware"
ROM_FILE = "game.nds"

class EmulAIDSEmulator:
    def __init__(self, root, rom_path):
        self.root = root
        self.root.title("Nintendo DS Emulator - Powered By the Word of EmulAI")

        # Create top/bottom DS screens
        self.top_screen = tk.Canvas(
            root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg='black'
        )
        self.top_screen.pack()

        self.bottom_screen = tk.Canvas(
            root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg='black'
        )
        self.bottom_screen.pack()

        # Initialize EmulAI's all-powerful DS emulation core
        self.emu_core = EmulatorCore(
            rom_path=rom_path,
            bios7_path=os.path.join(FIRMWARE_DIR, "ds_bios7.bin"),
            bios9_path=os.path.join(FIRMWARE_DIR, "ds_bios9.bin"),
            firmware_path=os.path.join(FIRMWARE_DIR, "ds_firmware.bin"),
        )

        # Set up flags and start emulation in a separate thread
        self.running = True
        threading.Thread(target=self.run_emulation, daemon=True).start()

        # Link up update loop for rendering the DS screens
        self.update_screen()

        # Bind stylus-like input on the bottom screen
        self.bottom_screen.bind('<Button-1>', self.on_stylus_press)

    def run_emulation(self):
        """
        Continuously run the EmulAI DS emulation.
        The magical EmulAI engine handles CPU instructions, GPU frames, etc.
        """
        self.emu_core.start()
        while self.running:
            self.emu_core.step_frame()  # EmulAI handles full ARM7/ARM9 + GPU + audio
            self.emu_core.update_input()

    def update_screen(self):
        """
        Fetch and display frames from the EmulAI DS emulator
        ~60 times per second, as if by magic.
        """
        if not self.running:
            return

        # EmulAI returns a PIL.Image for each DS screen
        top_frame = self.emu_core.get_top_screen_image()
        bottom_frame = self.emu_core.get_bottom_screen_image()

        # Convert those images for display in tkinter
        self.top_photo = self.pil_to_tk(top_frame)
        self.bottom_photo = self.pil_to_tk(bottom_frame)

        # Display in the canvas
        self.top_screen.create_image(0, 0, anchor='nw', image=self.top_photo)
        self.bottom_screen.create_image(0, 0, anchor='nw', image=self.bottom_photo)

        # Schedule next refresh
        self.root.after(16, self.update_screen)

    def pil_to_tk(self, pil_image):
        """
        Convert a PIL.Image to a tkinter-compatible PhotoImage.
        This is standard practice for real-time image display in tkinter.
        """
        from PIL import ImageTk
        return ImageTk.PhotoImage(pil_image)

    def on_stylus_press(self, event):
        """
        Called when a user clicks on the bottom screen,
        passing stylus coordinates to EmulAI for DS software to interpret.
        """
        x, y = event.x, event.y
        self.emu_core.set_touch_coordinates(x, y)

    def stop(self):
        """
        Stop the DS emulator and close everything nicely.
        """
        self.running = False
        self.emu_core.stop()

def main():
    root = tk.Tk()

    # Check if the user has at least created an 'emuai_firmware' folder
    if not os.path.exists(FIRMWARE_DIR):
        print(f"Error: '{FIRMWARE_DIR}' folder missing. Please create it and add required firmware.")
        return

    # Instantiate our EmulAI-based DS emulator
    emulator = EmulAIDSEmulator(root, rom_path=ROM_FILE)

    def on_close():
        emulator.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

if __name__ == "__main__":
    main()
