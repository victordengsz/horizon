# Copyright 2013, Mirantis Inc
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


from django.core.urlresolvers import reverse
from django import template
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import exceptions
from horizon import tables

from openstack_dashboard import api
from openstack_dashboard import policy


forbid_updates = set(["PENDING_CREATE", "PENDING_UPDATE", "PENDING_DELETE"])


class AddIKEPolicyLink(tables.LinkAction):
    name = "addikepolicy"
    verbose_name = _("Add IKE Policy")
    url = "horizon:project:vpn:addikepolicy"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("network", "create_ikepolicy"),)


class AddIPSecPolicyLink(tables.LinkAction):
    name = "addipsecpolicy"
    verbose_name = _("Add IPSec Policy")
    url = "horizon:project:vpn:addipsecpolicy"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("network", "create_ipsecpolicy"),)


class AddVPNServiceLink(tables.LinkAction):
    name = "addvpnservice"
    verbose_name = _("Add VPN Service")
    url = "horizon:project:vpn:addvpnservice"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("network", "create_vpnservice"),)


class AddIPSecSiteConnectionLink(tables.LinkAction):
    name = "addipsecsiteconnection"
    verbose_name = _("Add IPSec Site Connection")
    url = "horizon:project:vpn:addipsecsiteconnection"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("network", "create_ipsec_site_connection"),)


class DeleteVPNServiceLink(policy.PolicyTargetMixin, tables.DeleteAction):
    name = "deletevpnservice"
    policy_rules = (("network", "delete_vpnservice"),)

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete VPN Service",
            u"Delete VPN Services",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Scheduled deletion of VPN Service",
            u"Scheduled deletion of VPN Services",
            count
        )

    def allowed(self, request, datum=None):
        if datum and datum.ipsecsiteconns:
            return False
        return True

    def delete(self, request, obj_id):
        try:
            api.vpn.vpnservice_delete(request, obj_id)
        except Exception as e:
            exceptions.handle(
                request, _('Unable to delete VPN Service. %s') % e)


class DeleteIKEPolicyLink(policy.PolicyTargetMixin, tables.DeleteAction):
    name = "deleteikepolicy"
    policy_rules = (("network", "delete_ikepolicy"),)

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete IKE Policy",
            u"Delete IKE Policies",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Scheduled deletion of IKE Policy",
            u"Scheduled deletion of IKE Policies",
            count
        )

    def allowed(self, request, datum=None):
        if datum and datum.ipsecsiteconns:
            return False
        return True

    def delete(self, request, obj_id):
        try:
            api.vpn.ikepolicy_delete(request, obj_id)
        except Exception as e:
            exceptions.handle(
                request, _('Unable to delete IKE Policy. %s') % e)


class DeleteIPSecPolicyLink(policy.PolicyTargetMixin, tables.DeleteAction):
    name = "deleteipsecpolicy"
    policy_rules = (("network", "delete_ipsecpolicy"),)

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete IPSec Policy",
            u"Delete IPSec Policies",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Scheduled deletion of IPSec Policy",
            u"Scheduled deletion of IPSec Policies",
            count
        )

    def allowed(self, request, datum=None):
        if datum and datum.ipsecsiteconns:
            return False
        return True

    def delete(self, request, obj_id):
        try:
            api.vpn.ipsecpolicy_delete(request, obj_id)
        except Exception as e:
            exceptions.handle(
                request, _('Unable to delete IPSec Policy. %s') % e)


class DeleteIPSecSiteConnectionLink(policy.PolicyTargetMixin,
                                    tables.DeleteAction):
    name = "deleteipsecsiteconnection"
    policy_rules = (("network", "delete_ipsec_site_connection"),)

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete IPSec Site Connection",
            u"Delete IPSec Site Connections",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Scheduled deletion of IPSec Site Connection",
            u"Scheduled deletion of IPSec Site Connections",
            count
        )

    def delete(self, request, obj_id):
        try:
            api.vpn.ipsecsiteconnection_delete(request, obj_id)
        except Exception as e:
            exceptions.handle(
                request, _('Unable to delete IPSec Site Connection. %s') % e)


class UpdateVPNServiceLink(tables.LinkAction):
    name = "update_vpnservice"
    verbose_name = _("Edit VPN Service")
    classes = ("ajax-modal", "btn-update",)
    policy_rules = (("network", "update_vpnservice"),)

    def get_link_url(self, vpnservice):
        return reverse("horizon:project:vpn:update_vpnservice",
                       kwargs={'vpnservice_id': vpnservice.id})

    def allowed(self, request, datum=None):
        if datum and datum.status not in forbid_updates:
            return True
        return False


