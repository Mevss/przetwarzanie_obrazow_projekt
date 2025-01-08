import customtkinter as ctk
from customtkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk


class ImageBinarizerApp:
    def __init__(self, master):
        self.master = master
        master.title("Binaryzacja warunkowa")
        master.geometry("810x675")
        master.minsize(810, 675)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.languages = {
            'pl': {
                'title': 'Binaryzacja warunkowa',
                'title_label': 'Binaryzacja warunkowa',
                'load': 'Wczytaj obraz',
                'binarize': 'Binaryzuj',
                'save': 'Zapisz obraz',
                'histogram_label': "Histogram obrazu wejściowego",
                'output_histogram_label': "Histogram obrazu wyjściowego",
                'change_lang': 'English',
                'image': 'Obraz wejściowy',
                'final_image': 'Obraz wyjściowy',
                'lower_thresh': 'Dolny próg:',
                'higher_thresh': 'Górny próg:',
                'dropdown_label': 'Wybierz kierunek:',
                'dropdown_options': ['Lewo > Prawo', 'Prawo > Lewo', 'Góra > Dół', 'Dół > Góra'],
                'current_selection': 'Lewo > prawo',
                'brightness_level': 'Poziom jasności',
                'pixel_count': 'Liczba pikseli'
            },
            'en': {
                'title': 'Conditional binarization',
                'title_label': 'Conditional binarisation',
                'load': 'Load Image',
                'binarize': 'Binarise',
                'save': 'Save image',
                'histogram_label': "Input image histogram",
                'output_histogram_label': "Output image histogram",
                'change_lang': 'Polski',
                'image': 'Input Image',
                'final_image': 'Output Image',
                'lower_thresh': 'Lower threshold:',
                'higher_thresh': 'Higher threshold:',
                'dropdown_label': 'Select direction:',
                'dropdown_options': ['Left > Right', 'Right > Left', 'Top > Bottom', 'Bottom > Top'],
                'current_selection': 'Left > Right',
                'brightness_level': 'Brightness level',
                'pixel_count': 'Pixel count'
            }
        }

        self.current_lang = 'pl'
        self.original_image = None
        self.binary_image = None

        title_font = ("Helvetica", 24, "bold")
        button_font = ("Helvetica", 14, "bold")

        button_config = {'width': 140, 'height': 30, 'font': button_font}
        self.bg_color = "#2b2b2b"

        container = ctk.CTkFrame(master)
        container.pack(fill=ctk.BOTH, expand=True)

        title_frame = ctk.CTkFrame(container, fg_color=self.bg_color)
        title_frame.pack(fill=ctk.X, padx=5, pady=(5, 0))

        title_label = ctk.CTkLabel(title_frame, text="Binaryzacja warunkowa", font=title_font, height=10)
        title_label.pack(pady=5)
        self.title_label = title_label

        main_frame = ctk.CTkFrame(container, fg_color=self.bg_color)
        main_frame.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)

        menu_frame = ctk.CTkFrame(main_frame, width=200)  # Reduced from 240
        menu_frame.pack(side=ctk.LEFT, fill=ctk.Y, padx=5, pady=5)
        menu_frame.pack_propagate(False)

        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=5, pady=5)

        top_frame = ctk.CTkFrame(content_frame)
        top_frame.pack(fill=ctk.X, pady=5)

        input_frame = ctk.CTkFrame(top_frame)
        input_frame.pack(side=ctk.LEFT, padx=20, pady=5)

        self.image_label = ctk.CTkLabel(input_frame, text="Obraz wejściowy", font=button_font)
        self.image_label.pack(pady=2)
        self.original_canvas = ctk.CTkCanvas(input_frame, width=250, height=250, bg="white", highlightthickness=0)
        self.original_canvas.pack()

        # Histogram frame with reduced padding
        histogram_frame = ctk.CTkFrame(top_frame)
        histogram_frame.pack(side=ctk.LEFT, padx=20)

        self.histogram_label = ctk.CTkLabel(histogram_frame, text="Histogram obrazu wejściowego", font=button_font)
        self.histogram_label.pack(pady=2)
        self.histogram_canvas = ctk.CTkCanvas(histogram_frame, width=250, height=250, bg="white", highlightthickness=0)
        self.histogram_canvas.pack()

        output_frame = ctk.CTkFrame(content_frame)
        output_frame.pack(fill=ctk.X, pady=5)

        output_image_frame = ctk.CTkFrame(output_frame)
        output_image_frame.pack(side=ctk.LEFT, padx=20, pady=5)

        self.final_label = ctk.CTkLabel(output_image_frame, text="Obraz wyjściowy", font=button_font)
        self.final_label.pack(pady=2)
        self.final_canvas = ctk.CTkCanvas(output_image_frame, width=250, height=250, bg="white", highlightthickness=0)
        self.final_canvas.pack()

        output_histogram_frame = ctk.CTkFrame(output_frame)
        output_histogram_frame.pack(side=ctk.LEFT, padx=20)

        self.output_histogram_label = ctk.CTkLabel(output_histogram_frame, text="Histogram obrazu wyjściowego",
                                                   font=button_font)
        self.output_histogram_label.pack(pady=2)
        self.output_histogram_canvas = ctk.CTkCanvas(output_histogram_frame, width=250, height=250, bg="white",
                                                     highlightthickness=0)
        self.output_histogram_canvas.pack()

        self.load_button = ctk.CTkButton(menu_frame, text="Wczytaj obraz", command=self.load_image, **button_config)
        self.load_button.pack(pady=15, padx=5)

        self.lower_thresh_label = ctk.CTkLabel(menu_frame, text="Dolny próg:", **button_config)
        self.lower_thresh_label.pack(pady=(10, 0), padx=10)
        self.lower_thresh = ctk.CTkEntry(menu_frame, **button_config)
        self.lower_thresh.pack(pady=(0, 15), padx=10)
        self.lower_thresh.insert(0, "100")

        self.higher_thresh_label = ctk.CTkLabel(menu_frame, text="Górny próg:", **button_config)
        self.higher_thresh_label.pack(pady=(10, 0), padx=10)
        self.higher_thresh = ctk.CTkEntry(menu_frame, **button_config)
        self.higher_thresh.pack(pady=(0, 15), padx=10)
        self.higher_thresh.insert(0, "150")

        self.dropdown_label = ctk.CTkLabel(menu_frame, text="Wybierz kierunek:", font=button_font)
        self.dropdown_label.pack(pady=(10, 0), padx=5)

        self.dropdown_var = ctk.StringVar(value="Lewo > Prawo")
        self.dropdown_menu = ctk.CTkOptionMenu(menu_frame,
                                               values=["Lewo > Prawo", "Prawo > Lewo", "Góra > Dół", "Dół > Góra"],
                                               variable=self.dropdown_var, **button_config)
        self.dropdown_menu.pack(pady=(0, 15), padx=10)

        self.process_button = ctk.CTkButton(menu_frame, text="Binaryzuj", command=self.binarize_image, **button_config)
        self.process_button.pack(pady=15, padx=5)

        self.save_button = ctk.CTkButton(menu_frame, text="Zapisz obraz", command=self.save_image, **button_config)
        self.save_button.pack(pady=15, padx=5)

        self.language_button = ctk.CTkButton(menu_frame, text="English", command=self.change_language, **button_config)
        self.language_button.pack(side=ctk.BOTTOM, pady=10, padx=5)

    def draw_histogram(self, image, canvas, is_binary=False):
        if image is not None:
            canvas.delete("all")

            hist = cv2.calcHist([image], [0], None, [261], [-5, 256])

            scale_factor = 0.98
            canvas_height = int(250 * scale_factor)
            canvas_width = int(250 * scale_factor)

            max_val = np.max(hist)
            normalized_hist = hist * (canvas_height - 40) / max_val

            canvas.create_line(30, canvas_height - 30, canvas_width - 10, canvas_height - 30,
                               fill="black", width=2)
            canvas.create_line(30, 10, 30, canvas_height - 30, fill="black", width=2)

            bar_width = (canvas_width - 40) / 261
            for i in range(261):
                height = int(normalized_hist[i][0])
                x1 = 30 + i * bar_width
                y1 = canvas_height - 30
                x2 = 30 + (i + 1) * bar_width
                y2 = canvas_height - 30 - height
                canvas.create_line(x1, y1, x1, y2, fill="black")

            value_points = [0, 1, 50, 100, 150, 200, 255]
            for value in value_points:
                x = 30 + (value + 5) * (canvas_width - 40) / 260
                canvas.create_line(x, canvas_height - 30, x, canvas_height - 25, fill="black")
                canvas.create_text(x, canvas_height - 18, text=str(value), fill="black")

            lang = self.languages[self.current_lang]
            canvas.create_text(canvas_width // 2, canvas_height - 5,
                               text=lang['brightness_level'], fill="black", font=("Helvetica", 8, "bold"))
            canvas.create_text(15, canvas_height // 2,
                               text=lang['pixel_count'], fill="black", angle=90, font=("Helvetica", 8, "bold"))

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if file_path:
            img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            self.original_image = img.copy()

            display_img = cv2.resize(img, (250, 250), interpolation=cv2.INTER_AREA)

            display_img = Image.fromarray(display_img)
            self.original_photo = ImageTk.PhotoImage(display_img)
            self.original_canvas.create_image(125, 125, image=self.original_photo, anchor=ctk.CENTER)

            self.draw_histogram(self.original_image, self.histogram_canvas)

    # def load_image(self):
    #     # initial_dir = os.path.dirname(os.path.abspath(__file__))
    #     # initial_dir = os.path.dirname(sys.executable)
    #     if getattr(sys, 'frozen', False):
    #         base_dir = os.path.dirname(sys.executable)
    #     else:
    #         base_dir = os.path.dirname(os.path.abspath(__file__))
    # 
    #     assets_dir = os.path.join(base_dir, 'assets')
    # 
    #     if os.path.exists(assets_dir):
    #         initial_dir = assets_dir
    #     else:
    #         initial_dir = base_dir
    # 
    #     file_path = filedialog.askopenfilename(
    #         initialdir=initial_dir,
    #         filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
    #     )
    #     if file_path:
    #         img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    #         self.original_image = img.copy()
    # 
    #         display_img = cv2.resize(img, (250, 250), interpolation=cv2.INTER_AREA)
    # 
    #         display_img = Image.fromarray(display_img)
    #         self.original_photo = ImageTk.PhotoImage(display_img)
    #         self.original_canvas.create_image(125, 125, image=self.original_photo, anchor=ctk.CENTER)
    # 
    #         self.draw_histogram(self.original_image, self.histogram_canvas)
    
    def binarize_image(self):
        if self.original_image is not None:
            selected_direction = self.dropdown_var.get()
            try:
                prog1 = int(self.lower_thresh.get())
                prog2 = int(self.higher_thresh.get())
            except ValueError:
                prog1 = 100
                prog2 = 150

            binary = self.original_image.copy()
            rows, cols = binary.shape

            if (selected_direction == "Lewo > Prawo" and self.current_lang == 'pl') or (
                    selected_direction == "Left > Right" and self.current_lang == 'en'):
                for col in range(cols):
                    for row in range(rows):
                        pixel_value = binary[row, col]
                        if col == 0:
                            binary[row, col] = 255 if pixel_value > prog2 else 0
                        else:
                            previous_pixel = binary[row, col - 1]
                            if pixel_value > prog2:
                                binary[row, col] = 255
                            elif pixel_value < prog1:
                                binary[row, col] = 0
                            else:
                                binary[row, col] = previous_pixel

            elif (selected_direction == "Prawo > Lewo" and self.current_lang == 'pl') or (
                    selected_direction == "Right > Left" and self.current_lang == 'en'):
                for col in range(cols - 1, -1, -1):
                    for row in range(rows):
                        pixel_value = binary[row, col]
                        if col == cols - 1:
                            binary[row, col] = 255 if pixel_value > prog2 else 0
                        else:
                            previous_pixel = binary[row, col + 1]
                            if pixel_value > prog2:
                                binary[row, col] = 255
                            elif pixel_value < prog1:
                                binary[row, col] = 0
                            else:
                                binary[row, col] = previous_pixel

            elif (selected_direction == "Góra > Dół" and self.current_lang == 'pl') or (
                    selected_direction == "Top > Bottom" and self.current_lang == 'en'):
                for row in range(rows):
                    for col in range(cols):
                        pixel_value = binary[row, col]
                        if row == 0:
                            binary[row, col] = 255 if pixel_value > prog2 else 0
                        else:
                            previous_pixel = binary[row - 1, col]
                            if pixel_value > prog2:
                                binary[row, col] = 255
                            elif pixel_value < prog1:
                                binary[row, col] = 0
                            else:
                                binary[row, col] = previous_pixel

            elif (selected_direction == "Dół > Góra" and self.current_lang == 'pl') or (
                    selected_direction == "Bottom > Top" and self.current_lang == 'en'):
                for row in range(rows - 1, -1, -1):
                    for col in range(cols):
                        pixel_value = binary[row, col]
                        if row == rows - 1:
                            binary[row, col] = 255 if pixel_value > prog2 else 0
                        else:
                            previous_pixel = binary[row + 1, col]
                            if pixel_value > prog2:
                                binary[row, col] = 255
                            elif pixel_value < prog1:
                                binary[row, col] = 0
                            else:
                                binary[row, col] = previous_pixel

            self.binary_image = binary

            display_binary = cv2.resize(binary, (250, 250), interpolation=cv2.INTER_AREA)
            display_binary = Image.fromarray(display_binary)
            self.binary_photo = ImageTk.PhotoImage(display_binary)
            self.final_canvas.create_image(125, 125, image=self.binary_photo, anchor=ctk.CENTER)

            self.draw_histogram(self.binary_image, self.output_histogram_canvas, is_binary=True)

    def save_image(self):
        if self.binary_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"),
                                                                ("JPEG files", "*.jpg"),
                                                                ("All files", "*.*")])
            if file_path:
                save_img = cv2.resize(self.binary_image, (250, 250), interpolation=cv2.INTER_AREA)
                save_img = save_img.astype(np.uint8)
                cv2.imwrite(file_path, save_img)

    def change_language(self):
        self.current_lang = 'en' if self.current_lang == 'pl' else 'pl'
        self.update_language()

    def update_language(self):
        current_direction = self.dropdown_var.get()

        lang = self.languages[self.current_lang]
        self.master.title(lang['title'])
        self.title_label.configure(text=lang['title_label'])
        self.load_button.configure(text=lang['load'])
        self.process_button.configure(text=lang['binarize'])
        self.save_button.configure(text=lang['save'])
        self.language_button.configure(text=lang['change_lang'])
        self.image_label.configure(text=lang['image'])
        self.histogram_label.configure(text=lang['histogram_label'])
        self.output_histogram_label.configure(text=lang['output_histogram_label'])
        self.final_label.configure(text=lang['final_image'])
        self.lower_thresh_label.configure(text=lang['lower_thresh'])
        self.higher_thresh_label.configure(text=lang['higher_thresh'])
        self.dropdown_label.configure(text=lang['dropdown_label'])

        direction_map = {
            ('Lewo > Prawo', 'Left > Right'),
            ('Prawo > Lewo', 'Right > Left'),
            ('Góra > Dół', 'Top > Bottom'),
            ('Dół > Góra', 'Bottom > Top')
        }

        for pl_dir, en_dir in direction_map:
            if self.current_lang == 'pl' and current_direction == en_dir:
                current_direction = pl_dir
            elif self.current_lang == 'en' and current_direction == pl_dir:
                current_direction = en_dir

        self.dropdown_var.set(current_direction)
        self.dropdown_menu.configure(values=lang['dropdown_options'])

        self.draw_histogram(self.original_image, self.histogram_canvas)
        self.draw_histogram(self.binary_image, self.output_histogram_canvas, is_binary=True)


if __name__ == "__main__":
    root = ctk.CTk()
    app = ImageBinarizerApp(root)
    root.mainloop()
