"""
Redefinir senha de login (usuário Django).
Uso:
  Listar usuários:
    python manage.py reset_login_password
  Redefinir senha (com variáveis de ambiente):
    RESET_USERNAME=meu_usuario RESET_PASSWORD=nova_senha python manage.py reset_login_password
  Ou no PowerShell:
    $env:RESET_USERNAME='meu_usuario'; $env:RESET_PASSWORD='nova_senha'; python manage.py reset_login_password
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Lista usuários ou redefine a senha de um usuário (RESET_USERNAME e RESET_PASSWORD no ambiente)."

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get("RESET_USERNAME", "").strip()
        password = os.environ.get("RESET_PASSWORD", "")

        if username and password:
            try:
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Senha do usuário '{username}' alterada com sucesso."))
            except User.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"Usuário '{username}' não encontrado."))
        else:
            self.stdout.write("Usuários no banco:")
            for u in User.objects.all().order_by("username"):
                self.stdout.write(f"  - {u.username}")
            if not username:
                self.stdout.write("\nPara redefinir a senha, defina RESET_USERNAME e RESET_PASSWORD e rode de novo.")
            elif not password:
                self.stderr.write("Defina RESET_PASSWORD no ambiente.")
