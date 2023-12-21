// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © keio1989

import dokang/POA/9 as POA

//@version=5

strategy("Bollinger Bands Break Out",
         overlay=true, 
         initial_capital=10000, 
         commission_type=strategy.commission.percent, 
         commission_value=0.04,
         margin_long=0.1,
         margin_short=0.1,
         use_bar_magnifier=true)

select_bot = input.string("PoABot", "Select Your Bot ", options=["PoABot", "TVExtBot"], inline="bot")

// POABOT
password = input.string(defval="password", title="Password ", inline="pw", group="PoABot")

// TVEXTBOT
long_entry = input.string("Long Entry Message", "Entry   ", inline="entry", group="TVExtBot")
long_close = input.string("Long Close Message", "Close   ", inline="close", group="TVExtBot")

short_entry = input.string("Short Entry Message", "", inline="entry", group="TVExtBot")
short_close = input.string("Short Close Message", "", inline="close", group="TVExtBot")

// Alert Message 
long_entry_message(user_input_style) =>
    user_input_style == "PoABot" ? POA.entry_message(password) : user_input_style == "TVExtBot" ? long_entry : na
long_exit_message(user_input_style) =>
    user_input_style == "PoABot" ? POA.exit_message(password) : user_input_style == "TVExtBot" ? long_close : na
long_close_message(user_input_style) =>
    user_input_style == "PoABot" ? POA.close_message(password) : user_input_style == "TVExtBot" ? long_close : na

short_entry_message(user_input_style) =>
    user_input_style == "PoABot" ? POA.entry_message(password) : user_input_style == "TVExtBot" ? short_entry : na
short_exit_message(user_input_style) =>
    user_input_style == "PoABot" ? POA.exit_message(password) : user_input_style == "TVExtBot" ? short_close : na
short_close_message(user_input_style) =>
    user_input_style == "PoABot" ? POA.close_message(password) : user_input_style == "TVExtBot" ? short_close : na

// Calc Date 
start_time = input.time(defval = timestamp("31 Dec 2000 15:00 +0000"), title = "Start   ", inline="timestart", group="Trade Range")
end_time = input.time(defval = timestamp("31 Dec 2099 00:00 +0000"), title = "End  ", inline="timeend", group="Trade Range")

in_trade = POA.in_trade(start_time, end_time)

// Entry Size
exchange_decimal = input.int(2, "Exchange Min Amount Decimal ", minval=0, step=1, inline="ex2", group="Entry Size")
profit_balance = input.bool(true, "Trade with net profits included in equity", group="Entry Size")
sumcapital = profit_balance ? strategy.initial_capital + strategy.netprofit : strategy.initial_capital

long_size = input.float(5, "Long Entry Size ", step=0.1, inline='up', group="Entry Size")
long_type = input.string("Percent ", "", options=["Cash ", "Percent "], inline="up", group="Entry Size")
short_size = input.float(5, "Short Entry Size ", step=0.1, inline='dn', group="Entry Size")
short_type = input.string("Percent ", "", options=["Cash ", "Percent "], inline="dn", group="Entry Size")

long_per_size = sumcapital * long_size / 100
short_per_size = sumcapital * short_size / 100

long_size_type(user_input_style) =>
    user_input_style == "Cash " ? long_size * sumcapital : user_input_style == "Percent " ? long_per_size : na
short_size_type(user_input_style) =>
    user_input_style == "Cash " ? short_size * sumcapital : user_input_style == "Percent " ? short_per_size : na

// Entry Option by Volume and Colored bar
visible_bcolor= input.bool(true, "Visible Colored Bar", inline="color", group="Colored Bar by Volume ")
vollength = input.int(20, "MA Length ", minval=1, inline="vol", group="Colored Bar by Volume ")
avrg = ta.sma(volume, vollength)

thresholdExtraHigh = input.float(4, "High  ", step=0.5, inline="vol1", group="Colored Bar by Volume ")
thresholdHigh = input.float(2.5, "Medium ", step=0.5,inline="vol1", group="Colored Bar by Volume ")
thresholdMedium = input.float(1, "Normal ", step=0.5, inline="vol2", group="Colored Bar by Volume ")
thresholdNormal = input.float(0.5, "Low     ", step=0.5, inline="vol2", group="Colored Bar by Volume ")

vol1 = volume > avrg * thresholdExtraHigh
vol2 = volume >= avrg * thresholdHigh and volume <= avrg * thresholdExtraHigh
vol3 = volume >= avrg * thresholdMedium and volume <= avrg * thresholdHigh
vol4 = volume >= avrg * thresholdNormal and volume <= avrg * thresholdMedium
vol5 = volume < avrg * thresholdNormal

l_act_low_size             = input.bool(true, "Entry Vol Low    ", inline="act1", group="Colored Bar by Volume ")
l_act_normal_size          = input.bool(true, "Entry Vol Normal  ", inline="act2", group="Colored Bar by Volume ")
l_act_medium_size          = input.bool(true, "Entry Vol Medium  ", inline="act3", group="Colored Bar by Volume ")
l_act_high_size            = input.bool(true, "Entry Vol High    ", inline="act4", group="Colored Bar by Volume ")
l_act_extrahigh_size       = input.bool(true, "Entry Vol Extra High", inline="act5", group="Colored Bar by Volume ")