class UpdateIKEPolicyLink(tables.LinkAction):
    name = "updateikepolicy"
    verbose_name = _("Edit IKE Policy")
    classes = ("ajax-modal", "btn-update",)
    policy_rules = (("network", "update_ikepolicy"),)

    def get_link_url(self, ikepolicy):
        return reverse("horizon:project:vpn:update_ikepolicy",
                       kwargs={'ikepolicy_id': ikepolicy.id})

    def allowed(self, request, datum=None):
        return not datum['ipsecsiteconns']


class UpdateIPSecPolicyLink(tables.LinkAction):
    name = "updateipsecpolicy"
    verbose_name = _("Edit IPSec Policy")
    classes = ("ajax-modal", "btn-update",)
    policy_rules = (("network", "update_ipsecpolicy"),)

    def get_link_url(self, ipsecpolicy):
        return reverse("horizon:project:vpn:update_ipsecpolicy",
                       kwargs={'ipsecpolicy_id': ipsecpolicy.id})

    def allowed(self, request, datum=None):
        return not datum['ipsecsiteconns']


class UpdateIPSecSiteConnectionLink(tables.LinkAction):
    name = "updateipsecsiteconnection"
    verbose_name = _("Edit Connection")
    classes = ("ajax-modal", "btn-update",)
    policy_rules = (("network", "update_ipsec_site_connection"),)

    def get_link_url(self, ipsecsiteconnection):
        return reverse("horizon:project:vpn:update_ipsecsiteconnection",
                       kwargs={'ipsecsiteconnection_id':
                               ipsecsiteconnection.id})

    def allowed(self, request, datum=None):
        if datum and datum.status not in forbid_updates:
            return True
        return False


STATUS_CHOICES = (
    ("active", True),
    ("down", True),
    ("created", True),
    ("error", False),
    ("inactive", False),
)


STATUS_DISPLAY_CHOICES = (
    ("active", pgettext_lazy("Current status of an IPSec Site Connection"
                             " and VPN Service", u"Active")),
    ("down", pgettext_lazy("Current status of an IPSec Site Connection"
                           " and VPN Service", u"Down")),
    ("error", pgettext_lazy("Current status of an IPSec Site Connection"
                            " and VPN Service", u"Error")),
    ("created", pgettext_lazy("Current status of an IPSec Site Connection"
                              " and VPN Service", u"Created")),
    ("pending_create", pgettext_lazy("Current status of an"
                                     " IPSec Site Connection and VPN Service",
                                     u"Pending Create")),
    ("pending_update", pgettext_lazy("Current status of an"
                                     " IPSec Site Connection and VPN Service",
                                     u"Pending Update")),
    ("pending_delete", pgettext_lazy("Current status of an"
                                     " IPSec Site Connection and VPN Service",
                                     u"Pending Delete")),
    ("inactive", pgettext_lazy("Current status of an IPSec Site Connection"
                               " and VPN Service", u"Inactive")),
)


class UpdateIPSecSiteConnectionRow(tables.Row):
    ajax = True

    def get_data(self, request, conn_id):
        conn = api.vpn.ipsecsiteconnection_get(request, conn_id)
        conn.ikepolicy_name = conn['ikepolicy'].get('name',
                                                    conn['ikepolicy_id'])
        conn.ipsecpolicy_name = conn['ipsecpolicy'].get('name',
                                                        conn['ipsecpolicy_id'])
        conn.vpnservice_name = conn['vpnservice'].get('name',
                                                      conn['vpnservice_id'])
        return conn


class IPSSCFilterAction(tables.FilterAction):
    name = 'IPSSC_project_IKEPolicies'
    filter_type = 'server'
    filter_choices = (
        ('name', _("Name ="), True),
        ('vpnservice', _("VPN Service ="), True),
        ('vpnservice_id', _("VPN Service id ="), True),
        ('ikepolicy', _("IKE Policy ="), True),
        ('ikepolicy_id', _("IKE Policy id ="), True),
        ('ipsecpolicy', _("IPSec Policy ="), True),
        ('ipsecpolicy_id', _("IPSec Policy id ="), True),
        ('status', _("Status ="), True)
    )


class IPSecSiteConnectionsTable(tables.DataTable):
    id = tables.Column('id', hidden=True)
    name = tables.Column('name_or_id', verbose_name=_('Name'),
                         link="horizon:project:vpn:ipsecsiteconnectiondetails")
    description = tables.Column('description', verbose_name=_('Description'))
    vpnservice_name = tables.Column('vpnservice_name',
                                    verbose_name=_('VPN Service'))
    ikepolicy_name = tables.Column('ikepolicy_name',
                                   verbose_name=_('IKE Policy'))
    ipsecpolicy_name = tables.Column('ipsecpolicy_name',
                                     verbose_name=_('IPSec Policy'))
    status = tables.Column("status",
                           verbose_name=_("Status"),
                           status=True,
                           status_choices=STATUS_CHOICES,
                           display_choices=STATUS_DISPLAY_CHOICES)

    class Meta(object):
        name = "ipsecsiteconnectionstable"
        verbose_name = _("IPSec Site Connections")
        status_columns = ['status']
        row_class = UpdateIPSecSiteConnectionRow
        table_actions = (AddIPSecSiteConnectionLink,
                         DeleteIPSecSiteConnectionLink,
                         IPSSCFilterAction)
        row_actions = (UpdateIPSecSiteConnectionLink,
                       DeleteIPSecSiteConnectionLink)


