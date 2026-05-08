from app.models import Category, Product, User
from app import db


def seed_data():
    if Category.query.first():
        return

    categories = [
        Category(name='Ayurvedic Products', slug='ayurvedic',
                 description='Pure and natural Ayurvedic herbs, oils, and medicines', icon='spa'),
        Category(name='Agricultural Products', slug='agricultural',
                 description='Fresh farm produce, seeds, and organic fertilizers', icon='grass'),
    ]
    db.session.add_all(categories)
    db.session.flush()

    ayur = Category.query.filter_by(slug='ayurvedic').first()
    agri = Category.query.filter_by(slug='agricultural').first()

    products = [
        # Ayurvedic
        Product(name='Ashwagandha Root Powder', description='Pure Ashwagandha root powder known for stress relief, immunity boost, and energy. 100% organic, no additives.',
                price=299, original_price=399, stock=150, category_id=ayur.id, unit='250g pack',
                image_url='https://placehold.co/400x300/2d6a4f/white?text=Ashwagandha', is_featured=True),
        Product(name='Triphala Churna', description='Classic Ayurvedic blend of three fruits — Amalaki, Bibhitaki, Haritaki. Supports digestion and detoxification.',
                price=199, original_price=249, stock=200, category_id=ayur.id, unit='200g pack',
                image_url='https://placehold.co/400x300/2d6a4f/white?text=Triphala', is_featured=True),
        Product(name='Brahmi Oil', description='Cold-pressed Brahmi oil for hair growth, scalp nourishment, and mental clarity. Traditionally prepared.',
                price=349, original_price=450, stock=80, category_id=ayur.id, unit='100ml bottle',
                image_url='https://placehold.co/400x300/2d6a4f/white?text=Brahmi+Oil', is_featured=False),
        Product(name='Neem Leaf Capsules', description='Pure Neem extract capsules for blood purification, skin health, and anti-bacterial benefits.',
                price=249, original_price=299, stock=120, category_id=ayur.id, unit='60 capsules',
                image_url='https://placehold.co/400x300/2d6a4f/white?text=Neem+Caps', is_featured=False),
        Product(name='Tulsi Green Tea', description='Organic Tulsi (Holy Basil) green tea for immunity, stress relief, and respiratory health.',
                price=179, original_price=220, stock=300, category_id=ayur.id, unit='25 tea bags',
                image_url='https://placehold.co/400x300/2d6a4f/white?text=Tulsi+Tea', is_featured=True),
        Product(name='Chyawanprash', description='Traditional Ayurvedic immunity booster with over 40 herbs. Rich in Amla (Vitamin C). Suitable for all ages.',
                price=449, original_price=550, stock=90, category_id=ayur.id, unit='500g jar',
                image_url='https://placehold.co/400x300/2d6a4f/white?text=Chyawanprash', is_featured=True),
        Product(name='Turmeric Powder (Haldi)', description='Pure organic turmeric with high curcumin content. Anti-inflammatory, antioxidant, and immunity boosting.',
                price=149, original_price=180, stock=500, category_id=ayur.id, unit='500g pack',
                image_url='https://placehold.co/400x300/2d6a4f/white?text=Turmeric', is_featured=False),
        Product(name='Arjuna Bark Powder', description='Heart tonic — Arjuna bark powder supports cardiovascular health, blood pressure, and circulation.',
                price=269, original_price=320, stock=100, category_id=ayur.id, unit='200g pack',
                image_url='https://placehold.co/400x300/2d6a4f/white?text=Arjuna', is_featured=False),
        # Agricultural
        Product(name='Organic Basmati Rice', description='Premium long-grain aged Basmati rice. Naturally grown without pesticides. Aromatic and fluffy when cooked.',
                price=599, original_price=750, stock=200, category_id=agri.id, unit='5kg bag',
                image_url='https://placehold.co/400x300/52b788/white?text=Basmati+Rice', is_featured=True),
        Product(name='Cold-Pressed Mustard Oil', description='Traditional wooden-press extracted mustard oil. Rich in omega-3, ideal for cooking and massage.',
                price=399, original_price=480, stock=150, category_id=agri.id, unit='1 litre',
                image_url='https://placehold.co/400x300/52b788/white?text=Mustard+Oil', is_featured=True),
        Product(name='Hybrid Tomato Seeds', description='High-yield F1 hybrid tomato seeds. Disease-resistant, suitable for all seasons. 95% germination rate.',
                price=89, original_price=120, stock=500, category_id=agri.id, unit='10g packet',
                image_url='https://placehold.co/400x300/52b788/white?text=Tomato+Seeds', is_featured=False),
        Product(name='Organic Vermicompost', description='100% natural earthworm compost. Improves soil fertility, water retention, and crop yield.',
                price=249, original_price=300, stock=300, category_id=agri.id, unit='5kg bag',
                image_url='https://placehold.co/400x300/52b788/white?text=Vermicompost', is_featured=False),
        Product(name='Raw Honey (Forest)', description='Pure unprocessed forest honey collected from wild beehives. Rich in enzymes, antioxidants, and natural sugars.',
                price=699, original_price=850, stock=60, category_id=agri.id, unit='500g jar',
                image_url='https://placehold.co/400x300/52b788/white?text=Forest+Honey', is_featured=True),
        Product(name='A2 Desi Cow Ghee', description='Made from milk of indigenous Gir cows using traditional Bilona method. Pure, grainy texture, rich aroma.',
                price=899, original_price=1100, stock=40, category_id=agri.id, unit='500ml jar',
                image_url='https://placehold.co/400x300/52b788/white?text=A2+Ghee', is_featured=True),
        Product(name='Neem Cake Fertilizer', description='Organic neem seed cake fertilizer. Controls soil pests, nematodes, and improves nitrogen retention.',
                price=199, original_price=250, stock=400, category_id=agri.id, unit='2kg bag',
                image_url='https://placehold.co/400x300/52b788/white?text=Neem+Cake', is_featured=False),
        Product(name='Toor Dal (Organic)', description='Organically grown split pigeon peas. High protein, no preservatives, direct from farm.',
                price=329, original_price=400, stock=180, category_id=agri.id, unit='1kg pack',
                image_url='https://placehold.co/400x300/52b788/white?text=Toor+Dal', is_featured=False),
    ]
    db.session.add_all(products)

    admin = User(name='Admin', email='admin@ayurvedastore.com', is_admin=True)
    admin.set_password('admin123')
    db.session.add(admin)

    db.session.commit()
