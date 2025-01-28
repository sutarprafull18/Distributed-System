from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,blank=False,null=False)
    email = models.EmailField(unique=True,blank=False,null=True)

    class Meta:
        app_label = 'users_app'
        db_table = 'users_app_user'

    def save(self, *args, **kwargs):
        # Skip saving if name is blank or email already exists
        if not self.name or not self.name.strip():
            return None

        # Check for existing email
        if User.objects.using('users_db').filter(email=self.email).exists():
            return None

        super().save(using='users_db')
        return self

    def __str__(self):
        return f"{self.id} - {self.name} ({self.email})"