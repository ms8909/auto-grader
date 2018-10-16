# TODO: Split models into distinct .py files
from werkzeug.exceptions import BadRequest

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from sqlalchemy import PrimaryKeyConstraint, UniqueConstraint, MetaData, types
from sqlalchemy.dialects import mysql
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import aliased, backref
from sqlalchemy.sql import text

from markdown import markdown
import pytz

import functools

from collections import namedtuple, Counter

import contextlib
import csv
import datetime as dt
import json
import os
import logging
import shlex
import urllib.parse
import mimetypes

from server.constants import (VALID_ROLES, STUDENT_ROLE, STAFF_ROLES, TIMEZONE,
                              SCORE_KINDS, OAUTH_OUT_OF_BAND_URI,
                              INSTRUCTOR_ROLE, ROLE_DISPLAY_NAMES)

from server.extensions import cache, storage
from server.utils import (encode_id, chunks, generate_number_table,
                          humanize_name)
logger = logging.getLogger(__name__)

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

def transaction(f):
    """ Decorator for database (session) transactions."""
    @functools.wraps(f)
    def wrapper(*args, **kwds):
        try:
            value = f(*args, **kwds)
            db.session.commit()
            return value
        except:
            db.session.rollback()
            raise
    return wrapper

class Json(types.TypeDecorator):
    impl = types.Text

    def process_bind_param(self, value, dialect):
        # Python -> SQL
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        # SQL -> Python
        return json.loads(value)

class Timezone(types.TypeDecorator):
    impl = types.String(255)

    def process_bind_param(self, value, dialect):
        # Python -> SQL
        if not hasattr(value, 'zone'):
            if value not in pytz.common_timezones_set:
                logger.warning('Unknown TZ: {}'.format(value))
                # Unknown TZ, use default instead
                return TIMEZONE
            return value
        return value.zone

    def process_result_value(self, value, dialect):
        # SQL -> Python
        return pytz.timezone(value)
    def process_result_value(self, value, dialect):
        """ SQL -> Python
        Uses shlex.split to handle values with spaces.
        It's a fragile solution since it will break in some cases.
        For example if the last character is a backslash or otherwise meaningful
        to a shell.
        """
        values = []
        for val in shlex.split(value):
            if " " in val and '"' in val:
                values.append(val[1:-1])
            else:
                values.append(val)
        return values
