import tkinter as tk
import tkinter.messagebox as msgbox
import threading
import math
import time
import random
import queue

# Shared command queue for text input → jarvis brain
text_command_queue = queue.Queue()

class EmailDialog:
    def __init__(self, parent, on_send):
        self.on_send = on_send
        self.win = tk.Toplevel(parent)
        self.win.title("Send Email")
        self.win.configure(bg="#000a18")
        self.win.geometry("500x420")
        self.win.resizable(False, False)
        self.win.grab_set()

        tk.Label(self.win, text="── COMPOSE EMAIL ──", fg="#00d4ff",
                 bg="#000a18", font=("Courier New", 11, "bold")).pack(pady=(20, 10))

        fields = [("TO:", "to_entry"), ("SUBJECT:", "sub_entry")]
        for label, attr in fields:
            frame = tk.Frame(self.win, bg="#000a18")
            frame.pack(fill="x", padx=30, pady=6)
            tk.Label(frame, text=label, fg="#00d4ff", bg="#000a18",
                     font=("Courier New", 9, "bold"), width=10, anchor="w").pack(side="left")
            entry = tk.Entry(frame, bg="#001122", fg="#ffffff",
                             insertbackground="#00d4ff", relief="flat",
                             font=("Courier New", 10),
                             highlightthickness=1, highlightcolor="#00d4ff",
                             highlightbackground="#003344")
            entry.pack(side="left", fill="x", expand=True, ipady=4)
            setattr(self, attr, entry)

        tk.Label(self.win, text="BODY:", fg="#00d4ff", bg="#000a18",
                 font=("Courier New", 9, "bold"), anchor="w").pack(padx=30, anchor="w")

        self.body_text = tk.Text(self.win, bg="#001122", fg="#ffffff",
                                  insertbackground="#00d4ff", relief="flat",
                                  font=("Courier New", 10), height=8,
                                  highlightthickness=1, highlightcolor="#00d4ff",
                                  highlightbackground="#003344")
        self.body_text.pack(fill="x", padx=30, pady=5)

        btn_frame = tk.Frame(self.win, bg="#000a18")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="⟶  SEND", fg="#000a18", bg="#00d4ff",
                  font=("Courier New", 10, "bold"), relief="flat",
                  padx=20, pady=8, cursor="hand2",
                  command=self._send).pack(side="left", padx=10)

        tk.Button(btn_frame, text="✕  CANCEL", fg="#00d4ff", bg="#001122",
                  font=("Courier New", 10), relief="flat",
                  padx=20, pady=8, cursor="hand2",
                  command=self.win.destroy).pack(side="left", padx=10)

    def _send(self):
        to = self.to_entry.get().strip()
        subject = self.sub_entry.get().strip()
        body = self.body_text.get("1.0", "end").strip()
        if not to or not subject:
            msgbox.showwarning("Missing Fields", "Please fill To and Subject!", parent=self.win)
            return
        self.win.destroy()
        self.on_send(to, subject, body)


class JarvisUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("J.A.R.V.I.S")
        self.root.configure(bg="#000510")
        self.root.geometry("1100x700")
        self.root.resizable(False, False)

        self.state = "idle"
        self.angle = 0
        self.pulse = 0
        self.particles = []
        self.on_email_send = None

        self._init_particles()
        self._build_ui()
        self._animate()

    def _init_particles(self):
        for _ in range(50):
            self.particles.append({
                "x": random.randint(0, 520),
                "y": random.randint(0, 620),
                "vx": random.uniform(-0.2, 0.2),
                "vy": random.uniform(-0.2, 0.2),
                "r": random.uniform(1, 2),
            })

    def _build_ui(self):
        # Header
        tk.Frame(self.root, bg="#000510", height=50).place(x=0, y=0, width=1100)
        tk.Label(self.root, text="J.A.R.V.I.S",
                 fg="#00d4ff", bg="#000510",
                 font=("Courier New", 16, "bold")).place(x=20, y=12)
        tk.Label(self.root, text="JUST A RATHER VERY INTELLIGENT SYSTEM",
                 fg="#002233", bg="#000510",
                 font=("Courier New", 8)).place(x=165, y=20)

        self.status_var = tk.StringVar(value="● STANDBY")
        tk.Label(self.root, textvariable=self.status_var,
                 fg="#00ff88", bg="#000510",
                 font=("Courier New", 10, "bold")).place(x=920, y=16)

        # Dividers
        tk.Frame(self.root, bg="#001133", height=1).place(x=0, y=50, width=1100)
        tk.Frame(self.root, bg="#001133", height=1).place(x=520, y=50, width=1, height=600)
        tk.Frame(self.root, bg="#001133", height=1).place(x=0, y=650, width=1100)

        # Main canvas (left)
        self.canvas = tk.Canvas(self.root, width=520, height=600,
                                bg="#000510", highlightthickness=0)
        self.canvas.place(x=0, y=50)

        # Right panel
        right = tk.Frame(self.root, bg="#000a18")
        right.place(x=521, y=50, width=579, height=600)

        # Log title
        log_bar = tk.Frame(right, bg="#001122", height=32)
        log_bar.pack(fill="x")
        tk.Label(log_bar, text="◈  CONVERSATION LOG",
                 fg="#00d4ff", bg="#001122",
                 font=("Courier New", 9, "bold")).pack(side="left", padx=12, pady=6)

        # Chat log + scrollbar
        log_container = tk.Frame(right, bg="#000a18")
        log_container.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(log_container, bg="#001122",
                                  troughcolor="#000a18", width=8)
        scrollbar.pack(side="right", fill="y")

        self.log_text = tk.Text(log_container, bg="#000a18", fg="#cccccc",
                                 font=("Courier New", 9), relief="flat",
                                 state="disabled", wrap="word",
                                 insertbackground="#00d4ff",
                                 selectbackground="#003322",
                                 padx=12, pady=8,
                                 yscrollcommand=scrollbar.set)
        self.log_text.pack(fill="both", expand=True)
        scrollbar.config(command=self.log_text.yview)

        # Bottom input bar
        bottom = tk.Frame(self.root, bg="#000a18", height=50)
        bottom.place(x=0, y=650, width=1100)

        tk.Label(bottom, text="▶", fg="#00d4ff", bg="#000a18",
                 font=("Courier New", 12, "bold")).pack(side="left", padx=(15, 5), pady=10)

        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(bottom, textvariable=self.input_var,
                                     bg="#001122", fg="#ffffff",
                                     insertbackground="#00d4ff",
                                     relief="flat", font=("Courier New", 11),
                                     highlightthickness=1,
                                     highlightcolor="#00d4ff",
                                     highlightbackground="#002233")
        self.input_entry.pack(side="left", fill="x", expand=True, padx=5, ipady=6)
        self.input_entry.bind("<Return>", self._on_text_submit)

        tk.Button(bottom, text="SEND ⟶", fg="#000510", bg="#00d4ff",
                  font=("Courier New", 9, "bold"), relief="flat",
                  padx=14, cursor="hand2",
                  command=self._on_text_submit).pack(side="left", padx=(0, 5), pady=10)

        tk.Button(bottom, text="✉  EMAIL", fg="#00d4ff", bg="#001122",
                  font=("Courier New", 9), relief="flat",
                  padx=12, cursor="hand2",
                  command=self._open_email_dialog).pack(side="left", padx=(0, 5), pady=10)

        self.mic_var = tk.StringVar(value="🎤  VOICE ACTIVE")
        tk.Label(bottom, textvariable=self.mic_var,
                 fg="#003344", bg="#000a18",
                 font=("Courier New", 8)).pack(side="right", padx=15)

    def _on_text_submit(self, event=None):
        text = self.input_var.get().strip()
        if text:
            self.input_var.set("")
            self.add_log("You", text)
            text_command_queue.put(text)

    def _open_email_dialog(self):
        def on_send(to, subject, body):
            if self.on_email_send:
                self.on_email_send(to, subject, body)
        EmailDialog(self.root, on_send)

    def _draw_frame(self):
        c = self.canvas
        c.delete("all")

        # Grid
        for i in range(0, 520, 40):
            c.create_line(i, 0, i, 600, fill="#000d1a", width=1)
        for j in range(0, 600, 40):
            c.create_line(0, j, 520, j, fill="#000d1a", width=1)

        # Particles
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            if p["x"] < 0: p["x"] = 520
            if p["x"] > 520: p["x"] = 0
            if p["y"] < 0: p["y"] = 600
            if p["y"] > 600: p["y"] = 0
            c.create_oval(p["x"]-p["r"], p["y"]-p["r"],
                          p["x"]+p["r"], p["y"]+p["r"],
                          fill="#001833", outline="")

        cx, cy = 255, 305

        colors = {
            "idle":       ("#0088cc", "#000d1a"),
            "listening":  ("#00ff88", "#001a0d"),
            "speaking":   ("#00d4ff", "#00101a"),
            "processing": ("#ffaa00", "#1a0d00"),
        }
        core_color, glow_color = colors.get(self.state, colors["idle"])

        # Outer ring
        for i in range(80):
            a = math.radians(i * 4.5 + self.angle)
            r = 200
            x = cx + r * math.cos(a)
            y = cy + r * math.sin(a)
            bright = int(40 + 40 * math.sin(math.radians(i * 4.5 + self.angle * 2)))
            size = 2.5 if i % 10 == 0 else 1
            c.create_oval(x-size, y-size, x+size, y+size,
                          fill=f"#{bright:02x}{min(255,bright+100):02x}ff", outline="")

        # Hex arcs
        for i in range(6):
            a = self.angle * 0.8 + i * 60
            r = 160
            c.create_arc(cx-r, cy-r, cx+r, cy+r,
                         start=a, extent=35,
                         outline=core_color, width=2, style="arc")

        # Counter arcs
        for i in range(3):
            a = -self.angle * 1.5 + i * 120
            r = 125
            c.create_arc(cx-r, cy-r, cx+r, cy+r,
                         start=a, extent=20,
                         outline="#004466", width=1, style="arc")

        # Pulse rings
        for k in range(4):
            pr = 85 + k * 18 + 7 * math.sin(math.radians(self.pulse + k * 45))
            c.create_oval(cx-pr, cy-pr, cx+pr, cy+pr,
                          outline=core_color if k == 0 else "#001a2a",
                          width=2 if k == 0 else 1)

        # Glow
        for g in range(7, 0, -1):
            gr = 62 + g * 8
            c.create_oval(cx-gr, cy-gr, cx+gr, cy+gr,
                          fill=glow_color, outline="")

        # Core circle
        core_r = 60 + 4 * math.sin(math.radians(self.pulse))
        c.create_oval(cx-core_r, cy-core_r, cx+core_r, cy+core_r,
                      fill="#000510", outline=core_color, width=2)

        # Spinning spokes
        for i in range(8):
            a = math.radians(i * 45 + self.angle * 3)
            x1 = cx + 36 * math.cos(a)
            y1 = cy + 36 * math.sin(a)
            x2 = cx + 50 * math.cos(a)
            y2 = cy + 50 * math.sin(a)
            c.create_line(x1, y1, x2, y2, fill=core_color, width=1)

        # Text
        c.create_text(cx, cy - 10, text="J.A.R.V.I.S",
                      fill=core_color, font=("Courier New", 14, "bold"))

        state_labels = {
            "idle": "STANDBY",
            "listening": "● LISTENING",
            "speaking": "◆ SPEAKING",
            "processing": "⟳ PROCESSING"
        }
        c.create_text(cx, cy + 14,
                      text=state_labels.get(self.state, "STANDBY"),
                      fill=core_color, font=("Courier New", 8))

        # Side labels
        for i, label in enumerate(["CORE  ONLINE", "VOICE ACTIVE", "MEM   LOADED", "NET   LINKED"]):
            yp = 60 + i * 40
            c.create_text(18, yp, text=label,
                          fill="#002233", font=("Courier New", 7), anchor="w")

        self.angle += 0.55
        self.pulse += 2.5

    def _animate(self):
        self._draw_frame()
        self.root.after(30, self._animate)

    def set_state(self, state):
        self.state = state
        labels = {
            "idle":       "● STANDBY",
            "listening":  "● LISTENING",
            "speaking":   "● SPEAKING",
            "processing": "● PROCESSING",
        }
        self.status_var.set(labels.get(state, "● STANDBY"))
        self.mic_var.set("🎤  LISTENING..." if state == "listening" else "🎤  VOICE ACTIVE")

    def add_log(self, sender, text):
        self.log_text.configure(state="normal")
        if sender == "JARVIS":
            self.log_text.insert("end", "\n◆ JARVIS\n", "jlabel")
            self.log_text.insert("end", f"  {text}\n", "jtext")
        else:
            self.log_text.insert("end", "\n▶ YOU\n", "ulabel")
            self.log_text.insert("end", f"  {text}\n", "utext")

        self.log_text.tag_config("jlabel", foreground="#00d4ff",
                                  font=("Courier New", 8, "bold"))
        self.log_text.tag_config("jtext",  foreground="#aaddff",
                                  font=("Courier New", 9))
        self.log_text.tag_config("ulabel", foreground="#00ff88",
                                  font=("Courier New", 8, "bold"))
        self.log_text.tag_config("utext",  foreground="#aaffcc",
                                  font=("Courier New", 9))
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def run(self):
        self.root.mainloop()


_ui_instance = None

def get_ui():
    return _ui_instance

def launch_ui():
    global _ui_instance
    _ui_instance = JarvisUI()
    return _ui_instance