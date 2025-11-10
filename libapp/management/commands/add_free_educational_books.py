from django.core.management.base import BaseCommand
from libapp.models import DigitalBook
from django.utils import timezone
import os


class Command(BaseCommand):
    help = 'Add free educational books including Kannada stories and English learning materials'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Adding free educational books to digital library...'))
        
        # Kannada Stories for Children (1st to 10th std)
        kannada_stories = [
            # 1st Standard
            {
                'title': 'ಅಕ್ಷರಗಳು - 1ನೇ ತರಗತಿ',
                'author': 'ಕರ್ನಾಟಕ ಸರ್ಕಾರ',
                'description': 'ಅಕ್ಷರಗಳನ್ನು ಕಲಿಯುವ ಮಕ್ಕಳಿಗಾಗಿ ಮೂಲಭೂತ ಕನ್ನಡ ಪುಸ್ತಕ. ಸರಳ ಪದಗಳು ಮತ್ತು ಚಿತ್ರಗಳೊಂದಿಗೆ.',
                'book_type': 'EDUCATIONAL',
                'category': 'Kannada - 1st Standard',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'ಗಣಿತದ ಮೂಲಭೂತಗಳು - 1ನೇ ತರಗತಿ',
                'author': 'ಶಿಕ್ಷಣ ಇಲಾಖೆ',
                'description': 'ಸಂಖ್ಯೆಗಳು, ಸಂಕಲನ ಮತ್ತು ವ್ಯವಕಲನದ ಮೂಲಭೂತಗಳನ್ನು ಕಲಿಸುವ ಪುಸ್ತಕ.',
                'book_type': 'EDUCATIONAL',
                'category': 'Mathematics - 1st Standard',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            
            # 2nd Standard
            {
                'title': 'ಕನ್ನಡ ಕಥೆಗಳು - 2ನೇ ತರಗತಿ',
                'author': 'ಕರ್ನಾಟಕ ಸರ್ಕಾರ',
                'description': 'ಮಕ್ಕಳಿಗಾಗಿ ಸರಳ ಮತ್ತು ಮನರಂಜನೆಯ ಕನ್ನಡ ಕಥೆಗಳು. ಚಿತ್ರಗಳೊಂದಿಗೆ.',
                'book_type': 'LITERATURE',
                'category': 'Kannada Stories - 2nd Standard',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'ಪ್ರಕೃತಿ ಮತ್ತು ನಮ್ಮ ಸುತ್ತಲೂ - 2ನೇ ತರಗತಿ',
                'author': 'ಪರಿಸರ ಶಿಕ್ಷಣ',
                'description': 'ಪ್ರಕೃತಿ, ಪ್ರಾಣಿಗಳು ಮತ್ತು ಪರಿಸರದ ಬಗ್ಗೆ ಮಕ್ಕಳಿಗೆ ಕಲಿಸುವ ಪುಸ್ತಕ.',
                'book_type': 'EDUCATIONAL',
                'category': 'Environmental Studies - 2nd Standard',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            
            # 3rd Standard
            {
                'title': 'ಕನ್ನಡ ವ್ಯಾಕರಣ - 3ನೇ ತರಗತಿ',
                'author': 'ಕನ್ನಡ ಅಧ್ಯಯನ',
                'description': 'ಕನ್ನಡ ಭಾಷೆಯ ಮೂಲಭೂತ ವ್ಯಾಕರಣ ನಿಯಮಗಳು ಮತ್ತು ಅಭ್ಯಾಸಗಳು.',
                'book_type': 'EDUCATIONAL',
                'category': 'Kannada Grammar - 3rd Standard',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'ಗಣಿತದ ರಹಸ್ಯಗಳು - 3ನೇ ತರಗತಿ',
                'author': 'ಗಣಿತ ಶಿಕ್ಷಕರು',
                'description': 'ಗುಣಾಕಾರ, ಭಾಗಾಕಾರ ಮತ್ತು ಮೂಲಭೂತ ಗಣಿತ ಕಲಿಕೆ.',
                'book_type': 'EDUCATIONAL',
                'category': 'Mathematics - 3rd Standard',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            
            # 4th Standard
            {
                'title': 'ಕನ್ನಡ ಸಾಹಿತ್ಯ - 4ನೇ ತರಗತಿ',
                'author': 'ಕನ್ನಡ ಸಾಹಿತ್ಯ ಪರಿಷತ್ತು',
                'description': 'ಕನ್ನಡ ಸಾಹಿತ್ಯದ ಮೂಲಭೂತ ಪರಿಚಯ ಮತ್ತು ಪ್ರಸಿದ್ಧ ಕವಿಗಳ ಕವಿತೆಗಳು.',
                'book_type': 'LITERATURE',
                'category': 'Kannada Literature - 4th Standard',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'ಇತಿಹಾಸ ಮತ್ತು ಸಂಸ್ಕೃತಿ - 4ನೇ ತರಗತಿ',
                'author': 'ಇತಿಹಾಸ ಇಲಾಖೆ',
                'description': 'ಕರ್ನಾಟಕದ ಇತಿಹಾಸ ಮತ್ತು ಸಂಸ್ಕೃತಿಯ ಬಗ್ಗೆ ಮಕ್ಕಳಿಗೆ ಕಲಿಸುವ ಪುಸ್ತಕ.',
                'book_type': 'EDUCATIONAL',
                'category': 'History & Culture - 4th Standard',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            
            # 5th Standard
            {
                'title': 'ಕನ್ನಡ ಕಾವ್ಯ - 5ನೇ ತರಗತಿ',
                'author': 'ಕನ್ನಡ ಅಧ್ಯಾಪಕರು',
                'description': 'ಕನ್ನಡ ಕಾವ್ಯಗಳು, ಶ್ಲೋಕಗಳು ಮತ್ತು ಕವಿತೆಗಳ ಸಂಗ್ರಹ.',
                'book_type': 'LITERATURE',
                'category': 'Kannada Poetry - 5th Standard',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'ವಿಜ್ಞಾನದ ಪ್ರಪಂಚ - 5ನೇ ತರಗತಿ',
                'author': 'ವಿಜ್ಞಾನ ಇಲಾಖೆ',
                'description': 'ಮೂಲಭೂತ ವಿಜ್ಞಾನ ಪರಿಕಲ್ಪನೆಗಳು ಮತ್ತು ಪ್ರಯೋಗಗಳು.',
                'book_type': 'EDUCATIONAL',
                'category': 'Science - 5th Standard',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            
            # 6th Standard
            {
                'title': 'ಕನ್ನಡ ನಾಟಕಗಳು - 6ನೇ ತರಗತಿ',
                'author': 'ನಾಟಕ ಸಂಘ',
                'description': 'ಮಕ್ಕಳಿಗಾಗಿ ಸರಳ ಮತ್ತು ಮನರಂಜನೆಯ ಕನ್ನಡ ನಾಟಕಗಳು.',
                'book_type': 'LITERATURE',
                'category': 'Kannada Drama - 6th Standard',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'ಸಾಮಾಜಿಕ ವಿಜ್ಞಾನ - 6ನೇ ತರಗತಿ',
                'author': 'ಸಾಮಾಜಿಕ ವಿಜ್ಞಾನ ಇಲಾಖೆ',
                'description': 'ಸಮಾಜ, ಸರ್ಕಾರ ಮತ್ತು ನಾಗರಿಕತೆಯ ಬಗ್ಗೆ ಮೂಲಭೂತ ಪರಿಚಯ.',
                'book_type': 'EDUCATIONAL',
                'category': 'Social Science - 6th Standard',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            
            # 7th Standard
            {
                'title': 'ಕನ್ನಡ ಭಾಷೆಯ ಸೌಂದರ್ಯ - 7ನೇ ತರಗತಿ',
                'author': 'ಕನ್ನಡ ಭಾಷಾ ಸಂಸ್ಥೆ',
                'description': 'ಕನ್ನಡ ಭಾಷೆಯ ಸೌಂದರ್ಯ, ಶೈಲಿ ಮತ್ತು ಅಭಿವ್ಯಕ್ತಿ ವಿಧಾನಗಳು.',
                'book_type': 'EDUCATIONAL',
                'category': 'Kannada Language - 7th Standard',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'ಗಣಿತದ ಸೌಂದರ್ಯ - 7ನೇ ತರಗತಿ',
                'author': 'ಗಣಿತ ಅಧ್ಯಾಪಕರು',
                'description': 'ಬೀಜಗಣಿತ, ಜ್ಯಾಮಿತಿ ಮತ್ತು ಪ್ರಾಯೋಗಿಕ ಗಣಿತ.',
                'book_type': 'EDUCATIONAL',
                'category': 'Mathematics - 7th Standard',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            
            # 8th Standard
            {
                'title': 'ಕನ್ನಡ ಸಾಹಿತ್ಯ ಇತಿಹಾಸ - 8ನೇ ತರಗತಿ',
                'author': 'ಕನ್ನಡ ಸಾಹಿತ್ಯ ಇತಿಹಾಸಕಾರರು',
                'description': 'ಕನ್ನಡ ಸಾಹಿತ್ಯದ ಇತಿಹಾಸ ಮತ್ತು ಪ್ರಮುಖ ಸಾಹಿತಿಗಳು.',
                'book_type': 'LITERATURE',
                'category': 'Kannada Literature History - 8th Standard',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'ಭೌತಶಾಸ್ತ್ರ ಮತ್ತು ರಸಾಯನಶಾಸ್ತ್ರ - 8ನೇ ತರಗತಿ',
                'author': 'ವಿಜ್ಞಾನ ಇಲಾಖೆ',
                'description': 'ಮೂಲಭೂತ ಭೌತಶಾಸ್ತ್ರ ಮತ್ತು ರಸಾಯನಶಾಸ್ತ್ರ ಪರಿಕಲ್ಪನೆಗಳು.',
                'book_type': 'EDUCATIONAL',
                'category': 'Physics & Chemistry - 8th Standard',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            
            # 9th Standard
            {
                'title': 'ಕನ್ನಡ ಕಾವ್ಯ ಸಾಹಿತ್ಯ - 9ನೇ ತರಗತಿ',
                'author': 'ಕನ್ನಡ ಸಾಹಿತ್ಯ ಪರಿಷತ್ತು',
                'description': 'ಕನ್ನಡ ಕಾವ್ಯ ಸಾಹಿತ್ಯದ ವಿಶ್ಲೇಷಣೆ ಮತ್ತು ವಿಮರ್ಶೆ.',
                'book_type': 'LITERATURE',
                'category': 'Kannada Poetry Literature - 9th Standard',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'ಜೀವಶಾಸ್ತ್ರ ಮತ್ತು ಪರಿಸರ - 9ನೇ ತರಗತಿ',
                'author': 'ಜೀವಶಾಸ್ತ್ರ ಇಲಾಖೆ',
                'description': 'ಜೀವಶಾಸ್ತ್ರ ಮೂಲಭೂತಗಳು ಮತ್ತು ಪರಿಸರ ಸಂರಕ್ಷಣೆ.',
                'book_type': 'EDUCATIONAL',
                'category': 'Biology & Environment - 9th Standard',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            
            # 10th Standard
            {
                'title': 'ಕನ್ನಡ ಸಾಹಿತ್ಯ ವಿಮರ್ಶೆ - 10ನೇ ತರಗತಿ',
                'author': 'ಕನ್ನಡ ಸಾಹಿತ್ಯ ವಿಮರ್ಶಕರು',
                'description': 'ಕನ್ನಡ ಸಾಹಿತ್ಯ ವಿಮರ್ಶೆಯ ಮೂಲಭೂತಗಳು ಮತ್ತು ವಿಶ್ಲೇಷಣೆ.',
                'book_type': 'LITERATURE',
                'category': 'Kannada Literature Criticism - 10th Standard',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'ಸಂಯುಕ್ತ ಗಣಿತ ಮತ್ತು ವಿಜ್ಞಾನ - 10ನೇ ತರಗತಿ',
                'author': 'ಶಿಕ್ಷಣ ಇಲಾಖೆ',
                'description': 'ಸಂಯುಕ್ತ ಗಣಿತ, ಭೌತಶಾಸ್ತ್ರ, ರಸಾಯನಶಾಸ್ತ್ರ ಮತ್ತು ಜೀವಶಾಸ್ತ್ರ.',
                'book_type': 'EDUCATIONAL',
                'category': 'Combined Mathematics & Science - 10th Standard',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
        ]
        
        # English Learning Materials
        english_learning = [
            {
                'title': 'English Grammar Fundamentals',
                'author': 'English Learning Institute',
                'description': 'Complete guide to English grammar from basics to advanced. Perfect for beginners and intermediate learners.',
                'book_type': 'EDUCATIONAL',
                'category': 'English Grammar',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'English Vocabulary Builder',
                'author': 'Language Experts',
                'description': 'Essential English vocabulary with meanings, examples, and usage. Organized by difficulty levels.',
                'book_type': 'EDUCATIONAL',
                'category': 'English Vocabulary',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'Creative Writing Guide',
                'author': 'Writing Academy',
                'description': 'Learn creative writing techniques, story development, character creation, and narrative styles.',
                'book_type': 'EDUCATIONAL',
                'category': 'Creative Writing',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'Business English Communication',
                'author': 'Business Communication Institute',
                'description': 'Professional English for business communication, emails, presentations, and meetings.',
                'book_type': 'EDUCATIONAL',
                'category': 'Business English',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'English Pronunciation Mastery',
                'author': 'Phonetics Institute',
                'description': 'Master English pronunciation with phonetic guides, audio examples, and practice exercises.',
                'book_type': 'EDUCATIONAL',
                'category': 'English Pronunciation',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'Academic Writing Skills',
                'author': 'Academic Writing Center',
                'description': 'Learn academic writing, research papers, essays, and formal writing techniques.',
                'book_type': 'EDUCATIONAL',
                'category': 'Academic Writing',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'English Conversation Practice',
                'author': 'Conversation Experts',
                'description': 'Daily conversation scenarios, dialogues, and speaking practice exercises.',
                'book_type': 'EDUCATIONAL',
                'category': 'English Conversation',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'IELTS Preparation Guide',
                'author': 'IELTS Training Center',
                'description': 'Complete IELTS preparation with practice tests, tips, and strategies for all sections.',
                'book_type': 'EDUCATIONAL',
                'category': 'IELTS Preparation',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'TOEFL Study Material',
                'author': 'TOEFL Institute',
                'description': 'Comprehensive TOEFL preparation with reading, listening, speaking, and writing sections.',
                'book_type': 'EDUCATIONAL',
                'category': 'TOEFL Preparation',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'English Literature Appreciation',
                'author': 'Literature Department',
                'description': 'Introduction to English literature, famous authors, and literary analysis techniques.',
                'book_type': 'LITERATURE',
                'category': 'English Literature',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
        ]
        
        # Additional Free Educational Books
        additional_free_books = [
            {
                'title': 'Computer Basics for Beginners',
                'author': 'Computer Education Center',
                'description': 'Learn computer fundamentals, operating systems, and basic software usage.',
                'book_type': 'TECHNICAL',
                'category': 'Computer Basics',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'Digital Literacy Guide',
                'author': 'Digital Education Institute',
                'description': 'Essential digital skills for the modern world including internet safety and online tools.',
                'book_type': 'TECHNICAL',
                'category': 'Digital Literacy',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'Financial Literacy for Students',
                'author': 'Financial Education Center',
                'description': 'Learn about money management, savings, investments, and financial planning.',
                'book_type': 'EDUCATIONAL',
                'category': 'Financial Education',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'Health and Wellness Guide',
                'author': 'Health Education Department',
                'description': 'Comprehensive guide to physical and mental health, nutrition, and wellness.',
                'book_type': 'EDUCATIONAL',
                'category': 'Health & Wellness',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
            {
                'title': 'Environmental Awareness',
                'author': 'Environmental Education Center',
                'description': 'Learn about environmental protection, climate change, and sustainable living.',
                'book_type': 'EDUCATIONAL',
                'category': 'Environmental Education',
                'is_free': True,
                'online_reading_price': 0.00,
                'download_price': 0.00,
            },
        ]
        
        # Combine all books
        all_books = kannada_stories + english_learning + additional_free_books
        
        created_count = 0
        for book_data in all_books:
            # Check if book already exists
            if not DigitalBook.objects.filter(title=book_data['title']).exists():
                DigitalBook.objects.create(**book_data)
                created_count += 1
                self.stdout.write(f"Created: {book_data['title']}")
            else:
                self.stdout.write(f"Already exists: {book_data['title']}")
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully added {created_count} free educational books to the digital library!'
            )
        )
        
        # Display summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write('FREE EDUCATIONAL BOOKS SUMMARY:')
        self.stdout.write('='*60)
        self.stdout.write(f'📚 Kannada Stories (1st-10th std): {len(kannada_stories)} books')
        self.stdout.write(f'🇬🇧 English Learning Materials: {len(english_learning)} books')
        self.stdout.write(f'📖 Additional Free Books: {len(additional_free_books)} books')
        self.stdout.write(f'📊 Total Free Books Added: {created_count} books')
        self.stdout.write('='*60)
        
        self.stdout.write('\n📋 Categories included:')
        categories = set()
        for book in all_books:
            categories.add(book['category'])
        
        for category in sorted(categories):
            self.stdout.write(f'  • {category}')
        
        self.stdout.write('\n✅ All books are set as FREE with no charges for online reading or download!')
