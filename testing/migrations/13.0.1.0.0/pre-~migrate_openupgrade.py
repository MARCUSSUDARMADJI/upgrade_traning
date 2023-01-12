from openupgradelib import openupgrade

"""
This file contains the functions you can use in the openupgradelib for migration script
"""

@openupgrade.migrate()
def migrate(env, version):

    # RENAME

    openupgrade.rename_fields(
        env,
        [
            ("project.task", "project_task", "field_name_before", "field_name_after"),
        ],
    )

    openupgrade.rename_tables(
        env.cr,
        [
            ("mail_moderation", "mail_group_moderation"),
            ("mail_channel_moderator_rel", "mail_group_moderator_rel"),
        ],
    )

    openupgrade.rename_columns(
        env.cr,
        {
            "mail_group_moderator_rel": [
                ("mail_channel_id", "mail_group_id"),
            ]
        },
    )

    openupgrade.rename_xmlids(
        env.cr,
        [
            ("web.external_layout_background", "web.external_layout_striped"),
            ("web.external_layout_clean", "web.external_layout_bold"),
        ],
    )

    # REMOVE
    openupgrade.delete_records_safely_by_xml_id(
        env, [("testing.so_update_automation")]
    )

    # Logs query and affected rows at level DEBUG.
    openupgrade.logged_query(
        env.cr,
        """
            UPDATE ir_ui_view
            SET arch_db=replace(arch_db,
                'payment_term_id','sale_order_template_id')
            WHERE id=%s
        """,
        [env.ref("account.view_account_journal_form").id]
    )
