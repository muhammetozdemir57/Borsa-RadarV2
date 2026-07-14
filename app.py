import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import requests
import time
from datetime import datetime
 
# ==============================================================
# SAYFA AYARLARI
# ==============================================================
st.set_page_config(
   page_title="Borsa Radar V2",
   page_icon="📈",
   layout="wide"
)
 
st.markdown("""
<style>
.main {
   background-color: #0e1117;
}
.block-container {
   padding-top: 1.5rem;
}
.metric-card {
   background: #161b22;
   padding: 18px;
   border-radius: 14px;
   border: 1px solid #30363d;
}
.big-title {
   font-size: 42px;
   font-weight: 800;
   color: #00ff99;
}
.sub-title {
   color: #c9d1d9;
   font-size: 16px;
}
</style>
""", unsafe_allow_html=True)
 
st.markdown('<div class="big-title">📈 Borsa Radar V2</div>', unsafe_allow_html=True)
st.markdown(
   '<div class="sub-title">Regresyon Kanalı, Güçlü Sinyal Sistemi ve Backtest Motoru</div>',
   unsafe_allow_html=True
)
st.divider()
 
# ==============================================================
# BIST YEDEK SEMBOL LİSTESİ
# ==============================================================
BIST_FALLBACK = [
   "A1CAP","ACSEL","ADEL","ADESE","ADGYO","AEFES","AFYON","AGESA","AGHOL","AGROT",
   "AHGAZ","AKBNK","AKCNS","AKENR","AKFGY","AKFYE","AKGRT","AKMGY","AKSA","AKSEN",
   "AKSGY","AKSUE","AKYHO","ALARK","ALBRK","ALCAR","ALCTL","ALFAS","ALGYO","ALKA",
   "ALKIM","ALMAD","ALTNY","ANELE","ANGEN","ANHYT","ANSGR","ARASE","ARCLK","ARDYZ",
   "ARENA","ARSAN","ARZUM","ASELS","ASTOR","ASUZU","ATAGY","ATAKP","ATATP","AVHOL",
   "AVGYO","AVOD","AVPGY","AVTUR","AYDEM","AYEN","AYGAZ","AZTEK","BAGFS","BAKAB",
   "BANVT","BARMA","BASGZ","BAYRK","BEGYO","BERA","BEYAZ","BFREN","BIENY","BIGCH",
   "BIMAS","BINHO","BIOEN","BIZIM","BJKAS","BLCYT","BMSCH","BMSTL","BNTAS","BOBET",
   "BORLS","BORSK","BOSSA","BRISA","BRKSN","BRLSM","BRSAN","BRYAT","BSOKE","BTCIM",
   "BUCIM","BURCE","BURVA","BVSAN","BYDNR","CANTE","CATES","CCOLA","CEMAS","CEMTS",
   "CIMSA","CLEBI","CMBTN","CMENT","CONSE","CRDFA","CRFSA","CUSAN","CVKMD","CWENE",
   "DAGHL","DAGI","DAPGM","DARDL","DENGE","DERHL","DERIM","DESA","DESPC","DEVA",
   "DGATE","DGGYO","DGNMO","DITAS","DMRGD","DOAS","DOBUR","DOCO","DOFER","DOGUB",
   "DOHOL","DOKTA","DURDO","DYOBY","DZGYO","EBEBK","ECILC","ECZYT","EDATA","EDIP",
   "EGEEN","EGEPO","EGGUB","EGPRO","EGSER","EKGYO","EKOS","EKSUN","ELITE","EMKEL",
   "ENERY","ENJSA","ENKAI","ENSRI","EPLAS","ERBOS","ERCB","EREGL","ERSU","ESCAR",
   "ESCOM","ESEN","ETILR","EUHOL","EUPWR","EUREN","EYGYO","FADE","FENER","FLAP",
   "FMIZP","FONET","FORMT","FORTE","FRIGO","FROTO","FZLGY","GARAN","GARFA","GEDIK",
   "GEDZA","GENIL","GENTS","GEREL","GESAN","GIPTA","GLBMD","GLCVY","GLRYH","GLYHO",
   "GMTAS","GOKNR","GOLTS","GOODY","GOZDE","GRSEL","GRTRK","GSDDE","GSDHO","GSRAY",
   "GUBRF","GWIND","GZNMI","HALKB","HATEK","HATSN","HDFGS","HEDEF","HEKTS","HKTM",
   "HLGYO","HTTBT","HUBVC","HUNER","HURGZ","ICBCT","ICUGS","IDEAS","IDGYO","IEYHO",
   "IHAAS","IHEVA","IHGZT","IHLAS","IHLGM","IHYAY","IMASM","INDES","INFO","INGRM",
   "INTEM","INVEO","INVES","IPEKE","ISBIR","ISBTR","ISCTR","ISDMR","ISFIN","ISGSY",
   "ISGYO","ISKPL","ISMEN","ISSEN","ISYAT","IZENR","IZINV","IZMDC","JANTS","KAPLM",
   "KAREL","KARSN","KARTN","KARYE","KATMR","KAYSE","KBORU","KCAER","KCHOL","KENT",
   "KERVT","KFEIN","KGYO","KIMMR","KLGYO","KLKIM","KLMSN","KLNMA","KLRHO","KLSER",
   "KLSYN","KMPUR","KNFRT","KONKA","KONTR","KONYA","KOPOL","KORDS","KOZAA","KOZAL",
   "KRDMA","KRDMB","KRDMD","KRGYO","KRONT","KRPLS","KRSTL","KRTEK","KRVGD","KSTUR",
   "KTLEV","KTSKR","KUTPO","KUYAS","KZBGY","KZGYO","LIDER","LINK","LKMNH","LOGO",
   "LRSHO","LUKSK","MAALT","MACKO","MAGEN","MAKIM","MAKTK","MANAS","MARBL","MARKA",
   "MARTI","MAVI","MEDTR","MEGAP","MEGMT","MEKAG","MERCN","MERIT","MERKO","METRO",
   "METUR","MGROS","MHRGY","MIATK","MIPAZ","MNDRS","MNDTR","MOBTL","MPARK","MRGYO",
   "MRSHL","MSGYO","MTRKS","MTRYO","NATEN","NETAS","NIBAS","NTGAZ","NTHOL","NUGYO",
   "NUHCM","OBAMS","OBASE","ODAS","OFSYM","ONCSM","ORCAY","ORGE","ORMA","OSMEN",
   "OSTIM","OTKAR","OYAKC","OYLUM","OYYAT","OZATD","OZGYO","OZKGY","OZRDN","OZSUB",
   "PAGYO","PAMEL","PAPIL","PARSN","PASEU","PATEK","PCILT","PEKGY","PENGD","PENTA",
   "PETKM","PETUN","PGSUS","PINSU","PKART","PNLSN","PNSUT","POLHO","PRDGS","PRKAB",
   "PRKME","PRZMA","PSGYO","QUAGR","RALYH","RAYSG","REEDR","RGYAS","RNPOL","RODRG",
   "RTALB","RUBNS","RYGYO","RYSAS","SAFKR","SAHOL","SAMAT","SANEL","SANFM","SANKO",
   "SARKY","SASA","SAYAS","SDTTR","SEGYO","SEKFK","SEKUR","SELEC","SELVA","SEYKM",
   "SILVR","SISE","SKBNK","SKTAS","SKYMD","SMART","SMRTG","SNGYO","SNICA","SOKE",
   "SOKM","SONME","SRVGY","SUNTK","SURGY","SUWEN","TABGD","TARKM","TATEN","TATGD",
   "TAVHL","TCELL","TDGYO","TERA","TEZOL","TGSAS","THYAO","TKFEN","TKNSA","TLMAN",
   "TMPOL","TMSN","TNZTP","TOASO","TRCAS","TRGYO","TRILC","TSGYO","TSKB","TSPOR",
   "TTKOM","TTRAK","TUCLK","TUKAS","TUPRS","TUREX","TURGG","TURSG","ULAS","ULKER",
   "ULUFA","ULUSE","ULUUN","UNLU","USAK","VAKBN","VAKFN","VAKKO","VANGD","VBTYZ",
   "VERTU","VERUS","VESBE","VESTL","VKFYO","VKGYO","VRGYO","YAPRK","YATAS","YAYLA",
   "YBTAS","YEOTK","YESIL","YKBNK","YKSLN","YONGA","YUNSA","YYAPI","YYLGD","ZEDUR",
   "ZOREN","ZRGYO"
]
 
 
def clean_symbol(symbol):
   symbol = str(symbol).upper().strip()
   symbol = symbol.replace(".IS", "")
   symbol = symbol.replace("BIST:", "")
   return "".join(ch for ch in symbol if ch.isalnum())
 
 
