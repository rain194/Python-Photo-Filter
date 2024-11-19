"""
Implements all filter functions.
"""

from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import numpy as np
from typing import List

class Filters:
    """
    Class containing methods to apply various filters to images.
    """

    def classic_black_and_white(self, img: Image.Image) -> Image.Image:
        """
        Convert image to classic black and white.

        Args:
            img (Image.Image): Original image.

        Returns:
            Image.Image: Black and white image.
        """
        return img.convert("L").convert("RGB")

    def high_contrast_black_and_white(self, img: Image.Image) -> Image.Image:
        """
        Convert image to high contrast black and white.

        Args:
            img (Image.Image): Original image.

        Returns:
            Image.Image: High contrast black and white image.
        """
        img = img.convert("L")
        img = ImageOps.autocontrast(img)
        return img.convert("RGB")

    def vintage_filter(self, img: Image.Image) -> Image.Image:
        """
        Apply a vintage filter to the image.

        Args:
            img (Image.Image): Original image.

        Returns:
            Image.Image: Image with vintage filter applied.
        """
        img = ImageOps.colorize(img.convert("L"), black="#704214", white="#C0A080")
        return img

    def sepia_filter(self, img: Image.Image) -> Image.Image:
        """
        Apply a sepia filter to the image.

        Args:
            img (Image.Image): Original image.

        Returns:
            Image.Image: Image with sepia filter applied.
        """
        sepia = np.array(img.convert("RGB"))
        tr = [0.393, 0.769, 0.189]
        tg = [0.349, 0.686, 0.168]
        tb = [0.272, 0.534, 0.131]
        r = sepia[:, :, 0] * tr[0] + sepia[:, :, 1] * tr[1] + sepia[:, :, 2] * tr[2]
        g = sepia[:, :, 0] * tg[0] + sepia[:, :, 1] * tg[1] + sepia[:, :, 2] * tg[2]
        b = sepia[:, :, 0] * tb[0] + sepia[:, :, 1] * tb[1] + sepia[:, :, 2] * tb[2]
        sepia[:, :, 0] = np.clip(r, 0, 255)
        sepia[:, :, 1] = np.clip(g, 0, 255)
        sepia[:, :, 2] = np.clip(b, 0, 255)
        return Image.fromarray(sepia.astype('uint8'))

    def custom_filter(self, img: Image.Image, kernel_elements: List[float], kernel_size: int) -> Image.Image:
        """
        Apply a custom filter defined by a kernel.

        Args:
            img (Image.Image): Original image.
            kernel_elements (List[float]): Elements of the kernel.
            kernel_size (int): Size of the kernel.

        Returns:
            Image.Image: Filtered image.
        """
        kernel = ImageFilter.Kernel(
            size=(kernel_size, kernel_size),
            kernel=kernel_elements,
            scale=sum(kernel_elements) or 1,
            offset=0
        )
        return img.filter(kernel)

    def gaussian_blur(self, img: Image.Image, radius: float = 2.0) -> Image.Image:
        """
        Apply Gaussian blur to the image.

        Args:
            img (Image.Image): Original image.
            radius (float): Radius of the blur.

        Returns:
            Image.Image: Blurred image.
        """
        return img.filter(ImageFilter.GaussianBlur(radius=radius))

    def box_blur(self, img: Image.Image, radius: float = 2.0) -> Image.Image:
        """
        Apply box blur to the image.

        Args:
            img (Image.Image): Original image.
            radius (float): Radius of the blur.

        Returns:
            Image.Image: Blurred image.
        """
        return img.filter(ImageFilter.BoxBlur(radius=radius))

    def add_noise(self, img: Image.Image, amount: float = 64) -> Image.Image:
        """
        Add random noise to the image.

        Args:
            img (Image.Image): Original image.
            amount (float): The maximum noise to add.

        Returns:
            Image.Image: Image with noise added.
        """
        np_img = np.array(img)
        noise = np.random.randint(-amount, amount + 1, np_img.shape).astype('int16')
        np_img = np_img.astype('int16') + noise
        np_img = np.clip(np_img, 0, 255)
        return Image.fromarray(np_img.astype('uint8'))

    def sharpen(self, img: Image.Image) -> Image.Image:
        """
        Apply sharpen filter to the image.

        Args:
            img (Image.Image): Original image.

        Returns:
            Image.Image: Sharpened image.
        """
        return img.filter(ImageFilter.SHARPEN)

    def detail(self, img: Image.Image) -> Image.Image:
        """
        Enhance the detail of the image.

        Args:
            img (Image.Image): Original image.

        Returns:
            Image.Image: Image with enhanced detail.
        """
        return img.filter(ImageFilter.DETAIL)

    def find_edges(self, img: Image.Image) -> Image.Image:
        """
        Apply edge detection filter to the image.

        Args:
            img (Image.Image): Original image.

        Returns:
            Image.Image: Image with edges highlighted.
        """
        return img.filter(ImageFilter.FIND_EDGES)

    def edge_enhance(self, img: Image.Image) -> Image.Image:
        """
        Enhance the edges of the image.

        Args:
            img (Image.Image): Original image.

        Returns:
            Image.Image: Image with edges enhanced.
        """
        return img.filter(ImageFilter.EDGE_ENHANCE_MORE)

    def solarize(self, img: Image.Image, threshold: int = 128) -> Image.Image:
        """
        Apply solarize effect to the image.

        Args:
            img (Image.Image): Original image.
            threshold (int): Threshold value for solarization.

        Returns:
            Image.Image: Solarized image.
        """
        return ImageOps.solarize(img, threshold=threshold)

    def posterize(self, img: Image.Image, bits: int = 4) -> Image.Image:
        """
        Apply posterize effect to the image.

        Args:
            img (Image.Image): Original image.
            bits (int): Number of bits to keep for each color channel.

        Returns:
            Image.Image: Posterized image.
        """
        return ImageOps.posterize(img, bits=bits)

    def invert_colors(self, img: Image.Image) -> Image.Image:
        """
        Invert the colors of the image.

        Args:
            img (Image.Image): Original image.

        Returns:
            Image.Image: Image with inverted colors.
        """
        return ImageOps.invert(img)

    def emboss(self, img: Image.Image) -> Image.Image:
        """
        Apply emboss filter to the image.

        Args:
            img (Image.Image): Original image.

        Returns:
            Image.Image: Embossed image.
        """
        return img.filter(ImageFilter.EMBOSS)

    def contour(self, img: Image.Image) -> Image.Image:
        """
        Apply contour filter to the image.

        Args:
            img (Image.Image): Original image.

        Returns:
            Image.Image: Contoured image.
        """
        return img.filter(ImageFilter.CONTOUR)

    def reduce_noise(self, img: Image.Image) -> Image.Image:
        """
        Reduce noise in the image using a median filter.

        Args:
            img (Image.Image): Original image.

        Returns:
            Image.Image: Image with reduced noise.
        """
        return img.filter(ImageFilter.MedianFilter(size=3))
