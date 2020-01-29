from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import sentry.db.models.fields.bounded
import sentry.db.models.fields.foreignkey


class Migration(migrations.Migration):
    # This flag is used to mark that a migration shouldn't be automatically run in
    # production. We set this to True for operations that we think are risky and want
    # someone from ops to run manually and monitor.
    # General advice is that if in doubt, mark your migration as `is_dangerous`.
    # Some things you should always mark as dangerous:
    # - Adding indexes to large tables. These indexes should be created concurrently,
    #   unfortunately we can't run migrations outside of a transaction until Django
    #   1.10. So until then these should be run manually.
    # - Large data migrations. Typically we want these to be run manually by ops so that
    #   they can be monitored. Since data migrations will now hold a transaction open
    #   this is even more important.
    # - Adding columns to highly active tables, even ones that are NULL.
    is_dangerous = True


    dependencies = [
        ('sentry', '0027_exporteddata'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.CreateModel(
                    name='AlertRuleEnvironment',
                    fields=[
                        ('id', sentry.db.models.fields.bounded.BoundedBigAutoField(primary_key=True, serialize=False)),
                        ('alert_rule', sentry.db.models.fields.foreignkey.FlexibleForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sentry.AlertRule')),
                        ('environment', sentry.db.models.fields.foreignkey.FlexibleForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sentry.Environment')),
                    ],
                    options={
                        'db_table': 'sentry_alertruleenvironment',
                    },
                ),
                migrations.AddField(
                    model_name='alertrule',
                    name='environment',
                    field=models.ManyToManyField(related_name='alert_rule_environment', through='sentry.AlertRuleEnvironment', to='sentry.Environment'),
                ),
                migrations.AlterUniqueTogether(
                    name='alertruleenvironment',
                    unique_together=set([('alert_rule', 'environment')]),
                ),
            ],
            state_operations=[],
        ),
    ]
