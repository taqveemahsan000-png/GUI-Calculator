#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox as messagebox
from math import (
    sin, cos, tan, sqrt, log, log10, factorial, pi, e, radians, degrees
)

class CalculatorApplication:
    def __init__(self, root_window: tk.Tk) -> None:
        self.root = root_window
        self.root.title("Python GUI Calculator")
        self.root.geometry("400x600")
        self.root.resizable(True, True)

        self.is_degree_mode = tk.BooleanVar(value=True)
        self.input_text = tk.StringVar(value="")

        self._build_ui()
        self._configure_key_bindings()

    def _build_ui(self) -> None:
        display_frame = tk.Frame(self.root, padx=10, pady=10)
        display_frame.pack(fill="x")

        display_entry = tk.Entry(
            display_frame,
            textvariable=self.input_text,
            font=("Consolas", 20),
            justify="right",
            relief="groove",
            bd=3
        )
        display_entry.pack(fill="x", side="left", expand=True)

        scrollbar = tk.Scrollbar(display_frame, orient="horizontal", command=display_entry.xview)
        scrollbar.pack(side="bottom", fill="x")
        display_entry.config(xscrollcommand=scrollbar.set)

        mode_frame = tk.Frame(self.root, padx=10)
        mode_frame.pack(fill="x", pady=(0, 8))

        degree_toggle = tk.Checkbutton(
            mode_frame,
            text="Degree Mode",
            variable=self.is_degree_mode,
            onvalue=True,
            offvalue=False
        )
        degree_toggle.pack(anchor="w")

        buttons_frame = tk.Frame(self.root, padx=10, pady=10)
        buttons_frame.pack(fill="both", expand=True)

        button_layout = [
            ["C", "⌫", "(", ")", "÷"],
            ["7", "8", "9", "×", "√"],
            ["4", "5", "6", "-", "x²"],
            ["1", "2", "3", "+", "±"],
            ["0", ".", "π", "e", "="],
            ["sin", "cos", "tan", "log", "ln"],
        ]

        for row_index, row in enumerate(button_layout):
            row_frame = tk.Frame(buttons_frame)
            row_frame.pack(fill="x", pady=4, expand=True)
            for col_index, label in enumerate(row):
                button = tk.Button(
                    row_frame,
                    text=label,
                    font=("Inter", 14, "bold"),
                    width=6,
                    height=2,
                    relief="raised",
                    bd=2,
                    command=lambda l=label: self._on_button_press(l)
                )
                button.grid(row=0, column=col_index, padx=3, sticky="nsew")
                row_frame.grid_columnconfigure(col_index, weight=1)

    def _configure_key_bindings(self) -> None:
        self.root.bind("<Return>", lambda event: self._evaluate_expression())
        self.root.bind("<KP_Enter>", lambda event: self._evaluate_expression())
        self.root.bind("<BackSpace>", lambda event: self._handle_backspace())
        self.root.bind("<Escape>", lambda event: self._clear_input())
        self.root.bind("<Key>", self._handle_text_key)

    def _on_button_press(self, label: str) -> None:
        if label == "C":
            self._clear_input()
        elif label == "⌫":
            self._handle_backspace()
        elif label == "=":
            self._evaluate_expression()
        elif label == "√":
            self._insert_text("sqrt(")
        elif label == "x²":
            self._insert_text("**2")
        elif label == "±":
            self._toggle_sign()
        elif label == "÷":
            self._insert_text("/")
        elif label == "×":
            self._insert_text("*")
        elif label == "π":
            self._insert_text("pi")
        elif label == "e":
            self._insert_text("e")
        elif label in ("sin", "cos", "tan", "log", "ln"):
            mapping = {"ln": "log"}
            func_name = mapping.get(label, label)
            self._insert_text(f"{func_name}(")
        else:
            self._insert_text(label)

    def _handle_text_key(self, event: tk.Event) -> None:
        allowed_chars = "0123456789.+-*/()^"
        if event.char in allowed_chars:
            self._insert_text("^" if event.char == "^" else event.char)
        elif event.char.lower() in ("s", "c", "t", "l"):
            pass
        else:
            return

    def _insert_text(self, text: str) -> None:
        self.input_text.set(self.input_text.get() + text)

    def _clear_input(self) -> None:
        self.input_text.set("")

    def _handle_backspace(self) -> None:
        current = self.input_text.get()
        self.input_text.set(current[:-1])

    def _toggle_sign(self) -> None:
        expr = self.input_text.get()
        if not expr:
            return
        self.input_text.set(f"(-1)*({expr})")

    def _evaluate_expression(self) -> None:
        raw_expr = self.input_text.get()
        if not raw_expr.strip():
            return

        expr = raw_expr.replace("√", "sqrt")
        expr = expr.replace("^", "**")
        safe_env = self._build_safe_environment()

        try:
            result = eval(expr, {"__builtins__": None}, safe_env)
            self.input_text.set(str(result))
        except ZeroDivisionError:
            messagebox.showerror("Math Error", "Division by zero is undefined.")
        except Exception as error:
            messagebox.showerror("Error", f"Invalid expression:\n{error}")

    def _build_safe_environment(self) -> dict:
        if self.is_degree_mode.get():
            def sin_deg(x):
                return sin(radians(x))

            def cos_deg(x):
                return cos(radians(x))

            def tan_deg(x):
                return tan(radians(x))

            trig_map = {"sin": sin_deg, "cos": cos_deg, "tan": tan_deg}
        else:
            trig_map = {"sin": sin, "cos": cos, "tan": tan}

        env = {
            "sqrt": sqrt,
            "log": log,
            "log10": log10,
            "factorial": factorial,
            "pi": pi,
            "e": e,
            "radians": radians,
            "degrees": degrees,
            **trig_map,
        }
        return env

def main() -> None:
    root = tk.Tk()
    app = CalculatorApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()
