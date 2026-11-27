import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont

class ClearanceFlowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ClearanceFlow - School Clearance System")
        self.root.geometry("1200x750")
        self.root.configure(bg="#F5F7FA")
        self.root.minsize(1000, 650)

        # Colors
        self.bg_color = "#F5F7FA"
        self.sidebar_bg = "#FFFFFF"
        self.card_bg = "#FFFFFF"
        self.primary = "#3B82F6"
        self.success = "#22C55E"
        self.warning = "#F59E0B"
        self.danger = "#EF4444"
        self.text_dark = "#1E293B"
        self.text_muted = "#64748B"
        self.border = "#E2E8F0"

        self.setup_fonts()
        self.create_layout()
        self.show_dashboard()   # Start on Dashboard

    def setup_fonts(self):
        self.font_title = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.font_heading = tkfont.Font(family="Segoe UI", size=14, weight="bold")
        self.font_sub = tkfont.Font(family="Segoe UI", size=11)
        self.font_small = tkfont.Font(family="Segoe UI", size=10)
        self.font_bold = tkfont.Font(family="Segoe UI", size=11, weight="bold")

    def create_layout(self):
        # ========== SIDEBAR ==========
        self.sidebar = tk.Frame(self.root, bg=self.sidebar_bg, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo
        logo_frame = tk.Frame(self.sidebar, bg=self.sidebar_bg)
        logo_frame.pack(fill="x", pady=(25, 30), padx=20)

        tk.Label(logo_frame, text="ClearanceFlow",
                 font=tkfont.Font(family="Segoe UI", size=16, weight="bold"),
                 bg=self.sidebar_bg, fg=self.primary).pack(anchor="w")

        # Navigation buttons with commands
        self.nav_items = [
            ("🏠  Dashboard", self.show_dashboard),
            ("📋  My Clearance", self.show_my_clearance),
            ("🏢  Departments", self.show_departments),
            ("🕒  History", self.show_history),
            ("👤  Profile", self.show_profile),
        ]

        self.nav_buttons = []
        for text, command in self.nav_items:
            btn = tk.Button(self.sidebar, text=text, font=self.font_sub,
                            bg=self.sidebar_bg, fg=self.text_dark,
                            bd=0, relief="flat", anchor="w", padx=20, pady=12,
                            cursor="hand2", activebackground="#DBEAFE",
                            command=command)
            btn.pack(fill="x", padx=10, pady=2)
            self.nav_buttons.append(btn)

        # Help box
        help_frame = tk.Frame(self.sidebar, bg="#ECFDF5", padx=15, pady=15)
        help_frame.pack(side="bottom", fill="x", padx=15, pady=20)

        tk.Label(help_frame, text="Need Help?", font=self.font_bold,
                 bg="#ECFDF5", fg="#065F46").pack(anchor="w")
        tk.Label(help_frame, text="Check our FAQ or contact\nsupport for assistance.",
                 font=self.font_small, bg="#ECFDF5", fg="#047857",
                 justify="left").pack(anchor="w", pady=(5, 8))
        
        tk.Button(help_frame, text="Go to FAQ →", font=self.font_small,
                  bg="#ECFDF5", fg="#059669", bd=0, cursor="hand2",
                  activebackground="#D1FAE5",
                  command=self.open_faq).pack(anchor="w")

        # ========== MAIN AREA ==========
        self.main = tk.Frame(self.root, bg=self.bg_color)
        self.main.pack(side="left", fill="both", expand=True)

        # Header
        self.header = tk.Frame(self.main, bg=self.bg_color, height=70)
        self.header.pack(fill="x", padx=30, pady=(20, 10))
        self.header.pack_propagate(False)

        self.page_title = tk.Label(self.header, text="Dashboard", font=self.font_title,
                                   bg=self.bg_color, fg=self.text_dark)
        self.page_title.pack(side="left")

        # Student info + Logout
        student_frame = tk.Frame(self.header, bg=self.bg_color)
        student_frame.pack(side="right")

        tk.Label(student_frame, text="Alex Rivera  •  ID 2024-0847",
                 font=self.font_sub, bg=self.bg_color, fg=self.text_muted).pack(side="left", padx=(0, 15))

        tk.Button(student_frame, text="Logout", font=self.font_small,
                  bg="#FEE2E2", fg="#B91C1C", bd=0, padx=12, pady=6,
                  cursor="hand2", relief="flat",
                  command=self.logout).pack(side="left")

        # Content container (we will clear and rebuild this)
        self.content = tk.Frame(self.main, bg=self.bg_color)
        self.content.pack(fill="both", expand=True, padx=30, pady=10)

    # ========== HELPER: Clear content ==========
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def set_active_nav(self, index):
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.configure(bg="#EFF6FF", fg=self.primary)
            else:
                btn.configure(bg=self.sidebar_bg, fg=self.text_dark)

    # ========== PAGES ==========
    def show_dashboard(self):
        self.clear_content()
        self.page_title.config(text="Dashboard")
        self.set_active_nav(0)

        # Left column
        left_col = tk.Frame(self.content, bg=self.bg_color)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 15))

        # Progress Card
        progress_card = tk.Frame(left_col, bg=self.card_bg, padx=25, pady=20,
                                 highlightbackground=self.border, highlightthickness=1)
        progress_card.pack(fill="x", pady=(0, 15))

        tk.Label(progress_card, text="Overall Clearance", font=self.font_heading,
                 bg=self.card_bg, fg=self.text_dark).pack(anchor="w")

        prog_frame = tk.Frame(progress_card, bg=self.card_bg)
        prog_frame.pack(fill="x", pady=15)

        progress = ttk.Progressbar(prog_frame, orient="horizontal", length=300,
                                   mode="determinate", value=68)
        progress.pack(side="left", fill="x", expand=True)

        tk.Label(prog_frame, text="68%", font=tkfont.Font(family="Segoe UI", size=16, weight="bold"),
                 bg=self.card_bg, fg=self.success).pack(side="left", padx=(15, 0))

        tk.Label(progress_card, text="You're making good progress!\n2 of 4 departments have cleared you.",
                 font=self.font_sub, bg=self.card_bg, fg=self.text_muted,
                 justify="left").pack(anchor="w")

        # Department Status
        dept_card = tk.Frame(left_col, bg=self.card_bg, padx=25, pady=20,
                             highlightbackground=self.border, highlightthickness=1)
        dept_card.pack(fill="x", pady=(0, 15))

        header_row = tk.Frame(dept_card, bg=self.card_bg)
        header_row.pack(fill="x")
        tk.Label(header_row, text="Department Status", font=self.font_heading,
                 bg=self.card_bg, fg=self.text_dark).pack(side="left")
        tk.Button(header_row, text="View All", font=self.font_small,
                  bg=self.card_bg, fg=self.primary, bd=0, cursor="hand2",
                  command=self.show_departments).pack(side="right")

        departments = [
            ("📚  Library", "Cleared", self.success),
            ("💰  Finance", "Pending", self.warning),
            ("🎓  Academics", "In Review", self.primary),
            ("🏠  Hostel", "Not Started", self.text_muted),
        ]

        for name, status, color in departments:
            row = tk.Frame(dept_card, bg=self.card_bg)
            row.pack(fill="x", pady=8)
            tk.Label(row, text=name, font=self.font_sub,
                     bg=self.card_bg, fg=self.text_dark).pack(side="left")
            tk.Label(row, text=status, font=self.font_small,
                     bg=color, fg="white", padx=10, pady=3).pack(side="right")

        # Clearance Flow
        flow_card = tk.Frame(left_col, bg=self.card_bg, padx=25, pady=20,
                             highlightbackground=self.border, highlightthickness=1)
        flow_card.pack(fill="x")

        tk.Label(flow_card, text="Clearance Flow", font=self.font_heading,
                 bg=self.card_bg, fg=self.text_dark).pack(anchor="w", pady=(0, 15))

        steps = [
            ("1. Submit Request", "Submit your clearance request to begin the process.", True),
            ("2. Department Review", "Your request is being reviewed by the relevant departments.", False),
            ("3. Final Approval", "Awaiting final approval from the clearance committee.", False),
            ("4. Certificate Ready", "Your clearance certificate will be generated and available for download.", False),
        ]

        for title, desc, current in steps:
            step_frame = tk.Frame(flow_card, bg=self.card_bg)
            step_frame.pack(fill="x", pady=6)

            tk.Label(step_frame, text="●", font=("Segoe UI", 14),
                     bg=self.card_bg, fg=self.primary if current else self.border).pack(side="left", padx=(0, 12))

            text_frame = tk.Frame(step_frame, bg=self.card_bg)
            text_frame.pack(side="left", fill="x")

            tk.Label(text_frame, text=title, font=self.font_bold,
                     bg=self.card_bg, fg=self.primary if current else self.text_dark).pack(anchor="w")
            tk.Label(text_frame, text=desc, font=self.font_small,
                     bg=self.card_bg, fg=self.text_muted).pack(anchor="w")

        # Right column - Pending Actions
        right_col = tk.Frame(self.content, bg=self.bg_color, width=320)
        right_col.pack(side="right", fill="y")
        right_col.pack_propagate(False)

        pending_card = tk.Frame(right_col, bg=self.card_bg, padx=20, pady=20,
                                highlightbackground=self.border, highlightthickness=1)
        pending_card.pack(fill="both", expand=True)

        title_row = tk.Frame(pending_card, bg=self.card_bg)
        title_row.pack(fill="x", pady=(0, 15))
        tk.Label(title_row, text="Pending Actions", font=self.font_heading,
                 bg=self.card_bg, fg=self.text_dark).pack(side="left")
        tk.Label(title_row, text="⚠", font=("Segoe UI", 14),
                 bg=self.card_bg, fg=self.warning).pack(side="right")

        pending_items = [
            ("Fee Payment Outstanding", "You have an outstanding balance of ₦15,750.00", "Upload Document", self.warning),
            ("Academic Transcript", "Please upload your signed course form.", "Upload Document", self.primary),
            ("Hostel Clearance", "Start your hostel clearance process.", "Start Process", self.text_muted),
        ]

        for title, desc, btn_text, color in pending_items:
            item = tk.Frame(pending_card, bg="#F8FAFC", padx=15, pady=12,
                            highlightbackground=self.border, highlightthickness=1)
            item.pack(fill="x", pady=8)

            tk.Label(item, text=title, font=self.font_bold,
                     bg="#F8FAFC", fg=self.text_dark).pack(anchor="w")
            tk.Label(item, text=desc, font=self.font_small,
                     bg="#F8FAFC", fg=self.text_muted, wraplength=250,
                     justify="left").pack(anchor="w", pady=(4, 10))

            btn_frame = tk.Frame(item, bg="#F8FAFC")
            btn_frame.pack(fill="x")

            tk.Button(btn_frame, text=btn_text, font=self.font_small,
                      bg=color, fg="white", bd=0, padx=12, pady=5,
                      cursor="hand2", relief="flat",
                      command=lambda t=title: self.handle_action(t)).pack(side="left")

            tk.Button(btn_frame, text="View Details", font=self.font_small,
                      bg="#E2E8F0", fg=self.text_dark, bd=0, padx=12, pady=5,
                      cursor="hand2", relief="flat",
                      command=lambda t=title: self.view_details(t)).pack(side="left", padx=(8, 0))

        tk.Label(pending_card,
                 text="ℹ  All pending items must be completed\nto finish your clearance.",
                 font=self.font_small, bg=self.card_bg, fg=self.text_muted,
                 justify="left").pack(side="bottom", anchor="w", pady=(20, 0))

    def show_my_clearance(self):
        self.clear_content()
        self.page_title.config(text="My Clearance")
        self.set_active_nav(1)

        card = tk.Frame(self.content, bg=self.card_bg, padx=30, pady=30,
                        highlightbackground=self.border, highlightthickness=1)
        card.pack(fill="both", expand=True)

        tk.Label(card, text="My Clearance Details", font=self.font_heading,
                 bg=self.card_bg, fg=self.text_dark).pack(anchor="w", pady=(0, 20))

        info = [
            ("Student Name", "Alex Rivera"),
            ("Student ID", "2024-0847"),
            ("Programme", "B.Sc Computer Science"),
            ("Level", "400 Level"),
            ("Overall Status", "In Progress (68%)"),
        ]

        for label, value in info:
            row = tk.Frame(card, bg=self.card_bg)
            row.pack(fill="x", pady=8)
            tk.Label(row, text=label + ":", font=self.font_bold, width=18, anchor="w",
                     bg=self.card_bg, fg=self.text_muted).pack(side="left")
            tk.Label(row, text=value, font=self.font_sub,
                     bg=self.card_bg, fg=self.text_dark).pack(side="left")

        tk.Button(card, text="Download Clearance Certificate (when ready)",
                  font=self.font_sub, bg=self.primary, fg="white",
                  bd=0, padx=20, pady=10, cursor="hand2",
                  command=self.download_certificate).pack(pady=30)

    def show_departments(self):
        self.clear_content()
        self.page_title.config(text="Departments")
        self.set_active_nav(2)

        card = tk.Frame(self.content, bg=self.card_bg, padx=30, pady=30,
                        highlightbackground=self.border, highlightthickness=1)
        card.pack(fill="both", expand=True)

        tk.Label(card, text="Department Clearance Status", font=self.font_heading,
                 bg=self.card_bg, fg=self.text_dark).pack(anchor="w", pady=(0, 20))

        departments = [
            ("Library", "Cleared", "No outstanding books", self.success),
            ("Finance", "Pending", "Outstanding balance: ₦15,750", self.warning),
            ("Academics", "In Review", "Waiting for HOD approval", self.primary),
            ("Hostel", "Not Started", "Please start the process", self.text_muted),
            ("Sports", "Cleared", "Sports fee paid", self.success),
            ("Student Affairs", "Cleared", "No issues", self.success),
        ]

        for name, status, note, color in departments:
            row = tk.Frame(card, bg="#F8FAFC", padx=15, pady=12,
                           highlightbackground=self.border, highlightthickness=1)
            row.pack(fill="x", pady=6)

            tk.Label(row, text=name, font=self.font_bold, width=18, anchor="w",
                     bg="#F8FAFC", fg=self.text_dark).pack(side="left")
            tk.Label(row, text=status, font=self.font_small,
                     bg=color, fg="white", padx=10, pady=3).pack(side="left", padx=10)
            tk.Label(row, text=note, font=self.font_small,
                     bg="#F8FAFC", fg=self.text_muted).pack(side="left")

            tk.Button(row, text="View", font=self.font_small,
                      bg="#E2E8F0", fg=self.text_dark, bd=0, padx=12, pady=4,
                      cursor="hand2",
                      command=lambda n=name: self.view_details(n)).pack(side="right")

    def show_history(self):
        self.clear_content()
        self.page_title.config(text="History")
        self.set_active_nav(3)

        card = tk.Frame(self.content, bg=self.card_bg, padx=30, pady=30,
                        highlightbackground=self.border, highlightthickness=1)
        card.pack(fill="both", expand=True)

        tk.Label(card, text="Clearance History", font=self.font_heading,
                 bg=self.card_bg, fg=self.text_dark).pack(anchor="w", pady=(0, 20))

        history = [
            ("12 Nov 2026", "Submitted clearance request", "Completed"),
            ("13 Nov 2026", "Library clearance approved", "Completed"),
            ("13 Nov 2026", "Sports clearance approved", "Completed"),
            ("14 Nov 2026", "Finance review started", "In Progress"),
        ]

        for date, action, status in history:
            row = tk.Frame(card, bg="#F8FAFC", padx=15, pady=10,
                           highlightbackground=self.border, highlightthickness=1)
            row.pack(fill="x", pady=5)

            tk.Label(row, text=date, font=self.font_small, width=14, anchor="w",
                     bg="#F8FAFC", fg=self.text_muted).pack(side="left")
            tk.Label(row, text=action, font=self.font_sub,
                     bg="#F8FAFC", fg=self.text_dark).pack(side="left", padx=10)
            tk.Label(row, text=status, font=self.font_small,
                     bg=self.success if status == "Completed" else self.warning,
                     fg="white", padx=8, pady=2).pack(side="right")

    def show_profile(self):
        self.clear_content()
        self.page_title.config(text="Profile")
        self.set_active_nav(4)

        card = tk.Frame(self.content, bg=self.card_bg, padx=30, pady=30,
                        highlightbackground=self.border, highlightthickness=1)
        card.pack(fill="both", expand=True)

        tk.Label(card, text="Student Profile", font=self.font_heading,
                 bg=self.card_bg, fg=self.text_dark).pack(anchor="w", pady=(0, 20))

        fields = [
            ("Full Name", "Alex Rivera"),
            ("Student ID", "2024-0847"),
            ("Email", "alex.rivera@school.edu"),
            ("Phone", "+234 801 234 5678"),
            ("Department", "Computer Science"),
            ("Level", "400 Level"),
        ]

        for label, value in fields:
            row = tk.Frame(card, bg=self.card_bg)
            row.pack(fill="x", pady=10)
            tk.Label(row, text=label + ":", font=self.font_bold, width=15, anchor="w",
                     bg=self.card_bg, fg=self.text_muted).pack(side="left")
            tk.Label(row, text=value, font=self.font_sub,
                     bg=self.card_bg, fg=self.text_dark).pack(side="left")

        tk.Button(card, text="Edit Profile", font=self.font_sub,
                  bg=self.primary, fg="white", bd=0, padx=20, pady=10,
                  cursor="hand2", command=self.edit_profile).pack(pady=20)

    # ========== BUTTON COMMANDS ==========
    def handle_action(self, title):
        messagebox.showinfo("Action", f"Opening action for:\n\n{title}\n\n(This would open upload form or process)")

    def view_details(self, title):
        messagebox.showinfo("Details", f"Viewing details for:\n\n{title}")

    def download_certificate(self):
        messagebox.showwarning("Not Ready", "Your clearance is not yet 100% complete.\nCertificate will be available after final approval.")

    def open_faq(self):
        messagebox.showinfo("FAQ", "FAQ page would open here.\n\nCommon questions about clearance process.")

    def edit_profile(self):
        messagebox.showinfo("Edit Profile", "Profile editing form would open here.")

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            messagebox.showinfo("Logged Out", "You have been logged out successfully.")
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ClearanceFlowApp(root)
    root.mainloop()