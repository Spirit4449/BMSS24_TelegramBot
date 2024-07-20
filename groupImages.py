from PIL import Image, ImageDraw, ImageFont
import tempfile

def createGroupImage(members, bal, groupName, groupLead):
    print(members, bal, groupName, groupLead)

    # Define the font and color
    def textOnImage(text, y, font_size=35, font_path='Assets/MORESUGAR-REGULAR.TTF', font_color='black'):
        font = ImageFont.truetype(font_path, font_size)
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        image_width, _ = image.size
        text_position = ((image_width - text_width) // 2, y + 10)

        color_map = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'tan': (229, 246, 209)
        }
        text_color = color_map.get(font_color, (0, 0, 0))  # Default to black if color is not found

        draw.text(text_position, text, font=font, fill=text_color)

    # Map (number of members, bal) to template path
    template_map = {
        (8, True): 'Assets/Bal7members.png',
        (8, False): 'Assets/Kishore7members.png',
        (9, True): 'Assets/Bal8members.png',
        (9, False): 'Assets/Kishore8members.png',
        (10, True): 'Assets/Bal9members.png',
        (10, False): 'Assets/Kishore9members.png'
    }

    # Get the template path based on the number of members and bal status
    template_path = template_map.get((len(members), bal))
    if not template_path:
        raise ValueError("No template found for the given number of members and bal status")

    # Open the template image
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)

    # Define y positions based on the number of members
    y_positions = {
        8: [230, 438, 526, 612, 703, 790, 880, 960],
        9: [225, 414, 494, 572, 652, 730, 810, 888, 968],
        10: [200, 380, 455, 528, 602, 678, 750, 827, 903, 983]
    }

    # Add the group name
    textOnImage(groupName, 10, font_size=65, font_path='Assets/CORESANS.OTF', font_color='tan')

    # Check if the group lead is in the members and update positions accordingly
    if groupLead in members:
        members.remove(groupLead)
        members.insert(0, groupLead)  # Move the group lead to the front

    # Add member names
    for i, member in enumerate(members):
        if i < len(y_positions[len(members)]):  # Ensure we do not go out of bounds
            textOnImage(member, y_positions[len(members)][i])

    # Save the edited image to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        temp_filename = temp_file.name
        image.save(temp_filename)

    return temp_filename
