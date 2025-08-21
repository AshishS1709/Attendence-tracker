import tkinter as tk
from tkinter import ttk
import math

class AttendanceTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Tracker - Under 25 App")
        self.root.geometry("375x667")  # Mobile-like dimensions
        self.root.configure(bg="#f8fafc")
        
        # Sample data
        self.username = "e/ashish2217"  # Under 25 App Username
        self.overall_attendance = 78
        self.subjects = [
            {"name": "Mathematics", "attendance": 85, "total": 40, "present": 34, "color": "#22c55e"},
            {"name": "Physics", "attendance": 72, "total": 35, "present": 25, "color": "#eab308"},
            {"name": "Chemistry", "attendance": 65, "total": 38, "present": 25, "color": "#f97316"},
            {"name": "Computer Science", "attendance": 90, "total": 32, "present": 29, "color": "#3b82f6"},
            {"name": "English", "attendance": 68, "total": 30, "present": 20, "color": "#ef4444"},
        ]
        
        self.current_view = "home"
        self.create_ui()
    
    def create_ui(self):
        # Main container
        self.main_frame = tk.Frame(self.root, bg="#f8fafc")
        self.main_frame.pack(fill="both", expand=True)
        
        self.show_home_view()
    
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_home_view(self):
        self.clear_frame()
        self.current_view = "home"
        
        # Header
        header_frame = tk.Frame(self.main_frame, bg="#f8fafc", height=80)
        header_frame.pack(fill="x", padx=20, pady=10)
        header_frame.pack_propagate(False)
        
        # Under 25 Logo and Username
        logo_frame = tk.Frame(header_frame, bg="#f8fafc")
        logo_frame.pack(side="left", fill="y")
        
        logo_label = tk.Label(logo_frame, text="U25", bg="#8b5cf6", fg="white", 
                             font=("Arial", 16, "bold"), width=4, height=2)
        logo_label.pack(pady=5)
        
        username_label = tk.Label(logo_frame, text=f"@{self.username}", 
                                 fg="#6b7280", font=("Arial", 10))
        username_label.pack()
        
        # Welcome text
        welcome_frame = tk.Frame(header_frame, bg="#f8fafc")
        welcome_frame.pack(side="right", fill="y")
        
        welcome_label = tk.Label(welcome_frame, text="Hey there! 👋", 
                                fg="#1f2937", font=("Arial", 18, "bold"), bg="#f8fafc")
        welcome_label.pack(anchor="e", pady=10)
        
        # Main attendance circle
        circle_frame = tk.Frame(self.main_frame, bg="#f8fafc", height=250)
        circle_frame.pack(fill="x", padx=20, pady=20)
        circle_frame.pack_propagate(False)
        
        # Create circular progress
        self.create_circular_progress(circle_frame, self.overall_attendance)
        
        # Fun message based on attendance
        message = self.get_attendance_message(self.overall_attendance)
        message_frame = tk.Frame(self.main_frame, bg="#ffffff", relief="solid", bd=1)
        message_frame.pack(fill="x", padx=20, pady=10)
        
        message_label = tk.Label(message_frame, text=message["text"], 
                                fg=message["color"], font=("Arial", 12, "bold"),
                                bg="#ffffff", wraplength=300, justify="center")
        message_label.pack(pady=15)
        
        # Quick stats
        stats_frame = tk.Frame(self.main_frame, bg="#f8fafc")
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        stats_title = tk.Label(stats_frame, text="Quick Stats", 
                              fg="#1f2937", font=("Arial", 16, "bold"), bg="#f8fafc")
        stats_title.pack(anchor="w", pady=(0, 10))
        
        # Subject preview (top 3)
        for i, subject in enumerate(self.subjects[:3]):
            self.create_subject_preview(stats_frame, subject)
        
        # Navigation buttons
        nav_frame = tk.Frame(self.main_frame, bg="#f8fafc", height=80)
        nav_frame.pack(fill="x", side="bottom", padx=20, pady=10)
        nav_frame.pack_propagate(False)
        
        home_btn = tk.Button(nav_frame, text="🏠 Home", bg="#8b5cf6", fg="white",
                            font=("Arial", 12, "bold"), relief="flat", height=2,
                            command=self.show_home_view)
        home_btn.pack(side="left", fill="x", expand=True, padx=2)
        
        subjects_btn = tk.Button(nav_frame, text="📊 Subjects", bg="#6b7280", fg="white",
                               font=("Arial", 12, "bold"), relief="flat", height=2,
                               command=self.show_subjects_view)
        subjects_btn.pack(side="left", fill="x", expand=True, padx=2)
        
        reminders_btn = tk.Button(nav_frame, text="🔔 Alerts", bg="#6b7280", fg="white",
                                font=("Arial", 12, "bold"), relief="flat", height=2,
                                command=self.show_reminders_view)
        reminders_btn.pack(side="left", fill="x", expand=True, padx=2)
    
    def show_subjects_view(self):
        self.clear_frame()
        self.current_view = "subjects"
        
        # Header
        header_frame = tk.Frame(self.main_frame, bg="#f8fafc", height=60)
        header_frame.pack(fill="x", padx=20, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="Subject Breakdown", 
                              fg="#1f2937", font=("Arial", 20, "bold"), bg="#f8fafc")
        title_label.pack(anchor="w")
        
        # Scrollable frame for subjects
        canvas = tk.Canvas(self.main_frame, bg="#f8fafc", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f8fafc")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        
        # Subject cards
        for subject in self.subjects:
            self.create_subject_card(scrollable_frame, subject)
        
        # Navigation
        self.create_bottom_nav()
    
    def show_reminders_view(self):
        self.clear_frame()
        self.current_view = "reminders"
        
        # Header
        header_frame = tk.Frame(self.main_frame, bg="#f8fafc", height=60)
        header_frame.pack(fill="x", padx=20, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="Smart Reminders", 
                              fg="#1f2937", font=("Arial", 20, "bold"), bg="#f8fafc")
        title_label.pack(anchor="w")
        
        # Reminders content
        content_frame = tk.Frame(self.main_frame, bg="#f8fafc")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        reminders = self.generate_smart_reminders()
        
        for i, reminder in enumerate(reminders):
            reminder_frame = tk.Frame(content_frame, bg="#ffffff", relief="solid", bd=1)
            reminder_frame.pack(fill="x", pady=5)
            
            icon_label = tk.Label(reminder_frame, text=reminder["icon"], 
                                 font=("Arial", 16), bg="#ffffff")
            icon_label.pack(side="left", padx=10, pady=10)
            
            text_frame = tk.Frame(reminder_frame, bg="#ffffff")
            text_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)
            
            title_label = tk.Label(text_frame, text=reminder["title"], 
                                  fg="#1f2937", font=("Arial", 12, "bold"), 
                                  bg="#ffffff", anchor="w")
            title_label.pack(fill="x")
            
            desc_label = tk.Label(text_frame, text=reminder["description"], 
                                 fg="#6b7280", font=("Arial", 10), 
                                 bg="#ffffff", anchor="w", wraplength=250)
            desc_label.pack(fill="x")
        
        # Navigation
        self.create_bottom_nav()
    
    def create_circular_progress(self, parent, percentage):
        canvas = tk.Canvas(parent, width=200, height=200, bg="#f8fafc", highlightthickness=0)
        canvas.pack(expand=True)
        
        # Background circle
        canvas.create_oval(50, 50, 150, 150, outline="#e5e7eb", width=8, fill="")
        
        # Progress arc
        extent = (percentage / 100) * 360
        color = self.get_color_by_percentage(percentage)
        canvas.create_arc(50, 50, 150, 150, start=90, extent=-extent, 
                         outline=color, width=8, style="arc")
        
        # Center text
        canvas.create_text(100, 100, text=f"{percentage}%", 
                          font=("Arial", 24, "bold"), fill="#1f2937")
        canvas.create_text(100, 125, text="Overall", 
                          font=("Arial", 12), fill="#6b7280")
    
    def create_subject_preview(self, parent, subject):
        frame = tk.Frame(parent, bg="#ffffff", relief="solid", bd=1, height=50)
        frame.pack(fill="x", pady=2)
        frame.pack_propagate(False)
        
        # Subject name
        name_label = tk.Label(frame, text=subject["name"], 
                             fg="#1f2937", font=("Arial", 12, "bold"), 
                             bg="#ffffff")
        name_label.pack(side="left", padx=10, pady=10)
        
        # Attendance percentage
        perc_label = tk.Label(frame, text=f"{subject['attendance']}%", 
                             fg=subject["color"], font=("Arial", 12, "bold"), 
                             bg="#ffffff")
        perc_label.pack(side="right", padx=10, pady=10)
        
        # Progress bar
        progress_frame = tk.Frame(frame, bg="#ffffff")
        progress_frame.pack(side="right", fill="x", expand=True, padx=10)
        
        progress_bg = tk.Frame(progress_frame, bg="#e5e7eb", height=6)
        progress_bg.pack(fill="x", pady=20)
        
        progress_fill = tk.Frame(progress_bg, bg=subject["color"], height=6)
        progress_fill.place(relwidth=subject["attendance"]/100, relheight=1)
    
    def create_subject_card(self, parent, subject):
        card_frame = tk.Frame(parent, bg="#ffffff", relief="solid", bd=1)
        card_frame.pack(fill="x", pady=10, padx=5)
        
        # Header
        header_frame = tk.Frame(card_frame, bg="#ffffff")
        header_frame.pack(fill="x", padx=15, pady=10)
        
        name_label = tk.Label(header_frame, text=subject["name"], 
                             fg="#1f2937", font=("Arial", 14, "bold"), bg="#ffffff")
        name_label.pack(side="left")
        
        status_label = tk.Label(header_frame, text=self.get_subject_message(subject["attendance"]), 
                               fg=subject["color"], font=("Arial", 12, "bold"), bg="#ffffff")
        status_label.pack(side="right")
        
        # Stats
        stats_frame = tk.Frame(card_frame, bg="#ffffff")
        stats_frame.pack(fill="x", padx=15, pady=5)
        
        attendance_label = tk.Label(stats_frame, text=f"{subject['attendance']}%", 
                                   fg=subject["color"], font=("Arial", 20, "bold"), bg="#ffffff")
        attendance_label.pack(side="left")
        
        details_frame = tk.Frame(stats_frame, bg="#ffffff")
        details_frame.pack(side="right")
        
        present_label = tk.Label(details_frame, text=f"Present: {subject['present']}", 
                                fg="#6b7280", font=("Arial", 10), bg="#ffffff")
        present_label.pack(anchor="e")
        
        total_label = tk.Label(details_frame, text=f"Total: {subject['total']}", 
                              fg="#6b7280", font=("Arial", 10), bg="#ffffff")
        total_label.pack(anchor="e")
        
        # Progress bar
        progress_frame = tk.Frame(card_frame, bg="#ffffff")
        progress_frame.pack(fill="x", padx=15, pady=10)
        
        progress_bg = tk.Frame(progress_frame, bg="#e5e7eb", height=8)
        progress_bg.pack(fill="x")
        
        progress_fill = tk.Frame(progress_bg, bg=subject["color"], height=8)
        progress_fill.place(relwidth=subject["attendance"]/100, relheight=1)
    
    def create_bottom_nav(self):
        nav_frame = tk.Frame(self.main_frame, bg="#f8fafc", height=80)
        nav_frame.pack(fill="x", side="bottom", padx=20, pady=10)
        nav_frame.pack_propagate(False)
        
        buttons = [
            ("🏠 Home", self.show_home_view, "home"),
            ("📊 Subjects", self.show_subjects_view, "subjects"),
            ("🔔 Alerts", self.show_reminders_view, "reminders")
        ]
        
        for text, command, view in buttons:
            bg_color = "#8b5cf6" if self.current_view == view else "#6b7280"
            btn = tk.Button(nav_frame, text=text, bg=bg_color, fg="white",
                           font=("Arial", 12, "bold"), relief="flat", height=2,
                           command=command)
            btn.pack(side="left", fill="x", expand=True, padx=2)
    
    def get_attendance_message(self, percentage):
        if percentage >= 85:
            return {"text": "🎉 You're crushing it! Keep up the amazing work!", "color": "#22c55e"}
        elif percentage >= 75:
            return {"text": "✨ Great job! You're on track for success!", "color": "#3b82f6"}
        elif percentage >= 65:
            return {"text": "⚠️ Getting close to danger zone. Time to step up!", "color": "#eab308"}
        else:
            return {"text": "🚨 Red alert! Your attendance needs immediate attention!", "color": "#ef4444"}
    
    def get_subject_message(self, percentage):
        if percentage >= 85:
            return "Excellent! 🌟"
        elif percentage >= 75:
            return "Good job! 👍"
        elif percentage >= 65:
            return "Need improvement ⚠️"
        else:
            return "Critical! 🚨"
    
    def get_color_by_percentage(self, percentage):
        if percentage >= 85:
            return "#22c55e"  # Green
        elif percentage >= 75:
            return "#3b82f6"  # Blue
        elif percentage >= 65:
            return "#eab308"  # Yellow
        else:
            return "#ef4444"  # Red
    
    def generate_smart_reminders(self):
        reminders = []
        
        # Check for subjects below 75%
        low_attendance = [s for s in self.subjects if s["attendance"] < 75]
        for subject in low_attendance:
            reminders.append({
                "icon": "⚠️",
                "title": f"{subject['name']} Alert",
                "description": f"Your attendance is {subject['attendance']}%. Attend next {3} classes to improve!"
            })
        
        # General motivational reminders
        if self.overall_attendance >= 85:
            reminders.append({
                "icon": "🎯",
                "title": "Maintain Excellence",
                "description": "You're doing great! Keep maintaining this awesome attendance rate."
            })
        elif self.overall_attendance >= 75:
            reminders.append({
                "icon": "📈",
                "title": "Push for Excellence",
                "description": "You're doing well! Try to get above 85% for academic excellence."
            })
        else:
            reminders.append({
                "icon": "🚀",
                "title": "Recovery Mode",
                "description": "Time to focus! Plan your attendance strategy to get back on track."
            })
        
        # Weekly tip
        reminders.append({
            "icon": "💡",
            "title": "Weekly Tip",
            "description": "Set daily reminders 30 minutes before each class to never miss attendance!"
        })
        
        return reminders

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceTrackerApp(root)
    root.mainloop()