@st.cache_data(ttl=3600, show_spinner=False)
def get_bist_symbols():
   try:
       url = "https://www.oyakyatirim.com.tr/piyasa-verileri/XUTUM"
       headers = {"User-Agent": "Mozilla/5.0"}
       response = requests.get(url, headers=headers, timeout=15, verify=False)
       response.raise_for_status()
       tables = pd.read_html(response.text)
       symbols = []
 
       for table in tables:
           for col in table.columns:
               col_name = str(col).lower()
               if "sembol" in col_name or "kod" in col_name:
                   symbols.extend(table[col].dropna().astype(str).tolist())
 
       cleaned = sorted({clean_symbol(s) for s in symbols})
       cleaned = [s for s in cleaned if 3 <= len(s) <= 6]
 
       if len(cleaned) > 100:
           return cleaned
   except Exception:
       pass
 
   return sorted(set(BIST_FALLBACK))
 
 
@st.cache_data(ttl=900, show_spinner=False)
def get_stock_data(symbol, display_period="6mo"):
   try:
       ticker = symbol + ".IS"
       download_period = "2y" if display_period == "1y" else "1y"
       df = yf.Ticker(ticker).history(
           period=download_period,
           interval="1d",
           auto_adjust=True,
           repair=True
       )
 
       if df is None or df.empty:
           return None
 
       required_columns = ["Open", "High", "Low", "Close", "Volume"]
       if not all(column in df.columns for column in required_columns):
           return None
 
       df = df[required_columns].copy()
       df = df.replace([np.inf, -np.inf], np.nan).dropna()
       df = df[df["Volume"] > 0]
 
       if len(df) < 220:
           return None
 
       return df
   except Exception:
       return None
 
 
# ==============================================================
# TEKNİK İNDİKATÖRLER
# ==============================================================
def calc_rsi(series, period=14):
   delta = series.diff()
   gain = delta.clip(lower=0)
   loss = -delta.clip(upper=0)
   alpha = 1 / period
 
   avg_gain = gain.ewm(alpha=alpha, adjust=False, min_periods=period).mean()
   avg_loss = loss.ewm(alpha=alpha, adjust=False, min_periods=period).mean()
 
   rs = avg_gain / avg_loss.replace(0, np.nan)
   return (100 - (100 / (1 + rs))).fillna(50)
 
 
def calc_ema(series, period):
   return series.ewm(span=period, adjust=False).mean()
 
 
def calc_atr(df, period=14):
   high = df["High"]
   low = df["Low"]
   close = df["Close"]
   previous_close = close.shift(1)
 
   true_range = pd.concat([
       high - low,
       (high - previous_close).abs(),
       (low - previous_close).abs()
   ], axis=1).max(axis=1)
 
   return true_range.ewm(
       alpha=1 / period,
       adjust=False,
       min_periods=period
   ).mean()
 
 
def calc_obv(df):
   values = [0.0]
   for i in range(1, len(df)):
       if df["Close"].iloc[i] > df["Close"].iloc[i - 1]:
           values.append(values[-1] + df["Volume"].iloc[i])
       elif df["Close"].iloc[i] < df["Close"].iloc[i - 1]:
           values.append(values[-1] - df["Volume"].iloc[i])
       else:
           values.append(values[-1])
   return pd.Series(values, index=df.index, dtype=float)
 
 
def calc_macd(close):
   ema12 = calc_ema(close, 12)
   ema26 = calc_ema(close, 26)
   macd = ema12 - ema26
   signal = calc_ema(macd, 9)
   histogram = macd - signal
   return macd, signal, histogram
 
 
def calc_adx(df, period=14):
   high = df["High"]
   low = df["Low"]
   close = df["Close"]
 
   up_move = high.diff()
   down_move = -low.diff()
 
   plus_dm = pd.Series(
       np.where((up_move > down_move) & (up_move > 0), up_move, 0.0),
       index=df.index
   )
   minus_dm = pd.Series(
       np.where((down_move > up_move) & (down_move > 0), down_move, 0.0),
       index=df.index
   )
 
   previous_close = close.shift(1)
   true_range = pd.concat([
       high - low,
       (high - previous_close).abs(),
       (low - previous_close).abs()
   ], axis=1).max(axis=1)
 
   atr = true_range.ewm(alpha=1 / period, adjust=False, min_periods=period).mean()
   plus_dm_smoothed = plus_dm.ewm(alpha=1 / period, adjust=False, min_periods=period).mean()
   minus_dm_smoothed = minus_dm.ewm(alpha=1 / period, adjust=False, min_periods=period).mean()
 
   plus_di = 100 * plus_dm_smoothed / atr.replace(0, np.nan)
   minus_di = 100 * minus_dm_smoothed / atr.replace(0, np.nan)
   dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)
   adx = dx.ewm(alpha=1 / period, adjust=False, min_periods=period).mean()
 
   return adx.fillna(0), plus_di.fillna(0), minus_di.fillna(0)
 
 
