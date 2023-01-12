from odoo.upgrade import util
from lxml import etree
import logging

_logger = logging.getLogger(__name__)

"""
This file contains the functions you can use in the util for migration script
"""

def migrate(cr, version):

    # RENAME

    # rename model
    old_model_name = "model_a"
    new_model_name = "model_b"
    _logger.info(f"Rename model: {old_model_name} to {new_model_name}")
    util.rename_model(cr, old_model_name, new_model_name)
    _logger.info("Rename model done")

    # rename fields
    field_rename_pair = [
        ("x_active", "active"),
        ("x_name", "name"),
        ("x_number", "number"),
    ]

    for field in field_rename_pair:
        util.rename_field(cr, "sale.order", field[0], field[1])

    # rename xml_id
    util.rename_xmlid(cr, "module_a.field_x", "module_b.field_x")

    # REMOVE

    # remove field
    util.remove_field(cr, "account.move", "x_studio_material")

    # remove view
    view_ids = [
        "studio_customization.default_dashboard_vi_686e75a0-91dc-4a4f-838f-1a963bd25b7e",
        "studio_customization.default_form_view_fo_922af125-b4c1-42fa-825c-ba956dc99970",
        "studio_customization.default_graph_view_f_6e8232b5-64d4-43ae-9197-26376d9807a3",
    ]

    for view in view_ids:
        util.remove_view(cr, view)

    # remove record (e.g. server action, automatic action)
    util.remove_record(cr, "separate_stock_picking.separate_stock_picking_automation")

    # remove table & module
    util.remove_model(cr, "sale.reference")

    util.remove_module(cr, "multi_signature")

    # EDIT

    # edit view (by SQL)
    cr.execute(
        """
            UPDATE ir_ui_view
            SET active = 't',
                arch_db = replace(replace(replace(replace(arch_db,
                'o.date_invoice', 'o.invoice_date'),
                'o.payment_term_id', 'o.invoice_payment_term_id'),
                %s, %s),
                'o.number', 'o.name')
            WHERE id = %s
        """,
        ['x_studio_origin_group', 'x_origin_group', util.ref(cr, "__export__.report_tax_invoice_custom_document_hpr")],
    )

    # edit server action (by SQL)
    cr.execute(
        """
            UPDATE ir_act_server
            SET code = replace(replace(replace(code,
                'date_invoice', 'invoice_date'),
                'x_studio_invoice_month', 'x_invoice_month'),
                'x_studio_invoice_year', 'x_invoice_year')
            WHERE id = 431
        """
    )

    # edit view (by helper function)
    with util.edit_view(
        cr, xmlid="studio_customization.odoo_studio_res_part_61539d5a-09dc-4343-9dd9-cb7362599541"
    ) as arch:
        node = arch.find(""".//field[@name="debit"]""")
        node.getparent().remove(node)

        node = arch.find(""".//field[@name="x_studio_test_readonly"]""")
        node.attrib["readonly"] = "1"

        node = arch.find(""".//xpath[@expr="//field[@name='vat']"]""")
        new_node = etree.fromstring(
            """
              <field name="total_overdue"/>
            """
        )
        node.append(new_node)

        new_el1 = etree.fromstring(
            """
            <field name="credit" />
            """
        )
        for node in arch.xpath(""".//xpath[@expr="//field[@name='vat']"]"""):
            node.insert(0, new_el1)
