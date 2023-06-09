# Generated by Django 3.2.12 on 2022-05-17 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0008_auto_20220517_0411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpost',
            name='location',
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
        migrations.AddIndex(
            model_name='userpost',
            index=models.Index(fields=['location', 'created_on'], name='location_created_idx'),
        ),
        migrations.AddIndex(
            model_name='userpost',
            index=models.Index(fields=['location', '-created_on'], name='location_created_desc_idx'),
        ),
        migrations.AddIndex(
            model_name='userpost',
            index=models.Index(fields=['caption_text', '-updated_on'], name='caption_updated_idx'),
        ),
    ]