def normalized_slope(series, period=20):
   if len(series) < period:
       return 0.0
 
   values = series.tail(period).astype(float).values
   if not np.all(np.isfinite(values)):
       return 0.0
 
   x = np.arange(period, dtype=float)
   slope, _ = np.polyfit(x, values, 1)
   mean_value = np.mean(values)
   return float(slope / mean_value * 100) if mean_value != 0 else 0.0
 
 
def calc_regression_channel(close, period=60, std_multiplier=2.0):
   if len(close) < period:
       return None
 
   values = close.tail(period).astype(float).values
   if not np.all(np.isfinite(values)):
       return None
 
   x = np.arange(period, dtype=float)
   slope, intercept = np.polyfit(x, values, 1)
   fitted = intercept + slope * x
   residuals = values - fitted
   residual_std = float(np.std(residuals, ddof=1))
 
   upper = fitted + std_multiplier * residual_std
   lower = fitted - std_multiplier * residual_std
 
   ss_res = float(np.sum((values - fitted) ** 2))
   ss_tot = float(np.sum((values - np.mean(values)) ** 2))
   r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
   r_squared = max(0.0, min(r_squared, 1.0))
 
   middle_last = float(fitted[-1])
   upper_last = float(upper[-1])
   lower_last = float(lower[-1])
   last_close = float(values[-1])
   channel_width = upper_last - lower_last
   position = (last_close - lower_last) / channel_width if channel_width > 0 else 0.5
   slope_pct = slope / middle_last * 100 if middle_last != 0 else 0.0
 
   return {
       "middle": middle_last,
       "upper": upper_last,
       "lower": lower_last,
       "slope": float(slope),
       "slope_pct": float(slope_pct),
       "r_squared": float(r_squared),
       "position": float(position),
       "residual_std": residual_std
   }
 
 
