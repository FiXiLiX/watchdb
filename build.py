import json
import sys
import os
# eta 902 105 Denmark
def sanitize_filename(name):
    # Replace spaces and sanitize for filename
    return "".join([c if c.isalnum() or c in ('_', '-') else '_' for c in name]).strip('_')

def main(json_path, template_path):
    # Load JSON data
    with open(json_path, 'r') as f:
        watches = json.load(f)
    
    # Load HTML template
    with open(template_path, 'r') as f:
        template = f.read()
    
    # Create output directory if it doesn't exist
    output_dir = 'dist/watches'
    os.makedirs(output_dir, exist_ok=True)
    
    properties = {
        'NAME': ('name', ''),
        'DESCRIPTION': ('description', ''),
        'COLOR': ('color', 'Boja: '),
        'CASE_SIZE': ('case_size', 'Veličina kućišta: '),
        'MOVEMENT': ('movement', 'Mehanizam: '),
        'COUNTRY': ('country', 'Zemlja porekla: '),
        'PRICE': ('price', 'Cena: '),
        'BRACELET': ('bracelet', 'Narukvica: ')
    }

    for watch_name, watch_data in watches.items():
        content = template.replace('{{HEADING}}', watch_name)
        
        # Replace each property placeholder
        for placeholder, (prop_key, label) in properties.items():
            placeholder_tag = f'{{{{{placeholder}}}}}'
            if prop_key in watch_data:
                if prop_key == "name":
                    replacement = f"{watch_data[prop_key]}"
                elif prop_key == "description":
                    replacement = f"{watch_data[prop_key]}"
                else:
                    replacement = f"<span class='property'>{label}{watch_data[prop_key]}</span>"
            else:
                replacement = ''
            content = content.replace(placeholder_tag, replacement)
        
        slide_links = []
        slide_images = []
        if 'images' in watch_data:
            for index, img_url in enumerate(watch_data['images']):
                slide_number = index + 1
                slide_links.append(f'<a href="#slide-{slide_number}">{slide_number}</a>')
                slide_images.append(
                    f'<div id="slide-{slide_number}">\n'
                    f'    <img class="slide-img" alt="{watch_name}" src="{img_url}">\n'
                    f'</div>'
                )
        
        # Replace slideshow placeholders
        content = content.replace('{{SLIDE}}', '\n'.join(slide_links))
        content = content.replace('{{SLIDE_IMAGES}}', '\n'.join(slide_images))
        
        filename = sanitize_filename(watch_name) + ".html"
        output_path = os.path.join(output_dir, filename)
        
        with open(output_path, 'w', encoding="utf-8") as f:
            f.write(content)
        print(f"Generated: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_json> <path_to_template>")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2])