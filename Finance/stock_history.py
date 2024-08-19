import yfinance as yf

aa = yf.Ticker("AA")
arnc = yf.Ticker("ARNC")
hwm = yf.Ticker("HWM")
ge = yf.Ticker("GE")

aa.info

_aa = aa.history(start="2012-04-26", end="2012-04-27", auto_adjust=False)
_arnc = arnc.history(start="2012-04-26", end="2012-04-27", auto_adjust=False)
_hwm = hwm.history(start="2012-04-26", end="2012-04-27", auto_adjust=False)

_ge = ge.history(start="2021-07-01", end="2021-08-20", auto_adjust=False)
_ge2 = ge.history(start="2012-04-20", end="2012-04-30", auto_adjust=True)
_ge0 = ge.history(start="2017-01-30", end="2017-02-01", auto_adjust=False)


def fmv(ticker):
    return (ticker.High + ticker.Low) / 2


_aa_split = aa.history(start="2016-10-31", end="2016-11-08", auto_adjust=False)
_hwm_split2 = arnc.history(start="2020-03-20", end="2020-04-20", auto_adjust=True)

