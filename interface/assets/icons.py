"""
Icônes encodées en base64 pour l'interface.
"""

import base64
from PIL import Image, ImageDraw
import io

def create_icon(color: str, shape: str = 'circle', size: tuple = (16, 16)) -> str:
    """Crée une icône simple et la retourne en base64."""
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    if shape == 'circle':
        draw.ellipse([2, 2, size[0]-2, size[1]-2], fill=color)
    elif shape == 'square':
        draw.rectangle([2, 2, size[0]-2, size[1]-2], fill=color)
    elif shape == 'triangle':
        draw.polygon([
            (size[0]//2, 2),
            (size[0]-2, size[1]-2),
            (2, size[1]-2)
        ], fill=color)
    
    # Conversion en base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode()

# Création des icônes
FUND_ICON = create_icon('#4CAF50', 'circle')  # Vert
MANAGER_ICON = create_icon('#2196F3', 'square')  # Bleu
COMPOSITION_ICON = create_icon('#FFC107', 'triangle')  # Jaune
DETAIL_ICON = create_icon('#9C27B0', 'circle')  # Violet

def save_icons():
    """Sauvegarde les icônes dans des fichiers."""
    icons = {
        'fund_icon.png': FUND_ICON,
        'manager_icon.png': MANAGER_ICON,
        'composition_icon.png': COMPOSITION_ICON,
        'detail_icon.png': DETAIL_ICON
    }
    
    for filename, b64_data in icons.items():
        img_data = base64.b64decode(b64_data)
        with open(filename, 'wb') as f:
            f.write(img_data)

if __name__ == '__main__':
    save_icons() 