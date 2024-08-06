# Generated by Django 4.0 on 2021-12-30 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_balance', models.FloatField(default=0)),
                ('wallet_address', models.TextField(blank=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_removed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_wallet', to='accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='WalletTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('transaction_type', models.TextField(choices=[('pay', 'Pay'), ('deposit', 'Deposit'), ('received', 'Received')], max_length=40)),
                ('transaction_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('wallet', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wallet_transaction', to='wallet_management.wallet')),
            ],
        ),
    ]
