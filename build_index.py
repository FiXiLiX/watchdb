import json
import sys
import os

def sanitize_filename(name):
    return "".join([c if c.isalnum() or c in ('_', '-') else '_' for c in name]).strip('_')

def generate_index(json_path, template_path):
    # Load watch data
    with open(json_path, 'r') as f:
        watches = json.load(f)
    
    # Load index template
    with open(template_path, 'r') as f:
        template = f.read()
    
    generated_cards = []
    
    for watch_key, watch_data in watches.items():
        # Get first image or empty string if none
        image_url = watch_data.get('images', [''])[0]
        
        # Generate sanitized key for HTML IDs
        safe_key = sanitize_filename(watch_key)
        
        card_html = f"""
        <div class="watch-card">
            <div class="email-item email-item-selected pure-g featured" id="menu-{safe_key}" data-id="{safe_key}" onclick="openWatch('{safe_key}')">
                <div class="pure-u">
                    <img width="128 height="128" alt="{watch_data['name']}" style="aspect-ratio: 1 / 1; object-fit: cover;" class="email-avatar" src="{image_url}">
                </div>
        
                <div class="pure-u-3-4">
                    <h5 class="email-name">{watch_data.get('country', '')}</h5>
                    <h4 class="email-subject">{watch_data['name']}</h4>
                    <p class="email-desc">
                        {watch_data.get('price', '')}
                    </p>
                </div>
            </div>
        </div>
        """
        generated_cards.append(card_html)
    
    # Join all cards and insert into template
    final_content = template.replace('{{watches}}', '\n'.join(generated_cards))
    
    # Save index.html
    with open('dist/index.html', 'w') as f:
        f.write(final_content)
    print("Generated index.html successfully!")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_index.py <path_to_json> <path_to_index_template>")
        sys.exit(1)
    
    generate_index(sys.argv[1], sys.argv[2])