# ==============================================================
# GÜÇLÜ SİNYAL ANALİZ MOTORU
# ==============================================================
def analyze_stock(symbol, df, regression_period=60):
   required_columns = ["Open", "High", "Low", "Close", "Volume"]
 
   if df is None or df.empty or not all(c in df.columns for c in required_columns):
       return None
 
   df = df[required_columns].copy()
   df = df.replace([np.inf, -np.inf], np.nan).dropna()
   df = df[df["Volume"] > 0]
 
   minimum_rows = max(220, regression_period + 10)
   if len(df) < minimum_rows:
       return None
 
   close = df["Close"].astype(float)
   high = df["High"].astype(float)
   volume = df["Volume"].astype(float)
 
   last_close = float(close.iloc[-1])
   previous_close = float(close.iloc[-2])
   if last_close <= 0:
       return None
 
   rsi = calc_rsi(close, 14)
   rsi_value = float(rsi.iloc[-1])
   rsi_previous = float(rsi.iloc[-2])
   rsi_rising = rsi_value > rsi_previous
 
   ema20_series = calc_ema(close, 20)
   ema50_series = calc_ema(close, 50)
   ema200_series = calc_ema(close, 200)
 
   ema20 = float(ema20_series.iloc[-1])
   ema50 = float(ema50_series.iloc[-1])
   ema200 = float(ema200_series.iloc[-1])
   ema20_slope = normalized_slope(ema20_series, 10)
   ema50_slope = normalized_slope(ema50_series, 20)
 
   atr_value = float(calc_atr(df, 14).iloc[-1])
   if not np.isfinite(atr_value) or atr_value <= 0:
       atr_value = last_close * 0.02
   atr_pct = atr_value / last_close * 100
 
   adx, plus_di, minus_di = calc_adx(df, 14)
   adx_value = float(adx.iloc[-1])
   plus_di_value = float(plus_di.iloc[-1])
   minus_di_value = float(minus_di.iloc[-1])
 
   macd, macd_signal, macd_histogram = calc_macd(close)
   macd_bullish = bool(macd.iloc[-1] > macd_signal.iloc[-1])
   macd_accelerating = bool(macd_histogram.iloc[-1] > macd_histogram.iloc[-2])
   macd_fresh_cross = bool(
       macd.iloc[-1] > macd_signal.iloc[-1]
       and macd.iloc[-2] <= macd_signal.iloc[-2]
   )
 
   volume_ma20 = float(volume.rolling(20).mean().iloc[-1])
   volume_ratio = float(volume.iloc[-1] / volume_ma20) if volume_ma20 > 0 else 1.0
   volume_5_ratio = float(volume.tail(5).mean() / volume_ma20) if volume_ma20 > 0 else 1.0
   average_turnover_20 = float((close * volume).rolling(20).mean().iloc[-1])
 
   obv = calc_obv(df)
   obv_ema10 = calc_ema(obv, 10)
   obv_above_ema = bool(obv.iloc[-1] > obv_ema10.iloc[-1])
   obv_rising = normalized_slope(obv, 10) > 0
 
   regression = calc_regression_channel(close, regression_period, 2.0)
   if regression is None:
       return None
 
   regression_middle = regression["middle"]
   regression_upper = regression["upper"]
   regression_lower = regression["lower"]
   regression_slope_pct = regression["slope_pct"]
   regression_r2 = regression["r_squared"]
   channel_position = regression["position"]
 
   regression_up = regression_slope_pct > 0.03
   regression_strong_up = regression_slope_pct > 0.10 and regression_r2 >= 0.45
   channel_breakout = last_close > regression_upper and previous_close <= regression_upper
   near_upper_channel = 0.80 <= channel_position <= 1.05
   above_middle_channel = last_close > regression_middle
   below_lower_channel = last_close < regression_lower
 
   high_20_previous = float(high.shift(1).rolling(20).max().iloc[-1])
   high_55_previous = float(high.shift(1).rolling(55).max().iloc[-1])
   breakout_20 = last_close > high_20_previous
   breakout_55 = last_close > high_55_previous
 
   distance_from_ema20_pct = (last_close - ema20) / ema20 * 100 if ema20 > 0 else 0.0
   daily_change_pct = (last_close / previous_close - 1) * 100 if previous_close > 0 else 0.0
   momentum_5_pct = (last_close / float(close.iloc[-6]) - 1) * 100
   momentum_20_pct = (last_close / float(close.iloc[-21]) - 1) * 100
 
   primary_bull_trend = last_close > ema20 > ema50 > ema200
   medium_bull_trend = last_close > ema20 > ema50
   trend_slopes_positive = ema20_slope > 0 and ema50_slope > 0
   adx_bullish = adx_value >= 20 and plus_di_value > minus_di_value
   strong_adx_bullish = adx_value >= 25 and plus_di_value > minus_di_value
 
   trend_score = 0
   regression_score = 0
   momentum_score = 0
   volume_score = 0
   breakout_score = 0
   risk_penalty = 0
 
   if primary_bull_trend:
       trend_score += 12
   elif medium_bull_trend:
       trend_score += 8
   elif last_close > ema50:
       trend_score += 4
 
   if trend_slopes_positive:
       trend_score += 5
   if strong_adx_bullish:
       trend_score += 8
   elif adx_bullish:
       trend_score += 5
   trend_score = min(trend_score, 25)
 
   if regression_strong_up:
       regression_score += 9
   elif regression_up:
       regression_score += 5
   if regression_r2 >= 0.65:
       regression_score += 5
   elif regression_r2 >= 0.40:
       regression_score += 3
   if above_middle_channel:
       regression_score += 3
   if near_upper_channel:
       regression_score += 3
   regression_score = min(regression_score, 20)
 
   if 50 <= rsi_value <= 65 and rsi_rising:
       momentum_score += 7
   elif 45 <= rsi_value < 50 and rsi_rising:
       momentum_score += 5
   elif 50 <= rsi_value <= 70:
       momentum_score += 4
 
   if macd_fresh_cross:
       momentum_score += 6
   elif macd_bullish and macd_accelerating:
       momentum_score += 5
   elif macd_bullish:
       momentum_score += 3
 
   if momentum_5_pct > 0 and momentum_20_pct > 0:
       momentum_score += 4
   if 0 < daily_change_pct <= 7:
       momentum_score += 3
   momentum_score = min(momentum_score, 20)
 
   if 1.3 <= volume_ratio < 2.0:
       volume_score += 5
   elif 2.0 <= volume_ratio < 4.0:
       volume_score += 8
   elif volume_ratio >= 4.0:
       volume_score += 6
 
   if volume_5_ratio >= 1.15:
       volume_score += 3
   if obv_above_ema and obv_rising:
       volume_score += 4
   elif obv_above_ema:
       volume_score += 2
   volume_score = min(volume_score, 15)
 
   if breakout_55:
       breakout_score += 8
   elif breakout_20:
       breakout_score += 6
   if channel_breakout:
       breakout_score += 6
   if (breakout_20 or channel_breakout) and volume_ratio >= 1.5:
       breakout_score += 4
   if breakout_20 and macd_bullish and plus_di_value > minus_di_value:
       breakout_score += 2
   breakout_score = min(breakout_score, 20)
 
   if last_close < ema50:
       risk_penalty += 8
   if last_close < ema200:
       risk_penalty += 8
   if ema20_slope < 0:
       risk_penalty += 5
   if regression_slope_pct < 0:
       risk_penalty += 8
   if below_lower_channel:
       risk_penalty += 8
   if rsi_value >= 78:
       risk_penalty += 8
   elif rsi_value >= 72:
       risk_penalty += 4
   if distance_from_ema20_pct > max(12, atr_pct * 4):
       risk_penalty += 8
   elif distance_from_ema20_pct > max(8, atr_pct * 3):
       risk_penalty += 4
   if daily_change_pct > 9:
       risk_penalty += 5
   if average_turnover_20 < 5_000_000:
       risk_penalty += 8
   elif average_turnover_20 < 15_000_000:
       risk_penalty += 4
 
   raw_score = trend_score + regression_score + momentum_score + volume_score + breakout_score
   score = int(max(0, min(100, round(raw_score - risk_penalty))))
 
   confirmations = sum([
       primary_bull_trend,
       regression_up,
       adx_bullish,
       macd_bullish,
       obv_above_ema,
       volume_ratio >= 1.3,
       breakout_20 or channel_breakout
   ])
 
   if score >= 82 and confirmations >= 6 and regression_slope_pct > 0 and last_close > ema20:
       signal = "🔥 ÇOK GÜÇLÜ AL"
   elif score >= 70 and confirmations >= 5 and last_close > ema20:
       signal = "✅ GÜÇLÜ AL"
   elif score >= 55 and confirmations >= 4:
       signal = "🟡 TAKİP"
   elif last_close < ema50 and regression_slope_pct < 0 and minus_di_value > plus_di_value:
       signal = "🔻 SAT / UZAK DUR"
   else:
       signal = "⚪ ZAYIF"
 
   momentum_radar = 0
   if breakout_20:
       momentum_radar += 2
   if breakout_55:
       momentum_radar += 1
   if channel_breakout:
       momentum_radar += 2
   if 1.5 <= volume_ratio < 4:
       momentum_radar += 2
   elif volume_ratio >= 4:
       momentum_radar += 1
   if macd_fresh_cross or macd_accelerating:
       momentum_radar += 1
   if adx_value >= 25 and plus_di_value > minus_di_value:
       momentum_radar += 1
   if regression_strong_up:
       momentum_radar += 1
   if rsi_value > 75:
       momentum_radar -= 1
   momentum_radar = int(max(0, min(momentum_radar, 10)))
 
   if momentum_radar >= 8:
       momentum_status = "🔥 ÇOK GÜÇLÜ"
   elif momentum_radar >= 6:
       momentum_status = "🚀 GÜÇLÜ"
   elif momentum_radar >= 4:
       momentum_status = "🟡 ORTA"
   else:
       momentum_status = "⚪ ZAYIF"
 
   structural_stop = min(ema20, regression_middle, last_close - atr_value * 1.5)
   stop_loss = max(structural_stop, last_close - atr_value * 2.2)
   risk_per_share = last_close - stop_loss
 
   if risk_per_share <= 0:
       risk_per_share = atr_value * 1.5
       stop_loss = last_close - risk_per_share
 
   target_1 = last_close + risk_per_share * 1.5
   target_2 = last_close + risk_per_share * 2.5
   expected_pct = (target_1 - last_close) / last_close * 100
   risk_pct = (last_close - stop_loss) / last_close * 100
   risk_reward = (target_1 - last_close) / risk_per_share if risk_per_share > 0 else 0.0
 
   if primary_bull_trend and strong_adx_bullish:
       trend_text = "Güçlü"
   elif medium_bull_trend or regression_up:
       trend_text = "Pozitif"
   elif last_close < ema50 and regression_slope_pct < 0:
       trend_text = "Negatif"
   else:
       trend_text = "Kararsız"
 
   if channel_position > 1:
       channel_text = "Üst Kanal Üzeri"
   elif channel_position >= 0.75:
       channel_text = "Üst Bölge"
   elif channel_position >= 0.45:
       channel_text = "Orta Bölge"
   elif channel_position >= 0:
       channel_text = "Alt Bölge"
   else:
       channel_text = "Alt Kanal Altı"
 
   return {
       "Sembol": symbol,
       "Fiyat": round(last_close, 2),
       "Sinyal": signal,
       "Skor": score,
       "Onay": confirmations,
       "Momentum Puanı": momentum_radar,
       "Momentum Durumu": momentum_status,
       "Trend Puanı": trend_score,
       "Regresyon Puanı": regression_score,
       "Momentum Alt Puan": momentum_score,
       "Hacim Puanı": volume_score,
       "Kırılım Puanı": breakout_score,
       "Risk Cezası": risk_penalty,
       "RSI": round(rsi_value, 2),
       "ADX": round(adx_value, 2),
       "+DI": round(plus_di_value, 2),
       "-DI": round(minus_di_value, 2),
       "Hacim x": round(volume_ratio, 2),
       "5G Hacim x": round(volume_5_ratio, 2),
       "MACD": "Yeni AL" if macd_fresh_cross else "Pozitif" if macd_bullish else "Negatif",
       "OBV": "Güçlü" if obv_above_ema and obv_rising else "Pozitif" if obv_above_ema else "Zayıf",
       "Trend": trend_text,
       "Kırılım": "55 Gün" if breakout_55 else "20 Gün" if breakout_20 else "Regresyon" if channel_breakout else "Yok",
       "Reg. Eğim %": round(regression_slope_pct, 3),
       "Reg. R²": round(regression_r2, 3),
       "Kanal Konumu": channel_text,
       "Kanal Pozisyon": round(channel_position, 2),
       "Reg. Alt": round(regression_lower, 2),
       "Reg. Orta": round(regression_middle, 2),
       "Reg. Üst": round(regression_upper, 2),
       "EMA20": round(ema20, 2),
       "EMA50": round(ema50, 2),
       "EMA200": round(ema200, 2),
       "5G Momentum %": round(momentum_5_pct, 2),
       "20G Momentum %": round(momentum_20_pct, 2),
       "ATR %": round(atr_pct, 2),
       "Hedef 1": round(target_1, 2),
       "Hedef 2": round(target_2, 2),
       "Stop": round(stop_loss, 2),
       "Beklenti %": round(expected_pct, 2),
       "Risk %": round(risk_pct, 2),
       "Risk/Getiri": round(risk_reward, 2),
       "Ort. İşlem TL": round(average_turnover_20, 0)
   }
 
 
