# Generated by Django 3.0.8 on 2022-08-12 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_api3'),
    ]

    operations = [
        migrations.CreateModel(
            name='Api4',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.Base')),
                ('regId', models.CharField(max_length=20)),
                ('tmFc', models.CharField(max_length=20)),
                ('rnSt3Am', models.CharField(max_length=10)),
                ('rnSt3Pm', models.CharField(max_length=10)),
                ('rnSt4Am', models.CharField(max_length=10)),
                ('rnSt4Pm', models.CharField(max_length=10)),
                ('rnSt5Am', models.CharField(max_length=10)),
                ('rnSt5Pm', models.CharField(max_length=10)),
                ('rnSt6Am', models.CharField(max_length=10)),
                ('rnSt6Pm', models.CharField(max_length=10)),
                ('rnSt7Am', models.CharField(max_length=10)),
                ('rnSt7Pm', models.CharField(max_length=10)),
                ('rnSt8', models.CharField(max_length=10)),
                ('rnSt9', models.CharField(max_length=10)),
                ('rnSt10', models.CharField(max_length=10)),
                ('wf3Am', models.CharField(max_length=20)),
                ('wf3Pm', models.CharField(max_length=20)),
                ('wf4Am', models.CharField(max_length=20)),
                ('wf4Pm', models.CharField(max_length=20)),
                ('wf5Am', models.CharField(max_length=20)),
                ('wf5Pm', models.CharField(max_length=20)),
                ('wf6Am', models.CharField(max_length=20)),
                ('wf6Pm', models.CharField(max_length=20)),
                ('wf7Am', models.CharField(max_length=20)),
                ('wf7Pm', models.CharField(max_length=20)),
                ('wf8', models.CharField(max_length=20)),
                ('wf9', models.CharField(max_length=20)),
                ('wf10', models.CharField(max_length=20)),
            ],
            bases=('main.base',),
        ),
    ]
