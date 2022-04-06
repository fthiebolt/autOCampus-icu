def topic_match(filter, topic):

    filter_atoms = filter.split('/')
    topic_atoms = topic.split('/')

    # can't match
    if len(filter_atoms) == 0 or len(topic_atoms) == 0:
        return False

    # can't match
    if len(filter_atoms) > len(topic_atoms):
        return False

    for topic_atom in topic_atoms:
        fhead, *ftail = filter_atoms

        # match, topic end not relevant
        if fhead == "#":
            return True

        # can't match
        if fhead != "+" and fhead != topic_atom:
            return False

        filter_atoms = ftail

    return True
