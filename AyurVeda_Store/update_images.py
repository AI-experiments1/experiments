"""Fix incorrect / duplicate product image URLs in the database."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import Product

# Only the products whose images were confirmed wrong (person, watermelon, broccoli, animal, duplicates)
CORRECTED = {
    # was iced-drink / kombucha → proper herbal green-tea cup
    'Tulsi Green Tea':
        'https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=400&h=300&fit=crop',
    # was a person photo → ayurvedic herbal product jar
    'Chyawanprash':
        'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop',
    # was a watermelon → golden honey drizzle (famous Unsplash honey photo)
    'Raw Honey (Forest)':
        'https://images.unsplash.com/photo-1471193945509-9ad0617afabf?w=400&h=300&fit=crop',
    # was broccoli → yellow turmeric / golden spice powder
    'Turmeric Powder (Haldi)':
        'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=400&h=300&fit=crop',
    # was showing cherries → bark / brown herbal powder bowl
    'Arjuna Bark Powder':
        'https://images.unsplash.com/photo-1550258987-190a2d41a8ba?w=400&h=300&fit=crop',
    # was an animal photo → yellow split lentils / pigeon peas
    'Toor Dal (Organic)':
        'https://images.unsplash.com/photo-1598955907890-7aaf2e36b3dc?w=400&h=300&fit=crop',
    # was identical to Vermicompost → distinct neem / organic-matter image
    'Neem Cake Fertilizer':
        'https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=400&h=300&fit=crop',
}

app = create_app()
with app.app_context():
    updated = []
    for name, url in CORRECTED.items():
        p = Product.query.filter_by(name=name).first()
        if p:
            p.image_url = url
            updated.append(name)
        else:
            print(f'  [WARN] Product not found: {name}')
    db.session.commit()
    print(f'Updated {len(updated)} product image(s):')
    for n in updated:
        print(f'  ✓  {n}')
