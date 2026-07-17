from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@afleme.com', 'afleme1234!')
            self.stdout.write('관리자 계정 생성 완료')
        else:
            self.stdout.write('이미 존재함')