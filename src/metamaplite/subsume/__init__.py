""" Code for subsuming entities or removing subsumed entities """


def is_entity_subsumed(target, entitycoll):
    """Is entity subsumed?  If any entity in supplied entitylist subsumes
       target entity then the method returns true. """
    subsumed = False
    # print('target: %s, %s' % target)
    for entity in entitycoll:
        # print('entity: %s, %s' % entity)
        if (len(target.text) != len(entity.text)) & \
           (target.start >= entity.start) & \
           ((target.start + len(target.text)) <=
            (entity.start + len(entity.text))):
            # print("%s is subsumed by %s." % (target, entity))
            subsumed = True
    # print('%s subsumed = %s' % (target, subsumed))
    return subsumed


def remove_subsumed_entities(entitycoll):
    """Remove any entities subsumed by any other longer encompassing
       entity."""
    newentitylist = []
    for entity in entitycoll:
        if not is_entity_subsumed(entity, entitycoll):
            newentitylist.append(entity)
    return newentitylist


def resolve_overlaps(entitylist):
    """Remove any entities overlapping a previous entity.

    text:   quality healthcare service
            |                |       |
    entity0 +----------------+       |
                    |                |
            entity1 +----------------+

    The entity referings to "healthcare service" (entity1) should be
    removed.

    """
    newlist = []
    ovlist = []
    for entity0 in entitylist:
        newlist.append(entity0)
        for entity1 in entitylist:
            if entity0 != entity1:
                if (entity0.start < entity1.start) & \
                   (entity0.end > entity1.start):
                    ovlist.append(entity1)
    for entity in ovlist:
        if entity in newlist:
            newlist.remove(entity)
    return newlist
