# -*- coding: utf-8 -*-

import os
import logging


logger = logging.getLogger('django')


exclude = ["venv"]  # 需要排除的文件目录

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in set(dirs) - set(exclude)]
    if 'migrations' in dirs:
        _dir = dirs[dirs.index('migrations')]
        for root_j, dirs_j, files_j in os.walk(os.path.join(root, _dir)):
            for file_k in files_j:
                if file_k != '__init__.py':
                    dst_file = os.path.join(root_j, file_k)
                    logger.info('删除文件>>> ', dst_file)
                    os.remove(dst_file)
