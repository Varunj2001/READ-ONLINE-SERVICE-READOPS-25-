"""
Management command to add sample digital books
"""

from django.core.management.base import BaseCommand
from libapp.models import DigitalBook


class Command(BaseCommand):
    help = 'Add sample digital books to the database'

    def handle(self, *args, **options):
        # Sample digital books data
        digital_books = [
            {
                'title': 'Bhagavad Gita - Complete Text',
                'author': 'Vyasa',
                'description': 'The Bhagavad Gita, often referred to as the Gita, is a 700-verse Hindu scripture that is part of the epic Mahabharata. It is a conversation between Prince Arjuna and Lord Krishna, who serves as his charioteer.',
                'book_type': 'RELIGIOUS',
                'category': 'Hindu Scriptures',
                'online_reading_price': 50.00,
                'download_price': 100.00,
                'is_free': False,
            },
            {
                'title': 'Ramayana - Bala Kanda',
                'author': 'Valmiki',
                'description': 'The first book of the Ramayana, describing the birth and early life of Lord Rama, his marriage to Sita, and the beginning of his journey.',
                'book_type': 'RELIGIOUS',
                'category': 'Hindu Scriptures',
                'online_reading_price': 50.00,
                'download_price': 100.00,
                'is_free': False,
            },
            {
                'title': 'Mahabharata - Adi Parva',
                'author': 'Vyasa',
                'description': 'The first book of the Mahabharata, containing the story of the Kuru dynasty and the events leading to the great war.',
                'book_type': 'RELIGIOUS',
                'category': 'Hindu Scriptures',
                'online_reading_price': 50.00,
                'download_price': 100.00,
                'is_free': False,
            },
            {
                'title': 'Vedas - Rig Veda Samhita',
                'author': 'Ancient Sages',
                'description': 'The oldest of the four Vedas, containing hymns and mantras that form the foundation of Hindu philosophy and spirituality.',
                'book_type': 'RELIGIOUS',
                'category': 'Vedic Literature',
                'online_reading_price': 50.00,
                'download_price': 100.00,
                'is_free': False,
            },
            {
                'title': 'Upanishads - Principal Texts',
                'author': 'Various Sages',
                'description': 'A collection of philosophical texts that form the theoretical basis for the Vedanta school of Hindu philosophy.',
                'book_type': 'RELIGIOUS',
                'category': 'Vedic Literature',
                'online_reading_price': 50.00,
                'download_price': 100.00,
                'is_free': False,
            },
            {
                'title': 'Puranas - Vishnu Purana',
                'author': 'Vyasa',
                'description': 'One of the eighteen Mahapuranas, focusing on the stories and teachings related to Lord Vishnu.',
                'book_type': 'RELIGIOUS',
                'category': 'Puranas',
                'online_reading_price': 50.00,
                'download_price': 100.00,
                'is_free': False,
            },
            {
                'title': 'Yoga Sutras of Patanjali',
                'author': 'Patanjali',
                'description': 'A collection of 196 Sanskrit sutras on the theory and practice of yoga, providing a comprehensive guide to spiritual development.',
                'book_type': 'RELIGIOUS',
                'category': 'Yoga & Philosophy',
                'online_reading_price': 50.00,
                'download_price': 100.00,
                'is_free': False,
            },
            {
                'title': 'Arthashastra',
                'author': 'Kautilya (Chanakya)',
                'description': 'An ancient Indian treatise on statecraft, economic policy, and military strategy, written by the philosopher and royal advisor Chanakya.',
                'book_type': 'EDUCATIONAL',
                'category': 'Political Science',
                'online_reading_price': 50.00,
                'download_price': 100.00,
                'is_free': False,
            },
            {
                'title': 'Panchatantra',
                'author': 'Vishnu Sharma',
                'description': 'An ancient Indian collection of interrelated animal fables in Sanskrit verse and prose, arranged within a frame story.',
                'book_type': 'LITERATURE',
                'category': 'Fables & Stories',
                'online_reading_price': 50.00,
                'download_price': 100.00,
                'is_free': False,
            },
            {
                'title': 'Jataka Tales',
                'author': 'Buddhist Monks',
                'description': 'A voluminous body of literature native to India concerning the previous births of Gautama Buddha in both human and animal form.',
                'book_type': 'RELIGIOUS',
                'category': 'Buddhist Literature',
                'online_reading_price': 50.00,
                'download_price': 100.00,
                'is_free': False,
            },
            {
                'title': 'Tirukkural',
                'author': 'Thiruvalluvar',
                'description': 'A classic Tamil text consisting of 1,330 couplets dealing with the everyday virtues of an individual.',
                'book_type': 'LITERATURE',
                'category': 'Tamil Literature',
                'online_reading_price': 50.00,
                'download_price': 100.00,
                'is_free': False,
            },
            {
                'title': 'Introduction to Sanskrit',
                'author': 'Dr. Sanskrit Scholar',
                'description': 'A comprehensive guide to learning Sanskrit, covering grammar, vocabulary, and classical texts.',
                'book_type': 'EDUCATIONAL',
                'category': 'Language Learning',
                'online_reading_price': 50.00,
                'download_price': 100.00,
                'is_free': False,
            },
            {
                'title': 'Free Sample Book',
                'author': 'ReadOps Team',
                'description': 'A sample book to demonstrate the digital library features. This book is completely free to read and download.',
                'book_type': 'EDUCATIONAL',
                'category': 'Sample Books',
                'online_reading_price': 0.00,
                'download_price': 0.00,
                'is_free': True,
            },
        ]

        created_count = 0
        for book_data in digital_books:
            book, created = DigitalBook.objects.get_or_create(
                title=book_data['title'],
                defaults=book_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created: {book.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Already exists: {book.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully added {created_count} digital books!')
        )
