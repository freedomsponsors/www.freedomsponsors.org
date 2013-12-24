from core.models import Tag

__author__ = 'tony'


def addTag(name, objtype, objid):
    tag = Tag(name=name, objtype=objtype, objid=objid)
    tag.save()
    return tag


def removeTag(name, objtype, objid):
    query = Tag.objects.filter(name=name, objtype=objtype, objid=objid)
    if query.count() == 0:
        return
    tag = query[0]
    tag.delete()