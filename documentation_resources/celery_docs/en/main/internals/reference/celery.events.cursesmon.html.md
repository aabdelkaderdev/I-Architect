<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.events.cursesmon.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.events.cursesmon.html).

# `celery.events.cursesmon`

Graphical monitor of Celery events using curses.

class celery.events.cursesmon.CursesMonitor(*state*, *app*, *keymap=None*)[[source]](../../_modules/celery/events/cursesmon.html#CursesMonitor)
:   A curses based Celery task monitor.

    alert(*callback*, *title=None*)[[source]](../../_modules/celery/events/cursesmon.html#CursesMonitor.alert)

    alert\_remote\_control\_reply(*reply*)[[source]](../../_modules/celery/events/cursesmon.html#CursesMonitor.alert_remote_control_reply)

    background = 7

    property display\_height

    display\_task\_row(*lineno*, *task*)[[source]](../../_modules/celery/events/cursesmon.html#CursesMonitor.display_task_row)

    property display\_width

    draw()[[source]](../../_modules/celery/events/cursesmon.html#CursesMonitor.draw)

    find\_position()[[source]](../../_modules/celery/events/cursesmon.html#CursesMonitor.find_position)

    foreground = 0

    format\_row(*uuid*, *task*, *worker*, *timestamp*, *state*)[[source]](../../_modules/celery/events/cursesmon.html#CursesMonitor.format_row)

    greet = 'celery events 5.6.2 (recovery)'

    handle\_keypress()[[source]](../../_modules/celery/events/cursesmon.html#CursesMonitor.handle_keypress)

    help = 'j:down k:up i:info t:traceback r:result c:revoke ^c: quit'

    help\_title = 'Keys: '

    info\_str = 'Info: '

    init\_screen()[[source]](../../_modules/celery/events/cursesmon.html#CursesMonitor.init_screen)

    keyalias = {258: 'J', 259: 'K', 343: 'I'}

    keymap = {}

    property limit

    move\_selection(*direction=1*)[[source]](../../_modules/celery/events/cursesmon.html#CursesMonitor.move_selection)

    move\_selection\_down()[[source]](../../_modules/celery/events/cursesmon.html#CursesMonitor.move_selection_down)

    move\_selection\_up()[[source]](../../_modules/celery/events/cursesmon.html#CursesMonitor.move_selection_up)

    nap()[[source]](../../_modules/celery/events/cursesmon.html#CursesMonitor.nap)

    online\_str = 'Workers online: '

    readline(*x*, *y*)[[source]](../../_modules/celery/events/cursesmon.html#CursesMonitor.readline)

    resetscreen()[[source]](../../_modules/celery/events/cursesmon.html#CursesMonitor.resetscreen)

    revoke\_selection()[[source]](../../_modules/celery/events/cursesmon.html#CursesMonitor.revoke_selection)

    safe\_add\_str(*y*, *x*, *string*, *\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/events/cursesmon.html#CursesMonitor.safe_add_str)

    screen\_delay = 10

    property screen\_height

    property screen\_width

    selected\_position = 0

    selected\_str = 'Selected: '

    selected\_task = None

    selection\_info()[[source]](../../_modules/celery/events/cursesmon.html#CursesMonitor.selection_info)

    selection\_rate\_limit()[[source]](../../_modules/celery/events/cursesmon.html#CursesMonitor.selection_rate_limit)

    selection\_result()[[source]](../../_modules/celery/events/cursesmon.html#CursesMonitor.selection_result)

    selection\_traceback()[[source]](../../_modules/celery/events/cursesmon.html#CursesMonitor.selection_traceback)

    property tasks

    win = None

    property workers

celery.events.cursesmon.evtop(*app=None*)[[source]](../../_modules/celery/events/cursesmon.html#evtop)
:   Start curses monitor.