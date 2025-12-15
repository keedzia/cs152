import tkinter as tk
from tkinter import messagebox
from expert import RestaurantExpert

class RestaurantExpertGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Your Foodie Expert")
        self.root.geometry("500x600")
        self.root.configure(bg="#fff5f7")
        
        self.expert = None
        self.asked_questions = set()  # track which questions we've asked
        self.show_welcome_screen()
    
    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_welcome_screen(self):
        """Show the initial welcome screen"""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg="#fff5f7")
        frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        title = tk.Label(
            frame,
            text="🍽️ Your Foodie Expert",
            font=("Helvetica", 28, "bold"),
            bg="#fff5f7",
            fg="#d4649a"
        )
        title.pack(pady=10)
        
        subtitle = tk.Label(
            frame,
            text="Finding the perfect place near Esmeralda 920",
            font=("Helvetica", 10),
            bg="#fff5f7",
            fg="#b089a8"
        )
        subtitle.pack(pady=5)
        
        desc = tk.Label(
            frame,
            text="Answer a few questions and we'll recommend the best restaurant for you.",
            font=("Helvetica", 11),
            bg="#fff5f7",
            fg="#a87ab3",
            wraplength=400,
            justify=tk.CENTER
        )
        desc.pack(pady=20)
        
        start_btn = tk.Button(
            frame,
            text="Start",
            font=("Helvetica", 12, "bold"),
            bg="#fff5f7",
            fg="#f5a8d8",
            padx=30,
            pady=10,
            relief=tk.SOLID,
            bd=2,
            borderwidth=2,
            highlightthickness=0,
            activebackground="#fff5f7",
            activeforeground="#f289ca",
            command=self.start_questionnaire
        )
        start_btn.config(bg="#fff5f7", highlightbackground="#f5a8d8", highlightthickness=0)
        start_btn.pack(pady=20)
    
    def start_questionnaire(self):
        """Initialize the expert system and start asking questions"""
        self.expert = RestaurantExpert()
        self.asked_questions = set()
        self.ask_next_question()
    
    def ask_next_question(self):
        """Ask the next question - skip ones we've already asked"""
        if len(self.expert.remaining) <= 1:
            self.show_results()
            return
        
        # list of all possible questions
        questions = [
            ("type", "What type of place?", self.expert.get_available_types),
            ("cuisine", "What cuisine?", self.expert.get_available_cuisines),
            ("meal", "What meal?", self.expert.get_available_meals),
            ("budget", "What's your budget?", self.expert.get_available_budgets),
            ("vibe", "What vibe?", self.expert.get_available_vibes),
            ("distance", "Max distance?", lambda: self._get_distance_options()),
            ("wifi", "Is WiFi important?", self._get_wifi_options),
            ("reservations", "Do you need reservations?", self._get_reservation_options),
            ("group_size", "How many people?", lambda: self._get_group_size_options()),
            ("dietary", "Any dietary restrictions?", self.expert.get_available_dietary),
        ]
        
        # find the next question that has variation
        for q_type, q_text, q_func in questions:
            if q_type in self.asked_questions:
                continue
            
            options = q_func()
            
            # handle special cases
            if q_type == "dietary" and options:
                options = ["Any"] + options
            elif q_type == "wifi" or q_type == "reservations":
                if not options:
                    continue
            
            # ask if there's variation
            if options and len(options) > 1:
                self.ask_multiple_choice(q_text, options, q_type)
                return
            elif q_type == "wifi" or q_type == "reservations":
                # These return tuples, handle specially
                if options:
                    self.ask_multiple_choice(q_text, options, q_type)
                    return
        
        # no more questions with variation
        self.show_results()
    
    def _get_distance_options(self):
        """Get distance options"""
        min_dist, max_dist = self.expert.get_distance_range()
        if not max_dist or (max_dist - (min_dist or 0)) < 0.1:
            return []
        
        options = []
        self.distance_map = {}
        
        if max_dist and max_dist <= 2:
            options.append('short (0-2km)')
            self.distance_map['short (0-2km)'] = 2
        else:
            options.append('short (0-2km)')
            self.distance_map['short (0-2km)'] = 2
            options.append('medium (2-5km)')
            self.distance_map['medium (2-5km)'] = 5
            if max_dist and max_dist > 5:
                options.append('long (>5km)')
                self.distance_map['long (>5km)'] = 100
        
        return options if len(options) > 1 else []
    
    def _get_wifi_options(self):
        """Get WiFi options"""
        has_wifi, has_no_wifi = self.expert.check_wifi_options()
        if has_wifi and has_no_wifi:
            return ['Yes', "Doesn't matter"]
        return []
    
    def _get_reservation_options(self):
        """Get reservation options"""
        has_res, has_no_res = self.expert.check_reservation_options()
        if has_res and has_no_res:
            return ['Yes', "Doesn't matter"]
        return []
    
    def _get_group_size_options(self):
        """Get group size options"""
        min_size, max_size = self.expert.get_group_size_range()
        if not max_size:
            return []
        
        options = []
        self.size_map = {}
        
        if max_size >= 1:
            options.append('Solo')
            self.size_map['Solo'] = 1
        if max_size >= 6:
            options.append('Small (2-6)')
            self.size_map['Small (2-6)'] = 6
        if max_size >= 7:
            options.append('Large (7+)')
            self.size_map['Large (7+)'] = 7
        
        return options if len(options) > 1 else []
    
    def ask_multiple_choice(self, question, options, question_type):
        """Display a multiple choice question"""
        self.clear_window()
        
        # main container
        main_frame = tk.Frame(self.root, bg="#fff5f7")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=15, pady=15)
        
        # top section with question and restart button
        top_frame = tk.Frame(main_frame, bg="#fff5f7")
        top_frame.pack(fill=tk.X, pady=(0, 20))
        
        # question text with match count
        question_label = tk.Label(
            top_frame,
            text=f"Current matches: {len(self.expert.remaining)}\n{question}",
            font=("Helvetica", 14, "bold"),
            bg="#fff5f7",
            fg="#d4649a",
            wraplength=350,
            justify=tk.CENTER
        )
        question_label.pack(side=tk.LEFT, expand=True)
        
        # restart button on the right
        restart_btn = tk.Button(
            top_frame,
            text="Restart",
            font=("Helvetica", 9, "bold"),
            bg="#f5a8d8",
            fg="#d4649a",
            relief=tk.SOLID,
            bd=2,
            padx=12,
            pady=8,
            command=self.show_welcome_screen,
            highlightthickness=0,
            activebackground="#f289ca",
            activeforeground="#d4649a"
        )
        restart_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # scrollable options frame
        canvas_frame = tk.Frame(main_frame, bg="#fff5f7")
        canvas_frame.pack(expand=True, fill=tk.BOTH)
        
        canvas = tk.Canvas(canvas_frame, bg="#fff5f7", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
        options_frame = tk.Frame(canvas, bg="#fff5f7")
        
        options_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=options_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # create buttons for each option
        for option in options:
            btn = tk.Button(
                options_frame,
                text=option,
                font=("Helvetica", 13, "bold"),
                bg="#fff5f7",
                fg="#d4649a",
                padx=20,
                pady=15,
                relief=tk.SOLID,
                bd=2,
                activebackground="#f8bbd0",
                activeforeground="#d4649a",
                highlightthickness=0,
                highlightbackground="#d4649a",
                command=lambda opt=option: self.handle_answer(opt, question_type)
            )
            btn.pack(fill=tk.X, pady=10)
        
        canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # enable scrolling with mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def handle_answer(self, answer, question_type):
        """Process the user's answer"""
        # mark this question as asked
        self.asked_questions.add(question_type)
        
        try:
            if question_type == "type":
                self.expert.filter_by_type(answer)
            elif question_type == "meal":
                self.expert.filter_by_meal(answer)
            elif question_type == "cuisine":
                self.expert.filter_by_cuisine(answer)
            elif question_type == "budget":
                self.expert.filter_by_budget(answer)
            elif question_type == "distance":
                self.expert.filter_by_distance(self.distance_map[answer])
            elif question_type == "vibe":
                self.expert.filter_by_vibe(answer)
            elif question_type == "wifi":
                if answer == 'Yes':
                    self.expert.filter_by_wifi('yes')
            elif question_type == "reservations":
                if answer == 'Yes':
                    self.expert.filter_by_reservations('yes')
            elif question_type == "group_size":
                self.expert.filter_by_group_size(self.size_map[answer])
            elif question_type == "dietary":
                if answer == 'Any':
                    self.expert.filter_by_dietary('any')
                else:
                    self.expert.filter_by_dietary(answer)
        except Exception as e:
            print(f"Error filtering: {e}")
            messagebox.showerror("Error", f"Error processing answer: {str(e)}")
            return
        
        # check if we still have results
        if len(self.expert.remaining) == 0:
            messagebox.showwarning("No Match", "No restaurants match that selection. Starting over...")
            self.show_welcome_screen()
            return
        
        # continue to next question
        self.ask_next_question()
    
    def show_results(self):
        """Show the final results"""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg="#fff5f7")
        frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        if len(self.expert.remaining) == 0:
            title = tk.Label(
                frame,
                text="Sorry!",
                font=("Helvetica", 24, "bold"),
                bg="#fff5f7",
                fg="#f5a8d8"
            )
            title.pack(pady=10)
            
            msg = tk.Label(
                frame,
                text="No places match your criteria.",
                font=("Helvetica", 12),
                bg="#fff5f7",
                fg="#a87ab3"
            )
            msg.pack(pady=10)
        
        elif len(self.expert.remaining) == 1:
            title = tk.Label(
                frame,
                text="✨ Perfect Match!",
                font=("Helvetica", 24, "bold"),
                bg="#fff5f7",
                fg="#f5a8d8"
            )
            title.pack(pady=10)
            
            recommendation = tk.Label(
                frame,
                text=self.expert.remaining[0],
                font=("Helvetica", 16, "bold"),
                bg="#fff5f7",
                fg="#d4649a",
                padx=20,
                pady=15,
                relief=tk.SOLID,
                bd=2
            )
            recommendation.pack(fill=tk.X, pady=20)
        
        else:
            title = tk.Label(
                frame,
                text="Great Options:",
                font=("Helvetica", 24, "bold"),
                bg="#fff5f7",
                fg="#f5a8d8"
            )
            title.pack(pady=10)
            
            # ccrollable recommendations
            canvas = tk.Canvas(frame, bg="#fff5f7", highlightthickness=0)
            scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#fff5f7")
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            for place in self.expert.remaining:
                rec = tk.Label(
                    scrollable_frame,
                    text=place,
                    font=("Helvetica", 11),
                    bg="#fff5f7",
                    fg="#d4649a",
                    padx=15,
                    pady=10,
                    relief=tk.SOLID,
                    bd=2
                )
                rec.pack(fill=tk.X, pady=6)
            
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # restart button
        restart_btn = tk.Button(
            frame,
            text="← Start Over",
            font=("Helvetica", 11, "bold"),
            bg="#f5a8d8",
            fg="#d4649a",
            padx=20,
            pady=10,
            relief=tk.SOLID,
            bd=2,
            activebackground="#f289ca",
            activeforeground="#d4649a",
            highlightthickness=0,
            command=self.show_welcome_screen
        )
        restart_btn.pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    gui = RestaurantExpertGUI(root)
    root.mainloop()