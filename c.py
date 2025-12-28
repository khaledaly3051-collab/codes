import socket
import threading
import pickle
import time
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

class Event:
    def __init__(self, title, time_val):
        self.title = title
        self.time_val = time_val

class Subject:
    def __init__(self): self._observers = []
    def attach(self, observer): self._observers.append(observer)
    def notify(self, event): [o.update(event) for o in self._observers]

class NotificationService:
    def update(self, event):
        messagebox.showinfo("Smart Alert", f"⏰ Event Starting Now: {event.title}")

class CalendarManager(Subject):
    def __init__(self):
        super().__init__()
        self.events = []
        self.sock = None

    def add_event(self, event, sync=True):
        self.events.append(event)
        if sync and self.sock:
            try: self.sock.send(pickle.dumps(event))
            except: pass

    def check_notifications(self):
        while True:
            now = datetime.now().strftime("%H:%M")
            for e in self.events[:]:
                if e.time_val == now:
                    self.notify(e)
                    self.events.remove(e)
            time.sleep(10)

def start_app():
    root = tk.Tk()
    root.title("Smart Shared Calendar")
    root.geometry("400x450")
    
    manager = CalendarManager()
    manager.attach(NotificationService())

    frame = tk.Frame(root, pady=10)
    frame.pack()
    tk.Label(frame, text="Event:").grid(row=0, column=0)
    ent_title = ttk.Entry(frame)
    ent_title.grid(row=0, column=1)
    tk.Label(frame, text="Time (HH:MM):").grid(row=1, column=0)
    ent_time = ttk.Entry(frame)
    ent_time.grid(row=1, column=1)

    tree = ttk.Treeview(root, columns=("T", "E"), show="headings", height=8)
    tree.heading("T", text="Time"); tree.heading("E", text="Event Name")
    tree.pack(padx=10, pady=10, fill="both")

    def refresh():
        tree.delete(*tree.get_children())
        [tree.insert("", "end", values=(e.time_val, e.title)) for e in manager.events]

    def on_add():
        if ent_title.get() and ent_time.get():
            manager.add_event(Event(ent_title.get(), ent_time.get()))
            refresh()
            ent_title.delete(0, 'end'); ent_time.delete(0, 'end')

    ttk.Button(root, text="Add Shared Event", command=on_add).pack(pady=5)

    def listen_to_server():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(('127.0.0.1', 7002))
            manager.sock = s
            while True:
                data = s.recv(4096)
                if data: 
                    manager.add_event(pickle.loads(data), False)
                    refresh()
        except: print("Could not connect to server.")

    threading.Thread(target=listen_to_server, daemon=True).start()
    threading.Thread(target=manager.check_notifications, daemon=True).start()
    
    root.mainloop()

if __name__ == "__main__":
    start_app()