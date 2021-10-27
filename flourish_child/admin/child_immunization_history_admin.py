from django.contrib import admin
from edc_fieldsets.fieldlist import Fieldlist
from edc_fieldsets.fieldsets_modeladmin_mixin import FormLabel
from edc_model_admin import TabularInlineMixin, audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import (
    ChildImmunizationHistoryForm, VaccinesReceivedForm, VaccinesMissedForm)
from ..models import ChildImmunizationHistory, VaccinesMissed, VaccinesReceived
from .model_admin_mixins import ChildCrfModelAdminMixin


class VaccinesReceivedInlineAdmin(TabularInlineMixin, admin.TabularInline):
    model = VaccinesReceived
    form = VaccinesReceivedForm
    extra = 1

    fieldsets = (
        (None, {
            'fields': (
                'received_vaccine_name',
                'first_dose_dt',
                'second_dose_dt',
                'third_dose_dt',
                'booster_dose_dt')
        }),
    )


class VaccinesMissedInlineAdmin(TabularInlineMixin, admin.TabularInline):
    model = VaccinesMissed
    form = VaccinesMissedForm
    extra = 1

    fieldsets = (
        (None, {
            'fields': (
                'missed_vaccine_name',
                'reason_missed',
                'reason_missed_other')
        }), audit_fieldset_tuple
    )


@admin.register(ChildImmunizationHistory, site=flourish_child_admin)
class ChildImmunizationHistoryAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildImmunizationHistoryForm

    fieldsets = (
        (None, {
            'fields': (
                'child_visit',
                'report_datetime',
                'vaccines_received',
                'vaccines_missed',)
        }),
    )

    inlines = [VaccinesReceivedInlineAdmin, VaccinesMissedInlineAdmin, ]
    radio_fields = {'vaccines_received': admin.VERTICAL,
                    'vaccines_missed': admin.VERTICAL,
                    'rec_add_immunization': admin.VERTICAL}

    custom_form_labels = [
        FormLabel(
            field='rec_add_immunization',
            label=('Since the last scheduled visit in {previous}, have you '
                   'received any additional immunizations?'),
            previous_appointment=True)
        ]

    conditional_fieldlists = {
        'child_a_sec_qt_schedule1': Fieldlist(insert_fields=('rec_add_immunization',),
                                              remove_fields=('vaccines_received',),
                                              insert_after='report_datetime'),
        'child_a_quart_schedule1': Fieldlist(insert_fields=('rec_add_immunization',),
                                             remove_fields=('vaccines_received',),
                                             insert_after='report_datetime'),
        'child_b_quart_schedule1': Fieldlist(insert_fields=('rec_add_immunization',),
                                             remove_fields=('vaccines_received',),
                                             insert_after='report_datetime'),
        'child_b_sec_qt_schedule1': Fieldlist(insert_fields=('rec_add_immunization',),
                                              remove_fields=('vaccines_received',),
                                              insert_after='report_datetime'),
        'child_c_sec_qt_schedule1': Fieldlist(insert_fields=('rec_add_immunization',),
                                              remove_fields=('vaccines_received',),
                                              insert_after='report_datetime'),
        'child_c_quart_schedule1': Fieldlist(insert_fields=('rec_add_immunization',),
                                             remove_fields=('vaccines_received',),
                                             insert_after='report_datetime'),
        'child_pool_schedule1': Fieldlist(insert_fields=('rec_add_immunization',),
                                          remove_fields=('vaccines_received',),
                                          insert_after='report_datetime'),
    }
