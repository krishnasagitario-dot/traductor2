import csv
from django.core.management.base import BaseCommand
from appProyecto1.models import MedicalTerm

class Command(BaseCommand):
    help = 'Import medical terms from CSV: code,system,preferred_term,synonyms,language'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', type=str)

    def handle(self, *args, **options):
        path = options['csvfile']
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for r in reader:
                obj, created = MedicalTerm.objects.update_or_create(
                    code=r['code'],
                    system=r.get('system','SNOMED-CT'),
                    defaults={
                        'preferred_term': r.get('preferred_term',''),
                        'synonyms': r.get('synonyms',''),
                        'language': r.get('language','es')
                    }
                )
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Imported {count} terms'))
