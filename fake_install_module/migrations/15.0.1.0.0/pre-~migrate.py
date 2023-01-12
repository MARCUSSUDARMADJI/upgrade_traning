from odoo.upgrade import util
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):

    _logger.info("""
        -----Running migration script-----
    """)


"""
Run fake install in odoo-bin shell:
env.cr.execute(
"INSERT INTO ir_module_module(name, latest_version, state) VALUES ('fake_install_module', '0.0.1.0', 'to upgrade')"
)
env.cr.commit()
"""