# ==============================================================
# BACKTEST MOTORU
# ==============================================================
def calculate_forward_result(future_df, entry_price, target_price, stop_price, horizon):
   if future_df is None or future_df.empty:
       return None
 
   test_df = future_df.iloc[:horizon].copy()
   if len(test_df) < horizon:
       return None
 
   exit_close = float(test_df["Close"].iloc[-1])
   future_high = float(test_df["High"].max())
   future_low = float(test_df["Low"].min())
 
   close_return_pct = (exit_close / entry_price - 1) * 100
   max_gain_pct = (future_high / entry_price - 1) * 100
   max_drawdown_pct = (future_low / entry_price - 1) * 100
 
   target_hit_day = None
   stop_hit_day = None
 
   for day_number, (_, row) in enumerate(test_df.iterrows(), start=1):
       if target_hit_day is None and float(row["High"]) >= target_price:
           target_hit_day = day_number
       if stop_hit_day is None and float(row["Low"]) <= stop_price:
           stop_hit_day = day_number
 
   target_hit = target_hit_day is not None
   stop_hit = stop_hit_day is not None
 
   if target_hit and stop_hit:
       outcome = "STOP" if stop_hit_day <= target_hit_day else "HEDEF"
   elif target_hit:
       outcome = "HEDEF"
   elif stop_hit:
       outcome = "STOP"
   elif close_return_pct > 0:
       outcome = "POZİTİF"
   else:
       outcome = "NEGATİF"
 
   return {
       "Getiri %": round(close_return_pct, 2),
       "Maks. Kazanç %": round(max_gain_pct, 2),
       "Maks. Düşüş %": round(max_drawdown_pct, 2),
       "Hedef Oldu": target_hit,
       "Stop Oldu": stop_hit,
       "Hedef Günü": target_hit_day,
       "Stop Günü": stop_hit_day,
       "Sonuç": outcome
   }
 
 
def backtest_stock(
   symbol,
   df,
   regression_period=60,
   minimum_score=55,
   allowed_signals=None,
   forward_days=(1, 3, 5, 10),
   minimum_gap=5,
   step_size=1,
   warmup_bars=220
):
   if allowed_signals is None:
       allowed_signals = ["🔥 ÇOK GÜÇLÜ AL", "✅ GÜÇLÜ AL", "🟡 TAKİP"]
 
   if df is None or df.empty:
       return pd.DataFrame()
 
   df = df.copy().replace([np.inf, -np.inf], np.nan).dropna()
   required_columns = ["Open", "High", "Low", "Close", "Volume"]
   if not all(column in df.columns for column in required_columns):
       return pd.DataFrame()
 
   maximum_forward = max(forward_days)
   if len(df) < warmup_bars + maximum_forward + 1:
       return pd.DataFrame()
 
   records = []
   last_signal_index = -minimum_gap - 1
   final_test_index = len(df) - maximum_forward
 
   for current_index in range(warmup_bars, final_test_index, step_size):
       historical_df = df.iloc[:current_index + 1].copy()
 
       try:
           analysis = analyze_stock(symbol, historical_df, regression_period)
       except Exception:
           continue
 
       if analysis is None:
           continue
 
       signal = analysis.get("Sinyal", "⚪ ZAYIF")
       score = analysis.get("Skor", 0)
 
       if signal not in allowed_signals or score < minimum_score:
           continue
       if current_index - last_signal_index < minimum_gap:
           continue
 
       signal_date = df.index[current_index]
       entry_price = float(df["Close"].iloc[current_index])
       target_1 = float(analysis["Hedef 1"])
       target_2 = float(analysis["Hedef 2"])
       stop_price = float(analysis["Stop"])
 
       future_df = df.iloc[
           current_index + 1:current_index + 1 + maximum_forward
       ].copy()
 
       record = {
           "Sembol": symbol,
           "Sinyal Tarihi": signal_date,
           "Giriş Fiyatı": round(entry_price, 2),
           "Sinyal": signal,
           "Skor": score,
           "Onay": analysis.get("Onay", 0),
           "Momentum Puanı": analysis.get("Momentum Puanı", 0),
           "Trend Puanı": analysis.get("Trend Puanı", 0),
           "Regresyon Puanı": analysis.get("Regresyon Puanı", 0),
           "Risk Cezası": analysis.get("Risk Cezası", 0),
           "RSI": analysis.get("RSI", np.nan),
           "ADX": analysis.get("ADX", np.nan),
           "Hacim x": analysis.get("Hacim x", np.nan),
           "Reg. Eğim %": analysis.get("Reg. Eğim %", np.nan),
           "Reg. R²": analysis.get("Reg. R²", np.nan),
           "Kanal Pozisyon": analysis.get("Kanal Pozisyon", np.nan),
           "Kırılım": analysis.get("Kırılım", "Yok"),
           "Hedef 1": round(target_1, 2),
           "Hedef 2": round(target_2, 2),
           "Stop": round(stop_price, 2),
           "Risk %": analysis.get("Risk %", np.nan)
       }
 
       valid_record = True
       for horizon in forward_days:
           result = calculate_forward_result(
               future_df,
               entry_price,
               target_1,
               stop_price,
               horizon
           )
           if result is None:
               valid_record = False
               break
 
           record[f"{horizon}G Getiri %"] = result["Getiri %"]
           record[f"{horizon}G Maks. Kazanç %"] = result["Maks. Kazanç %"]
           record[f"{horizon}G Maks. Düşüş %"] = result["Maks. Düşüş %"]
           record[f"{horizon}G Hedef"] = result["Hedef Oldu"]
           record[f"{horizon}G Stop"] = result["Stop Oldu"]
           record[f"{horizon}G Sonuç"] = result["Sonuç"]
 
       if valid_record:
           records.append(record)
           last_signal_index = current_index
 
   return pd.DataFrame(records)
 
 
