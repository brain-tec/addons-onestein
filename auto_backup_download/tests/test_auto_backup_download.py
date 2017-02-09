# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo.exceptions import Warning


class TestAutoBackupDownload(common.TransactionCase):

    def test_01_create_not_existing(self):
        backup_dir = self.env.ref(
            'auto_backup_download.default_backup_directory')

        # test method get_dir()
        with self.assertRaises(Warning):
            backup_dir.get_dir()

        # test computed field file_ids
        self.assertEqual(len(backup_dir.file_ids), 0)

        # test count list of directory
        self.assertEqual(len(backup_dir.file_ids), backup_dir.file_count)

        # test reload list of directory
        with self.assertRaises(Warning):
            backup_dir.reload()
        self.assertEqual(len(backup_dir.file_ids), 0)
        self.assertEqual(len(backup_dir.file_ids), backup_dir.file_count)

    def test_02_create_existing(self):
        backup_dir = self.env.ref(
            'auto_backup_download.default_backup_directory')
        self.env['db.backup'].create({
            'name': 'Test Backup 1',
            'folder': '/tmp'
        })

        # test method get_dir()
        full_dir = backup_dir.get_dir()
        self.assertEqual(full_dir[-1], '/')

        # test computed field file_ids
        self.assertGreaterEqual(len(backup_dir.file_ids), 0)

        # test count list of directory
        self.assertEqual(len(full_dir.file_ids), full_dir.file_count)

        # test reload list of directory
        full_dir.reload()
        self.assertEqual(len(full_dir.file_ids), full_dir.file_count)
