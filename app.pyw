import ctypes
import locale
import tkinter as tk
from datetime import date, datetime
from tkinter import font

import ttkbootstrap as ttk
from ttkbootstrap import widgets

import model


class View(ttk.Window):
    def __init__(self, presenter: "Presenter"):
        super().__init__(resizable=(False, False), iconphoto="icon.png")

        self.presenter = presenter

        self.effort = tk.DoubleVar()
        self.capacity = tk.DoubleVar(value=1)
        self.duration = tk.DoubleVar()
        self.start_date = tk.StringVar()
        self.end_date = tk.StringVar()

        self._configure()

        self._frame = ttk.Frame(self, padding=10)
        self._frame.grid()
        self._frame.grid_rowconfigure((0, 1, 2), pad=5)
        self._frame.grid_columnconfigure(1, pad=20)
        self._frame.grid_columnconfigure(2, pad=30)

        self._init_effort_widgets()
        self._init_capa_widgets()
        self._init_duration_widgets()
        self._init_fixed_dates_widgets()

    def _configure(self):
        self.title("Aufwand - Dauer - Kapa")
        font.nametofont("TkDefaultFont")["size"] = 11
        font.nametofont("TkTextFont")["size"] = 11

    def _init_effort_widgets(self):
        ttk.Label(self._frame, text="Aufwand (in PT)").grid(
            row=0, column=0, sticky=tk.E
        )
        ttk.Spinbox(
            self._frame,
            textvariable=self.effort,
            width=7,
            from_=0.0,
            to=1000.0,
            increment=0.5,
        ).grid(row=0, column=1, sticky=tk.W)
        ttk.Button(
            self._frame, text="Berechnen", command=self.presenter.calc_effort
        ).grid(row=0, column=2)

    def _init_capa_widgets(self):
        ttk.Label(self._frame, text="Kapa (in FTE)").grid(row=1, column=0, sticky=tk.E)
        ttk.Spinbox(
            self._frame,
            textvariable=self.capacity,
            width=7,
            from_=0.1,
            to=5.0,
            increment=0.1,
        ).grid(row=1, column=1, sticky=tk.W)
        ttk.Button(
            self._frame, text="Berechnen", command=self.presenter.calc_capa
        ).grid(row=1, column=2)

    def _init_duration_widgets(self):
        ttk.Label(self._frame, text="Dauer (in Tagen)").grid(
            row=2, column=0, sticky=tk.E
        )
        ttk.Spinbox(
            self._frame,
            textvariable=self.duration,
            width=7,
            from_=0,
            to=500,
            increment=1,
        ).grid(row=2, column=1, sticky=tk.W)
        ttk.Button(
            self._frame, text="Berechnen", command=self.presenter.calc_duration
        ).grid(row=2, column=2)

    def _init_fixed_dates_widgets(self):
        data_frame = ttk.LabelFrame(self._frame, text="Festes Datum", height=50)
        data_frame.columnconfigure(1, pad=20)
        data_frame.grid(row=3, column=0, columnspan=3, ipadx=5, ipady=10, pady=(30, 10))

        ttk.Label(data_frame, text="Start-Datum").grid(row=0, column=0, sticky=tk.E)
        start_date_entry = widgets.DateEntry(data_frame, firstweekday=0)
        start_date_entry.entry["textvariable"] = self.start_date
        start_date_entry.grid(row=0, column=1, sticky=tk.E)

        ttk.Label(data_frame, text="End-Datum").grid(row=1, column=0, sticky=tk.E)
        end_date_entry = widgets.DateEntry(data_frame, firstweekday=0)
        end_date_entry.entry["textvariable"] = self.end_date
        end_date_entry.grid(row=1, column=1, sticky=tk.E)

        ttk.Button(
            data_frame,
            text="Arbeitstage übertragen",
            command=self.presenter.calc_working_days_in_date_range,
        ).grid(row=2, column=1, sticky=tk.E, pady=10)


class Presenter:
    def __init__(self):
        self.view: View

    def calc_effort(self):
        effort = model.calc_effort(
            duration_in_days=self.view.duration.get(),
            capacity_in_fte=self.view.capacity.get(),
        )
        self.view.effort.set(round(effort, 2))

    def calc_capa(self):
        capa = model.calc_capacity(
            effort_in_pd=self.view.effort.get(),
            duration_in_days=self.view.duration.get(),
        )
        self.view.capacity.set(round(capa, 2))

    def calc_duration(self):
        duration = model.calc_duration(
            effort_in_pd=self.view.effort.get(),
            capacity_in_fte=self.view.capacity.get(),
        )
        self.view.duration.set(round(duration, 2))

    def calc_working_days_in_date_range(self):
        from_ = datetime.strptime(self.view.start_date.get(), "%x").date()
        to = datetime.strptime(self.view.end_date.get(), "%x").date()
        duration = model.count_workdays(from_, to)
        self.view.duration.set(duration)


def main():
    locale.setlocale(locale.LC_NUMERIC, "en")
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Planning")
    presenter = Presenter()
    view = View(presenter)
    presenter.view = view
    view.mainloop()


if __name__ == "__main__":
    main()
