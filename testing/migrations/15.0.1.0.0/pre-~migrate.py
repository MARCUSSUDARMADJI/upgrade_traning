from odoo.upgrade import util
import logging
from lxml import etree

_logger = logging.getLogger(__name__)

"""
Migration script for using util to fix this custom module
"""

def migrate(cr, version):

    cr.execute("SELECT latest_version FROM ir_module_module WHERE name='base'")
    util.ENVIRON["__base_version"] = util.parse_version(cr.fetchone()[0])

    _logger.info("Rename field")
    util.rename_field(cr, "sale.order", "test_rename", "test")

    _logger.info("Fix view")
    cr.execute(
        """
            UPDATE ir_ui_view
            SET active = 't',
                arch_db = replace(arch_db,
                'test_rename', 'test')
            WHERE id = %s
        """,
        [util.ref(cr, "studio_customization.odoo_studio_sale_ord_6d78321b-99b6-44b0-8977-da263d9e7651")],
    )

    _logger.info("Fix server action")
    cr.execute(
        """
            UPDATE ir_act_server
            SET code = replace(code,
                'test_rename', 'test')
            WHERE id = 324
        """
    )

    _logger.info("Remove view")
    util.remove_view(cr, 'studio_customization.odoo_studio_account__5a52c937-c45a-4f21-91f2-10285419fcd0')

    _logger.info("Edit view")
    with util.edit_view(
        cr, xmlid="studio_customization.odoo_studio_res_part_61539d5a-09dc-4343-9dd9-cb7362599541"
    ) as arch:
        node = arch.find(""".//field[@name="x_studio_test_readonly"]""")
        node.attrib["readonly"] = "1"

        new_el1 = etree.fromstring(
            """
            <field name="credit" />
            """
        )
        for node in arch.xpath(""".//xpath[@expr="//field[@name='vat']"]"""):
            node.insert(0, new_el1)
