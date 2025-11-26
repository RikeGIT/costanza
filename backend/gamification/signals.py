from django.db.models.signals import post_save
from django.dispatch import receiver
from trilhas.models import ProgressoAtividade  # <--- Mudamos de Enrollment para o nome correto
from .models import Badge, UserBadge

@receiver(post_save, sender=ProgressoAtividade)
def award_activity_completion_badge(sender, instance, created, **kwargs):
    # Verifica se o status mudou para 'completed' (conforme definido no seu models.py)
    if instance.status == 'completed':
        try:
            # Tenta pegar a medalha pelo código (slug) que criamos no admin
            badge = Badge.objects.get(slug='pioneiro')
            
            # Dá a medalha ao usuário (se ele já não tiver)
            UserBadge.objects.get_or_create(user=instance.user, badge=badge)
            print(f">>> SUCESSO: Medalha {badge.name} concedida para {instance.user}!")
            
        except Badge.DoesNotExist:
            print(">>> AVISO: A medalha com slug 'pioneiro' não foi encontrada no banco.")