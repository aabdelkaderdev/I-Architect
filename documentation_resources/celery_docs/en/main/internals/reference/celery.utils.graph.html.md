<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.utils.graph.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.graph.html).

# `celery.utils.graph`

Dependency graph implementation.

exception celery.utils.graph.CycleError[[source]](../../_modules/celery/utils/graph.html#CycleError)
:   A cycle was detected in an acyclic graph.

class celery.utils.graph.DOT[[source]](../../_modules/celery/utils/graph.html#DOT)
:   Constants related to the dot format.

    ATTR = '{name}={value}'

    ATTRSEP = ', '

    DIRS = {'digraph': '->', 'graph': '--'}

    EDGE = '{INp}"{0}" {dir} "{1}" [{attrs}]'

    HEAD = '\n{IN}{type} {id} {{\n{INp}graph [{attrs}]\n'

    NODE = '{INp}"{0}" [{attrs}]'

    TAIL = '{IN}}}'

class celery.utils.graph.DependencyGraph(*it=None*, *formatter=None*)[[source]](../../_modules/celery/utils/graph.html#DependencyGraph)
:   A directed acyclic graph of objects and their dependencies.

    Supports a robust topological sort
    to detect the order in which they must be handled.

    Takes an optional iterator of `(obj, dependencies)`
    tuples to build the graph from.

    Warning

    Does not support cycle detection.

    add\_arc(*obj*)[[source]](../../_modules/celery/utils/graph.html#DependencyGraph.add_arc)
    :   Add an object to the graph.

    add\_edge(*A*, *B*)[[source]](../../_modules/celery/utils/graph.html#DependencyGraph.add_edge)
    :   Add an edge from object `A` to object `B`.

        I.e. `A` depends on `B`.

    connect(*graph*)[[source]](../../_modules/celery/utils/graph.html#DependencyGraph.connect)
    :   Add nodes from another graph.

    edges()[[source]](../../_modules/celery/utils/graph.html#DependencyGraph.edges)
    :   Return generator that yields for all edges in the graph.

    format(*obj*)[[source]](../../_modules/celery/utils/graph.html#DependencyGraph.format)

    items()

    iteritems()

    repr\_node(*obj*, *level=1*, *fmt='{0}({1})'*)[[source]](../../_modules/celery/utils/graph.html#DependencyGraph.repr_node)

    to\_dot(*fh*, *formatter=None*)[[source]](../../_modules/celery/utils/graph.html#DependencyGraph.to_dot)
    :   Convert the graph to DOT format.

        Parameters:
        :   - **fh** (*IO*) – A file, or a file-like object to write the graph to.
            - **formatter** ([*celery.utils.graph.GraphFormatter*](#celery.utils.graph.GraphFormatter "celery.utils.graph.GraphFormatter")) – Custom graph
              formatter to use.

    topsort()[[source]](../../_modules/celery/utils/graph.html#DependencyGraph.topsort)
    :   Sort the graph topologically.

        Returns:
        :   of objects in the order in which they must be handled.

        Return type:
        :   List

    update(*it*)[[source]](../../_modules/celery/utils/graph.html#DependencyGraph.update)
    :   Update graph with data from a list of `(obj, deps)` tuples.

    valency\_of(*obj*)[[source]](../../_modules/celery/utils/graph.html#DependencyGraph.valency_of)
    :   Return the valency (degree) of a vertex in the graph.

class celery.utils.graph.GraphFormatter(*root=None*, *type=None*, *id=None*, *indent=0*, *inw='    '*, *\*\*scheme*)[[source]](../../_modules/celery/utils/graph.html#GraphFormatter)
:   Format dependency graphs.

    FMT(*fmt*, *\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/utils/graph.html#GraphFormatter.FMT)

    attr(*name*, *value*)[[source]](../../_modules/celery/utils/graph.html#GraphFormatter.attr)

    attrs(*d*, *scheme=None*)[[source]](../../_modules/celery/utils/graph.html#GraphFormatter.attrs)

    draw\_edge(*a*, *b*, *scheme=None*, *attrs=None*)[[source]](../../_modules/celery/utils/graph.html#GraphFormatter.draw_edge)

    draw\_node(*obj*, *scheme=None*, *attrs=None*)[[source]](../../_modules/celery/utils/graph.html#GraphFormatter.draw_node)

    edge(*a*, *b*, *\*\*attrs*)[[source]](../../_modules/celery/utils/graph.html#GraphFormatter.edge)

    edge\_scheme = {'arrowcolor': 'black', 'arrowsize': 0.7, 'color': 'darkseagreen4'}

    graph\_scheme = {'bgcolor': 'mintcream'}

    head(*\*\*attrs*)[[source]](../../_modules/celery/utils/graph.html#GraphFormatter.head)

    label(*obj*)[[source]](../../_modules/celery/utils/graph.html#GraphFormatter.label)

    node(*obj*, *\*\*attrs*)[[source]](../../_modules/celery/utils/graph.html#GraphFormatter.node)

    node\_scheme = {'color': 'palegreen4', 'fillcolor': 'palegreen3'}

    scheme = {'arrowhead': 'vee', 'fontname': 'HelveticaNeue', 'shape': 'box', 'style': 'filled'}

    tail()[[source]](../../_modules/celery/utils/graph.html#GraphFormatter.tail)

    term\_scheme = {'color': 'palegreen2', 'fillcolor': 'palegreen1'}

    terminal\_node(*obj*, *\*\*attrs*)[[source]](../../_modules/celery/utils/graph.html#GraphFormatter.terminal_node)