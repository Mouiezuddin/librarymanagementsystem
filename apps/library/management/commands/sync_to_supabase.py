"""
Management command to sync Django data to Supabase
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.library.models import Category, Book, Member, BookIssue, Notification
from apps.library.supabase_client import supabase


class Command(BaseCommand):
    help = 'Sync Django database to Supabase'

    def add_arguments(self, parser):
        parser.add_argument(
            '--model',
            type=str,
            help='Specific model to sync (category, book, member, issue, notification, user)',
        )

    def handle(self, *args, **options):
        model = options.get('model')
        
        # Sync in correct order to respect foreign key constraints
        if not model or model == 'user':
            self.sync_users()
        
        if not model or model == 'category':
            self.sync_categories()
        
        if not model or model == 'book':
            self.sync_books()
        
        if not model or model == 'member':
            self.sync_members()
        
        if not model or model == 'issue':
            self.sync_issues()
        
        if not model or model == 'notification':
            self.sync_notifications()
        
        self.stdout.write(self.style.SUCCESS('Successfully synced data to Supabase'))

    def sync_categories(self):
        self.stdout.write('Syncing categories...')
        categories = Category.objects.all()
        
        for category in categories:
            data = {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'created_at': category.created_at.isoformat(),
            }
            supabase().table('library_category').upsert(data).execute()
        
        self.stdout.write(self.style.SUCCESS(f'Synced {categories.count()} categories'))

    def sync_books(self):
        self.stdout.write('Syncing books...')
        books = Book.objects.all()
        
        for book in books:
            data = {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'isbn': book.isbn,
                'category_id': book.category_id,
                'publisher': book.publisher,
                'publication_year': book.publication_year,
                'total_copies': book.total_copies,
                'available_copies': book.available_copies,
                'shelf_location': book.shelf_location,
                'description': book.description,
                'cover_image': str(book.cover_image) if book.cover_image else None,
                'created_at': book.created_at.isoformat(),
                'updated_at': book.updated_at.isoformat(),
            }
            supabase().table('library_book').upsert(data).execute()
        
        self.stdout.write(self.style.SUCCESS(f'Synced {books.count()} books'))

    def sync_members(self):
        self.stdout.write('Syncing members...')
        members = Member.objects.all()
        
        for member in members:
            data = {
                'id': member.id,
                'member_id': member.member_id,
                'user_id': member.user_id,
                'first_name': member.first_name,
                'last_name': member.last_name,
                'email': member.email,
                'phone': member.phone,
                'address': member.address,
                'membership_type': member.membership_type,
                'status': member.status,
                'date_of_birth': member.date_of_birth.isoformat() if member.date_of_birth else None,
                'join_date': member.join_date.isoformat(),
                'membership_expiry': member.membership_expiry.isoformat() if member.membership_expiry else None,
                'max_books_allowed': member.max_books_allowed,
                'created_at': member.created_at.isoformat(),
            }
            supabase().table('library_member').upsert(data).execute()
        
        self.stdout.write(self.style.SUCCESS(f'Synced {members.count()} members'))

    def sync_issues(self):
        self.stdout.write('Syncing book issues...')
        issues = BookIssue.objects.all()
        
        for issue in issues:
            data = {
                'id': issue.id,
                'member_id': issue.member_id,
                'book_id': issue.book_id,
                'issue_date': issue.issue_date.isoformat(),
                'due_date': issue.due_date.isoformat(),
                'return_date': issue.return_date.isoformat() if issue.return_date else None,
                'status': issue.status,
                'fine_amount': str(issue.fine_amount),
                'fine_paid': issue.fine_paid,
                'remarks': issue.remarks,
                'issued_by_id': issue.issued_by_id,
                'returned_to_id': issue.returned_to_id,
                'created_at': issue.created_at.isoformat(),
            }
            supabase().table('library_bookissue').upsert(data).execute()
        
        self.stdout.write(self.style.SUCCESS(f'Synced {issues.count()} book issues'))

    def sync_notifications(self):
        self.stdout.write('Syncing notifications...')
        notifications = Notification.objects.all()
        
        for notification in notifications:
            data = {
                'id': notification.id,
                'member_id': notification.member_id,
                'message': notification.message,
                'notification_type': notification.notification_type,
                'is_read': notification.is_read,
                'created_at': notification.created_at.isoformat(),
            }
            supabase().table('library_notification').upsert(data).execute()
        
        self.stdout.write(self.style.SUCCESS(f'Synced {notifications.count()} notifications'))

    def sync_users(self):
        self.stdout.write('Syncing users...')
        users = User.objects.all()
        
        for user in users:
            data = {
                'id': user.id,
                'password': user.password,
                'last_login': user.last_login.isoformat() if user.last_login else None,
                'is_superuser': user.is_superuser,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_staff': user.is_staff,
                'is_active': user.is_active,
                'date_joined': user.date_joined.isoformat(),
            }
            supabase().table('auth_user').upsert(data).execute()
        
        self.stdout.write(self.style.SUCCESS(f'Synced {users.count()} users'))
