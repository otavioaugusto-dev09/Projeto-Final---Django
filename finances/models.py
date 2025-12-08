from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Categoria(models.Model):
    TIPO_CHOICES = (
      ('despesa', 'Despesa'),
      ('receita', 'Receita'),
    )

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} - {self.tipo}"
    

class Movimentacao(models.Model):
    valor =  models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=200)
    data = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.descricao} - R${self.valor}"