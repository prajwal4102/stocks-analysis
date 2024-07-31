import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pandas_ta as ta
from backtesting import Strategy, Backtest

def simplified_strategy( sym):
    def get_data(symbol:str):
        data=yf.download(tickers=symbol,period='1000d',interval='1d')
        data.reset_index(inplace=True)
        return data

    #get the data
    data=get_data(sym)
    data=data[:]
    print(type(data.index))
    print(data.index)
    def identify_rejection(data):
        # Create a new column for shooting star
        data['rejection'] = data.apply(lambda row: 2 if (
            ( (min(row['Open'], row['Close']) - row['Low']) > (1.5 * abs(row['Close'] - row['Open']))) and 
            (row['High'] - max(row['Close'], row['Open'])) < (0.8 * abs(row['Close'] - row['Open'])) and 
            (abs(row['Open'] - row['Close']) > row['Open'] * 0.001)
        ) else 1 if (
            (row['High'] - max(row['Open'], row['Close'])) > (1.5 * abs(row['Open'] - row['Close'])) and 
            (min(row['Close'], row['Open']) - row['Low']) < (0.8 * abs(row['Open'] - row['Close'])) and 
            (abs(row['Open'] - row['Close']) > row['Open'] * 0.001)
        ) else 0, axis=1)

        return data

    data = identify_rejection(data)

    #plot the points 
    def pointpos(x,xsignal):
        if x[xsignal]==1:
            return x['High']+1e-4
        elif x[xsignal]==2:
            return x['Low']-1e-4
        else:return np.nan

    def plot_with_signal(dfpl):
        fig=go.Figure(data=[go.Candlestick(x=dfpl.index,
                                        open=dfpl['Open'],
                                        high=dfpl['High'],
                                        low=dfpl['Low'],
                                        close=dfpl['Close'])])
        fig.update_layout(
            autosize=False,
            width=1200,
            height=800,
            plot_bgcolor='black'
        )
        fig.update_xaxes(gridcolor='black')
        fig.update_yaxes(gridcolor='black')
        fig.add_scatter(
            x=dfpl.index,y=dfpl['pointpos'],mode="markers",marker=dict(size=8,color="MediumPurple"),name="Signal"
        )
        fig.show()



    #define support and resistance
    def support(df1, l, n1, n2): #n1 n2 before and after candle l
        if ( df1.Low[l-n1:l].min() < df1.Low[l] or
            df1.Low[l+1:l+n2+1].min() < df1.Low[l] ):
            return 0
        return 1

    def resistance(df1, l, n1, n2): #n1 n2 before and after candle l
        if ( df1.High[l-n1:l].max() > df1.High[l] or
        df1.High[l+1:l+n2+1].max() > df1.High[l] ):
            return 0
        return 1

    def closeResistance(l, levels, lim, df):
        if len(levels) == 0:
            return 0
        c1 = abs(df['High'][l] - min(levels, key=lambda x: abs(x - df['High'][l]))) <= lim
        c2 = abs(max(df['Open'][l], df['Close'][l]) - min(levels, key=lambda x: abs(x - df['High'][l]))) <= lim
        c3 = min(df['Open'][l], df['Close'][l]) < min(levels, key=lambda x: abs(x - df['High'][l]))
        c4 = df['Low'][l] < min(levels, key=lambda x: abs(x - df['High'][l]))
        if (c1 or c2) and c3 and c4:
            return min(levels, key=lambda x: abs(x - df['High'][l]))
        else:
            return 0

    def closeSupport(l, levels, lim, df):
        if len(levels) == 0:
            return 0
        c1 = abs(df['Low'][l] - min(levels, key=lambda x: abs(x - df['Low'][l]))) <= lim
        c2 = abs(min(df['Open'][l], df['Close'][l]) - min(levels, key=lambda x: abs(x - df['Low'][l]))) <= lim
        c3 = max(df['Open'][l], df['Close'][l]) > min(levels, key=lambda x: abs(x - df['Low'][l]))
        c4 = df['High'][l] > min(levels, key=lambda x: abs(x - df['Low'][l]))
        if (c1 or c2) and c3 and c4:
            return min(levels, key=lambda x: abs(x - df['Low'][l]))
        else:
            return 0

    def is_below_resistance(l, level_backCandles, level, df):
        return df.loc[l-level_backCandles:l-1, 'High'].max() < level

    def is_above_support(l, level_backCandles, level, df):
        return df.loc[l-level_backCandles:l-1, 'Low'].min() > level


    def check_candle_signal(l, n1, n2, levelbackCandles, windowbackCandles, df):
        ss = []
        rr = []
        for subrow in range(l-levelbackCandles, l-n2+1):
            if support(df, subrow, n1, n2):
                ss.append(df.Low[subrow])
            if resistance(df, subrow, n1, n2):
                rr.append(df.High[subrow])

        ss.sort() #keep lowest support when popping a level
        for i in range(1,len(ss)):
            if(i>=len(ss)):
                break
            if abs(ss[i]-ss[i-1])/ss[i]<=0.001: # merging close distance levels
                ss.pop(i)

        rr.sort(reverse=True) # keep highest resistance when popping one
        for i in range(1,len(rr)):
            if(i>=len(rr)):
                break
            if abs(rr[i]-rr[i-1])/rr[i]<=0.001: # merging close distance levels
                rr.pop(i)


        rrss = rr+ss
        rrss.sort()
        for i in range(1,len(rrss)):
            if(i>=len(rrss)):
                break
            if abs(rrss[i]-rrss[i-1])/rrss[i]<=0.001: # merging close distance levels
                rrss.pop(i)
        cR = closeResistance(l, rrss, df.Close[l]*0.003, df)
        cS = closeSupport(l, rrss, df.Close[l]*0.003, df)

        if (df.rejection[l] == 1 and cR and is_below_resistance(l,windowbackCandles,cR, df)):
            return 1
        elif(df.rejection[l] == 2 and cS and is_above_support(l,windowbackCandles,cS, df)):
            return 2
        else:
            return 0

    from tqdm import tqdm

    n1 = 8
    n2 = 8
    levelbackCandles = 60
    windowbackCandles = n2

    signal = [0 for i in range(len(data))]

    for row in tqdm(range(levelbackCandles+n1, len(data)-n2)):
        signal[row] = check_candle_signal(row, n1, n2, levelbackCandles, windowbackCandles, data)

    data["signal"] = signal


    data['pointpos']=data.apply(lambda row: pointpos(row,"signal"),axis=1)

    data.set_index("Date", inplace=True)
    data['ATR'] = ta.atr(high=data.High, low=data.Low, close=data.Close, length=14)
    data['RSI'] = ta.rsi(data.Close, length=5)

    def SIGNAL():
        return data.signal


    # Trader fixed SL and TP
    from backtesting import Strategy, Backtest
    class MyCandlesStrat(Strategy):  
        def init(self):
            super().init()
            self.signal1 = self.I(SIGNAL)
            self.ratio = 2
            self.risk_perc = 0.1

        def next(self):
            super().next() 
            if self.signal1==2:
                sl1 = self.data.Close[-1] - self.data.Close[-1]*self.risk_perc
                tp1 = self.data.Close[-1] + (self.data.Close[-1]*self.risk_perc)*self.ratio
                self.buy(sl=sl1, tp=tp1)
            elif self.signal1==1:
                sl1 = self.data.Close[-1] + self.data.Close[-1]*self.risk_perc
                tp1 = self.data.Close[-1] - (self.data.Close[-1]*self.risk_perc)*self.ratio
                self.sell(sl=sl1, tp=tp1)


    bt = Backtest(data, MyCandlesStrat, cash=100_000, commission=.000)
    stat = bt.run()
    print(stat)
    bt.plot()
    print(data[data['signal']!=0])
    data['pointpos']=data.apply(lambda row:pointpos(row,'signal'),axis=1)
    plot_with_signal(data)

import gradio as gr

# Gradio interface
iface = gr.Interface(fn=simplified_strategy,
                     inputs=[gr.Text(label="STOCK SYMBOL")],
                     outputs=gr.Plot(),
                     title="Fintelligence Fusion",

                     description="Please enter the stock you want to analyze with support and resistance strategy")

# Launch the interface
iface.launch()
