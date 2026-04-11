import random
from django.core.management.base import BaseCommand  # type: ignore
from apps.library.models import Book, Category  # type: ignore

class Command(BaseCommand):
    help = 'Adds 100 dummy books to the database'

    def handle(self, *args, **options):
        # Ensure we have at least one category to assign books to
        categories = list(Category.objects.all())
        if not categories:
            categories = [Category.objects.create(name="General")]

        prefixes = ["The Art of", "Introduction to", "Advanced", "Mastering", "A Beginner's Guide to", "History of", "Fundamentals of", "Modern", "Exploring"]
        topics = ["Science", "Programming", "History", "Mathematics", "Design", "Psychology", "Technology", "Space", "Economics", "Philosophy", "Art", "Music"]
        authors = ["John Smith", "Jane Doe", "Alan Turing", "Grace Hopper", "Ada Lovelace", "Isaac Newton", "Albert Einstein", "Marie Curie", "Nikola Tesla", "Galileo Galilei"]

        self.stdout.write('Adding 100 dummy books...')
        
        books_created = 0
        for i in range(100):
            # Generate random book data
            title = f"{random.choice(prefixes)} {random.choice(topics)} - Vol {i+1}"
            author = random.choice(authors)
            isbn = f"978-{random.randint(1000000000, 9999999999)}"
            category = random.choice(categories)
            copies = random.randint(1, 15)
            year = random.randint(1980, 2026)
            
            Book.objects.create(
                title=title,
                author=author,
                isbn=isbn,
                category=category,
                publisher="Automated Test Publisher",
                publication_year=year,
                total_copies=copies,
                available_copies=copies,
                shelf_location=f"{category.name[:3].upper()}-{random.randint(1, 100)}",
                description="This is an automatically generated book for testing purposes."
            )
            books_created += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully added {books_created} books.'))
