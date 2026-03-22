"""
Management command: python manage.py seed_data
Creates sample categories, books, and a demo admin user for testing.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import Category, Book
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Seeds the database with sample categories and books for demo purposes.'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding demo data...\n')

        # ── Create superuser ──────────────────────────────────────────
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@vidyaprakashan.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            UserProfile.objects.get_or_create(user=admin)
            self.stdout.write(self.style.SUCCESS('✅ Created superuser: admin / admin123'))
        else:
            self.stdout.write('   Superuser already exists.')

        # ── Create demo user ──────────────────────────────────────────
        if not User.objects.filter(username='testuser').exists():
            demo = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='test1234',
                first_name='Test',
                last_name='Reader'
            )
            UserProfile.objects.get_or_create(user=demo)
            self.stdout.write(self.style.SUCCESS('✅ Created demo user: testuser / test1234'))

        # ── Create categories ─────────────────────────────────────────
        categories_data = [
            {'name': 'Mathematics',      'icon': 'bi-calculator',      'description': 'Algebra, Geometry, Calculus and more'},
            {'name': 'Science',          'icon': 'bi-flask',            'description': 'Physics, Chemistry and Biology'},
            {'name': 'Computer Science', 'icon': 'bi-laptop',           'description': 'Programming, AI, Data Science'},
            {'name': 'History',          'icon': 'bi-hourglass-split',  'description': 'Ancient, Medieval and Modern History'},
            {'name': 'Literature',       'icon': 'bi-book',             'description': 'Hindi, English and Regional Literature'},
            {'name': 'Geography',        'icon': 'bi-globe',            'description': 'World and Indian Geography'},
            {'name': 'Economics',        'icon': 'bi-bar-chart-line',   'description': 'Micro and Macroeconomics'},
            {'name': 'General Knowledge','icon': 'bi-lightbulb',        'description': 'Current Affairs and GK'},
        ]

        categories = {}
        for data in categories_data:
            cat, created = Category.objects.get_or_create(
                name=data['name'],
                defaults={'icon': data['icon'], 'description': data['description']}
            )
            categories[data['name']] = cat
            if created:
                self.stdout.write(f'   📂 Category: {cat.name}')

        # ── Create sample books ───────────────────────────────────────
        books_data = [
            {
                'title': 'Advanced Mathematics Class XII',
                'author': 'R.D. Sharma',
                'category': 'Mathematics',
                'description': 'A comprehensive guide to CBSE Class XII Mathematics covering all chapters with solved examples, exercises, and previous year questions. Ideal for board exam preparation.',
                'price': 450.00,
                'is_featured': True,
                'pages': 850,
                'publisher': 'Vidya Prakashan',
                'publication_year': 2024,
            },
            {
                'title': 'Physics Concepts & Applications',
                'author': 'H.C. Verma',
                'category': 'Science',
                'description': 'Concepts of Physics covers the complete syllabus for IIT-JEE and CBSE. Every concept is explained with diagrams, derivations, and a large number of solved problems.',
                'price': 599.00,
                'is_featured': True,
                'pages': 1100,
                'publisher': 'Vidya Prakashan',
                'publication_year': 2024,
            },
            {
                'title': 'Python Programming for Beginners',
                'author': 'Guido van Learning',
                'category': 'Computer Science',
                'description': 'A beginner-friendly introduction to Python programming. Covers variables, loops, functions, OOP, file handling, and projects with hands-on exercises throughout.',
                'price': 350.00,
                'is_featured': True,
                'pages': 420,
                'publisher': 'Vidya Prakashan',
                'publication_year': 2023,
            },
            {
                'title': 'Modern Indian History',
                'author': 'Bipin Chandra',
                'category': 'History',
                'description': 'An authoritative account of India\'s freedom struggle and post-independence history. Essential reading for UPSC Civil Services and competitive examinations.',
                'price': 320.00,
                'is_featured': False,
                'pages': 680,
                'publisher': 'Vidya Prakashan',
                'publication_year': 2023,
            },
            {
                'title': 'Organic Chemistry Simplified',
                'author': 'O.P. Tandon',
                'category': 'Science',
                'description': 'Complete organic chemistry for medical and engineering entrance examinations. Covers all reaction mechanisms, named reactions, and stereochemistry with clarity.',
                'price': 480.00,
                'is_featured': True,
                'pages': 760,
                'publisher': 'Vidya Prakashan',
                'publication_year': 2024,
            },
            {
                'title': 'Indian Geography: A Complete Study',
                'author': 'Majid Husain',
                'category': 'Geography',
                'description': 'Comprehensive coverage of Indian and World Geography for competitive examinations including UPSC, SSC, and State PCS exams. Includes maps, tables, and diagrams.',
                'price': 395.00,
                'is_featured': False,
                'pages': 540,
                'publisher': 'Vidya Prakashan',
                'publication_year': 2024,
            },
            {
                'title': 'Data Structures & Algorithms',
                'author': 'Thomas H. Cormen',
                'category': 'Computer Science',
                'description': 'The definitive guide to algorithms and data structures. Covers sorting, searching, graphs, dynamic programming, and complexity analysis with rigorous proofs.',
                'price': 699.00,
                'is_featured': True,
                'pages': 1310,
                'publisher': 'Vidya Prakashan',
                'publication_year': 2023,
            },
            {
                'title': 'Microeconomics: Theory & Practice',
                'author': 'N. Gregory Mankiw',
                'category': 'Economics',
                'description': 'A student-friendly introduction to microeconomic principles. Covers supply and demand, market structures, consumer theory, and welfare economics with Indian case studies.',
                'price': 425.00,
                'is_featured': False,
                'pages': 590,
                'publisher': 'Vidya Prakashan',
                'publication_year': 2024,
            },
        ]

        for data in books_data:
            cat_name = data.pop('category')
            cat = categories.get(cat_name)
            book, created = Book.objects.get_or_create(
                title=data['title'],
                defaults={**data, 'category': cat, 'language': 'English', 'stock': 100, 'is_active': True}
            )
            if created:
                self.stdout.write(f'   📖 Book: {book.title}')

        self.stdout.write(self.style.SUCCESS('\n🎉 Demo data seeded successfully!\n'))
        self.stdout.write('   Login at /accounts/login/ with:')
        self.stdout.write('   Admin:    admin / admin123')
        self.stdout.write('   User:     testuser / test1234')
        self.stdout.write('   Admin Panel: /adminpanel/')
        self.stdout.write('   Django Admin: /django-admin/\n')
