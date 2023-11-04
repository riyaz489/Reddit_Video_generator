from enum import Enum

from PIL import Image, ImageDraw, ImageFont


class ImageTypes(Enum):
    Comment = 'Comment'
    Post = 'Post'


class ImageGenerator:
    def __init__(self, font_size=20, font='arial.ttf'):
        self.post_template = 'templates/post.png'
        self.comment_template = 'templates/comment.png'
        self.font_size = font_size
        self.font = font

    def generate_image(self, text: str, output_file_name: str, image_type: ImageTypes):

        template = self.comment_template if image_type == ImageTypes.Comment else self.post_template
        # Define the text to be written and font settings
        font = ImageFont.truetype(self.font, self.font_size)  # Replace with the path to your font file
        # Load the image template
        image = Image.open(template)  # Replace with your image file

        # Create a drawing context
        draw = ImageDraw.Draw(image)

        # Define the position to place the text (in pixels)
        text_position = (100, 100)

        # Define the text color
        text_color = (255, 255, 255)  # RGB color

        # Write the text onto the image
        draw.text(text_position, text, fill=text_color, font=font)

        # Save the modified image
        image.save(f'image_output/{output_file_name}.png')  # Replace with your desired output file name

