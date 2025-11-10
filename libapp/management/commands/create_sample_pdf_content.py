from django.core.management.base import BaseCommand
from libapp.models import DigitalBook
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import io


class Command(BaseCommand):
    help = 'Create sample PDF content for free educational books'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample PDF content for free books...'))
        
        # Get all free books
        free_books = DigitalBook.objects.filter(is_free=True)
        
        created_count = 0
        for book in free_books:
            if not book.pdf_file:  # Only create if no PDF exists
                # Create sample PDF content
                buffer = io.BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=letter)
                styles = getSampleStyleSheet()
                story = []
                
                # Title
                title_style = styles['Title']
                title = Paragraph(book.title, title_style)
                story.append(title)
                story.append(Spacer(1, 12))
                
                # Author
                author_style = styles['Heading2']
                author = Paragraph(f"by {book.author}", author_style)
                story.append(author)
                story.append(Spacer(1, 12))
                
                # Description
                desc_style = styles['Normal']
                description = Paragraph(book.description, desc_style)
                story.append(description)
                story.append(Spacer(1, 12))
                
                # Category and Type
                category_info = Paragraph(f"<b>Category:</b> {book.category}<br/><b>Type:</b> {book.get_book_type_display()}", desc_style)
                story.append(category_info)
                story.append(Spacer(1, 12))
                
                # Sample content based on category
                if 'Kannada' in book.category:
                    sample_content = self.get_kannada_sample_content(book)
                elif 'English' in book.category:
                    sample_content = self.get_english_sample_content(book)
                elif 'Mathematics' in book.category:
                    sample_content = self.get_math_sample_content(book)
                elif 'Science' in book.category:
                    sample_content = self.get_science_sample_content(book)
                else:
                    sample_content = self.get_general_sample_content(book)
                
                content_style = styles['Normal']
                content = Paragraph(sample_content, content_style)
                story.append(content)
                
                # Build PDF
                doc.build(story)
                buffer.seek(0)
                
                # Save PDF to book
                filename = f"{book.title.replace(' ', '_').replace('/', '_')}.pdf"
                book.pdf_file.save(filename, ContentFile(buffer.getvalue()), save=True)
                
                created_count += 1
                self.stdout.write(f"Created PDF for: {book.title}")
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} sample PDF files for free books!'
            )
        )
    
    def get_kannada_sample_content(self, book):
        if '1ನೇ ತರಗತಿ' in book.title and 'ಅಕ್ಷರಗಳು' in book.title:
            return """
            <b>ಅಕ್ಷರಗಳು - 1ನೇ ತರಗತಿ</b><br/><br/>
            
            <b>ಅಧ್ಯಾಯ 1: ಕನ್ನಡ ಸ್ವರಗಳು</b><br/><br/>
            
            ಕನ್ನಡ ಭಾಷೆಯಲ್ಲಿ 14 ಸ್ವರಗಳಿವೆ:<br/><br/>
            
            ಅ, ಆ, ಇ, ಈ, ಉ, ಊ, ಋ, ೠ, ಎ, ಏ, ಐ, ಒ, ಓ, ಔ<br/><br/>
            
            <b>ಸ್ವರಗಳ ಅಭ್ಯಾಸ:</b><br/>
            ಅ - ಅಮ್ಮ, ಅಪ್ಪ, ಅಕ್ಕ<br/>
            ಆ - ಆನೆ, ಆಕಾಶ, ಆರೋಗ್ಯ<br/>
            ಇ - ಇಲಿ, ಇದು, ಇಲ್ಲ<br/>
            ಈ - ಈಗ, ಈಶ್ವರ, ಈತ<br/>
            ಉ - ಉಪ್ಪು, ಉದ್ಯಾನ, ಉತ್ತರ<br/>
            ಊ - ಊಟ, ಊರ್, ಊಟ<br/><br/>
            
            <b>ಅಧ್ಯಾಯ 2: ಕನ್ನಡ ವ್ಯಂಜನಗಳು</b><br/><br/>
            
            ಕನ್ನಡ ಭಾಷೆಯಲ್ಲಿ 35 ವ್ಯಂಜನಗಳಿವೆ:<br/><br/>
            
            ಕ, ಖ, ಗ, ಘ, ಙ<br/>
            ಚ, ಛ, ಜ, ಝ, ಞ<br/>
            ಟ, ಠ, ಡ, ಢ, ಣ<br/>
            ತ, ಥ, ದ, ಧ, ನ<br/>
            ಪ, ಫ, ಬ, ಭ, ಮ<br/>
            ಯ, ರ, ಲ, ವ, ಶ<br/>
            ಷ, ಸ, ಹ, ಳ, ಕ್ಷ<br/><br/>
            
            <b>ವ್ಯಂಜನಗಳ ಅಭ್ಯಾಸ:</b><br/>
            ಕ - ಕಮಲ, ಕಪ್ಪು, ಕರಿ<br/>
            ಗ - ಗಿಡ, ಗುರು, ಗಾಳಿ<br/>
            ಚ - ಚಂದ್ರ, ಚಿತ್ರ, ಚಿಕ್ಕ<br/>
            ಜ - ಜಲ, ಜನ, ಜೀವ<br/>
            ತ - ತಾಯಿ, ತಂದೆ, ತಂಗಿ<br/>
            ದ - ದೀಪ, ದಾರಿ, ದಿನ<br/>
            ಪ - ಪುಸ್ತಕ, ಪಕ್ಷಿ, ಪೂಜೆ<br/>
            ಬ - ಬಾಳೆ, ಬೆಳ್ಳಿ, ಬೆಂಕಿ<br/><br/>
            
            <b>ಅಧ್ಯಾಯ 3: ಸರಳ ಪದಗಳು</b><br/><br/>
            
            <b>ಅಕ್ಷರಗಳನ್ನು ಒಟ್ಟಿಗೆ ಸೇರಿಸಿ ಪದಗಳನ್ನು ಮಾಡೋಣ:</b><br/><br/>
            
            ಅ + ಮ್ಮ = ಅಮ್ಮ<br/>
            ಅ + ಪ್ಪ = ಅಪ್ಪ<br/>
            ಕ + ಮಲ = ಕಮಲ<br/>
            ಗ + ಇಡ = ಗಿಡ<br/>
            ಚ + ಇತ್ರ = ಚಿತ್ರ<br/>
            ತ + ಆಯಿ = ತಾಯಿ<br/>
            ಪ + ಉಸ್ತಕ = ಪುಸ್ತಕ<br/><br/>
            
            <b>ಅಧ್ಯಾಯ 4: ಸಂಖ್ಯೆಗಳು</b><br/><br/>
            
            ಒಂದು, ಎರಡು, ಮೂರು, ನಾಲ್ಕು, ಐದು<br/>
            ಆರು, ಏಳು, ಎಂಟು, ಒಂಬತ್ತು, ಹತ್ತು<br/><br/>
            
            <b>ಅಧ್ಯಾಯ 5: ಬಣ್ಣಗಳು</b><br/><br/>
            
            ಕೆಂಪು, ಹಳದಿ, ನೀಲಿ, ಹಸಿರು, ಕಪ್ಪು<br/>
            ಬಿಳಿ, ನಾರಂಗಿ, ಗುಲಾಬಿ, ನೇರಳೆ<br/><br/>
            
            <b>ಅಧ್ಯಾಯ 6: ಪ್ರಾಣಿಗಳು</b><br/><br/>
            
            ಆನೆ, ಹುಲಿ, ಸಿಂಹ, ಹಸು, ಎಮ್ಮೆ<br/>
            ನಾಯಿ, ಬೆಕ್ಕು, ಕುದುರೆ, ಕೋಳಿ, ಕಾಗೆ<br/><br/>
            
            <b>ಅಧ್ಯಾಯ 7: ಹಣ್ಣುಗಳು</b><br/><br/>
            
            ಬಾಳೆ, ಸೇಬು, ಮಾವು, ದ್ರಾಕ್ಷಿ, ಸಂತರ<br/>
            ಕಿತ್ತಳೆ, ಪಪ್ಪಾಯಿ, ಅನಾನಸ್, ದಾಳಿಂಬೆ<br/><br/>
            
            <b>ಅಧ್ಯಾಯ 8: ತರಕಾರಿಗಳು</b><br/><br/>
            
            ಬಟಾಣಿ, ಗಜ್ಜರಿ, ಬೀಟ್, ಆಲೂಗಡ್ಡೆ<br/>
            ಈರುಳ್ಳಿ, ಟೊಮಾಟೊ, ಕ್ಯಾಬೇಜ್, ಬದನೆ<br/><br/>
            
            <b>ಅಧ್ಯಾಯ 9: ದೇಹದ ಭಾಗಗಳು</b><br/><br/>
            
            ತಲೆ, ಕಣ್ಣು, ಕಿವಿ, ಮೂಗು, ಬಾಯಿ<br/>
            ಕೈ, ಕಾಲು, ಹೊಟ್ಟೆ, ಬೆನ್ನು, ಹೃದಯ<br/><br/>
            
            <b>ಅಧ್ಯಾಯ 10: ಕುಟುಂಬ</b><br/><br/>
            
            ಅಮ್ಮ, ಅಪ್ಪ, ಅಕ್ಕ, ತಂಗಿ, ಅಣ್ಣ<br/>
            ತಮ್ಮ, ಅಜ್ಜ, ಅಜ್ಜಿ, ಮಾವ, ಅತ್ತೆ<br/><br/>
            
            <b>ಅಭ್ಯಾಸ:</b><br/>
            1. ಸ್ವರಗಳನ್ನು ಓದಿ ಮತ್ತು ಬರೆಯಿರಿ<br/>
            2. ವ್ಯಂಜನಗಳನ್ನು ಓದಿ ಮತ್ತು ಬರೆಯಿರಿ<br/>
            3. ಸರಳ ಪದಗಳನ್ನು ಓದಿ ಮತ್ತು ಬರೆಯಿರಿ<br/>
            4. ಸಂಖ್ಯೆಗಳನ್ನು ಓದಿ ಮತ್ತು ಬರೆಯಿರಿ<br/>
            5. ಬಣ್ಣಗಳನ್ನು ಗುರುತಿಸಿ<br/>
            6. ಪ್ರಾಣಿಗಳ ಹೆಸರುಗಳನ್ನು ಓದಿ<br/>
            7. ಹಣ್ಣುಗಳ ಹೆಸರುಗಳನ್ನು ಓದಿ<br/>
            8. ತರಕಾರಿಗಳ ಹೆಸರುಗಳನ್ನು ಓದಿ<br/>
            9. ದೇಹದ ಭಾಗಗಳನ್ನು ಗುರುತಿಸಿ<br/>
            10. ಕುಟುಂಬದ ಸದಸ್ಯರನ್ನು ಗುರುತಿಸಿ<br/><br/>
            
            <b>ಸ್ಮರಣೆ:</b> ಪ್ರತಿದಿನ ಅಕ್ಷರಗಳನ್ನು ಪುನರಾವರ್ತಿಸಿ. ಸರಳ ಪದಗಳನ್ನು ಓದಿ ಮತ್ತು ಬರೆಯಿರಿ. ಚಿತ್ರಗಳೊಂದಿಗೆ ಕಲಿಯಿರಿ.
            """
        elif 'ಗಣಿತದ ಮೂಲಭೂತಗಳು' in book.title:
            return """
            <b>ಗಣಿತದ ಮೂಲಭೂತಗಳು - 1ನೇ ತರಗತಿ</b><br/><br/>
            
            <b>ಅಧ್ಯಾಯ 1: ಸಂಖ್ಯೆಗಳ ಪರಿಚಯ</b><br/><br/>
            
            <b>1 ರಿಂದ 10 ರವರೆಗೆ ಸಂಖ್ಯೆಗಳು:</b><br/><br/>
            
            1 - ಒಂದು<br/>
            2 - ಎರಡು<br/>
            3 - ಮೂರು<br/>
            4 - ನಾಲ್ಕು<br/>
            5 - ಐದು<br/>
            6 - ಆರು<br/>
            7 - ಏಳು<br/>
            8 - ಎಂಟು<br/>
            9 - ಒಂಬತ್ತು<br/>
            10 - ಹತ್ತು<br/><br/>
            
            <b>ಅಧ್ಯಾಯ 2: ಸಂಕಲನ (Addition)</b><br/><br/>
            
            <b>ಸರಳ ಸಂಕಲನ:</b><br/><br/>
            
            1 + 1 = 2<br/>
            2 + 1 = 3<br/>
            2 + 2 = 4<br/>
            3 + 1 = 4<br/>
            3 + 2 = 5<br/>
            4 + 1 = 5<br/>
            4 + 2 = 6<br/>
            5 + 1 = 6<br/>
            5 + 2 = 7<br/>
            5 + 3 = 8<br/>
            5 + 4 = 9<br/>
            5 + 5 = 10<br/><br/>
            
            <b>ಅಧ್ಯಾಯ 3: ವ್ಯವಕಲನ (Subtraction)</b><br/><br/>
            
            <b>ಸರಳ ವ್ಯವಕಲನ:</b><br/><br/>
            
            2 - 1 = 1<br/>
            3 - 1 = 2<br/>
            3 - 2 = 1<br/>
            4 - 1 = 3<br/>
            4 - 2 = 2<br/>
            4 - 3 = 1<br/>
            5 - 1 = 4<br/>
            5 - 2 = 3<br/>
            5 - 3 = 2<br/>
            5 - 4 = 1<br/>
            6 - 1 = 5<br/>
            6 - 2 = 4<br/>
            6 - 3 = 3<br/>
            6 - 4 = 2<br/>
            6 - 5 = 1<br/><br/>
            
            <b>ಅಧ್ಯಾಯ 4: ಆಕಾರಗಳು</b><br/><br/>
            
            <b>ಮೂಲಭೂತ ಆಕಾರಗಳು:</b><br/><br/>
            
            ವೃತ್ತ (Circle) - ಚಂದ್ರ, ಸೂರ್ಯ<br/>
            ಚೌಕ (Square) - ಚೆಸ್ ಬೋರ್ಡ್<br/>
            ತ್ರಿಕೋನ (Triangle) - ಪರ್ವತ<br/>
            ಆಯತ (Rectangle) - ಪುಸ್ತಕ<br/>
            ಅಂಡಾಕಾರ (Oval) - ಮೊಟ್ಟೆ<br/><br/>
            
            <b>ಅಧ್ಯಾಯ 5: ಗಾತ್ರಗಳು</b><br/><br/>
            
            ದೊಡ್ಡದು - ಸಣ್ಣದು<br/>
            ಎತ್ತರ - ಕುಳ್ಳ<br/>
            ಉದ್ದ - ಚಿಕ್ಕದು<br/>
            ಅಗಲ - ಕಿರಿದು<br/>
            ದಪ್ಪ - ತೆಳು<br/><br/>
            
            <b>ಅಧ್ಯಾಯ 6: ಸ್ಥಾನಗಳು</b><br/><br/>
            
            ಮೇಲೆ - ಕೆಳಗೆ<br/>
            ಮುಂದೆ - ಹಿಂದೆ<br/>
            ಬಲಕ್ಕೆ - ಎಡಕ್ಕೆ<br/>
            ಒಳಗೆ - ಹೊರಗೆ<br/>
            ಮಧ್ಯೆ - ಅಂಚು<br/><br/>
            
            <b>ಅಧ್ಯಾಯ 7: ಸಮಯ</b><br/><br/>
            
            ಬೆಳಿಗ್ಗೆ - ಸೂರ್ಯ ಉದಯ<br/>
            ಮಧ್ಯಾಹ್ನ - ಸೂರ್ಯ ಮಧ್ಯಾಕಾಶ<br/>
            ಸಂಜೆ - ಸೂರ್ಯ ಅಸ್ತಮಾನ<br/>
            ರಾತ್ರಿ - ಚಂದ್ರ<br/><br/>
            
            <b>ಅಧ್ಯಾಯ 8: ದಿನಗಳು</b><br/><br/>
            
            ಸೋಮವಾರ, ಮಂಗಳವಾರ, ಬುಧವಾರ<br/>
            ಗುರುವಾರ, ಶುಕ್ರವಾರ, ಶನಿವಾರ, ಭಾನುವಾರ<br/><br/>
            
            <b>ಅಧ್ಯಾಯ 9: ತೂಕ ಮತ್ತು ಅಳತೆ</b><br/><br/>
            
            ಭಾರ - ಹಗುರ<br/>
            ಉದ್ದ - ಚಿಕ್ಕ<br/>
            ಅಗಲ - ಕಿರಿದು<br/>
            ಎತ್ತರ - ಕುಳ್ಳ<br/><br/>
            
            <b>ಅಧ್ಯಾಯ 10: ಹಣ</b><br/><br/>
            
            ₹1 - ಒಂದು ರೂಪಾಯಿ<br/>
            ₹2 - ಎರಡು ರೂಪಾಯಿ<br/>
            ₹5 - ಐದು ರೂಪಾಯಿ<br/>
            ₹10 - ಹತ್ತು ರೂಪಾಯಿ<br/><br/>
            
            <b>ಅಭ್ಯಾಸ:</b><br/>
            1. 1 ರಿಂದ 10 ರವರೆಗೆ ಸಂಖ್ಯೆಗಳನ್ನು ಬರೆಯಿರಿ<br/>
            2. ಸರಳ ಸಂಕಲನ ಮಾಡಿ<br/>
            3. ಸರಳ ವ್ಯವಕಲನ ಮಾಡಿ<br/>
            4. ಆಕಾರಗಳನ್ನು ಗುರುತಿಸಿ<br/>
            5. ಗಾತ್ರಗಳನ್ನು ಹೋಲಿಸಿ<br/>
            6. ಸ್ಥಾನಗಳನ್ನು ಗುರುತಿಸಿ<br/>
            7. ಸಮಯವನ್ನು ಗುರುತಿಸಿ<br/>
            8. ದಿನಗಳನ್ನು ಓದಿ<br/>
            9. ತೂಕ ಮತ್ತು ಅಳತೆಯನ್ನು ಹೋಲಿಸಿ<br/>
            10. ಹಣವನ್ನು ಗುರುತಿಸಿ<br/><br/>
            
            <b>ಸ್ಮರಣೆ:</b> ಪ್ರತಿದಿನ ಸಂಖ್ಯೆಗಳನ್ನು ಪುನರಾವರ್ತಿಸಿ. ಸರಳ ಲೆಕ್ಕಗಳನ್ನು ಮಾಡಿ. ದೈನಂದಿನ ಜೀವನದಲ್ಲಿ ಗಣಿತವನ್ನು ಬಳಸಿ.
            """
        elif 'ಕನ್ನಡ ಕಥೆಗಳು' in book.title:
            return """
            <b>ಕನ್ನಡ ಕಥೆಗಳು - 2ನೇ ತರಗತಿ</b><br/><br/>
            
            <b>ಕಥೆ 1: ಚಿಕ್ಕ ಮರ</b><br/><br/>
            
            ಒಂದು ಸಣ್ಣ ಮರವಿತ್ತು. ಅದು ಬೆಳೆಯಲು ಬಯಸಿತು. ಪ್ರತಿದಿನ ಸೂರ್ಯನ ಬೆಳಕು ಬೇಕಾಗಿತ್ತು. ಮಳೆ ಬೇಕಾಗಿತ್ತು. ಮರವು ಬೆಳೆಯುತ್ತಿತ್ತು. ಈಗ ಅದು ದೊಡ್ಡ ಮರವಾಗಿದೆ. ಪಕ್ಷಿಗಳು ಅದರ ಮೇಲೆ ಗೂಡು ಮಾಡುತ್ತವೆ. ಮಕ್ಕಳು ಅದರ ಕೆಳಗೆ ಆಡುತ್ತಾರೆ.<br/><br/>
            
            <b>ಕಥೆ 2: ಚಿಕ್ಕ ಮೀನು</b><br/><br/>
            
            ಒಂದು ಸಣ್ಣ ಮೀನಿತ್ತು. ಅದು ನೀರಿನಲ್ಲಿ ಈಜುತ್ತಿತ್ತು. ಅದಕ್ಕೆ ಸ್ನೇಹಿತರು ಬೇಕಾಗಿದ್ದರು. ಅದು ಇತರ ಮೀನುಗಳನ್ನು ಕಂಡಿತು. ಅವರು ಒಟ್ಟಿಗೆ ಆಡಿದರು. ಅವರು ಒಟ್ಟಿಗೆ ಈಜಿದರು. ಈಗ ಅವರಿಗೆ ಸ್ನೇಹಿತರು ಇದ್ದಾರೆ.<br/><br/>
            
            <b>ಕಥೆ 3: ಚಿಕ್ಕ ಹಕ್ಕಿ</b><br/><br/>
            
            ಒಂದು ಸಣ್ಣ ಹಕ್ಕಿತ್ತು. ಅದು ಹಾರಲು ಬಯಸಿತು. ಅದು ರೆಕ್ಕೆಗಳನ್ನು ಬಡಿಯಿತು. ಅದು ಹಾರಲು ಪ್ರಯತ್ನಿಸಿತು. ಮೊದಲು ಅದು ಕೆಳಗೆ ಬಿತ್ತು. ಆದರೆ ಅದು ಪ್ರಯತ್ನಿಸುತ್ತಲೇ ಇತ್ತು. ಅಂತಿಮವಾಗಿ ಅದು ಹಾರಲು ಕಲಿತಿತು.<br/><br/>
            
            <b>ಕಥೆ 4: ಚಿಕ್ಕ ಹುಡುಗ</b><br/><br/>
            
            ಒಂದು ಸಣ್ಣ ಹುಡುಗನಿತ್ತು. ಅವನ ಹೆಸರು ರಾಮ. ಅವನು ಶಾಲೆಗೆ ಹೋಗುತ್ತಿದ್ದ. ಅವನು ಪುಸ್ತಕಗಳನ್ನು ಓದುತ್ತಿದ್ದ. ಅವನು ಸ್ನೇಹಿತರೊಂದಿಗೆ ಆಡುತ್ತಿದ್ದ. ಅವನು ಉತ್ತಮ ವಿದ್ಯಾರ್ಥಿಯಾಗಿದ್ದ.<br/><br/>
            
            <b>ಕಥೆ 5: ಚಿಕ್ಕ ಹುಡುಗಿ</b><br/><br/>
            
            ಒಂದು ಸಣ್ಣ ಹುಡುಗಿಯಿತ್ತು. ಅವಳ ಹೆಸರು ಸೀತ. ಅವಳು ತಾಯಿಯೊಂದಿಗೆ ಮನೆಯಲ್ಲಿ ಇರುತ್ತಿದ್ದ. ಅವಳು ತಾಯಿಗೆ ಸಹಾಯ ಮಾಡುತ್ತಿದ್ದ. ಅವಳು ಪುಸ್ತಕಗಳನ್ನು ಓದುತ್ತಿದ್ದ. ಅವಳು ಉತ್ತಮ ಮಗಳಾಗಿದ್ದ.<br/><br/>
            
            <b>ಕಥೆ 6: ಚಿಕ್ಕ ನಾಯಿ</b><br/><br/>
            
            ಒಂದು ಸಣ್ಣ ನಾಯಿತ್ತು. ಅದರ ಹೆಸರು ಟಾಮಿ. ಅದು ಮನೆಯಲ್ಲಿ ಇರುತ್ತಿತ್ತು. ಅದು ಮಾಲೀಕರೊಂದಿಗೆ ಆಡುತ್ತಿತ್ತು. ಅದು ಚೆಂಡನ್ನು ಹಿಡಿಯುತ್ತಿತ್ತು. ಅದು ಉತ್ತಮ ಸ್ನೇಹಿತವಾಗಿತ್ತು.<br/><br/>
            
            <b>ಕಥೆ 7: ಚಿಕ್ಕ ಬೆಕ್ಕು</b><br/><br/>
            
            ಒಂದು ಸಣ್ಣ ಬೆಕ್ಕಿತ್ತು. ಅದರ ಹೆಸರು ಮಿಟ್ಟಿ. ಅದು ಮನೆಯಲ್ಲಿ ಇರುತ್ತಿತ್ತು. ಅದು ಇಲಿಗಳನ್ನು ಹಿಡಿಯುತ್ತಿತ್ತು. ಅದು ಹಾಲು ಕುಡಿಯುತ್ತಿತ್ತು. ಅದು ಉತ್ತಮ ಬೆಕ್ಕಾಗಿತ್ತು.<br/><br/>
            
            <b>ಕಥೆ 8: ಚಿಕ್ಕ ಆನೆ</b><br/><br/>
            
            ಒಂದು ಸಣ್ಣ ಆನೆಯಿತ್ತು. ಅದು ಕಾಡಿನಲ್ಲಿ ಇರುತ್ತಿತ್ತು. ಅದು ತಾಯಿಯೊಂದಿಗೆ ಇರುತ್ತಿತ್ತು. ಅದು ನೀರು ಕುಡಿಯುತ್ತಿತ್ತು. ಅದು ಹುಲ್ಲು ತಿನ್ನುತ್ತಿತ್ತು. ಅದು ಉತ್ತಮ ಆನೆಯಾಗಿತ್ತು.<br/><br/>
            
            <b>ಕಥೆ 9: ಚಿಕ್ಕ ಹುಲಿ</b><br/><br/>
            
            ಒಂದು ಸಣ್ಣ ಹುಲಿಯಿತ್ತು. ಅದು ಕಾಡಿನಲ್ಲಿ ಇರುತ್ತಿತ್ತು. ಅದು ತಾಯಿಯೊಂದಿಗೆ ಇರುತ್ತಿತ್ತು. ಅದು ಮಾಂಸ ತಿನ್ನುತ್ತಿತ್ತು. ಅದು ಓಡುತ್ತಿತ್ತು. ಅದು ಉತ್ತಮ ಹುಲಿಯಾಗಿತ್ತು.<br/><br/>
            
            <b>ಕಥೆ 10: ಚಿಕ್ಕ ಹಕ್ಕಿ ಮತ್ತು ಮರ</b><br/><br/>
            
            ಒಂದು ಸಣ್ಣ ಹಕ್ಕಿತ್ತು. ಅದು ಮರದ ಮೇಲೆ ಗೂಡು ಮಾಡಿತ್ತು. ಮರವು ಹಕ್ಕಿಗೆ ಆಶ್ರಯ ನೀಡಿತ್ತು. ಹಕ್ಕಿಯು ಮರಕ್ಕೆ ಹಾಡು ಹಾಡುತ್ತಿತ್ತು. ಅವರು ಉತ್ತಮ ಸ್ನೇಹಿತರಾಗಿದ್ದರು.<br/><br/>
            
            <b>ಅಭ್ಯಾಸ:</b><br/>
            1. ಕಥೆಗಳನ್ನು ಓದಿ<br/>
            2. ಕಥೆಗಳನ್ನು ಹೇಳಿ<br/>
            3. ಕಥೆಗಳನ್ನು ಬರೆಯಿ<br/>
            4. ಕಥೆಗಳಲ್ಲಿ ಬರುವ ಪಾತ್ರಗಳನ್ನು ಗುರುತಿಸಿ<br/>
            5. ಕಥೆಗಳಲ್ಲಿ ಬರುವ ಪ್ರಾಣಿಗಳನ್ನು ಗುರುತಿಸಿ<br/>
            6. ಕಥೆಗಳಲ್ಲಿ ಬರುವ ಸ್ಥಳಗಳನ್ನು ಗುರುತಿಸಿ<br/>
            7. ಕಥೆಗಳಲ್ಲಿ ಬರುವ ಕ್ರಿಯೆಗಳನ್ನು ಗುರುತಿಸಿ<br/>
            8. ಕಥೆಗಳನ್ನು ಚಿತ್ರಿಸಿ<br/>
            9. ಕಥೆಗಳನ್ನು ನಾಟಕ ಮಾಡಿ<br/>
            10. ಹೊಸ ಕಥೆಗಳನ್ನು ರಚಿಸಿ<br/><br/>
            
            <b>ಸ್ಮರಣೆ:</b> ಕಥೆಗಳನ್ನು ಆಸಕ್ತಿಯಿಂದ ಓದಿ. ಕಥೆಗಳಿಂದ ಕಲಿಯಿರಿ. ಕಥೆಗಳನ್ನು ಇತರರೊಂದಿಗೆ ಹಂಚಿಕೊಳ್ಳಿ.
            """
        else:
            return """
            <b>ಕನ್ನಡ ಶಿಕ್ಷಣ</b><br/><br/>
            
            ಇದು ಕನ್ನಡ ಭಾಷೆಯ ಮೂಲಭೂತ ಪರಿಚಯವಾಗಿದೆ. ಈ ಪುಸ್ತಕದಲ್ಲಿ ನೀವು ಕನ್ನಡ ಅಕ್ಷರಗಳು, ಪದಗಳು, ವಾಕ್ಯಗಳು ಮತ್ತು ಸಾಹಿತ್ಯದ ಬಗ್ಗೆ ಕಲಿಯುವಿರಿ.<br/><br/>
            
            <b>ಅಧ್ಯಾಯ 1: ಅಕ್ಷರಗಳು</b><br/>
            ಕನ್ನಡ ಭಾಷೆಯಲ್ಲಿ 49 ಅಕ್ಷರಗಳಿವೆ. ಇವುಗಳನ್ನು ಸ್ವರಗಳು ಮತ್ತು ವ್ಯಂಜನಗಳು ಎಂದು ವಿಭಾಗಿಸಲಾಗಿದೆ.<br/><br/>
            
            <b>ಅಧ್ಯಾಯ 2: ಪದಗಳು</b><br/>
            ಅಕ್ಷರಗಳನ್ನು ಒಟ್ಟಿಗೆ ಸೇರಿಸಿ ಪದಗಳನ್ನು ರಚಿಸಲಾಗುತ್ತದೆ. ಪ್ರತಿ ಪದಕ್ಕೆ ಅರ್ಥವಿದೆ.<br/><br/>
            
            <b>ಅಧ್ಯಾಯ 3: ವಾಕ್ಯಗಳು</b><br/>
            ಪದಗಳನ್ನು ಒಟ್ಟಿಗೆ ಸೇರಿಸಿ ವಾಕ್ಯಗಳನ್ನು ರಚಿಸಲಾಗುತ್ತದೆ. ವಾಕ್ಯಗಳು ಸಂಪೂರ್ಣ ಅರ್ಥವನ್ನು ನೀಡುತ್ತವೆ.<br/><br/>
            
            ಇದು ಉಚಿತ ಶಿಕ್ಷಣ ಸಾಮಗ್ರಿಯಾಗಿದೆ. ನೀವು ಇದನ್ನು ಉಚಿತವಾಗಿ ಓದಬಹುದು ಮತ್ತು ಡೌನ್ಲೋಡ್ ಮಾಡಬಹುದು.
            """
    
    def get_english_sample_content(self, book):
        if 'Grammar Fundamentals' in book.title:
            return """
            <b>English Grammar Fundamentals</b><br/><br/>
            
            <b>Chapter 1: Parts of Speech</b><br/><br/>
            
            <b>1. Nouns</b><br/>
            A noun is a word that names a person, place, thing, or idea.<br/><br/>
            
            Examples:<br/>
            Person: teacher, student, doctor<br/>
            Place: school, hospital, park<br/>
            Thing: book, car, computer<br/>
            Idea: love, freedom, happiness<br/><br/>
            
            <b>2. Pronouns</b><br/>
            A pronoun is a word that takes the place of a noun.<br/><br/>
            
            Examples:<br/>
            I, you, he, she, it, we, they<br/>
            me, him, her, us, them<br/>
            my, your, his, her, its, our, their<br/><br/>
            
            <b>3. Verbs</b><br/>
            A verb is a word that shows action or state of being.<br/><br/>
            
            Action verbs: run, jump, read, write, eat<br/>
            Being verbs: am, is, are, was, were, be, being, been<br/><br/>
            
            <b>4. Adjectives</b><br/>
            An adjective describes or modifies a noun.<br/><br/>
            
            Examples:<br/>
            big, small, red, blue, happy, sad, tall, short<br/><br/>
            
            <b>5. Adverbs</b><br/>
            An adverb describes or modifies a verb, adjective, or another adverb.<br/><br/>
            
            Examples:<br/>
            quickly, slowly, very, really, often, always<br/><br/>
            
            <b>Chapter 2: Sentence Structure</b><br/><br/>
            
            <b>Simple Sentence</b><br/>
            A simple sentence has one subject and one verb.<br/><br/>
            
            Examples:<br/>
            The cat sleeps.<br/>
            I read books.<br/>
            She is happy.<br/><br/>
            
            <b>Compound Sentence</b><br/>
            A compound sentence has two or more simple sentences joined by a conjunction.<br/><br/>
            
            Examples:<br/>
            I like tea, and she likes coffee.<br/>
            He is tall, but she is short.<br/>
            I will study, or I will fail.<br/><br/>
            
            <b>Chapter 3: Tenses</b><br/><br/>
            
            <b>Present Tense</b><br/>
            I eat. / I am eating.<br/>
            She reads. / She is reading.<br/><br/>
            
            <b>Past Tense</b><br/>
            I ate. / I was eating.<br/>
            She read. / She was reading.<br/><br/>
            
            <b>Future Tense</b><br/>
            I will eat. / I will be eating.<br/>
            She will read. / She will be reading.<br/><br/>
            
            <b>Chapter 4: Common Grammar Rules</b><br/><br/>
            
            1. Use "a" before words that start with a consonant sound.<br/>
            2. Use "an" before words that start with a vowel sound.<br/>
            3. Use "the" when referring to specific things.<br/>
            4. Capitalize the first letter of sentences and proper nouns.<br/>
            5. Use periods at the end of statements.<br/>
            6. Use question marks at the end of questions.<br/>
            7. Use exclamation marks for strong emotions.<br/><br/>
            
            <b>Practice Exercises:</b><br/>
            1. Identify the parts of speech in sentences<br/>
            2. Write simple and compound sentences<br/>
            3. Change sentences from present to past tense<br/>
            4. Add articles (a, an, the) to sentences<br/>
            5. Correct grammar mistakes in sentences<br/><br/>
            
            <b>Remember:</b> Practice grammar daily. Read English books and articles. Write sentences and paragraphs regularly.
            """
        elif 'Vocabulary Builder' in book.title:
            return """
            <b>English Vocabulary Builder</b><br/><br/>
            
            <b>Chapter 1: Basic Words (A-C)</b><br/><br/>
            
            <b>A Words:</b><br/>
            Apple - a red or green fruit<br/>
            Animal - a living creature<br/>
            Answer - a reply to a question<br/>
            Ask - to request information<br/>
            Always - at all times<br/><br/>
            
            <b>B Words:</b><br/>
            Book - pages bound together for reading<br/>
            Beautiful - very pretty or attractive<br/>
            Big - large in size<br/>
            Blue - the color of the sky<br/>
            Brother - a male sibling<br/><br/>
            
            <b>C Words:</b><br/>
            Cat - a small furry pet<br/>
            Car - a vehicle with four wheels<br/>
            Cold - low temperature<br/>
            Come - to move toward someone<br/>
            Computer - an electronic device<br/><br/>
            
            <b>Chapter 2: Common Words (D-F)</b><br/><br/>
            
            <b>D Words:</b><br/>
            Dog - a loyal pet animal<br/>
            Day - 24-hour period<br/>
            Door - entrance to a room<br/>
            Drink - to consume liquid<br/>
            Drive - to operate a vehicle<br/><br/>
            
            <b>E Words:</b><br/>
            Eat - to consume food<br/>
            Eye - organ for seeing<br/>
            Easy - not difficult<br/>
            Every - each one<br/>
            End - the finish of something<br/><br/>
            
            <b>F Words:</b><br/>
            Friend - someone you like<br/>
            Family - parents and children<br/>
            Food - something you eat<br/>
            Fast - moving quickly<br/>
            Fun - enjoyable activity<br/><br/>
            
            <b>Chapter 3: Action Words</b><br/><br/>
            
            <b>Movement:</b><br/>
            Walk - to move on foot<br/>
            Run - to move quickly<br/>
            Jump - to leap in the air<br/>
            Swim - to move in water<br/>
            Fly - to move through air<br/><br/>
            
            <b>Daily Actions:</b><br/>
            Wake up - to stop sleeping<br/>
            Brush - to clean teeth<br/>
            Wash - to clean with water<br/>
            Cook - to prepare food<br/>
            Sleep - to rest at night<br/><br/>
            
            <b>Chapter 4: Descriptive Words</b><br/><br/>
            
            <b>Size:</b><br/>
            Big, small, large, tiny, huge<br/><br/>
            
            <b>Color:</b><br/>
            Red, blue, green, yellow, black, white<br/><br/>
            
            <b>Feelings:</b><br/>
            Happy, sad, angry, excited, tired<br/><br/>
            
            <b>Weather:</b><br/>
            Sunny, rainy, cloudy, windy, hot, cold<br/><br/>
            
            <b>Chapter 5: Word Families</b><br/><br/>
            
            <b>Family Words:</b><br/>
            Father, mother, brother, sister, baby<br/><br/>
            
            <b>School Words:</b><br/>
            Teacher, student, classroom, book, pencil<br/><br/>
            
            <b>Home Words:</b><br/>
            House, room, kitchen, bedroom, bathroom<br/><br/>
            
            <b>Food Words:</b><br/>
            Bread, milk, water, fruit, vegetable<br/><br/>
            
            <b>Practice Exercises:</b><br/>
            1. Match words with their meanings<br/>
            2. Use new words in sentences<br/>
            3. Find synonyms and antonyms<br/>
            4. Group words by categories<br/>
            5. Create word associations<br/><br/>
            
            <b>Remember:</b> Learn 5-10 new words daily. Use them in conversations. Read to see words in context.
            """
        else:
            return """
            <b>English Learning Guide</b><br/><br/>
            
            Welcome to this comprehensive English learning resource. This book will help you improve your English language skills through structured lessons and practical exercises.<br/><br/>
            
            <b>Chapter 1: Grammar Fundamentals</b><br/>
            English grammar forms the foundation of effective communication. We'll cover parts of speech, sentence structure, and common grammatical rules.<br/><br/>
            
            <b>Chapter 2: Vocabulary Building</b><br/>
            Expanding your vocabulary is essential for better communication. Learn new words, their meanings, and how to use them in context.<br/><br/>
            
            <b>Chapter 3: Writing Skills</b><br/>
            Develop your writing abilities through various exercises and techniques. Practice different types of writing including essays, letters, and reports.<br/><br/>
            
            <b>Chapter 4: Speaking and Pronunciation</b><br/>
            Improve your spoken English with pronunciation guides, conversation practice, and speaking exercises.<br/><br/>
            
            This is a free educational resource. You can read and download this content at no cost.
            """
    
    def get_math_sample_content(self, book):
        return """
        <b>Mathematics Fundamentals</b><br/><br/>
        
        Mathematics is the language of science and a fundamental skill for problem-solving. This book covers essential mathematical concepts and their applications.<br/><br/>
        
        <b>Chapter 1: Numbers and Operations</b><br/>
        Learn about different types of numbers, basic operations (addition, subtraction, multiplication, division), and number properties.<br/><br/>
        
        <b>Chapter 2: Algebra</b><br/>
        Introduction to algebraic concepts including variables, equations, and solving problems using algebraic methods.<br/><br/>
        
        <b>Chapter 3: Geometry</b><br/>
        Explore shapes, angles, areas, and volumes. Learn about geometric properties and relationships.<br/><br/>
        
        <b>Chapter 4: Problem Solving</b><br/>
        Apply mathematical concepts to solve real-world problems through step-by-step approaches and logical thinking.<br/><br/>
        
        This educational content is provided free of charge for learning purposes.
        """
    
    def get_science_sample_content(self, book):
        return """
        <b>Science Education</b><br/><br/>
        
        Science helps us understand the world around us. This book introduces fundamental scientific concepts and encourages scientific thinking.<br/><br/>
        
        <b>Chapter 1: Scientific Method</b><br/>
        Learn about observation, hypothesis, experimentation, and conclusion. Understand how scientists approach problems.<br/><br/>
        
        <b>Chapter 2: Physics Basics</b><br/>
        Introduction to motion, forces, energy, and matter. Explore the fundamental laws that govern our physical world.<br/><br/>
        
        <b>Chapter 3: Chemistry Fundamentals</b><br/>
        Discover atoms, molecules, chemical reactions, and the properties of different substances.<br/><br/>
        
        <b>Chapter 4: Biology Essentials</b><br/>
        Learn about living organisms, their structure, function, and the processes that sustain life.<br/><br/>
        
        This free educational resource promotes scientific literacy and critical thinking.
        """
    
    def get_general_sample_content(self, book):
        return """
        <b>Educational Content</b><br/><br/>
        
        This book provides valuable educational content designed to enhance your knowledge and skills in various subjects.<br/><br/>
        
        <b>Learning Objectives</b><br/>
        By the end of this book, you will have gained important knowledge and skills that can be applied in your studies and daily life.<br/><br/>
        
        <b>Key Topics Covered</b><br/>
        • Fundamental concepts and principles<br/>
        • Practical applications and examples<br/>
        • Exercises and activities for practice<br/>
        • Assessment and evaluation methods<br/><br/>
        
        <b>How to Use This Book</b><br/>
        Read through each chapter carefully, complete the exercises, and apply what you learn in practical situations.<br/><br/>
        
        This is a free educational resource available for everyone to access and learn from.
        """
