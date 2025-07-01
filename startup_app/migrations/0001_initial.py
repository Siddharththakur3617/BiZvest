from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('sector_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Startup',
            fields=[
                ('startup_id', models.AutoField(primary_key=True, serialize=False)),
                ('startup_name', models.CharField(max_length=100)),
                ('descr', models.TextField()),
                ('founder', models.CharField(max_length=100)),
                ('valuation', models.IntegerField()),
                ('last_year_profit', models.IntegerField(blank=True, null=True)),
                ('burn_rate', models.FloatField(blank=True, null=True)),
                ('contact_no', models.CharField(max_length=13)),
                ('email_id', models.CharField(max_length=50)),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='startup_app.sector')),
            ],
        ),
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('investor_id', models.AutoField(primary_key=True, serialize=False)),
                ('founder', models.CharField(max_length=100)),
                ('company_name', models.CharField(max_length=100)),
                ('descr', models.TextField(blank=True, null=True)),
                ('net_worth', models.IntegerField()),
                ('contact_no', models.CharField(max_length=13)),
                ('email', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Choices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest', models.FloatField()),
                ('investor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='startup_app.investor')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='startup_app.sector')),
            ],
            options={
                'unique_together': {('investor', 'sector')},
            },
        ),
        migrations.CreateModel(
            name='Deals',
            fields=[
                ('deal_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_of_deal', models.CharField(max_length=10)),
                ('amount_invested', models.IntegerField(default=0)),
                ('loan_given', models.IntegerField(default=0)),
                ('loan_time', models.IntegerField(default=0)),
                ('loan_rate', models.FloatField(default=0.0)),
                ('equity', models.FloatField(default=0.0)),
                ('investor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='startup_app.investor')),
                ('startup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='startup_app.startup')),
            ],
        ),
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('offer_id', models.AutoField(primary_key=True, serialize=False)),
                ('investment_asked', models.IntegerField(default=0)),
                ('equity_offered', models.FloatField(default=0)),
                ('loan_req', models.IntegerField(default=0)),
                ('loan_rate', models.FloatField(default=0)),
                ('loan_time', models.IntegerField(default=12)),
                ('startup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='startup_app.startup')),
            ],
        ),
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('investor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='startup_app.investor')),
                ('startup', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='startup_app.startup')),
            ],
            options={
                'constraints': [
                    models.CheckConstraint(check=models.Q(investor__isnull=False) | models.Q(startup__isnull=False), name='investor_or_startup_not_null'),
                ],
            },
        ),
    ]