"""
Random Task Generator — GUI Application
Author: Student / Developer
"""

import json
import random
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ─── Constants ────────────────────────────────────────────────────────────────

HISTORY_FILE = "history.json"

PREDEFINED_TASKS = [
    {"title": "Прочитать статью по Python",      "category": "учёба"},
    {"title": "Пройти урок по алгоритмам",        "category": "учёба"},
    {"title": "Написать конспект лекции",          "category": "учёба"},
    {"title": "Порешать задачи на LeetCode",       "category": "учёба"},
    {"title": "Посмотреть обучающий курс",         "category": "учёба"},
    {"title": "Сделать зарядку (15 мин)",          "category": "спорт"},
    {"title": "Пробежка 3 км",                     "category": "спорт"},
    {"title": "Йога-растяжка",                     "category": "спорт"},
    {"title": "Отжимания и пресс",                 "category": "спорт"},
    {"title": "Прогулка на свежем воздухе",        "category": "спорт"},
    {"title": "Ответить на рабочие письма",        "category": "работа"},
    {"title": "Составить план на неделю",          "category": "работа"},
    {"title": "Провести код-ревью",                "category": "работа"},
    {"title": "Обновить документацию проекта",     "category": "работа"},
    {"title": "Разобрать задачи в трекере",        "category": "работа"},
]

CATEGORY_COLORS = {
    "все":    "#4A90D9",
    "учёба":  "#27AE60",
    "спорт":  "#E67E22",
    "работа": "#8E44AD",
}

CATEGORY_EMOJI = {
    "учёба":  "📚",
    "спорт":  "🏃",
    "работа": "💼",
}

# ─── History helpers ──────────────────────────────────────────────────────────

def load_history() -> list:
    """Load task history from JSON file."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except (json.JSONDecodeError, IOError):
            pass
    return []


def save_history(history: list) -> None:
    """Save task history to JSON file."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


# ─── Main Application ─────────────────────────────────────────────────────────

class RandomTaskApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("🎲 Random Task Generator")
        self.geometry("820x680")
        self.minsize(700, 560)
        self.configure(bg="#1E1E2E")
        self.resizable(True, True)

        # State
        self.tasks: list  = list(PREDEFINED_TASKS)   # mutable working list
        self.history: list = load_history()
        self.current_filter = tk.StringVar(value="все")

        self._build_ui()
        self._refresh_history_list()

    # ── UI construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Top banner ────────────────────────────────────────────────────────
        banner = tk.Frame(self, bg="#181825", pady=14)
        banner.pack(fill="x")
        tk.Label(
            banner, text="🎲  Random Task Generator",
            font=("Segoe UI", 20, "bold"),
            fg="#CDD6F4", bg="#181825"
        ).pack()
        tk.Label(
            banner, text="Нажмите кнопку — получите задачу!",
            font=("Segoe UI", 10),
            fg="#A6ADC8", bg="#181825"
        ).pack()

        # ── Main content area ─────────────────────────────────────────────────
        content = tk.Frame(self, bg="#1E1E2E")
        content.pack(fill="both", expand=True, padx=20, pady=14)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)
        content.rowconfigure(0, weight=1)

        self._build_left_panel(content)
        self._build_right_panel(content)

    def _build_left_panel(self, parent):
        left = tk.Frame(parent, bg="#1E1E2E")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # ── Current task card ─────────────────────────────────────────────────
        card = tk.Frame(left, bg="#313244", bd=0, relief="flat")
        card.pack(fill="x", pady=(0, 12))

        tk.Label(card, text="Текущая задача",
                 font=("Segoe UI", 10), fg="#A6ADC8", bg="#313244"
                 ).pack(anchor="w", padx=14, pady=(12, 2))

        self.task_label = tk.Label(
            card, text="Нажмите «Сгенерировать задачу»",
            font=("Segoe UI", 14, "bold"),
            fg="#CDD6F4", bg="#313244",
            wraplength=380, justify="left"
        )
        self.task_label.pack(anchor="w", padx=14, pady=(0, 4))

        self.category_badge = tk.Label(
            card, text="", font=("Segoe UI", 9, "bold"),
            fg="#1E1E2E", bg="#313244", padx=8, pady=2
        )
        self.category_badge.pack(anchor="w", padx=14, pady=(0, 12))

        # ── Filter row ────────────────────────────────────────────────────────
        filter_frame = tk.Frame(left, bg="#1E1E2E")
        filter_frame.pack(fill="x", pady=(0, 10))
        tk.Label(filter_frame, text="Фильтр:", font=("Segoe UI", 10),
                 fg="#A6ADC8", bg="#1E1E2E").pack(side="left", padx=(0, 8))

        for cat in ["все", "учёба", "спорт", "работа"]:
            color = CATEGORY_COLORS[cat]
            btn = tk.Radiobutton(
                filter_frame, text=cat.capitalize(),
                variable=self.current_filter, value=cat,
                font=("Segoe UI", 9, "bold"),
                fg=color, bg="#1E1E2E",
                selectcolor="#313244",
                activebackground="#1E1E2E", activeforeground=color,
                indicatoron=True, cursor="hand2"
            )
            btn.pack(side="left", padx=4)

        # ── Generate button ───────────────────────────────────────────────────
        self.gen_btn = tk.Button(
            left, text="🎲  Сгенерировать задачу",
            font=("Segoe UI", 13, "bold"),
            bg="#89B4FA", fg="#1E1E2E",
            activebackground="#74C7EC", activeforeground="#1E1E2E",
            relief="flat", bd=0, pady=12, cursor="hand2",
            command=self._generate_task
        )
        self.gen_btn.pack(fill="x", pady=(0, 14))

        # ── Add custom task ───────────────────────────────────────────────────
        add_frame = tk.LabelFrame(
            left, text=" ➕  Добавить свою задачу ",
            font=("Segoe UI", 9), fg="#A6ADC8", bg="#1E1E2E",
            bd=1, relief="groove"
        )
        add_frame.pack(fill="x")

        tk.Label(add_frame, text="Название:", font=("Segoe UI", 9),
                 fg="#A6ADC8", bg="#1E1E2E").grid(row=0, column=0, padx=8, pady=6, sticky="w")
        self.new_task_entry = tk.Entry(
            add_frame, font=("Segoe UI", 10),
            bg="#313244", fg="#CDD6F4",
            insertbackground="#CDD6F4", relief="flat", bd=4
        )
        self.new_task_entry.grid(row=0, column=1, columnspan=2, padx=(0, 8), pady=6, sticky="ew")
        self.new_task_entry.bind("<Return>", lambda e: self._add_custom_task())

        tk.Label(add_frame, text="Категория:", font=("Segoe UI", 9),
                 fg="#A6ADC8", bg="#1E1E2E").grid(row=1, column=0, padx=8, pady=(0, 8), sticky="w")
        self.new_task_cat = ttk.Combobox(
            add_frame, values=["учёба", "спорт", "работа"],
            font=("Segoe UI", 10), width=10, state="readonly"
        )
        self.new_task_cat.current(0)
        self.new_task_cat.grid(row=1, column=1, padx=(0, 6), pady=(0, 8), sticky="w")

        tk.Button(
            add_frame, text="Добавить",
            font=("Segoe UI", 9, "bold"),
            bg="#A6E3A1", fg="#1E1E2E",
            activebackground="#94E2D5", activeforeground="#1E1E2E",
            relief="flat", bd=0, padx=10, cursor="hand2",
            command=self._add_custom_task
        ).grid(row=1, column=2, padx=(0, 8), pady=(0, 8))

        add_frame.columnconfigure(1, weight=1)

    def _build_right_panel(self, parent):
        right = tk.Frame(parent, bg="#1E1E2E")
        right.grid(row=0, column=1, sticky="nsew")

        header = tk.Frame(right, bg="#1E1E2E")
        header.pack(fill="x", pady=(0, 6))
        tk.Label(header, text="📜  История задач",
                 font=("Segoe UI", 11, "bold"),
                 fg="#CDD6F4", bg="#1E1E2E").pack(side="left")
        tk.Button(
            header, text="🗑 Очистить",
            font=("Segoe UI", 8),
            bg="#F38BA8", fg="#1E1E2E",
            activebackground="#EBA0AC", activeforeground="#1E1E2E",
            relief="flat", bd=0, padx=6, pady=2, cursor="hand2",
            command=self._clear_history
        ).pack(side="right")

        list_frame = tk.Frame(right, bg="#313244")
        list_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.history_list = tk.Listbox(
            list_frame,
            font=("Segoe UI", 9),
            bg="#313244", fg="#CDD6F4",
            selectbackground="#45475A",
            selectforeground="#CDD6F4",
            relief="flat", bd=0,
            activestyle="none",
            yscrollcommand=scrollbar.set
        )
        self.history_list.pack(fill="both", expand=True, padx=2)
        scrollbar.config(command=self.history_list.yview)

        tk.Label(right, text=f"Всего сессий: {len(self.history)}",
                 font=("Segoe UI", 8), fg="#6C7086", bg="#1E1E2E",
                 name="counter_label").pack(anchor="e", pady=(4, 0))
        self.counter_label = right.children["counter_label"]

    # ── Logic ──────────────────────────────────────────────────────────────────

    def _generate_task(self):
        """Pick a random task, respecting the active category filter."""
        cat = self.current_filter.get()
        pool = [t for t in self.tasks if cat == "все" or t["category"] == cat]

        if not pool:
            messagebox.showinfo(
                "Нет задач",
                f"Нет задач в категории «{cat}».\n"
                "Добавьте задачи или смените фильтр."
            )
            return

        task = random.choice(pool)
        self._display_task(task)

        # Record in history
        entry = {
            "title":    task["title"],
            "category": task["category"],
            "time":     datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
        }
        self.history.insert(0, entry)
        save_history(self.history)
        self._refresh_history_list()

    def _display_task(self, task: dict):
        """Update the current-task card."""
        self.task_label.config(text=task["title"])
        cat  = task["category"]
        color = CATEGORY_COLORS.get(cat, "#89B4FA")
        emoji = CATEGORY_EMOJI.get(cat, "")
        self.category_badge.config(
            text=f" {emoji} {cat.capitalize()} ",
            bg=color
        )

    def _add_custom_task(self):
        """Validate and add a user-defined task to the pool."""
        title = self.new_task_entry.get().strip()
        cat   = self.new_task_cat.get()

        # ── Validation ────────────────────────────────────────────────────────
        if not title:
            messagebox.showwarning("Ошибка ввода", "Название задачи не может быть пустым!")
            self.new_task_entry.focus_set()
            return
        if len(title) < 3:
            messagebox.showwarning("Ошибка ввода", "Название должно содержать не менее 3 символов.")
            self.new_task_entry.focus_set()
            return
        if any(t["title"].lower() == title.lower() for t in self.tasks):
            messagebox.showwarning("Дубликат", f"Задача «{title}» уже существует.")
            return
        # ─────────────────────────────────────────────────────────────────────

        self.tasks.append({"title": title, "category": cat})
        self.new_task_entry.delete(0, tk.END)
        messagebox.showinfo("Добавлено ✅", f"Задача «{title}» добавлена в категорию «{cat}»!")

    def _refresh_history_list(self):
        """Re-render the history listbox from self.history."""
        self.history_list.delete(0, tk.END)
        for entry in self.history:
            cat   = entry.get("category", "")
            emoji = CATEGORY_EMOJI.get(cat, "•")
            line  = f"{emoji} {entry['time']}  —  {entry['title']}"
            self.history_list.insert(tk.END, line)
        self.counter_label.config(text=f"Всего записей: {len(self.history)}")

    def _clear_history(self):
        if not self.history:
            messagebox.showinfo("История пуста", "История задач уже пуста.")
            return
        if messagebox.askyesno("Подтверждение", "Очистить всю историю?"):
            self.history.clear()
            save_history(self.history)
            self._refresh_history_list()


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = RandomTaskApp()
    app.mainloop()
