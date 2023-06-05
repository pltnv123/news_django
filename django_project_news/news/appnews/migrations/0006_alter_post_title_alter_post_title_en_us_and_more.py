# Generated by Django 4.1.7 on 2023-05-03 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appnews', '0005_alter_author_ratingauthor_alter_post_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(help_text='Название поста', max_length=128),
        ),
        migrations.AlterField(
            model_name='post',
            name='title_en_us',
            field=models.CharField(help_text='Название поста', max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='title_ru',
            field=models.CharField(help_text='Название поста', max_length=128, null=True),
        ),
    ]