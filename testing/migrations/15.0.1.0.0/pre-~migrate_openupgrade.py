from openupgradelib import openupgrade
import logging

_logger = logging.getLogger(__name__)

"""
Migration script for using openupgradelib to fix this custom module
"""

@openupgrade.migrate()
def migrate(env, version):

    _logger.info("Running Openupgradelib migration script")

    _logger.info("Rename field")
    openupgrade.rename_fields(
        env,
        [
            ("sale.order", "sale_order", "test_rename", "test"),
        ],
    )

    _logger.info("Fix view")
    openupgrade.logged_query(
        env.cr,
        """
            UPDATE ir_ui_view
            SET active = 't',
                arch_db = replace(arch_db,
                'test_rename', 'test')
            WHERE id = %s
        """,
        [env.ref("studio_customization.odoo_studio_sale_ord_6d78321b-99b6-44b0-8977-da263d9e7651").id],
    )

    _logger.info("Fix server action")
    openupgrade.logged_query(
        env.cr,
        """
            UPDATE ir_act_server
            SET code = replace(code,
                'test_rename', 'test')
            WHERE id = 324
        """
    )

    _logger.info("Remove view")
    openupgrade.delete_records_safely_by_xml_id(
        env, [("studio_customization.odoo_studio_account__5a52c937-c45a-4f21-91f2-10285419fcd0")]
    )
