"""
GUI components for the Python Image Editor application.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, Menu, simpledialog
from PIL import Image, ImageTk
from filters import Filters
from history import History
from image_utils import ImageUtils
from typing import Optional
import os


class ImageEditorApp(tk.Tk):
    """
    Main application class for the image editor.
    """

    def __init__(self) -> None:
        super().__init__()
        self.title("Python Image Editor")
        self.geometry("1024x768")
        self.image: Optional[Image.Image] = None  # Current image object
        self.image_display: Optional[ImageTk.PhotoImage] = None  # Image for display
        self.history = History()
        self.filters = Filters()
        self.create_menu()
        self.create_widgets()
        self.image_utils = ImageUtils()
        self.bind("<Configure>", self.on_resize)
        self.bind_shortcuts()

        # Parameters for adjustable filters
        self.parameters = {
            "gaussian_blur_radius": 2.0,
            "box_blur_radius": 2.0,
            "add_noise_amount": 64,
            "solarize_threshold": 128,
            "posterize_bits": 4,
            "custom_kernel_size": 3,
            "custom_kernel_elements": [],
        }

    def create_menu(self) -> None:
        """
        Create the menu bar with all the menu items.
        """
        self.menu_bar = Menu(self)

        # File menu
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(
            label="Open Image\tCtrl+O", command=self.open_image, accelerator="Ctrl+O"
        )
        file_menu.add_command(
            label="Save As Copy\tCtrl+S", command=self.save_image, accelerator="Ctrl+S"
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Filters menu
        filters_menu = Menu(self.menu_bar, tearoff=0)

        # Black & White Filters
        bw_menu = Menu(filters_menu, tearoff=0)
        bw_menu.add_command(label="Classic B&W", command=self.apply_classic_bw)
        bw_menu.add_command(
            label="High Contrast B&W", command=self.apply_high_contrast_bw
        )
        filters_menu.add_cascade(label="Black & White", menu=bw_menu)

        # Color Effects
        color_menu = Menu(filters_menu, tearoff=0)
        color_menu.add_command(label="Vintage", command=self.apply_vintage_filter)
        color_menu.add_command(label="Sepia", command=self.apply_sepia_filter)
        # Solarize submenu
        solarize_menu = Menu(color_menu, tearoff=0)
        for threshold in [64, 128, 192]:
            solarize_menu.add_command(
                label=f"Threshold {threshold}",
                command=lambda t=threshold: self.apply_solarize_filter(t),
            )
        solarize_menu.add_command(
            label="Custom...", command=self.apply_solarize_filter_custom
        )
        color_menu.add_cascade(label="Solarize", menu=solarize_menu)
        # Posterize submenu
        posterize_menu = Menu(color_menu, tearoff=0)
        for bits in [1, 2, 4, 8]:
            posterize_menu.add_command(
                label=f"Bits {bits}",
                command=lambda b=bits: self.apply_posterize_filter(b),
            )
        posterize_menu.add_command(
            label="Custom...", command=self.apply_posterize_filter_custom
        )
        color_menu.add_cascade(label="Posterize", menu=posterize_menu)
        color_menu.add_command(label="Invert Colors", command=self.apply_invert_filter)
        filters_menu.add_cascade(label="Color Adjustments", menu=color_menu)

        # Sharpening Filters
        sharpen_menu = Menu(filters_menu, tearoff=0)
        sharpen_menu.add_command(label="Sharpen", command=self.apply_sharpen_filter)
        sharpen_menu.add_command(
            label="Enhance Detail", command=self.apply_detail_filter
        )
        filters_menu.add_cascade(label="Sharpening", menu=sharpen_menu)

        # Edge Detection Filters
        edge_menu = Menu(filters_menu, tearoff=0)
        edge_menu.add_command(label="Find Edges", command=self.apply_find_edges_filter)
        edge_menu.add_command(
            label="Edge Enhance", command=self.apply_edge_enhance_filter
        )
        filters_menu.add_cascade(label="Edge Detection", menu=edge_menu)

        # Artistic Effects
        artistic_menu = Menu(filters_menu, tearoff=0)
        artistic_menu.add_command(label="Emboss", command=self.apply_emboss_filter)
        artistic_menu.add_command(label="Contour", command=self.apply_contour_filter)
        filters_menu.add_cascade(label="Artistic Effects", menu=artistic_menu)

        # Noise Reduction
        noise_reduction_menu = Menu(filters_menu, tearoff=0)
        noise_reduction_menu.add_command(
            label="Reduce Noise", command=self.reduce_noise
        )
        filters_menu.add_cascade(label="Noise Reduction", menu=noise_reduction_menu)

        filters_menu.add_separator()
        filters_menu.add_command(
            label="Custom Filter", command=self.apply_custom_filter
        )
        filters_menu.add_separator()
        filters_menu.add_command(
            label="Filter Settings", command=self.open_filter_settings
        )
        self.menu_bar.add_cascade(label="Filters", menu=filters_menu)

        # Blurs menu
        blur_menu = Menu(self.menu_bar, tearoff=0)
        # Gaussian Blur submenu
        gaussian_blur_menu = Menu(blur_menu, tearoff=0)
        for radius in [1, 2, 5]:
            gaussian_blur_menu.add_command(
                label=f"Radius {radius}",
                command=lambda r=radius: self.apply_gaussian_blur(r),
            )
        gaussian_blur_menu.add_command(
            label="Custom...", command=self.apply_gaussian_blur_custom
        )
        blur_menu.add_cascade(label="Gaussian Blur", menu=gaussian_blur_menu)
        # Box Blur submenu
        box_blur_menu = Menu(blur_menu, tearoff=0)
        for radius in [1, 2, 5]:
            box_blur_menu.add_command(
                label=f"Radius {radius}",
                command=lambda r=radius: self.apply_box_blur(r),
            )
        box_blur_menu.add_command(label="Custom...", command=self.apply_box_blur_custom)
        blur_menu.add_cascade(label="Box Blur", menu=box_blur_menu)
        self.menu_bar.add_cascade(label="Blurs", menu=blur_menu)

        # Noise menu
        noise_menu = Menu(self.menu_bar, tearoff=0)
        # Add Noise submenu
        add_noise_menu = Menu(noise_menu, tearoff=0)
        for amount in [32, 64, 128]:
            add_noise_menu.add_command(
                label=f"Amount {amount}", command=lambda a=amount: self.add_noise(a)
            )
        add_noise_menu.add_command(label="Custom...", command=self.add_noise_custom)
        noise_menu.add_cascade(label="Add Noise", menu=add_noise_menu)
        self.menu_bar.add_cascade(label="Noise", menu=noise_menu)

        # History menu
        history_menu = Menu(self.menu_bar, tearoff=0)
        history_menu.add_command(
            label="Undo\tCtrl+Z", command=self.undo, accelerator="Ctrl+Z"
        )
        history_menu.add_command(
            label="Redo\tCtrl+Y", command=self.redo, accelerator="Ctrl+Y"
        )
        self.menu_bar.add_cascade(label="History", menu=history_menu)

        # Help menu
        help_menu = Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Help", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=self.menu_bar)

    def create_widgets(self) -> None:
        """
        Create GUI widgets.
        """
        # Create toolbar frame and pack it below the menu bar
        self.toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Try to load icons from the 'icons' folder
        icons_path = "icons"
        icons_available = os.path.isdir(icons_path)

        if icons_available:
            try:
                self.open_icon = ImageTk.PhotoImage(
                    Image.open(os.path.join(icons_path, "open.png")).resize((24, 24))
                )
                self.save_icon = ImageTk.PhotoImage(
                    Image.open(os.path.join(icons_path, "save.png")).resize((24, 24))
                )
                self.undo_icon = ImageTk.PhotoImage(
                    Image.open(os.path.join(icons_path, "undo.png")).resize((24, 24))
                )
                self.redo_icon = ImageTk.PhotoImage(
                    Image.open(os.path.join(icons_path, "redo.png")).resize((24, 24))
                )
                icons_loaded = True
            except Exception as e:
                print(f"Error loading icons: {e}")
                icons_loaded = False
        else:
            icons_loaded = False

        # Define emojis for toolbar buttons
        open_emoji = "📂"
        save_emoji = "💾"
        undo_emoji = "↩️"
        redo_emoji = "↪️"

        # Toolbar buttons
        if icons_loaded:
            open_btn = tk.Button(
                self.toolbar, image=self.open_icon, command=self.open_image
            )
            save_btn = tk.Button(
                self.toolbar, image=self.save_icon, command=self.save_image
            )
            undo_btn = tk.Button(self.toolbar, image=self.undo_icon, command=self.undo)
            redo_btn = tk.Button(self.toolbar, image=self.redo_icon, command=self.redo)
        else:
            open_btn = tk.Button(
                self.toolbar,
                text=open_emoji,
                command=self.open_image,
                font=("Segoe UI Emoji", 12),
            )
            save_btn = tk.Button(
                self.toolbar,
                text=save_emoji,
                command=self.save_image,
                font=("Segoe UI Emoji", 12),
            )
            undo_btn = tk.Button(
                self.toolbar,
                text=undo_emoji,
                command=self.undo,
                font=("Segoe UI Emoji", 12),
            )
            redo_btn = tk.Button(
                self.toolbar,
                text=redo_emoji,
                command=self.redo,
                font=("Segoe UI Emoji", 12),
            )

        open_btn.pack(side=tk.LEFT, padx=2, pady=2)
        save_btn.pack(side=tk.LEFT, padx=2, pady=2)
        undo_btn.pack(side=tk.LEFT, padx=2, pady=2)
        redo_btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Create canvas to display image
        self.canvas = tk.Canvas(self, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def bind_shortcuts(self) -> None:
        """
        Bind keyboard shortcuts to actions.
        """
        self.bind("<Control-o>", lambda event: self.open_image())
        self.bind("<Control-s>", lambda event: self.save_image())
        self.bind("<Control-z>", lambda event: self.undo())
        self.bind("<Control-y>", lambda event: self.redo())

    def open_image(self) -> None:
        """
        Open an image file and display it.
        """
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.ppm;*.heif;*.tiff;*.gif"),
                ("All Files", "*.*"),
            ]
        )
        if file_path:
            self.image = ImageUtils.load_image(file_path)
            if self.image:
                self.history.clear()
                self.history.add_state(self.image.copy())
                self.display_image(self.image)
            else:
                messagebox.showerror("Error", "Unsupported image format.")

    def save_image(self) -> None:
        """
        Save the current image as a copy.
        """
        if self.image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[
                    ("JPEG", "*.jpg;*.jpeg;*.JPG;*.JPEG"),
                    ("PNG", "*.png;*.PNG"),
                    ("Bitmap", "*.bmp;*.BMP"),
                    ("TIFF", "*.tiff;*.tif;*.TIFF;*.TIF"),
                    ("GIF", "*.gif;*.GIF"),
                    ("All Files", "*.*"),
                ],
            )
            if file_path:
                ImageUtils.save_image(self.image, file_path)
                messagebox.showinfo("Image Saved", "Image has been saved successfully.")
        else:
            messagebox.showwarning("No Image", "Please open an image first.")

    def display_image(self, img: Image.Image) -> None:
        """
        Display the image on the canvas.

        Args:
            img (Image.Image): The image to display.
        """
        # Resize image if too big for viewport
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img_width, img_height = img.size

        ratio = min(canvas_width / img_width, canvas_height / img_height, 1)
        display_size = (int(img_width * ratio), int(img_height * ratio))
        resized_img = img.resize(display_size, Image.LANCZOS)

        self.image_display = ImageTk.PhotoImage(resized_img)
        self.canvas.delete("all")
        self.canvas.create_image(
            canvas_width / 2,
            canvas_height / 2,
            image=self.image_display,
            anchor=tk.CENTER,
        )

    def on_resize(self, event) -> None:
        """
        Handle window resize event.
        """
        if self.image:
            self.display_image(self.image)

    def apply_classic_bw(self) -> None:
        """
        Apply classic black and white filter.
        """
        if self.image:
            self.image = self.filters.classic_black_and_white(self.image)
            self.history.add_state(self.image.copy())
            self.display_image(self.image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")

    def apply_high_contrast_bw(self) -> None:
        """
        Apply high contrast black and white filter.
        """
        if self.image:
            self.image = self.filters.high_contrast_black_and_white(self.image)
            self.history.add_state(self.image.copy())
            self.display_image(self.image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")

    def apply_vintage_filter(self) -> None:
        """
        Apply vintage color filter.
        """
        if self.image:
            self.image = self.filters.vintage_filter(self.image)
            self.history.add_state(self.image.copy())
            self.display_image(self.image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")

    def apply_sepia_filter(self) -> None:
        """
        Apply sepia filter.
        """
        if self.image:
            self.image = self.filters.sepia_filter(self.image)
            self.history.add_state(self.image.copy())
            self.display_image(self.image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")

    def apply_solarize_filter(self, threshold: int) -> None:
        """
        Apply solarize filter with specified threshold.
        """
        if self.image:
            self.image = self.filters.solarize(self.image, threshold=threshold)
            self.history.add_state(self.image.copy())
            self.display_image(self.image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")

    def apply_solarize_filter_custom(self) -> None:
        """
        Apply solarize filter with custom threshold.
        """
        threshold = simpledialog.askinteger(
            "Solarize Filter", "Enter threshold (0-255):", minvalue=0, maxvalue=255
        )
        if threshold is not None:
            self.apply_solarize_filter(threshold)

    def apply_posterize_filter(self, bits: int) -> None:
        """
        Apply posterize filter with specified bits.
        """
        if self.image:
            self.image = self.filters.posterize(self.image, bits=bits)
            self.history.add_state(self.image.copy())
            self.display_image(self.image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")

    def apply_posterize_filter_custom(self) -> None:
        """
        Apply posterize filter with custom bits.
        """
        bits = simpledialog.askinteger(
            "Posterize Filter", "Enter number of bits (1-8):", minvalue=1, maxvalue=8
        )
        if bits is not None:
            self.apply_posterize_filter(bits)

    def apply_invert_filter(self) -> None:
        """
        Invert image colors.
        """
        if self.image:
            self.image = self.filters.invert_colors(self.image)
            self.history.add_state(self.image.copy())
            self.display_image(self.image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")

    def apply_sharpen_filter(self) -> None:
        """
        Apply sharpen filter.
        """
        if self.image:
            self.image = self.filters.sharpen(self.image)
            self.history.add_state(self.image.copy())
            self.display_image(self.image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")

    def apply_detail_filter(self) -> None:
        """
        Apply detail enhancement filter.
        """
        if self.image:
            self.image = self.filters.detail(self.image)
            self.history.add_state(self.image.copy())
            self.display_image(self.image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")

    def apply_find_edges_filter(self) -> None:
        """
        Apply edge detection filter.
        """
        if self.image:
            self.image = self.filters.find_edges(self.image)
            self.history.add_state(self.image.copy())
            self.display_image(self.image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")

    def apply_edge_enhance_filter(self) -> None:
        """
        Apply edge enhancement filter.
        """
        if self.image:
            self.image = self.filters.edge_enhance(self.image)
            self.history.add_state(self.image.copy())
            self.display_image(self.image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")

    def apply_emboss_filter(self) -> None:
        """
        Apply emboss filter.
        """
        if self.image:
            self.image = self.filters.emboss(self.image)
            self.history.add_state(self.image.copy())
            self.display_image(self.image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")

    def apply_contour_filter(self) -> None:
        """
        Apply contour filter.
        """
        if self.image:
            self.image = self.filters.contour(self.image)
            self.history.add_state(self.image.copy())
            self.display_image(self.image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")

    def reduce_noise(self) -> None:
        """
        Reduce noise in the image.
        """
        if self.image:
            self.image = self.filters.reduce_noise(self.image)
            self.history.add_state(self.image.copy())
            self.display_image(self.image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")

    def apply_custom_filter(self) -> None:
        """
        Apply a custom filter defined by the user.
        """
        if self.image:
            kernel_size = simpledialog.askinteger(
                "Custom Filter",
                "Enter kernel size (e.g., 3, 5, 7):",
                minvalue=3,
                maxvalue=9,
            )
            if kernel_size and kernel_size % 2 == 1:
                # Open a new window to input kernel values
                kernel_window = tk.Toplevel(self)
                kernel_window.title("Enter Kernel Values")
                entries = []

                for i in range(kernel_size):
                    row_entries = []
                    for j in range(kernel_size):
                        e = tk.Entry(kernel_window, width=5)
                        e.grid(row=i, column=j, padx=2, pady=2)
                        e.insert(0, "0")
                        row_entries.append(e)
                    entries.append(row_entries)

                def apply_kernel():
                    kernel_elements = []
                    for row in entries:
                        for e in row:
                            try:
                                value = float(e.get())
                            except ValueError:
                                messagebox.showerror(
                                    "Invalid Input", "Please enter valid numbers."
                                )
                                return
                            kernel_elements.append(value)
                    kernel_window.destroy()
                    self.image = self.filters.custom_filter(
                        self.image, kernel_elements, kernel_size
                    )
                    self.history.add_state(self.image.copy())
                    self.display_image(self.image)

                apply_button = tk.Button(
                    kernel_window, text="Apply", command=apply_kernel
                )
                apply_button.grid(row=kernel_size, column=0, columnspan=kernel_size)
            else:
                messagebox.showerror(
                    "Invalid Input", "Kernel size must be an odd integer."
                )
        else:
            messagebox.showwarning("No Image", "Please open an image first.")

    def apply_gaussian_blur(self, radius: float) -> None:
        """
        Apply Gaussian blur to the image with specified radius.
        """
        if self.image:
            self.image = self.filters.gaussian_blur(self.image, radius=radius)
            self.history.add_state(self.image.copy())
            self.display_image(self.image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")

    def apply_gaussian_blur_custom(self) -> None:
        """
        Apply Gaussian blur with custom radius.
        """
        radius = simpledialog.askfloat(
            "Gaussian Blur", "Enter radius (e.g., 2.0):", minvalue=0.0
        )
        if radius is not None:
            self.apply_gaussian_blur(radius)

    def apply_box_blur(self, radius: float) -> None:
        """
        Apply box blur to the image with specified radius.
        """
        if self.image:
            self.image = self.filters.box_blur(self.image, radius=radius)
            self.history.add_state(self.image.copy())
            self.display_image(self.image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")

    def apply_box_blur_custom(self) -> None:
        """
        Apply box blur with custom radius.
        """
        radius = simpledialog.askfloat(
            "Box Blur", "Enter radius (e.g., 2.0):", minvalue=0.0
        )
        if radius is not None:
            self.apply_box_blur(radius)

    def add_noise(self, amount: float) -> None:
        """
        Add noise to the image with specified amount.
        """
        if self.image:
            self.image = self.filters.add_noise(self.image, amount=amount)
            self.history.add_state(self.image.copy())
            self.display_image(self.image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")

    def add_noise_custom(self) -> None:
        """
        Add noise with custom amount.
        """
        amount = simpledialog.askfloat(
            "Add Noise", "Enter noise amount (e.g., 64):", minvalue=0.0
        )
        if amount is not None:
            self.add_noise(amount)

    def open_filter_settings(self) -> None:
        """
        Open a window to adjust filter parameters.
        """
        settings_window = tk.Toplevel(self)
        settings_window.title("Filter Settings")
        settings_window.geometry("300x400")

        # Gaussian Blur Radius
        tk.Label(settings_window, text="Gaussian Blur Radius:").pack(pady=5)
        gaussian_blur_radius = tk.Scale(
            settings_window, from_=0.0, to=10.0, resolution=0.1, orient=tk.HORIZONTAL
        )
        gaussian_blur_radius.set(self.parameters["gaussian_blur_radius"])
        gaussian_blur_radius.pack()

        # Box Blur Radius
        tk.Label(settings_window, text="Box Blur Radius:").pack(pady=5)
        box_blur_radius = tk.Scale(
            settings_window, from_=0.0, to=10.0, resolution=0.1, orient=tk.HORIZONTAL
        )
        box_blur_radius.set(self.parameters["box_blur_radius"])
        box_blur_radius.pack()

        # Add Noise Amount
        tk.Label(settings_window, text="Add Noise Amount:").pack(pady=5)
        add_noise_amount = tk.Scale(
            settings_window, from_=0, to=255, resolution=1, orient=tk.HORIZONTAL
        )
        add_noise_amount.set(self.parameters["add_noise_amount"])
        add_noise_amount.pack()

        # Solarize Threshold
        tk.Label(settings_window, text="Solarize Threshold:").pack(pady=5)
        solarize_threshold = tk.Scale(
            settings_window, from_=0, to=255, resolution=1, orient=tk.HORIZONTAL
        )
        solarize_threshold.set(self.parameters["solarize_threshold"])
        solarize_threshold.pack()

        # Posterize Bits
        tk.Label(settings_window, text="Posterize Bits:").pack(pady=5)
        posterize_bits = tk.Scale(
            settings_window, from_=1, to=8, resolution=1, orient=tk.HORIZONTAL
        )
        posterize_bits.set(self.parameters["posterize_bits"])
        posterize_bits.pack()

        def save_settings():
            self.parameters["gaussian_blur_radius"] = gaussian_blur_radius.get()
            self.parameters["box_blur_radius"] = box_blur_radius.get()
            self.parameters["add_noise_amount"] = add_noise_amount.get()
            self.parameters["solarize_threshold"] = solarize_threshold.get()
            self.parameters["posterize_bits"] = posterize_bits.get()
            settings_window.destroy()

        tk.Button(settings_window, text="Save Settings", command=save_settings).pack(
            pady=10
        )

    def undo(self) -> None:
        """
        Undo the last action.
        """
        if self.history.can_undo():
            self.image = self.history.undo()
            self.display_image(self.image)
        else:
            messagebox.showinfo("Undo", "No more actions to undo.")

    def redo(self) -> None:
        """
        Redo the next action.
        """
        if self.history.can_redo():
            self.image = self.history.redo()
            self.display_image(self.image)
        else:
            messagebox.showinfo("Redo", "No more actions to redo.")

    def show_help(self) -> None:
        """
        Display the help information.
        """
        help_text = (
            "Python Image Editor Help\n"
            "Instructions:\n"
            "- Open an image using File > Open Image or the Open button.\n"
            "- Apply filters from the Filters menu.\n"
            "- Adjustable filters have submenus or settings.\n"
            "- Use Undo and Redo to navigate edit history.\n"
            "- Save your image using File > Save As Copy or the Save button.\n"
            "\nFor more information, visit our documentation."
        )
        messagebox.showinfo("Help", help_text)

    def show_about(self) -> None:
        """
        Display the about information.
        """
        about_text = (
            "Python Image Editor\n"
            "Version 1.0\n"
            "Developed using Python and Tkinter.\n"
            "For more information, visit our website."
        )
        messagebox.showinfo("About", about_text)
