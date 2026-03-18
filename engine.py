import tkinter as tk
import math

class SanctuaryEngine:
    def __init__(self, root):
        self.root = root
        self.lang = "JP" 
        self.show_legend = True
        self.texts = {
            "JP": {
                "title": "Project 聖域 - v7.3 (Slider Range Optimized)",
                "firing": "🔥 点火順序",
                "legend": " 🎨 サイクル・カラー凡例 ",
                "legend_btn": "凡例 表示/非表示",
                "left_bank": "--- LEFT BANK (奇数) ---",
                "right_bank": "--- RIGHT BANK (偶数) ---",
                "params": {
                    "ε": "圧縮比 (ε)", "bore": "ボア径 (mm)", "stroke": "ストローク (mm)",
                    "rod": "コンロッド長 (mm)", "speed": "回転速度", "cyl": "気筒数"
                },
                "stats": ["排気量", "S/B 比", "連桿比 λ", "理論効率", "有効効率"],
                "cycles": {
                    2: [("圧縮・吸気", "#f1c40f"), ("爆発・掃気", "#e67e22")],
                    4: [("吸気", "#3498db"), ("圧縮", "#f1c40f"), ("膨張(爆発)", "#e67e22"), ("排気", "#95a5a6")],
                    6: [("吸気", "#3498db"), ("圧縮", "#f1c40f"), ("膨張(爆発)", "#e67e22"), 
                        ("排気", "#95a5a6"), ("熱回収(空気)", "#2ecc71"), ("再排気", "#7f8c8d")]
                },
                "graph_btn": "📈 パフォーマンス"
            },
            "EN": {
                "title": "Project SANCTUARY - v7.3 (Slider Range Optimized)",
                "firing": "🔥 Firing Order",
                "legend": " 🎨 Cycle Color Legend ",
                "legend_btn": "Show/Hide Legend",
                "left_bank": "--- LEFT BANK (Odd) ---",
                "right_bank": "--- RIGHT BANK (Even) ---",
                "params": {
                    "ε": "Comp Ratio (ε)", "bore": "Bore (mm)", "stroke": "Stroke (mm)",
                    "rod": "Rod Length (mm)", "speed": "Speed", "cyl": "Cylinders"
                },
                "stats": ["Displ.", "S/B Ratio", "Rod Ratio λ", "Theo. Eff.", "Eff. Eff."],
                "cycles": {
                    2: [("Comp/Intake", "#f1c40f"), ("Power/Exhaust", "#e67e22")],
                    4: [("Intake", "#3498db"), ("Compression", "#f1c40f"), ("Power", "#e67e22"), ("Exhaust", "#95a5a6")],
                    6: [("Intake", "#3498db"), ("Comp", "#f1c40f"), ("Power", "#e67e22"), 
                        ("Exhaust", "#95a5a6"), ("Heat Recov", "#2ecc71"), ("Re-Exhaust", "#7f8c8d")]
                },
                "graph_btn": "📈 Performance"
            }
        }

        self.angle = 0
        self.mode = 4  
        self.root.title(self.texts[self.lang]["title"])
        self.root.geometry("1200x900")
        self.root.configure(bg="#f5f6fa")

        self.canvas = tk.Canvas(root, width=720, height=850, bg="#1e272e", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        self.panel = tk.Frame(root, bg="#f5f6fa")
        self.panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20)
        
        self.create_widgets()
        self.refresh_ui_text()
        self.update_animation()

    def create_widgets(self):
        top_frame = tk.Frame(self.panel, bg="#f5f6fa")
        top_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(top_frame, text="JP", command=lambda: self.switch_lang("JP"), width=4).pack(side=tk.LEFT, padx=2)
        tk.Button(top_frame, text="EN", command=lambda: self.switch_lang("EN"), width=4).pack(side=tk.LEFT, padx=2)
        
        self.btn_toggle_legend = tk.Button(top_frame, text="", command=self.toggle_legend_view, bg="#dcdde1")
        self.btn_toggle_legend.pack(side=tk.RIGHT, padx=5)

        self.lbl_firing = tk.Label(self.panel, text="", font=("Arial", 9, "bold"), bg="#f5f6fa")
        self.lbl_firing.pack(pady=(10, 0))
        self.entry_firing = tk.Entry(self.panel, font=("Consolas", 10), justify="center")
        self.entry_firing.insert(0, "1,6,5,10,2,7,3,8,4,9") 
        self.entry_firing.pack(pady=5, fill=tk.X, padx=10)

        self.legend_frame = tk.LabelFrame(self.panel, text="", font=("Arial", 10, "bold"), bg="#f5f6fa", padx=10, pady=5)
        self.legend_frame.pack(fill=tk.X, pady=10)

        btn_frame = tk.Frame(self.panel, bg="#f5f6fa")
        btn_frame.pack(pady=10)
        for m in [2, 4, 6]:
            tk.Button(btn_frame, text=f"{m}-Str", command=lambda x=m: self.set_mode(x), width=8).pack(side=tk.LEFT, padx=2)
        
        self.btn_graph = tk.Button(btn_frame, text="", command=self.show_torque_curve, width=12, bg="#e84118", fg="white", font=("Arial", 9, "bold"))
        self.btn_graph.pack(side=tk.LEFT, padx=10)

        self.params = {}
        self.param_labels = {}
        # --- 🛠️ 調整範囲を最適化 (下限を広げ、上限を現実的に) ---
        param_configs = [
            ("ε", 1.0, 25.0, 0.1, 12.3, "#c23616"),     # 圧縮比: 1.0から
            ("bore", 10.0, 100.0, 0.1, 66.0, "#e67e22"),   # ボア: 10mmから
            ("stroke", 10.0, 100.0, 0.1, 43.8, "#2980b9"), # ストローク: 10mmから
            ("rod", 30.0, 250.0, 1, 100, "#27ae60"),      # ロッド: 30mmから
            ("speed", 0, 30, 1, 10, "#7f8c8d"),           # 回転速度: 低速重視
            ("cyl", 1, 24, 1, 10, "#34495e")              # 気筒数: 24まで
        ]

        for key, f, t, res, d, col in param_configs:
            frame = tk.Frame(self.panel, bg="#f5f6fa")
            frame.pack(fill=tk.X, pady=2)
            lbl = tk.Label(frame, text="", font=("Arial", 9, "bold"), fg=col, bg="#f5f6fa", anchor="w")
            lbl.pack(side=tk.TOP, fill=tk.X)
            self.param_labels[key] = lbl
            row = tk.Frame(frame, bg="#f5f6fa")
            row.pack(fill=tk.X)
            s = tk.Scale(row, from_=f, to=t, resolution=res, orient="horizontal", length=180, bg="#f5f6fa", bd=0, 
                         command=lambda val, k=key: self.sync_scale_to_entry(k, val))
            s.set(d); s.pack(side=tk.LEFT)
            e = tk.Entry(row, width=8, font=("Consolas", 10), justify="center")
            e.insert(0, str(d)); e.pack(side=tk.LEFT, padx=10)
            e.bind("<Return>", lambda event, k=key: self.sync_entry_to_scale(k))
            self.params[key] = {"scale": s, "entry": e}

        self.info_label = tk.Label(self.panel, text="", font=("Consolas", 10), justify=tk.LEFT, bg="#2f3640", fg="#f5f6fa", padx=15, pady=15)
        self.info_label.pack(pady=20, fill=tk.BOTH, expand=True)

    def toggle_legend_view(self):
        self.show_legend = not self.show_legend
        if self.show_legend: self.legend_frame.pack(fill=tk.X, pady=10, after=self.entry_firing)
        else: self.legend_frame.pack_forget()

    def switch_lang(self, lang):
        self.lang = lang; self.root.title(self.texts[lang]["title"]); self.refresh_ui_text(); self.refresh_legend()

    def refresh_ui_text(self):
        t = self.texts[self.lang]
        self.lbl_firing.config(text=t["firing"]); self.legend_frame.config(text=t["legend"])
        self.btn_graph.config(text=t["graph_btn"]); self.btn_toggle_legend.config(text=t["legend_btn"])
        for key, label_widget in self.param_labels.items(): label_widget.config(text=t["params"][key])

    def sync_scale_to_entry(self, key, val):
        self.params[key]["entry"].delete(0, tk.END); self.params[key]["entry"].insert(0, val)

    def sync_entry_to_scale(self, key):
        try: val = float(self.params[key]["entry"].get()); self.params[key]["scale"].set(val)
        except ValueError: pass

    def set_mode(self, m): self.mode = m; self.refresh_legend()

    def refresh_legend(self):
        for child in self.legend_frame.winfo_children(): child.destroy()
        for name, color in self.texts[self.lang]["cycles"][self.mode]:
            f = tk.Frame(self.legend_frame, bg="#f5f6fa"); f.pack(fill=tk.X, pady=1)
            tk.Label(f, width=2, bg=color, bd=1, relief="solid").pack(side=tk.LEFT, padx=5)
            tk.Label(f, text=name, font=("Arial", 9), bg="#f5f6fa").pack(side=tk.LEFT)

    def show_torque_curve(self):
        if hasattr(self, 'graph_win') and self.graph_win.winfo_exists(): self.graph_win.lift(); return
        self.graph_win = tk.Toplevel(self.root); self.graph_win.title("Performance Curve"); self.graph_win.geometry("650x550")
        self.graph_cv = tk.Canvas(self.graph_win, width=600, height=500, bg="#2d3436"); self.graph_cv.pack(pady=20); self.draw_graph_content()

    def draw_graph_content(self):
        cv = self.graph_cv; cv.delete("all"); offset_x, offset_y, graph_w, graph_h = 60, 420, 500, 380; max_rpm, max_val = 12000, 400
        for i in range(0, 13):
            x = offset_x + (i*1000/max_rpm)*graph_w; cv.create_line(x, offset_y, x, offset_y-graph_h, fill="#3d4444", dash=(2, 2))
            if i%2==0: cv.create_text(x, offset_y+15, text=f"{i}k", fill="#dcdde1", font=("Arial", 8))
        for val in range(0, 401, 50):
            y = offset_y - (val/max_val)*graph_h; cv.create_line(offset_x, y, offset_x+graph_w, y, fill="#3d4444", dash=(2, 2))
            cv.create_text(offset_x-25, y, text=str(val), fill="#dcdde1", font=("Arial", 8))
        b, s, epsilon, cyl = float(self.params["bore"]["scale"].get()), float(self.params["stroke"]["scale"].get()), float(self.params["ε"]["scale"].get()), int(self.params["cyl"]["scale"].get())
        pts_t, pts_p = [], []
        for rpm in range(0, 12001, 200):
            ve = math.exp(-((rpm-9500)**2)/(2*3500**2)); tq = (b*s*epsilon/1200)*ve*(cyl/10)*12; ps = (tq*rpm)/716.2
            pts_t.append((offset_x+(rpm/max_rpm)*graph_w, offset_y-(tq/max_val)*graph_h)); pts_p.append((offset_x+(rpm/max_rpm)*graph_w, offset_y-(ps/max_val)*graph_h))
        cv.create_line(pts_t, fill="#e67e22", width=3, smooth=True); cv.create_line(pts_p, fill="#e84118", width=3, smooth=True)

    def update_animation(self):
        self.canvas.delete("engine")
        b = float(self.params["bore"]["scale"].get()); s = float(self.params["stroke"]["scale"].get()); l = float(self.params["rod"]["scale"].get())
        speed = float(self.params["speed"]["scale"].get()); cyl_count = int(self.params["cyl"]["scale"].get()); epsilon = float(self.params["ε"]["scale"].get())
        try: firing_order = [int(x.strip()) for x in self.entry_firing.get().split(",")]
        except: firing_order = list(range(1, cyl_count + 1))

        # --- スケール調整 ---
        # 10mmなどの小さな設定でも画面内に収まるように動的スケーリング
        draw_scale = 1.0 if b < 40 else 0.7
        upper_bank_y, lower_bank_y = 280, 650
        
        self.canvas.create_text(360, 40, text=self.texts[self.lang]["left_bank"], fill="#3498db", font=("Arial", 11, "bold"), tags="engine")
        self.canvas.create_text(360, 810, text=self.texts[self.lang]["right_bank"], fill="#e67e22", font=("Arial", 11, "bold"), tags="engine")

        cycle_deg = 360 if self.mode == 2 else (720 if self.mode == 4 else 1080)
        phase_gap = cycle_deg / cyl_count

        for i in range(cyl_count):
            cyl_id = i + 1; is_even = (cyl_id % 2 == 0); base_y = lower_bank_y if is_even else upper_bank_y
            pos_x = (i // 2) + 1; cols = math.ceil(cyl_count / 2); cx = (720 / (cols + 1)) * pos_x
            try: order_pos = firing_order.index(cyl_id) if cyl_id in firing_order else i
            except: order_pos = i
            cyl_angle = (self.angle - (order_pos * phase_gap)) % cycle_deg
            idx = min(len(self.texts[self.lang]["cycles"][self.mode])-1, int(cyl_angle // (cycle_deg / len(self.texts[self.lang]["cycles"][self.mode]))))
            name, color = self.texts[self.lang]["cycles"][self.mode][idx]
            r, rad = s/2, math.radians(cyl_angle)
            px, py = cx + (r * math.sin(rad)) * draw_scale, base_y - (r * math.cos(rad)) * draw_scale
            # 連桿比の計算 (極端な設定でのクラッシュ回避)
            rod_len = max(l * draw_scale, r * draw_scale + 5)
            piston_y = py - math.sqrt(max(0, rod_len**2 - (px-cx)**2))
            w_l, w_r = cx-(b/2)*draw_scale, cx+(b/2)*draw_scale
            wt, wb = base_y - 250*draw_scale, base_y + 80*draw_scale
            
            self.canvas.create_rectangle(w_l-5, wt, w_r+5, wb, fill="#2f3542", outline="#57606f", tags="engine")
            self.canvas.create_rectangle(w_l, wt, w_r, wb, fill="#1e272e", outline="", tags="engine")
            self.canvas.create_rectangle(w_l, wt, w_r, piston_y-20*draw_scale, fill=color, outline="", tags="engine")
            self.canvas.create_line(cx, base_y, px, py, width=5, fill="#dcdde1", tags="engine")
            self.canvas.create_line(px, py, cx, piston_y, width=4, fill="#3498db", tags="engine")
            self.canvas.create_rectangle(w_l, piston_y-20*draw_scale, w_r, piston_y, fill="#7f8c8d", outline="white", tags="engine")
            label_y = base_y + 110*draw_scale
            self.canvas.create_text(cx, label_y, text=f"#{cyl_id}", fill="white", font=("Arial", 9, "bold"), tags="engine")

        v_total = ((math.pi * (b/2)**2 * s) / 1000) * cyl_count
        eta_theoretical = 1 - (1 / (max(1.1, epsilon)**(1.4 - 1)))
        mode_corr = {2: 0.75, 4: 1.0, 6: 1.15}
        eta_effective = eta_theoretical * mode_corr.get(self.mode, 1.0) * (0.85 - (20 / b if b > 0 else 0))
        st = self.texts[self.lang]["stats"]
        self.info_label.config(text=(f" {st[0]} : {v_total:>7.1f} cc\n" f" {st[1]} : {s/b:>7.2f}\n" f" {st[2]} : {l/(s/2) if s>0 else 0:>7.2f}\n" f" {st[3]} : {eta_theoretical*100:>7.1f} %\n" f" {st[4]} : {max(0, eta_effective*100):>7.1f} %"))
        
        if hasattr(self, 'graph_win') and self.graph_win.winfo_exists(): self.draw_graph_content()
        self.angle += speed
        self.root.after(20, self.update_animation)

if __name__ == "__main__":
    root = tk.Tk(); app = SanctuaryEngine(root); root.mainloop()
