from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_INTEGER, FORMAT_DATETIME, TYPE_ARRAY, FORMAT_URI


class ProfileSchema:
    """"Schemas for model Profiles"""
    @classmethod
    def get_output(cls):
        return Schema(type=TYPE_OBJECT,
                      properties={
                          'id':
                          Schema(type=TYPE_INTEGER),
                          'email':
                          Schema(type=TYPE_STRING, description='Email user'),
                          'name':
                          Schema(type=TYPE_STRING, description='Tên user'),
                      })