s_act_low_size             = input.bool(true, "Entry Vol Low   ", inline="act1", group="Colored Bar by Volume ")
s_act_normal_size          = input.bool(true, "Entry Vol Normal  ", inline="act2", group="Colored Bar by Volume ")
s_act_medium_size          = input.bool(true, "Entry Vol Medium ", inline="act3", group="Colored Bar by Volume ")
s_act_high_size            = input.bool(true, "Entry Vol High    ", inline="act4", group="Colored Bar by Volume ")
s_act_extrahigh_size       = input.bool(true, "Entry Vol Extra High", inline="act5", group="Colored Bar by Volume ")

vol_long_entry = l_act_low_size and vol5 ? true : l_act_normal_size and vol4 ? true : l_act_medium_size and vol3 ? true : l_act_high_size and vol2 ? true : l_act_extrahigh_size and vol1 ? true : false
vol_short_entry = s_act_low_size and vol5 ? true : s_act_normal_size and vol4 ? true : s_act_medium_size and vol3 ? true : s_act_high_size and vol2 ? true : s_act_extrahigh_size and vol1 ? true : false

color_1 = input.color(#ffffff, "", inline="act1", group ="Colored Bar by Volume ") 
color_2 = input.color(#d1d4dc, "", inline="act2", group ="Colored Bar by Volume ") 
color_3 = input.color(#9598a1, "", inline="act3", group ="Colored Bar by Volume ") 
color_4 = input.color(#5d606b, "", inline="act4", group ="Colored Bar by Volume ") 
color_5 = input.color(#2a2e39, "", inline="act5", group ="Colored Bar by Volume ") 

color_bar = vol1 ? color_5 : vol2 ? color_4 : vol3 ? color_3 : vol4 ? color_2 : vol5 ? color_1 : na

barcolor(visible_bcolor ? color_bar : na, editable=false)

// Define the length of the Bollinger Bands
active_long = input.bool(true, "Activate Long    ", inline="act", group='Bollinger Bands')
active_short = input.bool(true, "Activate Short", inline="act", group='Bollinger Bands')
lbb_close = input.string('Lower ', 'Close Line ', options = ['Basis ', 'Lower '], inline='cl', group='Bollinger Bands')
sbb_close = input.string('Upper ', 'Close Line ', options = ['Basis ', 'Upper '], inline='cl', group='Bollinger Bands')
lbbmaType = input.string("SMA", "MA Type ", options = ["SMA", "EMA", "RMA", "WMA", "VWMA "], inline='ma', group='Bollinger Bands')
sbbmaType = input.string("SMA", "MA Type ", options = ["SMA", "EMA", "RMA", "WMA", "VWMA "], inline='ma', group='Bollinger Bands')
lbbLengthInput = input.int(15, title="Length  ", group="Bollinger Bands", inline="BB1")
lbbDevInput = input.float(2.0, title="StdDev  ", step=0.1, group="Bollinger Bands", inline="BB2")
lbbMinWidth = input.float(3.0, title="Min Width", step=0.5, group="Bollinger Bands", inline="BB3")
lbbDiff = input.bool(true, title='Enable BB Diff   ', group="Bollinger Bands", inline="BB4")
lbbDiffPerc = input.float(2, step=0.1, title='BB Diff % ', group="Bollinger Bands", inline="BB5")
sbbLengthInput = input.int(15, title="Length  ", group="Bollinger Bands", inline="BB1")
sbbDevInput = input.float(2.0, title="StdDev  ", step=0.1, group="Bollinger Bands", inline="BB2")
sbbMinWidth = input.float(3.0, title="Min Width ", step=0.5, group="Bollinger Bands", inline="BB3")
sbbDiff = input.bool(true, title='Enable BB Diff', group="Bollinger Bands", inline="BB4")
sbbDiffPerc = input.float(2, step=0.1, title='BB Diff % ', group="Bollinger Bands", inline="BB5")


// Calculate and plot the Bollinger Bands
lbbMiddle = ta.sma(close, lbbLengthInput)
lbbdev = lbbDevInput * ta.stdev(close, lbbLengthInput)
lbbdev := math.max(lbbdev, lbbMiddle * lbbMinWidth / 100)
lbbUpper = lbbMiddle + lbbdev
lbbLower = lbbMiddle - lbbdev


sbbMiddle = ta.sma(close, sbbLengthInput)
sbbdev = sbbDevInput * ta.stdev(close, sbbLengthInput)
sbbdev := math.max(sbbdev, sbbMiddle * sbbMinWidth / 100)
sbbUpper = sbbMiddle + sbbdev
sbbLower = sbbMiddle - sbbdev


lbbLowerCrossUnder = ta.crossunder(close, lbbLower)
lbbUpperCrossOver = ta.crossover(close, lbbUpper)

sbbLowerCrossUnder = ta.crossunder(close, sbbLower)
sbbUpperCrossOver = ta.crossover(close, sbbUpper)

lbbDiffCond = lbbDiff ? ((lbbUpper / lbbLower) * 100) - 100 >= lbbDiffPerc : true
sbbDiffCond = sbbDiff ? ((sbbUpper / sbbLower) * 100) - 100 >= sbbDiffPerc : true

// Plots Bollinger Bands
plot(active_long ? lbbMiddle : na, "Long Basis", color=color.blue)
lbbUpperPlot = plot(active_long ? lbbUpper : na, "Long Upper", color=color.new(color.blue, 80))
lbbLowerrPlot = plot(active_long ? lbbLower : na, "Long Lower", color=color.new(color.blue, 80))
fill(lbbUpperPlot, lbbLowerrPlot, title = "Long Background", color=active_long ? color.new(color.blue, 90) : na)

plot(active_short ? sbbMiddle : na, "Short Basis", color=color.red)
sbbUpperPlot = plot(active_short ? sbbUpper : na, "Short Upper", color=color.new(color.red, 80))
sbbLowerrPlot = plot(active_short ? sbbLower : na, "Short Lower", color=color.new(color.red, 80))
fill(sbbUpperPlot, sbbLowerrPlot, title = "Short Background", color=active_short ? color.new(color.red, 90) : na)

// Autonomous Recursive Moving Average
enable_long_arma = input(true, "Enable Long     ", inline="ara1", group="Autonomous Recursive Moving Average")
enable_short_arma = input(true, "Enable Short ", inline="ara1", group="Autonomous Recursive Moving Average")

ara_length = input.int(13, title='Length ', group='Autonomous Recursive Moving Average', inline='ara2')
gamma = input.float(3.0, title='Gamma ', group='Autonomous Recursive Moving Average', inline='ara2')

ma = 0.
mad = 0.

src_ = close
ma := nz(mad[1], src_)
d = ta.cum(math.abs(src_[ara_length] - ma)) / bar_index * gamma
mad := ta.sma(ta.sma(src_ > nz(mad[1], src_) + d ? src_ + d : src_ < nz(mad[1], src_) - d ? src_ - d : nz(mad[1], src_), ara_length), ara_length)

arma_long_condt = enable_long_arma ? close > mad : true
arma_short_condt = enable_short_arma ? close < mad : true

plot(mad, title='ARA', color=color.new(color.orange, 20), style=plot.style_line, linewidth=2)

// Define the settings for the Volatility Filter
lvolatilityFilterInput = input.bool(true, title="Enable Long     ", group="Volatility Filter", inline="Vol1")
lvolatilityFilterStDevLength = input(15, title="StdDev ", group="Volatility Filter", inline="Vol2")
lvolatilityStDevMaLength = input(15, title="MA  ", group="Volatility Filter", inline="Vol3")

svolatilityFilterInput = input.bool(true, title="Enable Short", group="Volatility Filter", inline="Vol1")
svolatilityFilterStDevLength = input(15, title="StdDev ", group="Volatility Filter", inline="Vol2")
svolatilityStDevMaLength = input(15, title="MA  ", group="Volatility Filter", inline="Vol3")

// Calculate and view Volatility Filter
lstdDevClose = ta.stdev(close, lvolatilityFilterStDevLength)
lvolatilityCondition = lvolatilityFilterInput ? lstdDevClose > ta.sma(lstdDevClose, lvolatilityStDevMaLength) : true

sstdDevClose = ta.stdev(close, svolatilityFilterStDevLength)
svolatilityCondition = svolatilityFilterInput ? sstdDevClose > ta.sma(sstdDevClose, svolatilityStDevMaLength) : true

// Historical Volatility Filter
enable_long_vol = input(true, "Enable Long     ", inline="vol1", group="Historical Volatility Filter")
enable_short_vol = input(true, "Enable Short ",  inline="vol1", group="Historical Volatility Filter")
HVlength = input.int(10, "Length ", minval=1, inline="vol2", group="Historical Volatility Filter")
HVthreshold = input.int(1, "Threshold ", minval=1, inline="vol2", group="Historical Volatility Filter")
HVper = timeframe.isintraday or timeframe.isdaily and timeframe.multiplier == 1 ? 1 : 7
HV = 100 * ta.stdev(math.log(close / close[1]), HVlength) * math.sqrt(365 / HVper)

HV_long_condt = enable_long_vol ? (HV - HV[1]) > HVthreshold : true
HV_short_condt = enable_short_vol ? (HV - HV[1]) > HVthreshold : true

// ADX Filter
enable_long_adx = input(true, "Enable Long     ", inline="adx1", group="ADX Filter")
enable_short_adx = input(true, "Enable Short ", inline="adx1", group="ADX Filter")
long_adxlen = input.int(14, "Length ", minval=1, inline="adx2", group="ADX Filter")
short_adxlen = input.int(14, "Length ", minval=1, inline="adx2", group="ADX Filter")

TrueRange = math.max(math.max(high - low, math.abs(high - nz(close[1]))), math.abs(low - nz(close[1])))
DirectionalMovementPlus = high - nz(high[1]) > nz(low[1]) - low ? math.max(high - nz(high[1]), 0) : 0
DirectionalMovementMinus = nz(low[1]) - low > high - nz(high[1]) ? math.max(nz(low[1]) - low, 0) : 0

long_SmoothedTrueRange = 0.0
long_SmoothedTrueRange := nz(long_SmoothedTrueRange[1]) - nz(long_SmoothedTrueRange[1]) / long_adxlen + TrueRange

long_SmoothedDirectionalMovementPlus = 0.0
long_SmoothedDirectionalMovementPlus := nz(long_SmoothedDirectionalMovementPlus[1]) - nz(long_SmoothedDirectionalMovementPlus[1]) / long_adxlen + DirectionalMovementPlus

long_SmoothedDirectionalMovementMinus = 0.0
long_SmoothedDirectionalMovementMinus := nz(long_SmoothedDirectionalMovementMinus[1]) - nz(long_SmoothedDirectionalMovementMinus[1]) / long_adxlen + DirectionalMovementMinus

long_DIPlus = long_SmoothedDirectionalMovementPlus / long_SmoothedTrueRange * 100
long_DIMinus = long_SmoothedDirectionalMovementMinus / long_SmoothedTrueRange * 100
long_DX = math.abs(long_DIPlus - long_DIMinus) / (long_DIPlus + long_DIMinus) * 100
long_ADX = ta.sma(long_DX, long_adxlen)

short_SmoothedTrueRange = 0.0
short_SmoothedTrueRange := nz(short_SmoothedTrueRange[1]) - nz(short_SmoothedTrueRange[1]) / short_adxlen + TrueRange

short_SmoothedDirectionalMovementPlus = 0.0
short_SmoothedDirectionalMovementPlus := nz(short_SmoothedDirectionalMovementPlus[1]) - nz(short_SmoothedDirectionalMovementPlus[1]) / short_adxlen + DirectionalMovementPlus

short_SmoothedDirectionalMovementMinus = 0.0
short_SmoothedDirectionalMovementMinus := nz(short_SmoothedDirectionalMovementMinus[1]) - nz(short_SmoothedDirectionalMovementMinus[1]) / short_adxlen + DirectionalMovementMinus

short_DIPlus = short_SmoothedDirectionalMovementPlus / short_SmoothedTrueRange * 100
short_DIMinus = short_SmoothedDirectionalMovementMinus / short_SmoothedTrueRange * 100
short_DX = math.abs(short_DIPlus - short_DIMinus) / (short_DIPlus + short_DIMinus) * 100
short_ADX = ta.sma(short_DX, short_adxlen)

adx_long_condt = enable_long_adx ? long_DIPlus > long_DIPlus[1] and long_DIPlus > long_DIMinus : true
adx_short_condt = enable_short_adx ? short_DIMinus > short_DIMinus[1] and short_DIPlus < short_DIMinus : true

// INPUT ============================================================================================================
bool openLongPosition = in_trade and active_long and lbbUpperCrossOver and lbbDiffCond and lvolatilityCondition and HV_long_condt and adx_long_condt and vol_long_entry and arma_long_condt
bool openShortPosition = in_trade and active_short and sbbLowerCrossUnder and sbbDiffCond and svolatilityCondition and HV_short_condt and adx_short_condt and vol_short_entry and arma_short_condt

bool closeLongPosition = active_long and lbb_close == 'Lower ' ? lbbLowerCrossUnder : ta.crossunder(close, lbbMiddle)
bool closeShortPosition = active_short and sbb_close == 'Upper ' ? sbbUpperCrossOver : ta.crossover(close, sbbMiddle)

// LOGIC ============================================================================================================
// the open signals when not already into a position
bool validOpenLongPosition = openLongPosition and not (strategy.opentrades.size(strategy.opentrades - 1) > 0)
bool validOpenShortPosition = openShortPosition and not (strategy.opentrades.size(strategy.opentrades - 1) < 0)

bool longIsActive = validOpenLongPosition or strategy.opentrades.size(strategy.opentrades - 1) > 0 and not closeLongPosition
bool shortIsActive = validOpenShortPosition or strategy.opentrades.size(strategy.opentrades - 1) < 0 and not closeShortPosition

//#endregion ========================================================================================================
//#region SHARED VARIABLES

// INPUT ============================================================================================================
atrLength = input.int(defval = 14, title = 'ATR Length ', minval = 1, inline = 'ATR', group = 'General')

// LOGIC ============================================================================================================
// take profit has to communicate its execution with the stop loss logic when 'TP' mode is selected
var bool longTrailingTakeProfitExecuted = false
var bool shortTrailingTakeProfitExecuted = false

float openAtr = ta.valuewhen(validOpenLongPosition or validOpenShortPosition, ta.atr(atrLength), 0)

//#endregion ========================================================================================================
//#region TAKE PROFIT

// INPUT ============================================================================================================
longtakeProfitTrailingEnabled = input.bool(defval = false, title = 'TO %', inline = 'Trailing', group = 'Take Profit')
longdistancePerc = input.float(defval = 0.5, title = '', minval = 0.01, maxval = 100, step = 0.05, tooltip = 'The method to calculate the Trail Offset for the Trailing Take Profit.', inline = 'Trailing', group = 'Take Profit') / 100
shorttakeProfitTrailingEnabled = input.bool(defval = false, title = 'TO %', inline = 'Trailing', group = 'Take Profit')
shortdistancePerc = input.float(defval = 0.5, title = ' ', minval = 0.01, maxval = 100, step = 0.05, tooltip = 'The method to calculate the Trail Offset for the Trailing Take Profit.', inline = 'Trailing', group = 'Take Profit') / 100
longtakeProfitMethod = input.string(defval = 'PERC', title = 'Method ', options = ['PERC', 'ATR'], inline = 'Method', group = 'Take Profit')
shorttakeProfitMethod = input.string(defval = 'PERC', title = 'Method ', options = ['PERC', 'ATR'], inline = 'Method', group = 'Take Profit')
longtakeProfitQuantityPerc = input.float(defval = 100, title = 'Qty %  ', minval = 0.0, maxval = 100, step = 1.0, inline = 'Qty', group = 'Take Profit')
shorttakeProfitQuantityPerc = input.float(defval = 100, title = 'Qty %  ', minval = 0.0, maxval = 100, step = 1.0, inline = 'Qty', group = 'Take Profit')
longTakeProfitPerc = input.float(defval = 4.0, title = 'Profit  ', minval = 0.05, step = 0.05, inline = 'Take Profit Perc', group = 'Take Profit') / 100
shortTakeProfitPerc = input.float(defval = 2.0, title = 'Profit  ', minval = 0.05, step = 0.05, inline = 'Take Profit Perc', group = 'Take Profit') / 100
longTakeProfitAtrMul = input.float(defval = 1.0, title = 'Multiplier ', minval = 0.1, step = 0.1, inline = 'Take Profit ATR Multiplier', group = 'Take Profit')
shortTakeProfitAtrMul = input.float(defval = 1.0, title = 'Multiplier ', minval = 0.1, step = 0.1, inline = 'Take Profit ATR Multiplier', group = 'Take Profit')

// LOGIC ============================================================================================================
// calculate take profit price when enter long position and peserve its value until the position closes
getLongTakeProfitPrice() =>
    switch longtakeProfitMethod
        'PERC' => close * (1 + longTakeProfitPerc)
        'ATR' => close + longTakeProfitAtrMul * openAtr
        => na

var float longTakeProfitPrice = na
longTakeProfitPrice := if (longIsActive and not longTrailingTakeProfitExecuted)
    if (validOpenLongPosition)
        getLongTakeProfitPrice()
    else
        nz(longTakeProfitPrice[1], getLongTakeProfitPrice())
else
    na

longTrailingTakeProfitExecuted := strategy.opentrades.size(strategy.opentrades - 1) > 0 and (longTrailingTakeProfitExecuted[1] or strategy.opentrades.size(strategy.opentrades - 1) < strategy.opentrades.size(strategy.opentrades - 1)[1] or strategy.opentrades.size(strategy.opentrades - 1)[1] == 0 and high >= longTakeProfitPrice)

longTrailingTakeProfitStepTicks = longTakeProfitPrice * longdistancePerc / syminfo.mintick

// calculate take profit price when enter short position and peserve its value until the position closes
getShortTakeProfitPrice() =>
    switch shorttakeProfitMethod
        'PERC' => close * (1 - shortTakeProfitPerc)
        'ATR' => close - shortTakeProfitAtrMul * openAtr
        => na

var float shortTakeProfitPrice = na
shortTakeProfitPrice := if (shortIsActive and not shortTrailingTakeProfitExecuted)
    if (validOpenShortPosition)
        getShortTakeProfitPrice()
    else
        nz(shortTakeProfitPrice[1], getShortTakeProfitPrice())
else
    na

shortTrailingTakeProfitExecuted := strategy.opentrades.size(strategy.opentrades - 1) < 0 and (shortTrailingTakeProfitExecuted[1] or strategy.opentrades.size(strategy.opentrades - 1) > strategy.opentrades.size(strategy.opentrades - 1)[1] or strategy.opentrades.size(strategy.opentrades - 1)[1] == 0 and low <= shortTakeProfitPrice)

shortTrailingTakeProfitStepTicks = shortTakeProfitPrice * shortdistancePerc / syminfo.mintick

// PLOT =============================================================================================================
var takeProfitColor = color.new(color.fuchsia, 0)
plot(series = longTakeProfitPrice, title = 'Long Take Profit', color = takeProfitColor, linewidth = 1, style = plot.style_linebr, offset = 1)
plot(series = shortTakeProfitPrice, title = 'Short Take Profit', color = takeProfitColor, linewidth = 1, style = plot.style_linebr, offset = 1)

//#endregion ========================================================================================================
//#region STOP LOSS 

// INPUT ============================================================================================================
stopLossTrailingEnabled = input.string(defval = 'OFF', title = 'Enable Trailing ', options = ['TP', 'ON', 'OFF'], inline = 'Stop Loss Trailing', group = 'Stop Loss')

longbreakEvenEnabled = input.bool(defval = false, title = 'Long Break Even   ', tooltip = 'When Take Profit price target is hit, move the Stop Loss to the entry price(or to a more strict price defined by the Stop Loss %/ATR Multiplier).', inline = 'Break even', group = 'Stop Loss')
shortbreakEvenEnabled = input.bool(defval = false, title = 'Short Break Even', tooltip = 'When Take Profit price target is hit, move the Stop Loss to the entry price(or to a more strict price defined by the Stop Loss %/ATR Multiplier).', inline = 'Break even', group = 'Stop Loss')
longstopLossMethod = input.string(defval = 'PERC', title = 'Method  ', options = ['PERC', 'ATR', 'BOTH'], inline = 'Method', group = 'Stop Loss')
shortstopLossMethod = input.string(defval = 'PERC', title = 'Method  ', options = ['PERC', 'ATR', 'BOTH'], inline = 'Method', group = 'Stop Loss')
longTrailingStopLossPerc = input.float(defval = 4.0, title = 'Stop Loss ', minval = 0.05, maxval = 100, step = 0.05, inline = 'Trailing Stop Loss Perc', group = 'Stop Loss') / 100
shortTrailingStopLossPerc = input.float(defval = 4.0, title = 'Stop Loss  ', minval = 0.05, maxval = 100, step = 0.05, inline = 'Trailing Stop Loss Perc', group = 'Stop Loss') / 100
longStopLossAtrMul = input.float(defval = 2.0, title = 'Multiplier ', minval = 0.1, step = 0.1, inline = 'Trailing Stop Loss ATR Multiplier', group = 'Stop Loss')
shortStopLossAtrMul = input.float(defval = 2.0, title = 'Multiplier ', minval = 0.1, step = 0.1, inline = 'Trailing Stop Loss ATR Multiplier', group = 'Stop Loss')

// LOGIC ============================================================================================================
getLongStopLossPrice(baseSrc) =>
    switch longstopLossMethod
        'PERC' => baseSrc * (1 - longTrailingStopLossPerc)
        'ATR' => baseSrc - longStopLossAtrMul * openAtr
        'BOTH' => math.max(baseSrc * (1 - longTrailingStopLossPerc), baseSrc - longStopLossAtrMul * openAtr)
        => na

// trailing starts when the take profit price is reached if 'TP' mode is set or from the very begining if 'ON' mode is selected
bool longTakeProfitTrailingEnabled = stopLossTrailingEnabled == 'ON' or stopLossTrailingEnabled == 'TP' and longTrailingTakeProfitExecuted

// calculate trailing stop loss price when enter long position and peserve its value until the position closes
var float longStopLossPrice = na
longStopLossPrice := if (longIsActive)
    if (validOpenLongPosition)
        getLongStopLossPrice(close)
    else
        stopPrice = getLongStopLossPrice(longTakeProfitTrailingEnabled ? high : strategy.opentrades.entry_price(strategy.opentrades - 1))
        stopPrice := longbreakEvenEnabled and longTrailingTakeProfitExecuted ? math.max(stopPrice, strategy.opentrades.entry_price(strategy.opentrades - 1)) : stopPrice
        math.max(stopPrice, nz(longStopLossPrice[1]))
else
    na

getShortStopLossPrice(baseSrc) =>
    switch shortstopLossMethod
        'PERC' => baseSrc * (1 + shortTrailingStopLossPerc)
        'ATR' => baseSrc + shortStopLossAtrMul * openAtr
        'BOTH' => math.min(baseSrc * (1 + shortTrailingStopLossPerc), baseSrc + shortStopLossAtrMul * openAtr)
        => na

// trailing starts when the take profit price is reached if 'TP' mode is set or from the very begining if 'ON' mode is selected
bool shortTakeProfitTrailingEnabled = stopLossTrailingEnabled == 'ON' or stopLossTrailingEnabled == 'TP' and shortTrailingTakeProfitExecuted

// calculate trailing stop loss price when enter short position and peserve its value until the position closes
var float shortStopLossPrice = na
shortStopLossPrice := if (shortIsActive)
    if (validOpenShortPosition)
        getShortStopLossPrice(close)
    else
        stopPrice = getShortStopLossPrice(shortTakeProfitTrailingEnabled ? low : strategy.opentrades.entry_price(strategy.opentrades - 1))
        stopPrice := shortbreakEvenEnabled and shortTrailingTakeProfitExecuted ? math.min(stopPrice, strategy.opentrades.entry_price(strategy.opentrades - 1)) : stopPrice
        math.min(stopPrice, nz(shortStopLossPrice[1], 999999.9))
else
    na

// PLOT =============================================================================================================
var stopLossColor = color.new(color.silver, 0)
plot(series = longStopLossPrice, title = 'Long Stop Loss', color = stopLossColor, linewidth = 1, style = plot.style_linebr, offset = 1)
plot(series = shortStopLossPrice, title = 'Short Stop Loss', color = stopLossColor, linewidth = 1, style = plot.style_linebr, offset = 1)

//#endregion ========================================================================================================
//#region POSITION ORDERS

lot_size = validOpenLongPosition ? long_size_type(long_type) : validOpenShortPosition ? short_size_type(short_type) : na

// LOGIC ============================================================================================================
// close on trend reversal
if (closeLongPosition)
    strategy.close(id = 'Long Entry', comment = 'TR Long', alert_message = long_close_message(select_bot), immediately = true)

// getting into position
if (validOpenLongPosition)
    strategy.close(id = 'Short Entry', comment = 'TR Short', alert_message = short_close_message(select_bot), immediately = true)
    strategy.entry(id = 'Long Entry', direction = strategy.long, qty = math.round(lot_size / close, exchange_decimal), alert_message = long_entry_message(select_bot))

// submit exit order for trailing take profit price also set the stop loss for the take profit percentage in case that stop loss is reached first
// submit exit order for trailing stop loss price for the remaining percent of the quantity not reserved by the take profit order
if (longIsActive)
    strategy.exit(id = 'Long Take Profit / Stop Loss', from_entry = 'Long Entry', qty_percent = longtakeProfitQuantityPerc, limit = longtakeProfitTrailingEnabled ? na : longTakeProfitPrice, stop = longStopLossPrice, trail_price = longtakeProfitTrailingEnabled ? longTakeProfitPrice : na, trail_offset = longtakeProfitTrailingEnabled ? longTrailingTakeProfitStepTicks : na, comment = 'Long TP', comment_loss = 'Long SL', alert_message = long_exit_message(select_bot))
    strategy.exit(id = 'Long Stop Loss', from_entry = 'Long Entry', stop = longStopLossPrice, comment = 'Long Stop', alert_message = long_exit_message(select_bot))

// close on trend reversal
if (closeShortPosition)
    strategy.close(id = 'Short Entry', comment = 'TR Short', alert_message = short_close_message(select_bot), immediately = true)

// getting into position
if (validOpenShortPosition)
    strategy.close(id = 'Long Entry', comment = 'TR Long', alert_message = long_close_message(select_bot), immediately = true)
    strategy.entry(id = 'Short Entry', direction = strategy.short, qty = math.round(lot_size / close, exchange_decimal), alert_message = short_entry_message(select_bot))

// submit exit order for trailing take profit price also set the stop loss for the take profit percentage in case that stop loss is reached first
// submit exit order for trailing stop loss price for the remaining percent of the quantity not reserved by the take profit order
if (shortIsActive)
    strategy.exit(id = 'Short Take Profit / Stop Loss', from_entry = 'Short Entry', qty_percent = shorttakeProfitQuantityPerc, limit = shorttakeProfitTrailingEnabled ? na : shortTakeProfitPrice, stop = shortStopLossPrice, trail_price = shorttakeProfitTrailingEnabled ? shortTakeProfitPrice : na, trail_offset = shorttakeProfitTrailingEnabled ? shortTrailingTakeProfitStepTicks : na, comment = 'Short TP', comment_loss = 'Short SL', alert_message = short_exit_message(select_bot))
    strategy.exit(id = 'Short Stop Loss', from_entry = 'Short Entry', stop = shortStopLossPrice, comment = 'Short Stop', alert_message = short_exit_message(select_bot))

// PLOT =============================================================================================================
var posColor = color.new(color.gray, 0)
plot(series = strategy.opentrades.entry_price(strategy.opentrades - 1), title = 'Position', color = posColor, linewidth = 1, style = plot.style_linebr)

//Table

PnL = strategy.grossprofit - strategy.grossloss
ex_PnL = math.round(strategy.openprofit, 1)

totalbalance = strategy.initial_capital + strategy.netprofit

used_equity = math.round(strategy.position_avg_price * strategy.position_size)
ratio_equity = strategy.position_size > 0 ? math.round(used_equity / totalbalance * 100, 1) : 0

mdd = strategy.opentrades.max_drawdown(strategy.opentrades - 1)

totalTrades = strategy.closedtrades
winningTrades = na(totalTrades) ? na : totalTrades - strategy.losstrades

winRate = totalTrades > 0 ? (winningTrades / totalTrades) * 100 : 0

profitFactor = math.abs(strategy.grossprofit) > 0 ? strategy.grossprofit / math.abs(strategy.grossloss) : na

avgBarsPerTrade() =>
    sumBarsPerTrade = 0
    for tradeNo = 0 to strategy.closedtrades - 1
        // Loop through all closed trades, starting with the oldest.
        sumBarsPerTrade += strategy.closedtrades.exit_bar_index(tradeNo) - strategy.closedtrades.entry_bar_index(tradeNo) + 1
    result = nz(sumBarsPerTrade / strategy.closedtrades)

show_status           = input.bool(true,'', group='Status Table', inline='t1')
status_text_size      = input.string(size.tiny, 'Size ', options=[size.tiny, size.small, size.normal], group='Status Table', inline='t1')
status_table_position = input.string(position.bottom_left, 'Position ', options=[position.bottom_left, position.bottom_right, position.bottom_center, position.top_left, position.top_right, position.top_center], group='Status Table', inline='t1')

show_performance           = input.bool(true, '', group='Profit Table', inline='t2')
performance_text_size      = input.string(size.small, 'Size ', options=[size.tiny, size.small, size.normal], group='Profit Table', inline='t2')
performance_table_position = input.string(position.bottom_right, 'Position ', options=[position.bottom_left, position.bottom_right, position.bottom_center, position.top_left, position.top_right, position.top_center], group='Profit Table', inline='t2')

// ------------------------------------------------------------------------------------------------------------------ //

profit_color1 = PnL > 0 ? color.lime : color.red
profit_color2 = strategy.openprofit < 0 ? color.red : color.lime

var Table = table.new(status_table_position, columns=10, rows=20, border_width=1, bgcolor=color.black, border_color=color.gray)

if show_status
    table.cell(table_id=Table, column=0, row=0, text='Position Size', text_size=status_text_size, text_color=color.gray)
    table.cell(table_id=Table, column=0, row=1, text=str.tostring(strategy.position_size), text_size=status_text_size, text_color=color.green)
    table.cell(table_id=Table, column=0, row=2, text='Avg Price', text_size=status_text_size, text_color=color.gray)
    table.cell(table_id=Table, column=0, row=3, text=str.tostring(math.round_to_mintick(strategy.position_avg_price)), text_size=status_text_size, text_color=color.green)

    table.cell(table_id=Table, column=1, row=0, text='Unrealized PnL', text_size=status_text_size, text_color=color.gray)
    table.cell(table_id=Table, column=1, row=1, text=str.tostring(math.round(strategy.openprofit, 1)) + ' ' + syminfo.currency, text_size=status_text_size, text_color=profit_color2)
    table.cell(table_id=Table, column=1, row=2, text_color=color.gray, text_size=status_text_size, text='Net profit')
    table.cell(table_id=Table, column=1, row=3, text=str.tostring(math.round(PnL, 1)) + ' ' + syminfo.currency, text_size=status_text_size, text_color=profit_color1)

    table.cell(table_id=Table, column=2, row=0, text='Win Rate', text_size=status_text_size, text_color=color.gray)
    table.cell(table_id=Table, column=2, row=1, text=str.tostring(math.round(winRate, 1)), text_size=status_text_size, text_color=color.green)
    table.cell(table_id=Table, column=2, row=2, text='Profit Factor', text_size=status_text_size, text_color=color.gray)
    table.cell(table_id=Table, column=2, row=3, text=str.tostring(math.round(profitFactor, 2)), text_size=status_text_size, text_color=color.olive)

    table.cell(table_id=Table, column=4, row=0, text='Max Drawdown', text_size=status_text_size, text_color=color.gray)
    table.cell(table_id=Table, column=4, row=1, text=str.tostring(math.round(mdd, 1)), text_size=status_text_size, text_color=color.green)
    table.cell(table_id=Table, column=4, row=2, text='Bars Per Trade', text_size=status_text_size, text_color=color.gray)
    table.cell(table_id=Table, column=4, row=3, text=str.tostring(int(avgBarsPerTrade())), text_size=status_text_size, text_color=color.olive)

if show_performance
    new_month = month(time) != month(time[1])
    new_year  = year(time)  != year(time[1])
    
    eq = strategy.initial_capital + strategy.netprofit
    
    bar_pnl = eq / eq[1] - 1
    
    cur_month_pnl = 0.0
    cur_year_pnl  = 0.0
    
    // Current Monthly P&L
    cur_month_pnl := new_month ? 0.0 : 
                     (1 + cur_month_pnl[1]) * (1 + bar_pnl) - 1 
    
    // Current Yearly P&L
    cur_year_pnl := new_year ? 0.0 : 
                     (1 + cur_year_pnl[1]) * (1 + bar_pnl) - 1  
    
    // Arrays to store Yearly and Monthly P&Ls
    var month_pnl  = array.new_float(0)
    var month_time = array.new_int(0)
    
    var year_pnl  = array.new_float(0)
    var year_time = array.new_int(0)
    
    last_computed = false
    
    if (not na(cur_month_pnl[1]) and (new_month or barstate.islastconfirmedhistory))
        if (last_computed[1])
            array.pop(month_pnl)
            array.pop(month_time)
            
        array.push(month_pnl , cur_month_pnl[1])
        array.push(month_time, time[1])
    
    if (not na(cur_year_pnl[1]) and (new_year or barstate.islastconfirmedhistory))
        if (last_computed[1])
            array.pop(year_pnl)
            array.pop(year_time)
            
        array.push(year_pnl , cur_year_pnl[1])
        array.push(year_time, time[1])
    
    last_computed := barstate.islastconfirmedhistory ? true : nz(last_computed[1])
    
    // Monthly P&L Table    
    var monthly_table = table(na)
    
    if (barstate.islastconfirmedhistory)
        monthly_table := table.new(performance_table_position, columns = 14, rows = array.size(year_pnl) + 1, border_width = 1)
    
        table.cell(monthly_table, 0,  0, "", text_size=performance_text_size,     bgcolor = color.gray)
        table.cell(monthly_table, 1,  0, "Jan", text_size=performance_text_size,  bgcolor = color.gray)
        table.cell(monthly_table, 2,  0, "Feb", text_size=performance_text_size,  bgcolor = color.gray)
        table.cell(monthly_table, 3,  0, "Mar", text_size=performance_text_size,  bgcolor = color.gray)
        table.cell(monthly_table, 4,  0, "Apr", text_size=performance_text_size,  bgcolor = color.gray)
        table.cell(monthly_table, 5,  0, "May", text_size=performance_text_size,  bgcolor = color.gray)
        table.cell(monthly_table, 6,  0, "Jun", text_size=performance_text_size,  bgcolor = color.gray)
        table.cell(monthly_table, 7,  0, "Jul", text_size=performance_text_size,  bgcolor = color.gray)
        table.cell(monthly_table, 8,  0, "Aug", text_size=performance_text_size,  bgcolor = color.gray)
        table.cell(monthly_table, 9,  0, "Sep", text_size=performance_text_size,  bgcolor = color.gray)
        table.cell(monthly_table, 10, 0, "Oct", text_size=performance_text_size,  bgcolor = color.gray)
        table.cell(monthly_table, 11, 0, "Nov", text_size=performance_text_size,  bgcolor = color.gray)
        table.cell(monthly_table, 12, 0, "Dec", text_size=performance_text_size,  bgcolor = color.gray)
        table.cell(monthly_table, 13, 0, "Year", text_size=performance_text_size, bgcolor = color.gray)
    
    
        for yi = 0 to array.size(year_pnl) - 1
            table.cell(monthly_table, 0,  yi + 1, str.tostring(year(array.get(year_time, yi))), text_size=performance_text_size, bgcolor = color.gray)
            
            y_color = array.get(year_pnl, yi) > 0 ? color.new(color.teal, transp = 40) : color.new(color.gray, transp = 40)
            table.cell(monthly_table, 13, yi + 1, str.tostring(math.round(array.get(year_pnl, yi) * 100, 1)), bgcolor = y_color, text_size=performance_text_size, text_color=color.new(color.white, 0))
            
        for mi = 0 to array.size(month_time) - 1
            m_row   = year(array.get(month_time, mi))  - year(array.get(year_time, 0)) + 1
            m_col   = month(array.get(month_time, mi)) 
            m_color = array.get(month_pnl, mi) > 0 ? color.new(color.teal, transp = 40) : color.new(color.gray, transp = 40)
            
            table.cell(monthly_table, m_col, m_row, str.tostring(math.round(array.get(month_pnl, mi) * 100, 1)), bgcolor = m_color, text_size=performance_text_size, text_color=color.new(color.white, 0))
        