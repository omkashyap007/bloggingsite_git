from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from users.models import Profile 
from blog.models import Fame



@receiver(post_save , sender= User) 
def create_profile(sender , instance , created , **kwargs) : 
    if created : 
        Profile.objects.create(user = instance )
        
@receiver(post_save , sender = User )
def save_profile(sender , instance , **kwargs) : 
    instance.profile.save()
    
    
@receiver(post_save , sender= User) 
def create_fame(sender , instance , created , **kwargs) : 
    if created : 
        Fame.objects.create(user = instance )
        
@receiver(post_save , sender = User )
def save_fame(sender , instance , **kwargs) : 
    instance.fame.save()