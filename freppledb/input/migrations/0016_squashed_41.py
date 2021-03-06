#
# Copyright (C) 2017 by frePPLe bv
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from django.core.management import call_command
from django.db import migrations, models
import django.utils.timezone
import datetime
import freppledb.common.fields


def loadParameters(apps, schema_editor):
    from django.core.management.commands.loaddata import Command

    call_command(
        Command(),
        "parameters.json",
        app_label="input",
        verbosity=0,
        database=schema_editor.connection.alias,
    )


class Migration(migrations.Migration):

    dependencies = [("common", "0008_squashed_41"), ("admin", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Buffer",
            fields=[
                (
                    "lft",
                    models.PositiveIntegerField(
                        db_index=True, blank=True, editable=False, null=True
                    ),
                ),
                (
                    "rght",
                    models.PositiveIntegerField(editable=False, blank=True, null=True),
                ),
                (
                    "lvl",
                    models.PositiveIntegerField(editable=False, blank=True, null=True),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=300,
                        help_text="Unique identifier",
                        verbose_name="name",
                        serialize=False,
                        primary_key=True,
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="source",
                        null=True,
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        verbose_name="last modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        max_length=500,
                        blank=True,
                        verbose_name="description",
                        null=True,
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="category",
                        null=True,
                    ),
                ),
                (
                    "subcategory",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="subcategory",
                        null=True,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        max_length=20,
                        blank=True,
                        verbose_name="type",
                        choices=[("default", "default"), ("infinite", "infinite")],
                        null=True,
                        default="default",
                    ),
                ),
                (
                    "onhand",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="onhand",
                        decimal_places=6,
                        help_text="current inventory",
                        null=True,
                        default="0.00",
                    ),
                ),
                (
                    "minimum",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="minimum",
                        decimal_places=6,
                        help_text="safety stock",
                        null=True,
                        default="0.00",
                    ),
                ),
                (
                    "min_interval",
                    models.DurationField(
                        blank=True,
                        verbose_name="min_interval",
                        null=True,
                        help_text="Batching window for grouping replenishments in batches",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "buffers",
                "verbose_name": "buffer",
                "abstract": False,
                "ordering": ["name"],
                "db_table": "buffer",
            },
        ),
        migrations.CreateModel(
            name="Calendar",
            fields=[
                (
                    "source",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="source",
                        null=True,
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        verbose_name="last modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=300,
                        verbose_name="name",
                        serialize=False,
                        primary_key=True,
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        max_length=500,
                        blank=True,
                        verbose_name="description",
                        null=True,
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="category",
                        null=True,
                    ),
                ),
                (
                    "subcategory",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="subcategory",
                        null=True,
                    ),
                ),
                (
                    "defaultvalue",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="default value",
                        decimal_places=6,
                        help_text="Value to be used when no entry is effective",
                        null=True,
                        default="0.00",
                    ),
                ),
            ],
            options={
                "db_table": "calendar",
                "verbose_name_plural": "calendars",
                "verbose_name": "calendar",
                "abstract": False,
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="CalendarBucket",
            fields=[
                (
                    "source",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="source",
                        null=True,
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        verbose_name="last modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "id",
                    models.AutoField(
                        verbose_name="identifier", serialize=False, primary_key=True
                    ),
                ),
                (
                    "startdate",
                    models.DateTimeField(
                        blank=True, verbose_name="start date", null=True
                    ),
                ),
                (
                    "enddate",
                    models.DateTimeField(
                        blank=True,
                        verbose_name="end date",
                        null=True,
                        default=datetime.datetime(2030, 12, 31, 0, 0),
                    ),
                ),
                (
                    "value",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="value",
                        decimal_places=6,
                        default="0.00",
                    ),
                ),
                (
                    "priority",
                    models.IntegerField(
                        blank=True, verbose_name="priority", null=True, default=0
                    ),
                ),
                ("monday", models.BooleanField(verbose_name="Monday", default=True)),
                ("tuesday", models.BooleanField(verbose_name="Tuesday", default=True)),
                (
                    "wednesday",
                    models.BooleanField(verbose_name="Wednesday", default=True),
                ),
                (
                    "thursday",
                    models.BooleanField(verbose_name="Thursday", default=True),
                ),
                ("friday", models.BooleanField(verbose_name="Friday", default=True)),
                (
                    "saturday",
                    models.BooleanField(verbose_name="Saturday", default=True),
                ),
                ("sunday", models.BooleanField(verbose_name="Sunday", default=True)),
                (
                    "starttime",
                    models.TimeField(
                        blank=True,
                        verbose_name="start time",
                        null=True,
                        default=datetime.time(0, 0),
                    ),
                ),
                (
                    "endtime",
                    models.TimeField(
                        blank=True,
                        verbose_name="end time",
                        null=True,
                        default=datetime.time(23, 59, 59),
                    ),
                ),
                (
                    "calendar",
                    models.ForeignKey(
                        verbose_name="calendar",
                        related_name="buckets",
                        to="input.Calendar",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "calendar buckets",
                "verbose_name": "calendar bucket",
                "abstract": False,
                "ordering": ["calendar", "id"],
                "db_table": "calendarbucket",
            },
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "lft",
                    models.PositiveIntegerField(
                        db_index=True, blank=True, editable=False, null=True
                    ),
                ),
                (
                    "rght",
                    models.PositiveIntegerField(editable=False, blank=True, null=True),
                ),
                (
                    "lvl",
                    models.PositiveIntegerField(editable=False, blank=True, null=True),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=300,
                        help_text="Unique identifier",
                        verbose_name="name",
                        serialize=False,
                        primary_key=True,
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="source",
                        null=True,
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        verbose_name="last modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        max_length=500,
                        blank=True,
                        verbose_name="description",
                        null=True,
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="category",
                        null=True,
                    ),
                ),
                (
                    "subcategory",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="subcategory",
                        null=True,
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        verbose_name="owner",
                        related_name="xchildren",
                        to="input.Customer",
                        help_text="Hierarchical parent",
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={
                "db_table": "customer",
                "verbose_name_plural": "customers",
                "verbose_name": "customer",
                "abstract": False,
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Demand",
            fields=[
                (
                    "lft",
                    models.PositiveIntegerField(
                        db_index=True, blank=True, editable=False, null=True
                    ),
                ),
                (
                    "rght",
                    models.PositiveIntegerField(editable=False, blank=True, null=True),
                ),
                (
                    "lvl",
                    models.PositiveIntegerField(editable=False, blank=True, null=True),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=300,
                        help_text="Unique identifier",
                        verbose_name="name",
                        serialize=False,
                        primary_key=True,
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="source",
                        null=True,
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        verbose_name="last modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        max_length=500,
                        blank=True,
                        verbose_name="description",
                        null=True,
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="category",
                        null=True,
                    ),
                ),
                (
                    "subcategory",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="subcategory",
                        null=True,
                    ),
                ),
                (
                    "due",
                    models.DateTimeField(
                        help_text="Due date of the demand", verbose_name="due"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        max_length=10,
                        blank=True,
                        verbose_name="status",
                        help_text='Status of the demand. Only "open" demands are planned',
                        choices=[
                            ("inquiry", "inquiry"),
                            ("quote", "quote"),
                            ("open", "open"),
                            ("closed", "closed"),
                            ("canceled", "canceled"),
                        ],
                        null=True,
                        default="open",
                    ),
                ),
                (
                    "quantity",
                    models.DecimalField(
                        max_digits=15, verbose_name="quantity", decimal_places=6
                    ),
                ),
                (
                    "priority",
                    models.IntegerField(
                        help_text="Priority of the demand (lower numbers indicate more important demands)",
                        verbose_name="priority",
                        default=10,
                    ),
                ),
                (
                    "minshipment",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="minimum shipment",
                        decimal_places=6,
                        help_text="Minimum shipment quantity when planning this demand",
                        null=True,
                    ),
                ),
                (
                    "maxlateness",
                    models.DurationField(
                        blank=True,
                        verbose_name="maximum lateness",
                        null=True,
                        help_text="Maximum lateness allowed when planning this demand",
                    ),
                ),
                (
                    "delay",
                    models.DurationField(
                        editable=False, blank=True, verbose_name="delay", null=True
                    ),
                ),
                (
                    "plannedquantity",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="planned quantity",
                        decimal_places=6,
                        editable=False,
                        help_text="Quantity planned for delivery",
                        null=True,
                    ),
                ),
                (
                    "deliverydate",
                    models.DateTimeField(
                        editable=False,
                        blank=True,
                        verbose_name="delivery date",
                        null=True,
                        help_text="Delivery date of the demand",
                    ),
                ),
                (
                    "plan",
                    freppledb.common.fields.JSONField(
                        editable=False, blank=True, null=True, default="{}"
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        to="input.Customer",
                        verbose_name="customer",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "db_table": "demand",
                "verbose_name_plural": "sales orders",
                "verbose_name": "sales order",
                "abstract": False,
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "lft",
                    models.PositiveIntegerField(
                        db_index=True, blank=True, editable=False, null=True
                    ),
                ),
                (
                    "rght",
                    models.PositiveIntegerField(editable=False, blank=True, null=True),
                ),
                (
                    "lvl",
                    models.PositiveIntegerField(editable=False, blank=True, null=True),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=300,
                        help_text="Unique identifier",
                        verbose_name="name",
                        serialize=False,
                        primary_key=True,
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="source",
                        null=True,
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        verbose_name="last modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        max_length=500,
                        blank=True,
                        verbose_name="description",
                        null=True,
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="category",
                        null=True,
                    ),
                ),
                (
                    "subcategory",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="subcategory",
                        null=True,
                    ),
                ),
                (
                    "cost",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="cost",
                        decimal_places=6,
                        help_text="Cost of the item",
                        null=True,
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        verbose_name="owner",
                        related_name="xchildren",
                        to="input.Item",
                        help_text="Hierarchical parent",
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={
                "db_table": "item",
                "verbose_name_plural": "items",
                "verbose_name": "item",
                "abstract": False,
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="ItemDistribution",
            fields=[
                (
                    "source",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="source",
                        null=True,
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        verbose_name="last modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "id",
                    models.AutoField(
                        verbose_name="identifier", serialize=False, primary_key=True
                    ),
                ),
                (
                    "leadtime",
                    models.DurationField(
                        blank=True,
                        verbose_name="lead time",
                        null=True,
                        help_text="lead time",
                    ),
                ),
                (
                    "sizeminimum",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="size minimum",
                        decimal_places=6,
                        help_text="A minimum shipping quantity",
                        null=True,
                        default="1.0",
                    ),
                ),
                (
                    "sizemultiple",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="size multiple",
                        decimal_places=6,
                        help_text="A multiple shipping quantity",
                        null=True,
                    ),
                ),
                (
                    "cost",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="cost",
                        decimal_places=6,
                        help_text="Shipping cost per unit",
                        null=True,
                    ),
                ),
                (
                    "priority",
                    models.IntegerField(
                        blank=True,
                        verbose_name="priority",
                        null=True,
                        help_text="Priority among all alternates",
                        default=1,
                    ),
                ),
                (
                    "effective_start",
                    models.DateTimeField(
                        blank=True,
                        verbose_name="effective start",
                        null=True,
                        help_text="Validity start date",
                    ),
                ),
                (
                    "effective_end",
                    models.DateTimeField(
                        blank=True,
                        verbose_name="effective end",
                        null=True,
                        help_text="Validity end date",
                    ),
                ),
                (
                    "resource_qty",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="resource quantity",
                        decimal_places=6,
                        help_text="Resource capacity consumed per distributed unit",
                        null=True,
                        default="1.0",
                    ),
                ),
                (
                    "fence",
                    models.DurationField(
                        blank=True,
                        verbose_name="fence",
                        null=True,
                        help_text="Frozen fence for creating new shipments",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        verbose_name="item",
                        related_name="distributions",
                        to="input.Item",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "db_table": "itemdistribution",
                "verbose_name_plural": "item distributions",
                "verbose_name": "item distribution",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ItemSupplier",
            fields=[
                (
                    "source",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="source",
                        null=True,
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        verbose_name="last modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "id",
                    models.AutoField(
                        verbose_name="identifier", serialize=False, primary_key=True
                    ),
                ),
                (
                    "leadtime",
                    models.DurationField(
                        blank=True,
                        verbose_name="lead time",
                        null=True,
                        help_text="Purchasing lead time",
                    ),
                ),
                (
                    "sizeminimum",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="size minimum",
                        decimal_places=6,
                        help_text="A minimum purchasing quantity",
                        null=True,
                        default="1.0",
                    ),
                ),
                (
                    "sizemultiple",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="size multiple",
                        decimal_places=6,
                        help_text="A multiple purchasing quantity",
                        null=True,
                    ),
                ),
                (
                    "cost",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="cost",
                        decimal_places=6,
                        help_text="Purchasing cost per unit",
                        null=True,
                    ),
                ),
                (
                    "priority",
                    models.IntegerField(
                        blank=True,
                        verbose_name="priority",
                        null=True,
                        help_text="Priority among all alternates",
                        default=1,
                    ),
                ),
                (
                    "effective_start",
                    models.DateTimeField(
                        blank=True,
                        verbose_name="effective start",
                        null=True,
                        help_text="Validity start date",
                    ),
                ),
                (
                    "effective_end",
                    models.DateTimeField(
                        blank=True,
                        verbose_name="effective end",
                        null=True,
                        help_text="Validity end date",
                    ),
                ),
                (
                    "resource_qty",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="resource quantity",
                        decimal_places=6,
                        help_text="Resource capacity consumed per purchased unit",
                        null=True,
                        default="1.0",
                    ),
                ),
                (
                    "fence",
                    models.DurationField(
                        blank=True,
                        verbose_name="fence",
                        null=True,
                        help_text="Frozen fence for creating new procurements",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        verbose_name="item",
                        related_name="itemsuppliers",
                        to="input.Item",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "db_table": "itemsupplier",
                "verbose_name_plural": "item suppliers",
                "verbose_name": "item supplier",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "lft",
                    models.PositiveIntegerField(
                        db_index=True, blank=True, editable=False, null=True
                    ),
                ),
                (
                    "rght",
                    models.PositiveIntegerField(editable=False, blank=True, null=True),
                ),
                (
                    "lvl",
                    models.PositiveIntegerField(editable=False, blank=True, null=True),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=300,
                        help_text="Unique identifier",
                        verbose_name="name",
                        serialize=False,
                        primary_key=True,
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="source",
                        null=True,
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        verbose_name="last modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        max_length=500,
                        blank=True,
                        verbose_name="description",
                        null=True,
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="category",
                        null=True,
                    ),
                ),
                (
                    "subcategory",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="subcategory",
                        null=True,
                    ),
                ),
                (
                    "available",
                    models.ForeignKey(
                        blank=True,
                        verbose_name="available",
                        to="input.Calendar",
                        help_text="Calendar defining the working hours and holidays of this location",
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        verbose_name="owner",
                        related_name="xchildren",
                        to="input.Location",
                        help_text="Hierarchical parent",
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={
                "db_table": "location",
                "verbose_name_plural": "locations",
                "verbose_name": "location",
                "abstract": False,
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Operation",
            fields=[
                (
                    "source",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="source",
                        null=True,
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        verbose_name="last modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=300,
                        verbose_name="name",
                        serialize=False,
                        primary_key=True,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        max_length=20,
                        blank=True,
                        verbose_name="type",
                        choices=[
                            ("fixed_time", "fixed_time"),
                            ("time_per", "time_per"),
                            ("routing", "routing"),
                            ("alternate", "alternate"),
                            ("split", "split"),
                        ],
                        null=True,
                        default="fixed_time",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        max_length=500,
                        blank=True,
                        verbose_name="description",
                        null=True,
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="category",
                        null=True,
                    ),
                ),
                (
                    "subcategory",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="subcategory",
                        null=True,
                    ),
                ),
                (
                    "priority",
                    models.IntegerField(
                        blank=True,
                        verbose_name="priority",
                        null=True,
                        help_text="Priority among all alternates",
                        default=1,
                    ),
                ),
                (
                    "effective_start",
                    models.DateTimeField(
                        blank=True,
                        verbose_name="effective start",
                        null=True,
                        help_text="Validity start date",
                    ),
                ),
                (
                    "effective_end",
                    models.DateTimeField(
                        blank=True,
                        verbose_name="effective end",
                        null=True,
                        help_text="Validity end date",
                    ),
                ),
                (
                    "fence",
                    models.DurationField(
                        blank=True,
                        verbose_name="release fence",
                        null=True,
                        help_text="Operationplans within this time window from the current day are expected to be released to production ERP",
                    ),
                ),
                (
                    "posttime",
                    models.DurationField(
                        blank=True,
                        verbose_name="post-op time",
                        null=True,
                        help_text="A delay time to be respected as a soft constraint after ending the operation",
                    ),
                ),
                (
                    "sizeminimum",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="size minimum",
                        decimal_places=6,
                        help_text="A minimum quantity for operationplans",
                        null=True,
                        default="1.0",
                    ),
                ),
                (
                    "sizemultiple",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="size multiple",
                        decimal_places=6,
                        help_text="A multiple quantity for operationplans",
                        null=True,
                    ),
                ),
                (
                    "sizemaximum",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="size maximum",
                        decimal_places=6,
                        help_text="A maximum quantity for operationplans",
                        null=True,
                    ),
                ),
                (
                    "cost",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="cost",
                        decimal_places=6,
                        help_text="Cost per operationplan unit",
                        null=True,
                    ),
                ),
                (
                    "duration",
                    models.DurationField(
                        blank=True,
                        verbose_name="duration",
                        null=True,
                        help_text="A fixed duration for the operation",
                    ),
                ),
                (
                    "duration_per",
                    models.DurationField(
                        blank=True,
                        verbose_name="duration per unit",
                        null=True,
                        help_text="A variable duration for the operation",
                    ),
                ),
                (
                    "search",
                    models.CharField(
                        max_length=20,
                        blank=True,
                        verbose_name="search mode",
                        help_text="Method to select preferred alternate",
                        choices=[
                            ("PRIORITY", "priority"),
                            ("MINCOST", "minimum cost"),
                            ("MINPENALTY", "minimum penalty"),
                            ("MINCOSTPENALTY", "minimum cost plus penalty"),
                        ],
                        null=True,
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        blank=True,
                        verbose_name="item",
                        related_name="operations",
                        to="input.Item",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        to="input.Location",
                        verbose_name="location",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "db_table": "operation",
                "verbose_name_plural": "operations",
                "verbose_name": "operation",
                "abstract": False,
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="OperationMaterial",
            fields=[
                (
                    "source",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="source",
                        null=True,
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        verbose_name="last modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "id",
                    models.AutoField(
                        verbose_name="identifier", serialize=False, primary_key=True
                    ),
                ),
                (
                    "quantity",
                    models.DecimalField(
                        max_digits=15,
                        help_text="Quantity to consume or produce per operationplan unit",
                        verbose_name="quantity",
                        decimal_places=6,
                        default="1.00",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        max_length=20,
                        blank=True,
                        verbose_name="type",
                        help_text="Consume/produce material at the start or the end of the operationplan",
                        choices=[
                            ("start", "Start"),
                            ("end", "End"),
                            ("fixed_start", "Fixed start"),
                            ("fixed_end", "Fixed end"),
                        ],
                        null=True,
                        default="start",
                    ),
                ),
                (
                    "effective_start",
                    models.DateTimeField(
                        blank=True,
                        verbose_name="effective start",
                        null=True,
                        help_text="Validity start date",
                    ),
                ),
                (
                    "effective_end",
                    models.DateTimeField(
                        blank=True,
                        verbose_name="effective end",
                        null=True,
                        help_text="Validity end date",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=300,
                        blank=True,
                        verbose_name="name",
                        null=True,
                        help_text="Optional name of this operation material",
                    ),
                ),
                (
                    "priority",
                    models.IntegerField(
                        blank=True,
                        verbose_name="priority",
                        null=True,
                        help_text="Priority of this operation material in a group of alternates",
                        default=1,
                    ),
                ),
                (
                    "search",
                    models.CharField(
                        max_length=20,
                        blank=True,
                        verbose_name="search mode",
                        help_text="Method to select preferred alternate",
                        choices=[
                            ("PRIORITY", "priority"),
                            ("MINCOST", "minimum cost"),
                            ("MINPENALTY", "minimum penalty"),
                            ("MINCOSTPENALTY", "minimum cost plus penalty"),
                        ],
                        null=True,
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        verbose_name="item",
                        related_name="operationmaterials",
                        to="input.Item",
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "operation",
                    models.ForeignKey(
                        verbose_name="operation",
                        related_name="operationmaterials",
                        to="input.Operation",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "db_table": "operationmaterial",
                "verbose_name_plural": "operation materials",
                "verbose_name": "operation material",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="OperationPlan",
            fields=[
                (
                    "source",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="source",
                        null=True,
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        verbose_name="last modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "id",
                    models.AutoField(
                        verbose_name="identifier",
                        serialize=False,
                        help_text="Unique identifier of an operationplan",
                        primary_key=True,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        max_length=20,
                        blank=True,
                        verbose_name="status",
                        help_text="Status of the order",
                        choices=[
                            ("proposed", "proposed"),
                            ("approved", "approved"),
                            ("confirmed", "confirmed"),
                            ("closed", "closed"),
                        ],
                        null=True,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        max_length=5,
                        db_index=True,
                        help_text="Order type",
                        verbose_name="type",
                        choices=[
                            ("STCK", "inventory"),
                            ("MO", "manufacturing order"),
                            ("PO", "purchase order"),
                            ("DO", "distribution order"),
                            ("DLVR", "customer shipment"),
                        ],
                        default="MO",
                    ),
                ),
                (
                    "reference",
                    models.CharField(
                        max_length=300,
                        blank=True,
                        verbose_name="reference",
                        null=True,
                        help_text="External reference of this order",
                    ),
                ),
                (
                    "quantity",
                    models.DecimalField(
                        max_digits=15,
                        decimal_places=6,
                        verbose_name="quantity",
                        default="1.00",
                    ),
                ),
                (
                    "color",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="color",
                        decimal_places=6,
                        null=True,
                        default="0.00",
                    ),
                ),
                (
                    "startdate",
                    models.DateTimeField(
                        blank=True,
                        verbose_name="start date",
                        null=True,
                        help_text="start date",
                    ),
                ),
                (
                    "enddate",
                    models.DateTimeField(
                        blank=True,
                        verbose_name="end date",
                        null=True,
                        help_text="end date",
                    ),
                ),
                (
                    "criticality",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="criticality",
                        decimal_places=6,
                        editable=False,
                        null=True,
                    ),
                ),
                (
                    "delay",
                    models.DurationField(
                        editable=False, blank=True, verbose_name="delay", null=True
                    ),
                ),
                (
                    "plan",
                    freppledb.common.fields.JSONField(
                        editable=False, blank=True, null=True, default="{}"
                    ),
                ),
                (
                    "due",
                    models.DateTimeField(
                        editable=False,
                        blank=True,
                        verbose_name="due",
                        null=True,
                        help_text="Due date of the demand/forecast",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=1000,
                        db_index=True,
                        blank=True,
                        verbose_name="name",
                        null=True,
                    ),
                ),
                (
                    "demand",
                    models.ForeignKey(
                        blank=True,
                        verbose_name="demand",
                        to="input.Demand",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "destination",
                    models.ForeignKey(
                        blank=True,
                        verbose_name="destination",
                        related_name="destinations",
                        to="input.Location",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        blank=True,
                        verbose_name="item",
                        to="input.Item",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        blank=True,
                        verbose_name="location",
                        to="input.Location",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "operation",
                    models.ForeignKey(
                        blank=True,
                        verbose_name="operation",
                        to="input.Operation",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "origin",
                    models.ForeignKey(
                        blank=True,
                        verbose_name="origin",
                        related_name="origins",
                        to="input.Location",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        verbose_name="owner",
                        related_name="xchildren",
                        to="input.OperationPlan",
                        help_text="Hierarchical parent",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "db_table": "operationplan",
                "verbose_name_plural": "operationplans",
                "verbose_name": "operationplan",
                "abstract": False,
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="OperationPlanMaterial",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        auto_created=True,
                        serialize=False,
                        primary_key=True,
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="source",
                        null=True,
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        verbose_name="last modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "quantity",
                    models.DecimalField(
                        max_digits=15, verbose_name="quantity", decimal_places=6
                    ),
                ),
                ("flowdate", models.DateTimeField(db_index=True, verbose_name="date")),
                (
                    "onhand",
                    models.DecimalField(
                        max_digits=15, verbose_name="onhand", decimal_places=6
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        max_length=20,
                        blank=True,
                        verbose_name="status",
                        help_text="Status of the OperationPlanMaterial",
                        choices=[("proposed", "proposed"), ("confirmed", "confirmed")],
                        null=True,
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        blank=True,
                        verbose_name="item",
                        related_name="operationplanmaterials",
                        to="input.Item",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        blank=True,
                        verbose_name="location",
                        related_name="operationplanmaterials",
                        to="input.Location",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "operationplan",
                    models.ForeignKey(
                        verbose_name="operationplan",
                        related_name="materials",
                        to="input.OperationPlan",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "db_table": "operationplanmaterial",
                "verbose_name_plural": "operationplan materials",
                "verbose_name": "operationplan material",
                "ordering": ["item", "location", "flowdate"],
            },
        ),
        migrations.CreateModel(
            name="OperationPlanResource",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        auto_created=True,
                        serialize=False,
                        primary_key=True,
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="source",
                        null=True,
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        verbose_name="last modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "resource",
                    models.CharField(
                        max_length=300, db_index=True, verbose_name="resource"
                    ),
                ),
                (
                    "quantity",
                    models.DecimalField(
                        max_digits=15, verbose_name="quantity", decimal_places=6
                    ),
                ),
                (
                    "startdate",
                    models.DateTimeField(db_index=True, verbose_name="startdate"),
                ),
                (
                    "enddate",
                    models.DateTimeField(db_index=True, verbose_name="enddate"),
                ),
                (
                    "setup",
                    models.CharField(max_length=300, verbose_name="setup", null=True),
                ),
                (
                    "status",
                    models.CharField(
                        max_length=20,
                        blank=True,
                        verbose_name="status",
                        help_text="Status of the OperationPlanResource",
                        choices=[("proposed", "proposed"), ("confirmed", "confirmed")],
                        null=True,
                    ),
                ),
                (
                    "operationplan",
                    models.ForeignKey(
                        verbose_name="operationplan",
                        related_name="resources",
                        to="input.OperationPlan",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "db_table": "operationplanresource",
                "verbose_name_plural": "operationplan resources",
                "verbose_name": "operationplan resource",
                "ordering": ["resource", "startdate"],
            },
        ),
        migrations.CreateModel(
            name="OperationResource",
            fields=[
                (
                    "source",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="source",
                        null=True,
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        verbose_name="last modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "id",
                    models.AutoField(
                        verbose_name="identifier", serialize=False, primary_key=True
                    ),
                ),
                (
                    "quantity",
                    models.DecimalField(
                        max_digits=15,
                        decimal_places=6,
                        verbose_name="quantity",
                        default="1.00",
                    ),
                ),
                (
                    "effective_start",
                    models.DateTimeField(
                        blank=True,
                        verbose_name="effective start",
                        null=True,
                        help_text="Validity start date",
                    ),
                ),
                (
                    "effective_end",
                    models.DateTimeField(
                        blank=True,
                        verbose_name="effective end",
                        null=True,
                        help_text="Validity end date",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=300,
                        blank=True,
                        verbose_name="name",
                        null=True,
                        help_text="Optional name of this load",
                    ),
                ),
                (
                    "priority",
                    models.IntegerField(
                        blank=True,
                        verbose_name="priority",
                        null=True,
                        help_text="Priority of this load in a group of alternates",
                        default=1,
                    ),
                ),
                (
                    "setup",
                    models.CharField(
                        max_length=300,
                        blank=True,
                        verbose_name="setup",
                        null=True,
                        help_text="Setup required on the resource for this operation",
                    ),
                ),
                (
                    "search",
                    models.CharField(
                        max_length=20,
                        blank=True,
                        verbose_name="search mode",
                        help_text="Method to select preferred alternate",
                        choices=[
                            ("PRIORITY", "priority"),
                            ("MINCOST", "minimum cost"),
                            ("MINPENALTY", "minimum penalty"),
                            ("MINCOSTPENALTY", "minimum cost plus penalty"),
                        ],
                        null=True,
                    ),
                ),
                (
                    "operation",
                    models.ForeignKey(
                        verbose_name="operation",
                        related_name="operationresources",
                        to="input.Operation",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "db_table": "operationresource",
                "verbose_name_plural": "operation resources",
                "verbose_name": "operation resource",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Resource",
            fields=[
                (
                    "lft",
                    models.PositiveIntegerField(
                        db_index=True, blank=True, editable=False, null=True
                    ),
                ),
                (
                    "rght",
                    models.PositiveIntegerField(editable=False, blank=True, null=True),
                ),
                (
                    "lvl",
                    models.PositiveIntegerField(editable=False, blank=True, null=True),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=300,
                        help_text="Unique identifier",
                        verbose_name="name",
                        serialize=False,
                        primary_key=True,
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="source",
                        null=True,
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        verbose_name="last modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        max_length=500,
                        blank=True,
                        verbose_name="description",
                        null=True,
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="category",
                        null=True,
                    ),
                ),
                (
                    "subcategory",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="subcategory",
                        null=True,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        max_length=20,
                        blank=True,
                        verbose_name="type",
                        choices=[
                            ("default", "default"),
                            ("buckets", "buckets"),
                            ("infinite", "infinite"),
                        ],
                        null=True,
                        default="default",
                    ),
                ),
                (
                    "maximum",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="maximum",
                        decimal_places=6,
                        help_text="Size of the resource",
                        null=True,
                        default="1.00",
                    ),
                ),
                (
                    "cost",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="cost",
                        decimal_places=6,
                        help_text="Cost for using 1 unit of the resource for 1 hour",
                        null=True,
                    ),
                ),
                (
                    "maxearly",
                    models.DurationField(
                        blank=True,
                        verbose_name="max early",
                        null=True,
                        help_text="Time window before the ask date where we look for available capacity",
                    ),
                ),
                (
                    "setup",
                    models.CharField(
                        max_length=300,
                        blank=True,
                        verbose_name="setup",
                        null=True,
                        help_text="Setup of the resource at the start of the plan",
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        blank=True,
                        verbose_name="location",
                        to="input.Location",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "maximum_calendar",
                    models.ForeignKey(
                        blank=True,
                        verbose_name="maximum calendar",
                        to="input.Calendar",
                        help_text="Calendar defining the resource size varying over time",
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        verbose_name="owner",
                        related_name="xchildren",
                        to="input.Resource",
                        help_text="Hierarchical parent",
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={
                "db_table": "resource",
                "verbose_name_plural": "resources",
                "verbose_name": "resource",
                "abstract": False,
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="ResourceSkill",
            fields=[
                (
                    "source",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="source",
                        null=True,
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        verbose_name="last modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "id",
                    models.AutoField(
                        verbose_name="identifier", serialize=False, primary_key=True
                    ),
                ),
                (
                    "effective_start",
                    models.DateTimeField(
                        blank=True,
                        verbose_name="effective start",
                        null=True,
                        help_text="Validity start date",
                    ),
                ),
                (
                    "effective_end",
                    models.DateTimeField(
                        blank=True,
                        verbose_name="effective end",
                        null=True,
                        help_text="Validity end date",
                    ),
                ),
                (
                    "priority",
                    models.IntegerField(
                        blank=True,
                        verbose_name="priority",
                        null=True,
                        help_text="Priority of this skill in a group of alternates",
                        default=1,
                    ),
                ),
                (
                    "resource",
                    models.ForeignKey(
                        verbose_name="resource",
                        related_name="skills",
                        to="input.Resource",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "resource skills",
                "verbose_name": "resource skill",
                "abstract": False,
                "ordering": ["resource", "skill"],
                "db_table": "resourceskill",
            },
        ),
        migrations.CreateModel(
            name="SetupMatrix",
            fields=[
                (
                    "source",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="source",
                        null=True,
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        verbose_name="last modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=300,
                        verbose_name="name",
                        serialize=False,
                        primary_key=True,
                    ),
                ),
            ],
            options={
                "db_table": "setupmatrix",
                "verbose_name_plural": "setup matrices",
                "verbose_name": "setup matrix",
                "abstract": False,
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="SetupRule",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        auto_created=True,
                        serialize=False,
                        primary_key=True,
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="source",
                        null=True,
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        verbose_name="last modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                ("priority", models.IntegerField(verbose_name="priority")),
                (
                    "fromsetup",
                    models.CharField(
                        max_length=300,
                        blank=True,
                        verbose_name="from setup",
                        null=True,
                        help_text="Name of the old setup (wildcard characters are supported)",
                    ),
                ),
                (
                    "tosetup",
                    models.CharField(
                        max_length=300,
                        blank=True,
                        verbose_name="to setup",
                        null=True,
                        help_text="Name of the new setup (wildcard characters are supported)",
                    ),
                ),
                (
                    "duration",
                    models.DurationField(
                        blank=True,
                        verbose_name="duration",
                        null=True,
                        help_text="Duration of the changeover",
                    ),
                ),
                (
                    "cost",
                    models.DecimalField(
                        max_digits=15,
                        blank=True,
                        verbose_name="cost",
                        decimal_places=6,
                        help_text="Cost of the conversion",
                        null=True,
                    ),
                ),
                (
                    "setupmatrix",
                    models.ForeignKey(
                        verbose_name="setup matrix",
                        related_name="rules",
                        to="input.SetupMatrix",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "setup matrix rules",
                "verbose_name": "setup matrix rule",
                "abstract": False,
                "ordering": ["priority"],
                "db_table": "setuprule",
            },
        ),
        migrations.CreateModel(
            name="Skill",
            fields=[
                (
                    "source",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="source",
                        null=True,
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        verbose_name="last modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=300,
                        help_text="Unique identifier",
                        verbose_name="name",
                        serialize=False,
                        primary_key=True,
                    ),
                ),
            ],
            options={
                "db_table": "skill",
                "verbose_name_plural": "skills",
                "verbose_name": "skill",
                "abstract": False,
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="SubOperation",
            fields=[
                (
                    "source",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="source",
                        null=True,
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        verbose_name="last modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "id",
                    models.AutoField(
                        verbose_name="identifier", serialize=False, primary_key=True
                    ),
                ),
                (
                    "priority",
                    models.IntegerField(
                        help_text="Sequence of this operation among the suboperations. Negative values are ignored.",
                        verbose_name="priority",
                        default=1,
                    ),
                ),
                (
                    "effective_start",
                    models.DateTimeField(
                        blank=True,
                        verbose_name="effective start",
                        null=True,
                        help_text="Validity start date",
                    ),
                ),
                (
                    "effective_end",
                    models.DateTimeField(
                        blank=True,
                        verbose_name="effective end",
                        null=True,
                        help_text="Validity end date",
                    ),
                ),
                (
                    "operation",
                    models.ForeignKey(
                        help_text="Parent operation",
                        verbose_name="operation",
                        related_name="suboperations",
                        to="input.Operation",
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "suboperation",
                    models.ForeignKey(
                        help_text="Child operation",
                        verbose_name="suboperation",
                        related_name="superoperations",
                        to="input.Operation",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "suboperations",
                "verbose_name": "suboperation",
                "abstract": False,
                "ordering": ["operation", "priority", "suboperation"],
                "db_table": "suboperation",
            },
        ),
        migrations.CreateModel(
            name="Supplier",
            fields=[
                (
                    "lft",
                    models.PositiveIntegerField(
                        db_index=True, blank=True, editable=False, null=True
                    ),
                ),
                (
                    "rght",
                    models.PositiveIntegerField(editable=False, blank=True, null=True),
                ),
                (
                    "lvl",
                    models.PositiveIntegerField(editable=False, blank=True, null=True),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=300,
                        help_text="Unique identifier",
                        verbose_name="name",
                        serialize=False,
                        primary_key=True,
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="source",
                        null=True,
                    ),
                ),
                (
                    "lastmodified",
                    models.DateTimeField(
                        db_index=True,
                        verbose_name="last modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        max_length=500,
                        blank=True,
                        verbose_name="description",
                        null=True,
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="category",
                        null=True,
                    ),
                ),
                (
                    "subcategory",
                    models.CharField(
                        max_length=300,
                        db_index=True,
                        blank=True,
                        verbose_name="subcategory",
                        null=True,
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        verbose_name="owner",
                        related_name="xchildren",
                        to="input.Supplier",
                        help_text="Hierarchical parent",
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={
                "db_table": "supplier",
                "verbose_name_plural": "suppliers",
                "verbose_name": "supplier",
                "abstract": False,
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="resourceskill",
            name="skill",
            field=models.ForeignKey(
                verbose_name="skill",
                related_name="resources",
                to="input.Skill",
                on_delete=models.CASCADE,
            ),
        ),
        migrations.AddField(
            model_name="resource",
            name="setupmatrix",
            field=models.ForeignKey(
                blank=True,
                verbose_name="setup matrix",
                to="input.SetupMatrix",
                help_text="Setup matrix defining the conversion time and cost",
                null=True,
                on_delete=models.SET_NULL,
            ),
        ),
        migrations.AddField(
            model_name="operationresource",
            name="resource",
            field=models.ForeignKey(
                verbose_name="resource",
                related_name="operationresources",
                to="input.Resource",
                on_delete=models.CASCADE,
            ),
        ),
        migrations.AddField(
            model_name="operationresource",
            name="skill",
            field=models.ForeignKey(
                blank=True,
                verbose_name="skill",
                related_name="operationresources",
                to="input.Skill",
                null=True,
                on_delete=models.SET_NULL,
            ),
        ),
        migrations.AddField(
            model_name="operationplan",
            name="supplier",
            field=models.ForeignKey(
                blank=True,
                verbose_name="supplier",
                to="input.Supplier",
                null=True,
                on_delete=models.CASCADE,
            ),
        ),
        migrations.AddField(
            model_name="itemsupplier",
            name="location",
            field=models.ForeignKey(
                blank=True,
                verbose_name="location",
                related_name="itemsuppliers",
                to="input.Location",
                null=True,
                on_delete=models.CASCADE,
            ),
        ),
        migrations.AddField(
            model_name="itemsupplier",
            name="resource",
            field=models.ForeignKey(
                blank=True,
                verbose_name="resource",
                related_name="itemsuppliers",
                to="input.Resource",
                help_text="Resource to model the supplier capacity",
                null=True,
                on_delete=models.SET_NULL,
            ),
        ),
        migrations.AddField(
            model_name="itemsupplier",
            name="supplier",
            field=models.ForeignKey(
                verbose_name="supplier",
                related_name="suppliers",
                to="input.Supplier",
                on_delete=models.CASCADE,
            ),
        ),
        migrations.AddField(
            model_name="itemdistribution",
            name="location",
            field=models.ForeignKey(
                blank=True,
                verbose_name="location",
                related_name="itemdistributions_destination",
                to="input.Location",
                null=True,
                on_delete=models.CASCADE,
            ),
        ),
        migrations.AddField(
            model_name="itemdistribution",
            name="origin",
            field=models.ForeignKey(
                verbose_name="origin",
                related_name="itemdistributions_origin",
                to="input.Location",
                on_delete=models.CASCADE,
            ),
        ),
        migrations.AddField(
            model_name="itemdistribution",
            name="resource",
            field=models.ForeignKey(
                blank=True,
                verbose_name="resource",
                related_name="itemdistributions",
                to="input.Resource",
                help_text="Resource to model the distribution capacity",
                null=True,
                on_delete=models.SET_NULL,
            ),
        ),
        migrations.AddField(
            model_name="demand",
            name="item",
            field=models.ForeignKey(
                to="input.Item", verbose_name="item", on_delete=models.CASCADE
            ),
        ),
        migrations.AddField(
            model_name="demand",
            name="location",
            field=models.ForeignKey(
                to="input.Location", verbose_name="location", on_delete=models.CASCADE
            ),
        ),
        migrations.AddField(
            model_name="demand",
            name="operation",
            field=models.ForeignKey(
                blank=True,
                verbose_name="delivery operation",
                related_name="used_demand",
                to="input.Operation",
                help_text="Operation used to satisfy this demand",
                null=True,
                on_delete=models.SET_NULL,
            ),
        ),
        migrations.AddField(
            model_name="demand",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                verbose_name="owner",
                related_name="xchildren",
                to="input.Demand",
                help_text="Hierarchical parent",
                null=True,
                on_delete=models.SET_NULL,
            ),
        ),
        migrations.AddField(
            model_name="buffer",
            name="item",
            field=models.ForeignKey(
                to="input.Item", verbose_name="item", on_delete=models.CASCADE
            ),
        ),
        migrations.AddField(
            model_name="buffer",
            name="location",
            field=models.ForeignKey(
                to="input.Location", verbose_name="location", on_delete=models.CASCADE
            ),
        ),
        migrations.AddField(
            model_name="buffer",
            name="minimum_calendar",
            field=models.ForeignKey(
                blank=True,
                verbose_name="minimum calendar",
                to="input.Calendar",
                help_text="Calendar storing a time-dependent safety stock profile",
                null=True,
                on_delete=models.SET_NULL,
            ),
        ),
        migrations.AddField(
            model_name="buffer",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                verbose_name="owner",
                related_name="xchildren",
                to="input.Buffer",
                help_text="Hierarchical parent",
                null=True,
                on_delete=models.SET_NULL,
            ),
        ),
        migrations.CreateModel(
            name="DeliveryOrder",
            fields=[],
            options={
                "proxy": True,
                "verbose_name_plural": "customer shipments",
                "verbose_name": "customer shipment",
            },
            bases=("input.operationplan",),
        ),
        migrations.CreateModel(
            name="DistributionOrder",
            fields=[],
            options={
                "proxy": True,
                "verbose_name_plural": "distribution orders",
                "verbose_name": "distribution order",
            },
            bases=("input.operationplan",),
        ),
        migrations.CreateModel(
            name="ManufacturingOrder",
            fields=[],
            options={
                "proxy": True,
                "verbose_name_plural": "manufacturing orders",
                "verbose_name": "manufacturing order",
            },
            bases=("input.operationplan",),
        ),
        migrations.CreateModel(
            name="PurchaseOrder",
            fields=[],
            options={
                "proxy": True,
                "verbose_name_plural": "purchase orders",
                "verbose_name": "purchase order",
            },
            bases=("input.operationplan",),
        ),
        migrations.AlterUniqueTogether(
            name="suboperation",
            unique_together=set([("operation", "priority", "suboperation")]),
        ),
        migrations.AlterUniqueTogether(
            name="setuprule", unique_together=set([("setupmatrix", "priority")])
        ),
        migrations.AlterUniqueTogether(
            name="resourceskill", unique_together=set([("resource", "skill")])
        ),
        migrations.AlterUniqueTogether(
            name="operationresource",
            unique_together=set([("operation", "resource", "effective_start")]),
        ),
        migrations.AlterUniqueTogether(
            name="operationmaterial",
            unique_together=set([("operation", "item", "effective_start")]),
        ),
        migrations.AlterUniqueTogether(
            name="itemsupplier",
            unique_together=set([("item", "location", "supplier", "effective_start")]),
        ),
        migrations.AlterUniqueTogether(
            name="itemdistribution",
            unique_together=set([("item", "location", "origin", "effective_start")]),
        ),
        migrations.AlterUniqueTogether(
            name="calendarbucket",
            unique_together=set([("calendar", "startdate", "enddate", "priority")]),
        ),
        migrations.AlterUniqueTogether(
            name="buffer", unique_together=set([("item", "location")])
        ),
        migrations.RunPython(loadParameters),
    ]
