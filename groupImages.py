from PIL import Image, ImageDraw, ImageFont
import tempfile
import os

def createGroupImage(bkid):
    # Define the text and font
    def textOnImage(text, y, font_size=35, font_path='Assets/MORESUGAR-REGULAR.TTF', font_color='black'):
        font = ImageFont.truetype(font_path, font_size)
        # Calculate the size of the text to be added using textbbox
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Calculate the position to center the text
        image_width, image_height = image.size
        text_position = ((image_width - text_width) // 2, y+10)
        # Define the text color
        if font_color == 'black':
            text_color = (0, 0, 0)  # White color in RGB
        elif font_color == 'white':
            text_color = (255, 255, 255)
        elif font_color == 'tan':
            text_color = (229, 246, 209)

        # Add text to the image
        draw.text(text_position, text, font=font, fill=text_color)


    members = 7
    bal = True
    
    if members == 7 and bal == True:
        template_path = 'Assets/Bal7members.png'
    elif members == 7 and bal == False:
        template_path = 'Assets/Kishore7members.png'
    elif members == 8 and bal == True:
        template_path = 'Assets/Bal8members.png'
    elif members == 8 and bal == False:
        template_path = 'Assets/Kishore8members.png'
    elif members == 9 and bal == True:
        template_path = 'Assets/Bal9members.png'
    elif members == 9 and bal == False:
        template_path = 'Assets/Kishore9members.png'

    
    image = Image.open(template_path)

    # Create a draw object
    draw = ImageDraw.Draw(image)


    
    # textOnImage("Jaibhai Atlanta", 230)
    # textOnImage("Jaibhai Atlanta", 438)
    # textOnImage("Jaibhai Atlanta", 526)
    # textOnImage("Jaibhai Atlanta", 612)
    # textOnImage("Jaibhai Atlanta", 703)
    # textOnImage("Jaibhai Atlanta", 790)
    # textOnImage("Jaibhai Atlanta", 880)
    # textOnImage("Jaibhai Atlanta", 967)



    # textOnImage("Jaibhai", 225)
    # textOnImage("Sahilbhai", 414)
    # textOnImage("Haribhai", 494)
    # textOnImage("Dharikbhai", 572)
    # textOnImage("Nilaybhai", 652)
    # textOnImage("Nischaybhai", 730)
    # textOnImage("Aksharbhai", 810)
    # textOnImage("Gnanbhai Atlanta", 888)
    # textOnImage("Jaibhai Tampa", 966)

    # textOnImage("Dharma dwellers", 10, font_size=65, font_path='Assets/CORESANS.OTF', font_color='tan')
    # textOnImage("Jaibhai Atlanta", 200)
    # textOnImage("Jaibhai Atlanta", 380)
    # textOnImage("Jaibhai Atlanta", 455)
    # textOnImage("Jaibhai Atlanta", 528)
    # textOnImage("Jaibhai Atlanta", 602)
    # textOnImage("Jaibhai Atlanta", 678)
    # textOnImage("Jaibhai Atlanta", 750)
    # textOnImage("Jaibhai Atlanta", 827)
    # textOnImage("Jaibhai Atlanta", 903)
    # textOnImage("Jaibhai Atlanta", 976)


    # Create a temporary file to save the edited image
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        temp_filename = temp_file.name

        # Save the edited image to the temporary file
        image.save(temp_filename)

    return temp_filename
