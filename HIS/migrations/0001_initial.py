# Generated by Django 4.1.7 on 2023-03-06 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_name', models.CharField(max_length=100)),
                ('doctor_name', models.CharField(max_length=100)),
                ('appointment_date', models.DateField()),
                ('appointment_time', models.TimeField()),
                ('reason', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('contact_info', models.CharField(max_length=100)),
                ('patient_type', models.CharField(choices=[('OPD', 'OPD'), ('IPD', 'IPD'), ('Emergency', 'Emergency')], max_length=20)),
                ('Date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PatientDischarge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discharge_type', models.CharField(max_length=50)),
                ('discharge_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('discharged_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HIS.doctor')),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HIS.patient')),
            ],
        ),
        migrations.CreateModel(
            name='OTSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surgery_name', models.CharField(max_length=100)),
                ('cvt_surgeon_name', models.CharField(max_length=100)),
                ('perfusionist', models.CharField(max_length=100)),
                ('surgery_code', models.CharField(max_length=100)),
                ('anaesthesia_doctor_name', models.CharField(max_length=100)),
                ('surgery_note', models.TextField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('surgery_for', models.CharField(max_length=100)),
                ('estimate_time_of_surgery', models.CharField(max_length=50)),
                ('is_approved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('doctor_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HIS.doctor')),
                ('patient_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HIS.patient')),
                ('speciality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HIS.specialty')),
            ],
        ),
        migrations.CreateModel(
            name='IPDPatient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bar_code', models.CharField(max_length=20, unique=True)),
                ('consent_token', models.CharField(blank=True, max_length=50, null=True)),
                ('loa', models.CharField(blank=True, max_length=50, null=True)),
                ('disabilities', models.TextField(blank=True, null=True)),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='HIS.patient')),
                ('primary_consulting_doc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HIS.doctor')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HIS.specialty')),
                ('ward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HIS.ward')),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='specialty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HIS.specialty'),
        ),
        migrations.CreateModel(
            name='DeathSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_code', models.CharField(max_length=20)),
                ('patient_name', models.CharField(max_length=100)),
                ('death_date', models.DateField()),
                ('admission_no', models.CharField(max_length=20)),
                ('confirm', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HIS.patient')),
            ],
        ),
    ]
