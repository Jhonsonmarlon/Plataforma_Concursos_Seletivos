from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),  # Ajustado para depender da migração inicial
    ]

    operations = [
        # Primeiro adiciona o novo campo cep
        migrations.AddField(
            model_name='escola',
            name='cep',
            field=models.CharField(default='', max_length=9),
            preserve_default=False,
        ),
        # Copia os dados de cnpj para cep
        migrations.RunPython(
            code=lambda apps, schema_editor: apps.get_model('core', 'Escola').objects.update(cep=models.F('cnpj'))
        ),
        # Remove o campo antigo cnpj
        migrations.RemoveField(
            model_name='escola',
            name='cnpj',
        ),
    ] 