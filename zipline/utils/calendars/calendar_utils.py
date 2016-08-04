from zipline.errors import (
    InvalidCalendarName,
    CalendarNameCollision,
)
from zipline.utils.calendars.exchange_calendar_cfe import CFEExchangeCalendar
from zipline.utils.calendars.exchange_calendar_ice import ICEExchangeCalendar
from zipline.utils.calendars.exchange_calendar_nyse import NYSEExchangeCalendar
from zipline.utils.calendars.exchange_calendar_cme import CMEExchangeCalendar
from zipline.utils.calendars.exchange_calendar_bmf import BMFExchangeCalendar
from zipline.utils.calendars.exchange_calendar_lse import LSEExchangeCalendar
from zipline.utils.calendars.exchange_calendar_tsx import TSXExchangeCalendar

_static_calendars = {}


def get_calendar(name):
    """
    Retrieves an instance of an TradingCalendar whose name is given.

    Parameters
    ----------
    name : str
        The name of the TradingCalendar to be retrieved.

    Returns
    -------
    TradingCalendar
        The desired calendar.
    """
    if name not in _static_calendars:
        if name in ["NYSE", "NASDAQ", "BATS"]:
            cal = NYSEExchangeCalendar()
        elif name in ["CME", "CBOT", "COMEX", "NYMEX"]:
            cal = CMEExchangeCalendar()
        elif name in ["ICEUS", "NYFE"]:
            cal = ICEExchangeCalendar()
        elif name == "CFE":
            cal = CFEExchangeCalendar()
        elif name == 'BMF':
            cal = BMFExchangeCalendar()
        elif name == 'LSE':
            cal = LSEExchangeCalendar()
        elif name == 'TSX':
            cal = TSXExchangeCalendar()

        else:
            raise InvalidCalendarName(calendar_name=name)

        register_calendar(name, cal)

    return _static_calendars[name]


def deregister_calendar(cal_name):
    """
    If a calendar is registered with the given name, it is de-registered.

    Parameters
    ----------
    cal_name : str
        The name of the calendar to be deregistered.
    """
    try:
        _static_calendars.pop(cal_name)
    except KeyError:
        pass


def clear_calendars():
    """
    Deregisters all current registered calendars
    """
    _static_calendars.clear()


def register_calendar(name, calendar, force=False):
    """
    Registers a calendar for retrieval by the get_calendar method.

    Parameters
    ----------
    name: str
        The key with which to register this calendar.
    calendar: TradingCalendar
        The calendar to be registered for retrieval.
    force : bool, optional
        If True, old calendars will be overwritten on a name collision.
        If False, name collisions will raise an exception. Default: False.

    Raises
    ------
    CalendarNameCollision
        If a calendar is already registered with the given calendar's name.
    """
    # If we are forcing the registration, remove an existing calendar with the
    # same name.
    if force:
        deregister_calendar(name)

    # Check if we are already holding a calendar with the same name
    if name in _static_calendars:
        raise CalendarNameCollision(calendar_name=name)

    _static_calendars[name] = calendar
