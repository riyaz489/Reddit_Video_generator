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

    def convert_post_txt_to_representable_lines(self):
        max_lines = 28
        max_chars = 85
    def convert_comment_txt_to_representable_lines(self):
        max_lines = 12
        max_chars = 79

    @staticmethod
    def divide_txt_into_lines(txt, max_chars):
        res = []

        # if there is no space then split word itself
        if len(txt.split(' ')) <= 1:
            while len(txt) > max_chars:
                res.append(txt[:max_chars])
                txt = txt[max_chars:]
            return res

        while len(txt) > max_chars:
            temp = max_chars
            if txt[max_chars] != ' ':
                temp = len(' '.join(txt[:max_chars].split(' ')[:-1]))
            res.append(txt[:temp])
            txt = txt[temp:]
        return res if len(res) > 0 else txt


if __name__ == '__main__':


    print(ImageGenerator.divide_txt_into_lines('sdf '*100, 10))
    # comment
    # max_lines = 12
    # max_chars = 79
    # text = 'd' * 1000000

    #post
    # lines 28
    # MAX CHARS = 85
    # ImageGenerator().generate_image(text, 'out', ImageTypes.Post)