def run_backtest_engine(
   symbols,
   regression_period=60,
   minimum_score=55,
   allowed_signals=None,
   forward_days=(1, 3, 5, 10),
   minimum_gap=5,
   step_size=1,
   data_period="5y",
   progress_callback=None
):
   all_results = []
   failed_symbols = []
   total_symbols = len(symbols)
 
   for index, symbol in enumerate(symbols):
       try:
           df = yf.Ticker(symbol + ".IS").history(
               period=data_period,
               interval="1d",
               auto_adjust=True,
               repair=True
           )
 
           required_columns = ["Open", "High", "Low", "Close", "Volume"]
           if df is None or df.empty or not all(c in df.columns for c in required_columns):
               failed_symbols.append(symbol)
               continue
 
           df = df[required_columns].copy()
           df = df.replace([np.inf, -np.inf], np.nan).dropna()
           df = df[df["Volume"] > 0]
 
           symbol_results = backtest_stock(
               symbol=symbol,
               df=df,
               regression_period=regression_period,
               minimum_score=minimum_score,
               allowed_signals=allowed_signals,
               forward_days=forward_days,
               minimum_gap=minimum_gap,
               step_size=step_size,
               warmup_bars=220
           )
 
           if not symbol_results.empty:
               all_results.append(symbol_results)
       except Exception:
           failed_symbols.append(symbol)
 
       if progress_callback is not None:
           progress_callback(index + 1, total_symbols, symbol)
 
   combined = pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()
   return combined, failed_symbols
 
 
def calculate_profit_factor(returns):
   returns = pd.to_numeric(returns, errors="coerce").dropna()
   gross_profit = returns[returns > 0].sum()
   gross_loss = abs(returns[returns < 0].sum())
 
   if gross_loss == 0:
       return float("inf") if gross_profit > 0 else 0.0
   return float(gross_profit / gross_loss)
 
 
def summarize_backtest(results, forward_days=(1, 3, 5, 10)):
   if results is None or results.empty:
       return pd.DataFrame()
 
   rows = []
   for horizon in forward_days:
       return_column = f"{horizon}G Getiri %"
       max_gain_column = f"{horizon}G Maks. Kazanç %"
       drawdown_column = f"{horizon}G Maks. Düşüş %"
       target_column = f"{horizon}G Hedef"
       stop_column = f"{horizon}G Stop"
 
       if return_column not in results.columns:
           continue
 
       returns = pd.to_numeric(results[return_column], errors="coerce").dropna()
       if returns.empty:
           continue
 
       rows.append({
           "Süre": f"{horizon} Gün",
           "Sinyal Sayısı": len(returns),
           "Pozitif Oran %": round((returns > 0).mean() * 100, 2),
           "En Az %3 Kazanç": round((returns >= 3).mean() * 100, 2),
           "Ortalama Getiri %": round(returns.mean(), 2),
           "Medyan Getiri %": round(returns.median(), 2),
           "Maksimum Getiri %": round(returns.max(), 2),
           "Maksimum Kayıp %": round(returns.min(), 2),
           "Ort. Maks. Yükseliş %": round(results[max_gain_column].mean(), 2),
           "Ort. Maks. Düşüş %": round(results[drawdown_column].mean(), 2),
           "Hedef Oranı %": round(results[target_column].fillna(False).mean() * 100, 2),
           "Stop Oranı %": round(results[stop_column].fillna(False).mean() * 100, 2),
           "Profit Factor": round(calculate_profit_factor(returns), 2)
       })
 
   return pd.DataFrame(rows)
 
 
def summarize_by_signal(results, horizon=5):
   if results is None or results.empty:
       return pd.DataFrame()
 
   return_column = f"{horizon}G Getiri %"
   target_column = f"{horizon}G Hedef"
   stop_column = f"{horizon}G Stop"
   rows = []
 
   for signal, group in results.groupby("Sinyal"):
       returns = pd.to_numeric(group[return_column], errors="coerce").dropna()
       if returns.empty:
           continue
 
       rows.append({
           "Sinyal": signal,
           "Sinyal Sayısı": len(returns),
           "Başarı Oranı %": round((returns > 0).mean() * 100, 2),
           "Ortalama Getiri %": round(returns.mean(), 2),
           "Medyan Getiri %": round(returns.median(), 2),
           "Hedef Oranı %": round(group[target_column].fillna(False).mean() * 100, 2),
           "Stop Oranı %": round(group[stop_column].fillna(False).mean() * 100, 2),
           "Profit Factor": round(calculate_profit_factor(returns), 2)
       })
 
   summary = pd.DataFrame(rows)
   return summary.sort_values("Ortalama Getiri %", ascending=False) if not summary.empty else summary
 
 
