from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Curso(models.Model):
    nome = models.CharField(max_length=120)
    imagem = models.ImageField(upload_to='cursos/', blank=True, null=True)

    def __str__(self):
        return self.nome


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        
        # Define a senha padrão se nenhuma for fornecida
        if not password:
            password = "senha123"  # Defina sua senha padrão aqui
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    cursos = models.ManyToManyField(Curso, through='Matricula')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    alterou_senha = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    def __str__(self):
        return self.nome


class Matricula(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    data_matricula = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.aluno.nome} - {self.curso.nome}'
