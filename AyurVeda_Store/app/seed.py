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
                image_url='https://images.unsplash.com/photo-1615485500704-8e990f9900f7?w=400&h=300&fit=crop', is_featured=True),
        Product(name='Triphala Churna', description='Classic Ayurvedic blend of three fruits — Amalaki, Bibhitaki, Haritaki. Supports digestion and detoxification.',
                price=199, original_price=249, stock=200, category_id=ayur.id, unit='200g pack',
                image_url='https://images.unsplash.com/photo-1601055903647-ddf1ee9701b7?w=400&h=300&fit=crop', is_featured=True),
        Product(name='Brahmi Oil', description='Cold-pressed Brahmi oil for hair growth, scalp nourishment, and mental clarity. Traditionally prepared.',
                price=349, original_price=450, stock=80, category_id=ayur.id, unit='100ml bottle',
                image_url='https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=400&h=300&fit=crop', is_featured=False),
        Product(name='Neem Leaf Capsules', description='Pure Neem extract capsules for blood purification, skin health, and anti-bacterial benefits.',
                price=249, original_price=299, stock=120, category_id=ayur.id, unit='60 capsules',
                image_url='https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&h=300&fit=crop', is_featured=False),
        Product(name='Tulsi Green Tea', description='Organic Tulsi (Holy Basil) green tea for immunity, stress relief, and respiratory health.',
                price=179, original_price=220, stock=300, category_id=ayur.id, unit='25 tea bags',
                image_url='https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=400&h=300&fit=crop', is_featured=True),
        Product(name='Chyawanprash', description='Traditional Ayurvedic immunity booster with over 40 herbs. Rich in Amla (Vitamin C). Suitable for all ages.',
                price=449, original_price=550, stock=90, category_id=ayur.id, unit='500g jar',
                image_url='https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop', is_featured=True),
        Product(name='Turmeric Powder (Haldi)', description='Pure organic turmeric with high curcumin content. Anti-inflammatory, antioxidant, and immunity boosting.',
                price=149, original_price=180, stock=500, category_id=ayur.id, unit='500g pack',
                image_url='https://images.unsplash.com/photo-1506368249639-73a05d6f6488?w=400&h=300&fit=crop', is_featured=False),
        Product(name='Arjuna Bark Powder', description='Heart tonic — Arjuna bark powder supports cardiovascular health, blood pressure, and circulation.',
                price=269, original_price=320, stock=100, category_id=ayur.id, unit='200g pack',
                image_url='https://images.unsplash.com/photo-1448375240586-882707db888b?w=400&h=300&fit=crop', is_featured=False),
        # Agricultural
        Product(name='Organic Basmati Rice', description='Premium long-grain aged Basmati rice. Naturally grown without pesticides. Aromatic and fluffy when cooked.',
                price=599, original_price=750, stock=200, category_id=agri.id, unit='5kg bag',
                image_url='https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop', is_featured=True),
        Product(name='Cold-Pressed Mustard Oil', description='Traditional wooden-press extracted mustard oil. Rich in omega-3, ideal for cooking and massage.',
                price=399, original_price=480, stock=150, category_id=agri.id, unit='1 litre',
                image_url='https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400&h=300&fit=crop', is_featured=True),
        Product(name='Hybrid Tomato Seeds', description='High-yield F1 hybrid tomato seeds. Disease-resistant, suitable for all seasons. 95% germination rate.',
                price=89, original_price=120, stock=500, category_id=agri.id, unit='10g packet',
                image_url='https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=400&h=300&fit=crop', is_featured=False),
        Product(name='Organic Vermicompost', description='100% natural earthworm compost. Improves soil fertility, water retention, and crop yield.',
                price=249, original_price=300, stock=300, category_id=agri.id, unit='5kg bag',
                image_url='https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&h=300&fit=crop', is_featured=False),
        Product(name='Raw Honey (Forest)', description='Pure unprocessed forest honey collected from wild beehives. Rich in enzymes, antioxidants, and natural sugars.',
                price=699, original_price=850, stock=60, category_id=agri.id, unit='500g jar',
                image_url='https://images.unsplash.com/photo-1471193945509-9ad0617afabf?w=400&h=300&fit=crop', is_featured=True),
        Product(name='A2 Desi Cow Ghee', description='Made from milk of indigenous Gir cows using traditional Bilona method. Pure, grainy texture, rich aroma.',
                price=899, original_price=1100, stock=40, category_id=agri.id, unit='500ml jar',
                image_url='https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400&h=300&fit=crop', is_featured=True),
        Product(name='Neem Cake Fertilizer', description='Organic neem seed cake fertilizer. Controls soil pests, nematodes, and improves nitrogen retention.',
                price=199, original_price=250, stock=400, category_id=agri.id, unit='2kg bag',
                image_url='https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=400&h=300&fit=crop', is_featured=False),
        Product(name='Toor Dal (Organic)', description='Organically grown split pigeon peas. High protein, no preservatives, direct from farm.',
                price=329, original_price=400, stock=180, category_id=agri.id, unit='1kg pack',
                image_url='https://images.unsplash.com/photo-1598955907890-7aaf2e36b3dc?w=400&h=300&fit=crop', is_featured=False),
    ]
    db.session.add_all(products)

    admin = User(name='Admin', email='admin@ayurvedastore.com', is_admin=True)
    admin.set_password('admin123')
    db.session.add(admin)

    db.session.commit()