def summarize_by_score_range(results, horizon=5):
   if results is None or results.empty:
       return pd.DataFrame()
 
   return_column = f"{horizon}G Getiri %"
   score_bins = [0, 54, 64, 69, 74, 79, 84, 89, 100]
   score_labels = ["0-54", "55-64", "65-69", "70-74", "75-79", "80-84", "85-89", "90-100"]
 
   test_data = results.copy()
   test_data["Skor Aralığı"] = pd.cut(
       test_data["Skor"],
       bins=score_bins,
       labels=score_labels,
       include_lowest=True
   )
 
   rows = []
   for score_range, group in test_data.groupby("Skor Aralığı", observed=True):
       returns = pd.to_numeric(group[return_column], errors="coerce").dropna()
       if returns.empty:
           continue
 
       rows.append({
           "Skor Aralığı": str(score_range),
           "Sinyal Sayısı": len(returns),
           "Başarı Oranı %": round((returns > 0).mean() * 100, 2),
           "Ortalama Getiri %": round(returns.mean(), 2),
           "Medyan Getiri %": round(returns.median(), 2),
           "Profit Factor": round(calculate_profit_factor(returns), 2)
       })
 
   return pd.DataFrame(rows)
 
 
def summarize_by_symbol(results, horizon=5):
   if results is None or results.empty:
       return pd.DataFrame()
 
   return_column = f"{horizon}G Getiri %"
   rows = []
 
   for symbol, group in results.groupby("Sembol"):
       returns = pd.to_numeric(group[return_column], errors="coerce").dropna()
       if returns.empty:
           continue
 
       rows.append({
           "Sembol": symbol,
           "Sinyal Sayısı": len(returns),
           "Başarı Oranı %": round((returns > 0).mean() * 100, 2),
           "Ortalama Getiri %": round(returns.mean(), 2),
           "Medyan Getiri %": round(returns.median(), 2),
           "En İyi %": round(returns.max(), 2),
           "En Kötü %": round(returns.min(), 2),
           "Profit Factor": round(calculate_profit_factor(returns), 2)
       })
 
   summary = pd.DataFrame(rows)
   if not summary.empty:
       summary = summary.sort_values(
           ["Ortalama Getiri %", "Başarı Oranı %"],
           ascending=False
       )
   return summary
 
 
# ==============================================================
# UYGULAMA ARAYÜZÜ
# ==============================================================
symbols = get_bist_symbols()
app_mode = st.sidebar.radio("Çalışma Modu", ["🔍 Güncel Radar", "🧪 Backtest Motoru"])
 
if app_mode == "🔍 Güncel Radar":
   with st.sidebar:
       st.header("⚙️ Radar Ayarları")
       st.info(f"Bulunan sembol sayısı: {len(symbols)}")
 
       scan_count = st.slider(
           "Taranacak hisse sayısı",
           min_value=10,
           max_value=len(symbols),
           value=min(100, len(symbols)),
           step=10
       )
 
       period = st.selectbox("Gösterim periyodu", ["3mo", "6mo", "1y"], index=1)
       regression_period = st.select_slider(
           "Regresyon kanal periyodu",
           options=[20, 30, 45, 60, 90, 120],
           value=60
       )
       min_score = st.slider("Minimum skor filtresi", 0, 100, 0, 5)
       minimum_turnover = st.number_input(
           "Minimum 20 günlük ortalama işlem hacmi (TL)",
           min_value=0,
           value=10_000_000,
           step=5_000_000
       )
       minimum_r2 = st.slider("Minimum regresyon R²", 0.0, 1.0, 0.0, 0.05)
       only_buy = st.checkbox("Sadece AL / TAKİP sinyalleri", value=False)
       run_scan = st.button("🔍 BIST RADAR TARAMASINI BAŞLAT", use_container_width=True)
 
   col1, col2, col3, col4 = st.columns(4)
   col1.metric("📋 Sembol", len(symbols))
   col2.metric("📊 Periyot", period)
   col3.metric("🎯 Min Skor", min_score)
   col4.metric("🔍 Tarama", scan_count)
   st.divider()
 
   if run_scan:
       selected_symbols = symbols[:scan_count]
       results = []
       progress = st.progress(0)
       status = st.empty()
       start_time = time.time()
 
       for i, symbol in enumerate(selected_symbols):
           status.write(f"⏳ {symbol} taranıyor...")
           df = get_stock_data(symbol, period)
 
           if df is not None:
               try:
                   result = analyze_stock(symbol, df, regression_period)
                   if result is not None:
                       results.append(result)
               except Exception:
                   pass
 
           progress.progress((i + 1) / len(selected_symbols))
 
       elapsed = time.time() - start_time
       status.write("✅ Tarama tamamlandı.")
 
       if results:
           data = pd.DataFrame(results).sort_values("Skor", ascending=False)
           data = data[data["Skor"] >= min_score]
           data = data[data["Ort. İşlem TL"] >= minimum_turnover]
           data = data[data["Reg. R²"] >= minimum_r2]
 
           if only_buy:
               data = data[data["Sinyal"].isin([
                   "🔥 ÇOK GÜÇLÜ AL",
                   "✅ GÜÇLÜ AL",
                   "🟡 TAKİP"
               ])]
 
           st.success(
               f"Tarama tamamlandı. Süre: {elapsed:.1f} saniye | Sonuç: {len(data)} hisse"
           )
 
           m1, m2, m3, m4 = st.columns(4)
           m1.metric("🔥 En Yüksek Skor", int(data["Skor"].max()) if len(data) else 0)
           m2.metric("✅ AL Sinyali", len(data[data["Skor"] >= 70]))
           m3.metric("🔥 Çok Güçlü AL", len(data[data["Skor"] >= 82]))
           m4.metric("🚀 Momentum Adayı", len(data[data["Momentum Puanı"] >= 7]))
 
           st.subheader("🔥 En Güçlü Radar Sonuçları")
           st.dataframe(data, use_container_width=True, hide_index=True)
 
           st.subheader("🚀 Güçlü Momentum ve Kırılım Radar")
           momentum_candidates = data[
               (data["Momentum Puanı"] >= 7)
               & (data["Skor"] >= 65)
               & (data["Reg. Eğim %"] > 0)
               & (data["Hacim x"] >= 1.3)
           ]
 
           if len(momentum_candidates):
               st.dataframe(momentum_candidates, use_container_width=True, hide_index=True)
           else:
               st.warning("Şu an güçlü momentum ve kırılım adayı bulunamadı.")
 
           st.subheader("✅ Güçlü AL Listesi")
           strong_buy = data[data["Skor"] >= 70]
           if len(strong_buy):
               st.dataframe(strong_buy, use_container_width=True, hide_index=True)
           else:
               st.warning("Güçlü AL sinyali bulunamadı.")
 
           csv = data.to_csv(index=False).encode("utf-8-sig")
           st.download_button(
               "📥 Sonuçları CSV indir",
               data=csv,
               file_name=f"borsa_radar_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
               mime="text/csv",
               use_container_width=True
           )
       else:
           st.error("Veri alınamadı veya sonuç üretilemedi.")
   else:
       st.warning("Sol menüden ayarları seçip tarama butonuna bas.")
 
