#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'XZ'

from models import User, Blog, Comment
from transwarp import db

if __name__ == '__main__':
    db.create_engine('xz', 'interact', 'awesome')
    b = Blog(user_name='XZ', name='Test Blog', summary='Summary of Test', content='Content of Test')
    b.insert()
