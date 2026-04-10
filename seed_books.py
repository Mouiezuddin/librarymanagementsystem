import os
import django
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')
django.setup()

from library.models import Book, Category

def seed_library():
    print("🚀 Initializing Nexa Lib Seeding...")
    
    # 1. Define Categories
    categories_names = ["Computer Science", "Business Management", "Commerce", "AI"]
    categories = {}
    for name in categories_names:
        cat, _ = Category.objects.get_or_create(name=name)
        categories[name] = cat
        print(f"✅ Verified Category: {name}")

    # 2. Define Patterns for Real-Sounding Titles
    cs_patterns = ["Algorithms in {v}", "Advanced {v}", "{v} for Professionals", "Mastering {v}", "The Future of {v}"]
    cs_topics = ["Python", "Java", "Web Development", "Cyber Security", "Database Systems", "Cloud Computing", "Software Architecture"]
    
    ai_patterns = ["Deep Learning and {v}", "The Ethics of {v}", "Neural Networks: {v}", "{v} in Modern World", "Practical {v}"]
    ai_topics = ["NLP", "Robotics", "Computer Vision", "Reinforced Learning", "Generative AI", "Statistical Modeling", "Autonomous Systems"]
    
    biz_patterns = ["Essentials of {v}", "Strategic {v}", "Modern {v}", "Leaders in {v}", "The {v} Playbook"]
    biz_topics = ["Leadership", "Operations", "Finance", "Strategy", "Global Marketing", "Organizational Behavior", "Supply Chain"]
    
    comm_patterns = ["Fundamentals of {v}", "International {v}", "Digital {v}", "{v} & Trade", "{v} Law Essentials"]
    comm_topics = ["E-Commerce", "Logistics", "Economics", "Stock Markets", "Banking", "Accounting", "Taxation"]

    # 3. Generate 500 Books (125 per category)
    books_to_add = []
    authors = ["Robert Martin", "Andrew Ng", "Geoffrey Hinton", "Simon Sinek", "Adam Smith", "Michael Porter", "Satya Nadella", "Sam Altman", "Peter Drucker", "Donald Knuth", "Linus Torvalds"]

    topic_map = {
        "Computer Science": (cs_patterns, cs_topics),
        "AI": (ai_patterns, ai_topics),
        "Business Management": (biz_patterns, biz_topics),
        "Commerce": (comm_patterns, comm_topics)
    }

    for cat_name, (patterns, topics) in topic_map.items():
        cat = categories[cat_name]
        print(f"📖 Generating 125 books for {cat_name}...")
        for i in range(1, 126):
            title = random.choice(patterns).format(v=random.choice(topics))
            title = f"{title} (Vol. {i})"
            
            copies = random.randint(2, 15)
            books_to_add.append(Book(
                title=title,
                author=random.choice(authors),
                category=cat,
                isbn=f"978-{random.randint(100, 999)}-{random.randint(1000, 9999)}-{random.randint(0, 9)}",
                publisher="Nexa Lib Press",
                publication_year=random.randint(2018, 2024),
                total_copies=copies,
                available_copies=copies,
                shelf_location=f"Floor {random.randint(1, 4)}, Rack {random.choice(['A','B','C','D'])}{random.randint(1,20)}"
            ))

    # 4. Perform Bulk Create
    print(f"⚡ Bulk injecting 500 books...")
    # Using ignore_conflicts=True just in case of random ISBN collision
    Book.objects.bulk_create(books_to_add, ignore_conflicts=True)
    print("✨ Successfully seeded 500 books into Nexa Lib archives!")

if __name__ == "__main__":
    seed_library()
