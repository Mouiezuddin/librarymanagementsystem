# Generated migration for adding database constraints

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='book',
            constraint=models.CheckConstraint(
                check=models.Q(total_copies__gte=1),
                name='book_total_copies_positive'
            ),
        ),
        migrations.AddConstraint(
            model_name='book',
            constraint=models.CheckConstraint(
                check=models.Q(available_copies__gte=0),
                name='book_available_copies_non_negative'
            ),
        ),
        migrations.AddConstraint(
            model_name='book',
            constraint=models.CheckConstraint(
                check=models.Q(available_copies__lte=models.F('total_copies')),
                name='book_available_lte_total'
            ),
        ),
    ]
