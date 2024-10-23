import customtkinter as ctk
from customtkinter import filedialog    
import cv2
from PIL import Image, ImageTk

class ImageBinarizerApp:
    def __init__(self, master):
        self.master = master
        master.title("Binaryzacja")
        master.geometry("800x600")
        master.minsize(600, 600)

        ctk.set_appearance_mode("dark")  
        ctk.set_default_color_theme("blue")
        
        self.languages = {
            'pl': {
                'title': 'Binaryzacja',
                'load': 'Wczytaj obraz',
                'binarize': 'Binaryzuj',
                'save': 'Zapisz',
                'change_lang': 'English',
                'image': 'Obraz początkowy',
                'final_image': 'Obraz końcowy',
                'lower_thresh': 'Dolny próg:',
                'higher_thresh': 'Górny próg:',
                'dropdown_label': 'Wybierz kierunek:',
                'dropdown_options': ['Lewo > Prawo', 'Prawo > Lewo', 'Góra > Dół', 'Dół > Góra'],
                'current_selection': 'Lewo > prawo'
            },
            'en': {
                'title': 'Binarization',
                'load': 'Load Image',
                'binarize': 'Binarize',
                'save': 'Save',
                'change_lang': 'Polish',
                'image': 'Starting Image',
                'final_image': 'Final Image',
                'lower_thresh': 'Lower threshold:',
                'higher_thresh': 'Higher threshold:',
                'dropdown_label': 'Select direction:',
                'dropdown_options': ['Left > Right', 'Right > Left', 'Top > Bottom', 'Bottom > Top'],
                'current_selection': 'Left > Right'
            }
        }

        self.current_lang = 'pl'
        self.original_image = None
        self.binary_image = None
        font = ("Arial", 15, "bold")
        
        main_frame = ctk.CTkFrame(master)
        main_frame.pack(fill=ctk.BOTH, expand=True)

        menu_frame = ctk.CTkFrame(main_frame, width=240)
        menu_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=0, pady=0)
        menu_frame.pack_propagate(False)

        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=10, pady=10)

        self.load_button = ctk.CTkButton(menu_frame, text="Wczytaj obraz", command=self.load_image, font=font)
        self.load_button.pack(pady=20, padx=10)

        self.lower_thresh_label = ctk.CTkLabel(menu_frame, text="Dolny próg:", font=font)
        self.lower_thresh_label.pack(pady=(20, 0), padx=10)
        self.lower_thresh = ctk.CTkEntry(menu_frame, width=140, font=font)
        self.lower_thresh.pack(pady=(0, 10), padx=10)
        self.lower_thresh.insert(0, "100")

        self.higher_thresh_label = ctk.CTkLabel(menu_frame, text="Górny próg:", font=font)
        self.higher_thresh_label.pack(pady=(10, 0), padx=10)
        self.higher_thresh = ctk.CTkEntry(menu_frame, width=140, font=font)
        self.higher_thresh.pack(pady=(0, 20), padx=10)
        self.higher_thresh.insert(0, "150")

        self.dropdown_label = ctk.CTkLabel(menu_frame, text="Wybierz kierunek:", font=font)
        self.dropdown_label.pack(pady=(10, 0), padx=10)

        self.dropdown_var = ctk.StringVar(value="Lewo > Prawo")
        self.dropdown_menu = ctk.CTkOptionMenu(menu_frame, values=["Lewo > Prawo", "Prawo > Lewo", "Góra > Dół", "Dół > Góra"], variable=self.dropdown_var, font=font)
        self.dropdown_menu.pack(pady=(0, 20), padx=10)
        
        self.process_button = ctk.CTkButton(menu_frame, text="Binaryzuj", command=self.binarize_image, font=font)
        self.process_button.pack(pady=20, padx=10)

        self.save_button = ctk.CTkButton(menu_frame, text="Zapisz", command=self.save_image, font=font)
        self.save_button.pack(pady=20, padx=10)

        self.language_button = ctk.CTkButton(menu_frame, text="English", command=self.change_language, font=font)
        self.language_button.pack(side=ctk.BOTTOM, pady=20, padx=10)

        self.image_label = ctk.CTkLabel(content_frame, text="Obraz początkowy", font=font)
        self.image_label.pack()
        self.original_canvas = ctk.CTkCanvas(content_frame, width=250, height=250, bg="lightgray")
        self.original_canvas.pack(pady=10)

        self.final_label = ctk.CTkLabel(content_frame, text="Obraz końcowy", font=font)
        self.final_label.pack()
        self.final_canvas = ctk.CTkCanvas(content_frame, width=250, height=250, bg="lightgray")
        self.final_canvas.pack(pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if file_path:
            img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE) # Wczytanie obrazu w odcieniach szarości
            self.original_image = img.copy() # Zapisanie oryginalnego obrazu
            img = cv2.resize(img, (250, 250), interpolation=cv2.INTER_AREA) # Zmiana rozmiaru obrazu
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB) # Konwersja na RGB
            img_pil = Image.fromarray(img) # Tworzenie obrazu PIL
            self.original_photo = ImageTk.PhotoImage(img_pil) # Tworzenie obrazu Tkinter
            self.original_canvas.create_image(125, 125, image=self.original_photo, anchor=ctk.CENTER)

    def binarize_image(self):
        if self.original_image is not None:
            selected_direction = self.dropdown_var.get()
            print(f"Wybrany kierunek binaryzacji: {selected_direction}")
            try:
                prog1 = int(self.lower_thresh.get())
                prog2 = int(self.higher_thresh.get())
            except ValueError:
                prog1 = 100
                prog2 = 150

            binary = self.original_image.copy()
            rows, cols = binary.shape

            if (selected_direction == "Lewo > Prawo" and self.current_lang == 'pl') or (selected_direction == "Left > Right" and self.current_lang == 'en'):
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

            elif (selected_direction == "Prawo > Lewo" and self.current_lang == 'pl') or (selected_direction == "Right > Left" and self.current_lang == 'en'):
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

            elif (selected_direction == "Góra > Dół" and self.current_lang == 'pl') or (selected_direction == "Top > Bottom" and self.current_lang == 'en'):
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

            elif (selected_direction == "Dół > Góra" and self.current_lang == 'pl') or (selected_direction == "Bottom > Top" and self.current_lang == 'en'):
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
            binary_pil = Image.fromarray(binary)
            self.binary_photo = ImageTk.PhotoImage(binary_pil)
            
            self.final_canvas.create_image(125, 125, image=self.binary_photo, anchor=ctk.CENTER)


    def save_image(self):
        if self.binary_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"),
                                                                ("JPEG files", "*.jpg"),
                                                                ("All files", "*.*")])
            if file_path:
                cv2.imwrite(file_path, self.binary_image)

    def change_language(self):
        self.current_lang = 'en' if self.current_lang == 'pl' else 'pl'
        self.update_language()

    def update_language(self):
        current_direction = self.dropdown_var.get()

        lang = self.languages[self.current_lang]
        self.master.title(lang['title'])
        self.load_button.configure(text=lang['load'])
        self.process_button.configure(text=lang['binarize'])
        self.save_button.configure(text=lang['save'])
        self.language_button.configure(text=lang['change_lang'])
        self.image_label.configure(text=lang['image'])
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



if __name__ == "__main__":
    root = ctk.CTk()
    app = ImageBinarizerApp(root)
    root.mainloop()