def get_local_ips(vpn):
    template_name = 'project/vpn/_vpn_ips.html'
    context = {"external_v4_ip": vpn.get('external_v4_ip'),
               "external_v6_ip": vpn.get('external_v6_ip')}
    return template.loader.render_to_string(template_name, context)


class UpdateVPNServiceRow(tables.Row):
    ajax = True

    def get_data(self, request, vpn_id):
        vpn = api.vpn.vpnservice_get(request, vpn_id)
        vpn.router_name = vpn['router'].get('name', vpn['router_id'])
        vpn.subnet_name = vpn['subnet'].get('cidr', vpn['subnet_id'])
        return vpn


class VPNServicesFilterAction(tables.FilterAction):
    name = 'vpnservices_project_IKEPolicies'
    filter_type = 'server'
    filter_choices = (
        ('name', _("Name ="), True),
        ('subnet_id', _("Subnet id ="), True),
        ('subnet_name', _("Subnet ="), True),
        ('router_id', _("Router id="), True),
        ('router_name', _("Router ="), True),
    )


class VPNServicesTable(tables.DataTable):
    id = tables.Column('id', hidden=True)
    name = tables.Column("name_or_id", verbose_name=_('Name'),
                         link="horizon:project:vpn:vpnservicedetails")
    description = tables.Column('description', verbose_name=_('Description'))
    local_ips = tables.Column(get_local_ips,
                              verbose_name=_("Local Side Public IPs"))
    subnet_name = tables.Column('subnet_name', verbose_name=_('Subnet'))
    router_name = tables.Column('router_name', verbose_name=_('Router'))
    status = tables.Column("status",
                           verbose_name=_("Status"),
                           status=True,
                           status_choices=STATUS_CHOICES,
                           display_choices=STATUS_DISPLAY_CHOICES)

    class Meta(object):
        name = "vpnservicestable"
        verbose_name = _("VPN Services")
        status_columns = ['status']
        row_class = UpdateVPNServiceRow
        table_actions = (AddVPNServiceLink,
                         DeleteVPNServiceLink,
                         VPNServicesFilterAction)
        row_actions = (UpdateVPNServiceLink, DeleteVPNServiceLink)


class PoliciesFilterAction(tables.FilterAction):
    name = 'filter_project_IKEPolicies'
    filter_type = 'server'
    filter_choices = (
        ('name', _("Name ="), True),
        ('auth_algorithm', _("Authorization algorithm ="), True),
        ('encryption_algorithm', _("Encryption algorithm ="), True),
        ('pfs', _("PFS ="), True),
    )


class IKEPoliciesTable(tables.DataTable):
    id = tables.Column('id', hidden=True)
    name = tables.Column("name_or_id", verbose_name=_('Name'),
                         link="horizon:project:vpn:ikepolicydetails")
    description = tables.Column('description', verbose_name=_('Description'))
    auth_algorithm = tables.Column('auth_algorithm',
                                   verbose_name=_('Authorization algorithm'))
    encryption_algorithm = tables.Column(
        'encryption_algorithm',
        verbose_name=_('Encryption algorithm'))
    pfs = tables.Column("pfs", verbose_name=_('PFS'))

    class Meta(object):
        name = "ikepoliciestable"
        verbose_name = _("IKE Policies")
        table_actions = (AddIKEPolicyLink,
                         DeleteIKEPolicyLink,
                         PoliciesFilterAction)
        row_actions = (UpdateIKEPolicyLink, DeleteIKEPolicyLink)


class IPSecPoliciesTable(tables.DataTable):
    id = tables.Column('id', hidden=True)
    name = tables.Column("name_or_id", verbose_name=_('Name'),
                         link="horizon:project:vpn:ipsecpolicydetails")
    description = tables.Column('description', verbose_name=_('Description'))
    auth_algorithm = tables.Column('auth_algorithm',
                                   verbose_name=_('Authorization algorithm'))
    encryption_algorithm = tables.Column(
        'encryption_algorithm',
        verbose_name=_('Encryption algorithm'))
    pfs = tables.Column("pfs", verbose_name=_('PFS'))

    class Meta(object):
        name = "ipsecpoliciestable"
        verbose_name = _("IPSec Policies")
        table_actions = (AddIPSecPolicyLink,
                         DeleteIPSecPolicyLink,
                         PoliciesFilterAction)
        row_actions = (UpdateIPSecPolicyLink, DeleteIPSecPolicyLink)