elif app_mode == "🧪 Backtest Motoru":
   st.header("🧪 Borsa Radar Backtest Motoru")
 
   with st.sidebar:
       st.header("🧪 Backtest Ayarları")
       backtest_symbol_count = st.slider(
           "Test edilecek hisse sayısı",
           min_value=1,
           max_value=min(len(symbols), 100),
           value=min(10, len(symbols)),
           step=1
       )
       backtest_period = st.selectbox("Geçmiş veri süresi", ["2y", "5y", "10y"], index=1)
       backtest_regression_period = st.select_slider(
           "Regresyon periyodu",
           options=[20, 30, 45, 60, 90, 120],
           value=60
       )
       backtest_min_score = st.slider("Minimum sinyal skoru", 40, 95, 60, 5)
       selected_signal_types = st.multiselect(
           "Test edilecek sinyaller",
           ["🔥 ÇOK GÜÇLÜ AL", "✅ GÜÇLÜ AL", "🟡 TAKİP"],
           default=["🔥 ÇOK GÜÇLÜ AL", "✅ GÜÇLÜ AL"]
       )
       signal_gap = st.slider("Aynı hissede sinyaller arası gün", 1, 30, 5, 1)
       test_step = st.selectbox(
           "Test sıklığı",
           options=[1, 2, 3, 5],
           index=0,
           format_func=lambda value: "Her işlem günü" if value == 1 else f"Her {value} işlem gününde"
       )
       selected_horizon = st.selectbox("Ana değerlendirme süresi", [1, 3, 5, 10], index=2)
       run_backtest = st.button("🧪 BACKTEST BAŞLAT", use_container_width=True)
 
   bt1, bt2, bt3, bt4 = st.columns(4)
   bt1.metric("Hisse Sayısı", backtest_symbol_count)
   bt2.metric("Geçmiş", backtest_period)
   bt3.metric("Minimum Skor", backtest_min_score)
   bt4.metric("Regresyon", backtest_regression_period)
 
   st.warning(
       "Backtest geçmiş performansı ölçer. Gelecekte aynı sonucun oluşacağını garanti etmez."
   )
 
   if run_backtest:
       if not selected_signal_types:
           st.error("En az bir sinyal türü seçmelisin.")
           st.stop()
 
       # Alfabetik ilk hisseler yerine liste boyunca dengeli örnekleme
       step = max(1, len(symbols) // backtest_symbol_count)
       selected_backtest_symbols = symbols[::step][:backtest_symbol_count]
 
       progress_bar = st.progress(0)
       progress_text = st.empty()
 
       def update_backtest_progress(completed, total, current_symbol):
           progress_bar.progress(completed / total)
           progress_text.write(f"⏳ {current_symbol} test ediliyor... {completed}/{total}")
 
       start_time = time.time()
       backtest_results, failed_symbols = run_backtest_engine(
           symbols=selected_backtest_symbols,
           regression_period=backtest_regression_period,
           minimum_score=backtest_min_score,
           allowed_signals=selected_signal_types,
           forward_days=(1, 3, 5, 10),
           minimum_gap=signal_gap,
           step_size=test_step,
           data_period=backtest_period,
           progress_callback=update_backtest_progress
       )
       elapsed = time.time() - start_time
 
       progress_bar.progress(1.0)
       progress_text.write("✅ Backtest tamamlandı.")
 
       if backtest_results.empty:
           st.error("Seçilen koşullara uygun geçmiş sinyal bulunamadı.")
       else:
           st.success(
               f"Backtest tamamlandı. Süre: {elapsed:.1f} saniye | Sinyal: {len(backtest_results)}"
           )
 
           main_return_column = f"{selected_horizon}G Getiri %"
           main_returns = pd.to_numeric(
               backtest_results[main_return_column],
               errors="coerce"
           ).dropna()
 
           positive_rate = (main_returns > 0).mean() * 100 if len(main_returns) else 0
           average_return = main_returns.mean() if len(main_returns) else 0
           profit_factor = calculate_profit_factor(main_returns)
 
           metric1, metric2, metric3, metric4 = st.columns(4)
           metric1.metric("Toplam Sinyal", len(backtest_results))
           metric2.metric(f"{selected_horizon}G Başarı", f"%{positive_rate:.1f}")
           metric3.metric(f"{selected_horizon}G Ort. Getiri", f"%{average_return:.2f}")
           metric4.metric("Profit Factor", "∞" if np.isinf(profit_factor) else f"{profit_factor:.2f}")
 
           st.subheader("📊 Genel Backtest Özeti")
           st.dataframe(
               summarize_backtest(backtest_results),
               use_container_width=True,
               hide_index=True
           )
 
           st.subheader(f"🔥 Sinyal Türü Performansı ({selected_horizon} Gün)")
           st.dataframe(
               summarize_by_signal(backtest_results, selected_horizon),
               use_container_width=True,
               hide_index=True
           )
 
           st.subheader(f"🎯 Skor Aralığı Performansı ({selected_horizon} Gün)")
           st.dataframe(
               summarize_by_score_range(backtest_results, selected_horizon),
               use_container_width=True,
               hide_index=True
           )
 
           st.subheader(f"🏢 Hisse Bazlı Performans ({selected_horizon} Gün)")
           st.dataframe(
               summarize_by_symbol(backtest_results, selected_horizon),
               use_container_width=True,
               hide_index=True
           )
 
           st.subheader("📋 Tüm Geçmiş Sinyaller")
           displayed_results = backtest_results.sort_values("Sinyal Tarihi", ascending=False)
           st.dataframe(displayed_results, use_container_width=True, hide_index=True)
 
           backtest_csv = backtest_results.to_csv(index=False).encode("utf-8-sig")
           st.download_button(
               "📥 Backtest sonuçlarını CSV indir",
               data=backtest_csv,
               file_name=f"borsa_radar_backtest_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
               mime="text/csv",
               use_container_width=True
           )
 
           if failed_symbols:
               with st.expander("⚠️ Verisi alınamayan hisseler"):
                   st.write(", ".join(failed_symbols))
 
st.divider()
st.caption(
   "⚠️ Bu uygulama yatırım tavsiyesi değildir. Eğitim, teknik analiz ve geçmiş performans testi amaçlıdır."
)
Borsa Radar V2 - Eğitim ve teknik analiz amaçlıdır.
