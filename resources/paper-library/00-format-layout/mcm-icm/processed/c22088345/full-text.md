# C22088345.pdf 可检索文本

> 本文件由原 PDF 自动提取，仅用于检索和定位；公式、表格与版式以原 PDF 或对应页图为准。

- 源文件：`../../C22088345.pdf`
- SHA-256：`7161D7DBA97E75A3FF224F4773F3B5E4C1ED97A956C5C34C169CF907DC245124`
- 页数：25

## 第 001 页

[查看原页版式](pages/page-001.jpg)

~~~~text
Problem Chosen
C
2022
MCM/ICM
Summary Sheet
Team Control Number
2208834
An Improved Pairs Trading Strategy Based on
Cointegration of Gold and Bitcoin
Summary
As a traditional investment, gold is often seen as a safe haven asset with stable returns due to
its commodity nature, while bitcoin is seen as an emerging trading asset with high volatility and
more arbitrage opportunities. The purpose of this report is to establish a trading model for gold
and bitcoin that uses price data up to the day to provide the best investment return. We provide a
pairs trading strategy that outperforms all other strategies and is robust and has lower risk.
In order to get the best trading strategy, we ﬁrstly observe the pre-processed and normalized
data, and ﬁnd that there is a cointegration relationship between them. Secondly, we process the
data using the Modiﬁed Dollar Neutral strategy (MDN), which is an improvement of the pairs
trading.By using MDN, we predict the data and make a buying and selling decision. Finally, we
conduct a backtest using the data of the last ﬁve years, and the results show that after continuous
trading and asset transformation using the pairs trading strategy, the $1,000 on September 10, 2016
turn into $106,986.1 on September 10, 2021, with a nearly 107 times year-on-year increase in net
asset value and a huge return rate.
For the purpose of proving that our strategy is the best strategy, we compare the pairs trading
strategy with random trading strategy and machine learning strategy LSTM and XGBoost respec-
tively. The results show that the Sharpe ratio of pairs trading strategy is 1.53-2.32 times that
of other trading strategies, excess return is 1.49-3.17 times that of other trading strategies, and
geometric return is 1.63-3.25 times that of other trading strategies, indicating that pairs trading
strategy has higher proﬁtability and lower risk.
Then, we analyze the sensitivity of this strategy to transaction costs. The results show that: i.
There is a negative exponential relationship between transaction cost and return. When the
transaction cost is 0, the theoretical return can reach $120000. ii. Transaction cost is positively
correlated with the number of transactions. When the commission ratio is 0.5%, the total return
will approach 0 after 500 simulated transactions. The experimental results are in good agreement
with our mathematical derivation.
In addition, we consider the impact of market risk on trading strategy. We divide the market
risk into price risk and reinvestment risk. Then we emphatically explore the non-investable
interval highly related to transaction cost under the reinvestment risk, and then set parameters:
risk aversion coeﬃcient (λ) is used to discuss the impact of diﬀerent risk aversion degrees of
diﬀerent investors on investment utility, as a supplement to the matching strategy.
Finally, we write a memo for traders based on the results of the pairs trading strategy, the
strength and the possible improvements of the model comparison, and the results of the sensitivity
analysis to make our results more scientiﬁc and practical.
Keywords: Modiﬁed Dollar Neutral Strategy; Cointegration; Pairs Trading; Risk Evaluation
~~~~

## 第 002 页

[查看原页版式](pages/page-002.jpg)

~~~~text
Team # 2208834
Page 1 of 24
Contents
1
Introduction
3
1.1
Problem Background . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
3
1.2
Our work
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
3
2
Assumptions
3
3
Model Preparation
4
3.1
Exploratory Data Analysis (EDA)
. . . . . . . . . . . . . . . . . . . . . . . . . .
4
3.1.1
Data Observation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
4
3.1.2
Stationarity Test
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
4
3.2
Data Cleaning . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
5
3.3
L2 Norm Normalization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
6
4
Investment Strategy of Pairs Trading Based on Cointegration
6
4.1
Data Exploration
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
6
4.1.1
Data Observation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
6
4.1.2
Cointegration Theory . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
6
4.1.3
Johanson Cointegration Test . . . . . . . . . . . . . . . . . . . . . . . . .
7
4.1.4
Calculation Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
7
4.2
Pairs Trading
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
7
4.2.1
Pairs Trading Strategies
. . . . . . . . . . . . . . . . . . . . . . . . . . .
8
4.2.2
Related Formula
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
8
4.2.3
Pairs Trading Algorithm . . . . . . . . . . . . . . . . . . . . . . . . . . .
9
5
Strategies Analysis and Comparison
9
5.1
Basic Strategies . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
9
5.1.1
Theoretical Method . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
9
5.1.2
Strategy under Stochastic Simulation Method . . . . . . . . . . . . . . . .
11
5.1.3
Machine Learning Approach——XGBoost . . . . . . . . . . . . . . . . .
11
5.1.4
Machine Learning Approach——LSTM . . . . . . . . . . . . . . . . . . .
11
5.2
Reiterate the Pairs Trading Strategy
. . . . . . . . . . . . . . . . . . . . . . . . .
11
~~~~

## 第 003 页

[查看原页版式](pages/page-003.jpg)

~~~~text
Team # 2208834
Page 2 of 24
5.3
Horizontal Comparison of Indicators . . . . . . . . . . . . . . . . . . . . . . . . .
12
5.3.1
Comparison of Basic Indicators . . . . . . . . . . . . . . . . . . . . . . .
12
5.3.2
Developing Indicators
. . . . . . . . . . . . . . . . . . . . . . . . . . . .
13
5.4
Vertical Comparison of Pairs Trading Strategy . . . . . . . . . . . . . . . . . . . .
14
5.5
Conclusion
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
14
6
The impact of Risk on Investment Strategy
15
6.1
Impact of Market Risk on Investment Strategy . . . . . . . . . . . . . . . . . . . .
15
6.1.1
Price Risk . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
16
6.1.2
Reinvestment Risk . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
16
6.2
The Inﬂuence of Individuals’ Risk Aversion on Trading Strategy . . . . . . . . . .
17
7
Sensitivity Analysis
17
8
Conclusions
19
8.1
Summary of Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
19
8.1.1
Results of Problem 1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
19
8.1.2
Results of Problem 2 . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
19
8.1.3
Results of Problem 3 . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
20
8.1.4
Results of Problem 4 . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
20
8.2
Strength . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
20
8.3
Possible Improvements . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
20
Appendices
23
Appendix A Code Structure and Related Works
23
~~~~

## 第 004 页

[查看原页版式](pages/page-004.jpg)

~~~~text
Team # 2208834
Page 3 of 24
1
Introduction
1.1
Problem Background
Market trading usually involves buying and selling risk assets. Investors want to limit their trading
risk while maximizing returns, and this can be achieve by invest wisely in a variety of assets.
Serious gold investors (gold bugs) love gold because of its ability to store value during tumul-
tuous times and its use as an inﬂation hedge. Bitcoin buyers and other crypto enthusiasts, however,
would argue that bitcoin oﬀers the same level of protection but is superior due to its ease of storage
and transfer.
Under the same initial capital conditions, diﬀerent portfolios will bring diﬀerent returns and
associated risks, so it is necessary to study the best way to balance portfolio, that is to say, the
appropriate proportions of gold and bitcoin in the portfolio.
1.2
Our work
In order to facilitate the evaluation of the trading model, we build a backtesting system(See the
appendix). All of our models (the best model and the three baseline models) are easily estimated
using this system. In order to create the optimal trading strategy, we build a pairs trading model
based on two given assets. Through trading simulation, we can the trading results of any model
(how much is the initial $1000 investment worth on 9/10/2021). By comparing the transactions of
these models, we conﬁrm the superiority of our model. Then we test the robustness of the model
and the sensitivity to transaction costs, and ﬁnally convey our model, strategy and results to traders
through memos.
To solve these problems, our team will do the following:
• As preparation, we explore the data and test the stationarity of the data set. We clean, select
and normalize the tested data.
• We consider the relationship between gold price trend and bitcoin price trend, and ﬁnd that
they passed the cointegration test. On this basis, we use the paired trading strategy to back
test the data, so as to obtain the trading mode and trading strategy.
• In order to conﬁrm that our model is optimal, we constructed three baseline models for
comparison, namely, random strategy, xgboost strategy and attention-based LSTM strategy.
The latter two are based on current mainstream machine learning or time series analysis
models. We compare and analyze returns(arithmetic return, geometric time weighted return,
Jensen alpha), robustness, risk indicators (Sharpe ratio) and other indicators(information
ratio, tracking error) of the three methods. By disturbing our model’s parameters, we test the
robustness of the model to its own parameters.
• Based on the previous research, we also consider the risk of transactions. We divide the
market risks that aﬀect the trading strategy into price risk and Reinvestment risk, and take
personal risk preference into account to explore their impact on the choice of trading strategy.
2
Assumptions
In order to simplify the above problems, we make the following reasonable assumptions:
~~~~

## 第 005 页

[查看原页版式](pages/page-005.jpg)

~~~~text
Team # 2208834
Page 4 of 24
• Assumption1: The data given obeys to the basic assumptions of historical simulation method.
History will repeat itself, and the subsequent market price can be simulated according to the
historical price to get the predicted price.
• Assumption2: Markets are relatively perfect and ﬂexible. All transactions have no transac-
tion delay, whether buying or selling, which are immediate transactions, immediate success;
The transaction cost of the same asset remains the same every time it is traded; Transactions
can be subdivided indeﬁnitely, with no size limit.
• Assumption3:In reality short-selling and leverage is allowed, but if we use unlimited leverage
or borrow approach, there is no approach that will beat the method which investors add the
endless leverage on the rising asset. This will make our study meaningless. So, in our
strategies design, we don’ t think of the short-selling and leverage.
• Assumption4: Asset prices remain the same for the same day, and all transactions are settled
at the day’s closing price.
3
Model Preparation
3.1
Exploratory Data Analysis (EDA)
3.1.1
Data Observation
We select the oﬃcial data set, lbma-gold CSV and bchain-mkpru CSV for data observation. The
two data sets show the closing price in U.S. dollars of gold on the indicated date and the price in
U.S. dollars of a single bitcoin on the indicated date from November 9, 2016 to 9,2021. First, we
describe the basic data as follows:
(a) gold
(b) bitcoin
Figure 1: The daily asset prices
To better observe price changes, we calculated daily returns:
Return = (Ct −Ct−1) /Ct−1 × 100%
(1)
We can get the information from the histogram of historical ﬂuctuating prices in Figure 2.
3.1.2
Stationarity Test
In order to facilitate the calculation of the model in the next step, we test the stationarity of the data
set. For the given data set, we use the mainstream unit root test method to test whether there is a
~~~~

## 第 006 页

[查看原页版式](pages/page-006.jpg)

~~~~text
Team # 2208834
Page 5 of 24
(a) gold_return
(b) bitcoin_return
Figure 2: Histogram of the return distribution
unit root in the series. If there is, it is a non-stationary series, and if there is not, it is a stationary
series.
The inspection process is consistent with DF inspection. If we want to strictly judge whether
the sequence is wide and stable, we can directly test whether it is stable without intercept term and
trend term; If the original hypothesis cannot be rejected (e.g. p > 0.05), that means the series
is non-stationary, it is still necessary to test whether the series is stable. If the trend is not stable
and the trend is not stable, the ﬁrst-order diﬀerence and other stabilization methods can be used
for processing before testing. If the trend is stable, the diﬀerence method should not be used for
stabilization due to excessive diﬀerence.Through the stationarity test, we can get the following ACF
diagram.
(a) acf_normal
(b) acf_diﬀer1
(c) acf_diﬀer2
Figure 3: ACF inspection chart
Through ADF test, we can see that the original data set is relatively stable and tends to normal
distribution. Therefore, we will use the original data for further consideration.
3.2
Data Cleaning
Whether the data is clean or not is directly related to the accuracy and robustness of the ﬁnal model,
and will also aﬀect the ﬁnal conclusion. Therefore, we cleaned the bitcoin price and gold price
data obtained in previous years to enhance the accuracy and credibility of our results.
We ﬁrst deal with the missing value of the data. In the process of processing, we ﬁnd that
because there are certain trading days for gold trading, and bitcoin can be traded at any time, there
is inevitably a vacancy in gold price data. Considering that the data of gold price on non-trading
days will not be aﬀected by market trends and consumer preferences, we ﬁll the data of vacancy
value with the ﬁrst valid data before it.
~~~~

## 第 007 页

[查看原页版式](pages/page-007.jpg)

~~~~text
Team # 2208834
Page 6 of 24
Figure 4: Handling the missing values
3.3
L2 Norm Normalization
The L2 norm of vector x (x1, x2, . . . , xn) is deﬁned as:
norm(x) =
q
x2
1 + x2
2 + . . . + x2
n
(2)
The equivalent form of the above equation is as follows:
x′
i =
xi
norm(x)
(3)
In the description of the model below, we will use the data processed above for further operation.
4
Investment Strategy of Pairs Trading Based on Cointegration
4.1
Data Exploration
4.1.1
Data Observation
After normalizing the data, we can see from the ﬁgure that the trend of bitcoin price has experienced
four stages of stability - rise - fall - rise again, and the trend of gold price has gone through ﬁve
stages of stability - rise - fall - rise again - fall again. And we can see that compared with the trend
of gold price, the price of bitcoin has a certain lag. Therefore, we guess that there is a certain
correlation between the price trend of bitcoin price and the trend of gold price.
Figure 5: Observation of price correlation
4.1.2
Cointegration Theory
The contents of cointegration are:
~~~~

## 第 008 页

[查看原页版式](pages/page-008.jpg)

~~~~text
Team # 2208834
Page 7 of 24
Suppose sequence Xt is d-order cointegration,donated by Xt ∼I(d). If there is a non-zero
vector β and the condition holds Yt = βXt ∼I(d−b), then Xt is said to have b,d-order cointegration
relations, donated by Xt ∼CI(d, b). We call β as a cointegration vector.
Especially, when Xt and Yt are both integration of order one, in general, the linear combination
of Xt and Yt is still an integration of order one. But for some non-zero vectors β, it makes:
Yt −βXt ∼I(0).At this time, the non-zero vector β is called cointegration vector.
Each of
these βt is the cointegration coeﬃcient at time t.In other words, if the two sets of sequences are
non-stationary, but are stationary after the ﬁrst-order diﬀerence, and the two sets of sequences are
stationary after some linear combination, there is a cointegration relationship between them.
4.1.3
Johanson Cointegration Test
Nonstationary series are prone to pseudo regression, and the signiﬁcance of cointegration is to
test whether the causal relationship described by their regression equation is pseudo regression.
Therefore, we decide to use Johansen cointegration test to test the data set.
Johanson cointegration test is a test method based on VAR model, but it can also be directly
used for cointegration test between multiple variables.
Test trace statistics:
LRM = −n
N
X
i=M−1
log (1 −λi)
(4)
Where, M is the number of cointegration vectors, λi is the ith eigenvalue arranged by size,and N is
the sample size.
4.1.4
Calculation Results
Therefore, by calculating their respective rates of return, we can get the correlation coeﬃcient of
their rates of return and the degree of their deviation from the mean, and test the cointegration
of the two groups of data. After testing, we ﬁnd that there is a lagging cointegration relationship
between the price trend of bitcoin and the price trend of gold. This lays the foundation for our
following trading methods.
4.2
Pairs Trading
The basic idea of pairs trading is to ﬁnd two stocks with highly similar historical trends in the stock
market. Due to the similarity of their ﬂuctuations, at the same period of time, the rising and falling
trends and ranges of the two are basically the same, which is the so-called "equilibrium". When
there is a large deviation in the trend at a certain moment, we will enter the long position (i.e.
buying) of the stock below the average and the short position (i.e. short selling) of the stock above
the average. When the two return to the mean value, we close the positions of the two stocks to
lock in the income.
We approximately regard bitcoin and gold as two stocks, and apply the pairs trading strategy
to the trading between bitcoin market and gold market. We use the historical data provided by
the topic to predict the future price of bitcoin and gold, and make decisions to maximize our
own income.Ultimately,we use dollar neutral strategy to build the prediction and decision-making
system of bitcoin and gold.
~~~~

## 第 009 页

[查看原页版式](pages/page-009.jpg)

~~~~text
Team # 2208834
Page 8 of 24
4.2.1
Pairs Trading Strategies
When capturing the abnormal rise of bitcoin price trend, the pairs trading strategy will choose to
buy bitcoin; On the contrary, when capturing the abnormal decline of bitcoin price trend, the pairs
trading strategy will choose to sell bitcoin(in Figure 6, the red triangle indicates buying bitcoin and
the green triangle indicates selling bitcoin).
Figure 6: Corresponding buying and selling strategy
4.2.2
Related Formula
We record the price of gold at time t as PG (t),the price of bitcoin at time t as PB (t).The yields of
the two ﬁnancial assets from t1 to t2 are respectively:
RA (t1, t2) = ln
PA (t2)
PA (t1)

RB (t1, t2) = ln
PB (t2)
PB (t1)

(5)
During this period, the correlation coeﬃcients are:
ρAB (t1, t2) =
Pt2
t=t1+1

RA(t −1, t) −¯RA (t1, t2)

·

RB(t −1, t) −¯RB (t1, t2)

qPt2
t=t1+1

RA(t −1, t) −¯RA (t1, t2)
2 · Pt2
t=t1+1

RB(t −1, t) −¯RB (t1, t2)
2
(6)
The equilibrium price is assumed to be:
¯RAB (t1, t2) = 1
2 (RA (t1, t2) + RB (t1, t2))
(7)
From the above formula, we can calculate the deviation degree of gold price and bitcoin price from
the mean value as follows:
˜RA (t1, t2) = RA −¯RAB (t1, t2)
˜RB (t1, t2) = RB −¯RAB (t1, t2)
(8)
In the algorithm, we add a long short position constraint to meet the needs of the actual situation:
~~~~

## 第 010 页

[查看原页版式](pages/page-010.jpg)

~~~~text
Team # 2208834
Page 9 of 24
i) Total Position Limit
PA(t) · |QA(t)| + PB(t) · |QB(t)| = 2 · I
(9)
ii) Currency Neutrality Conditions
PA(t) · QA(t) + PB(t) · QB(t) = 0
(10)
4.2.3
Pairs Trading Algorithm
Based on the above basic data and restrictions, the process of obtaining the matching transaction
strategy is as follows:
Algorithm 1: Pairs Trading Strategy(MDN)
Initialization:Account A: [C, G, B] = [1000, 0, 0]([ cash, gold, bitcoin ])
for t ←1 to T do
t1 = 0,t2 = t −k
Get the price data at t1 and t2:PB(t1),PG(t1),PB(t2),PG(t2)
Calculate the return oﬀset for each asset, denotes as: ˜RA, ˜RB
if Asset a position is not 0 and ˜RA(t −1, t) · ˜RA(t −2, t −1) < 0 then
Close out
end
if
 ˜RA(t −1, t) −¯RB(t −1, t)
 > ϵ then
Open positions to buy undervalued assets( ˜RA < 0)
end
Update Account A
end
5
Strategies Analysis and Comparison
In this section, we brieﬂy describe how the baseline models are constructed. Then we compare
the three baseline models with our model horizontally. Finally, we adjust model parameters and
observe the robustness of model performance vertically.
5.1
Basic Strategies
5.1.1
Theoretical Method
i) Feature Creation
With reference to various technical indicators, we constructed the following features(??) using
raw data. The calculation of basic features is relatively simple, and only the calculation formula
is shown here.
LogReturn : rt = ln Pt
Pt−1
(11)
PastReturns = Rt−1
(12)
~~~~

## 第 011 页

[查看原页版式](pages/page-011.jpg)

~~~~text
Team # 2208834
Page 10 of 24
Momentum = Pt −Pt−k
(13)
MovingAverage :SMAi = 1
n
n−1
X
i=0
Pt−i
(14)
ExponentialMA : EMAt = EMAt−1 + α [Pt −EMAt−1]
(15)
After the feature construction is completed, the feature is normalized ﬁrst. In order to improve
information exposure, the model is easy to learn. (Training models with non-normalized data
yielded poor results)
ii) Feature Selection
Before feature selection, we ﬁrst use TSNE dimension reduction to observe whether the data is
separable(Figure). As can be seen from the Figure 7,we are able to draw an conclusion that the
result of feature construction is separable.Then we looked at the correlations between features.As
can be seen from the Figure 8, almost the same type of features will have a strong correlation, but
most of the heterogeneity between diﬀerent kinds of features is guaranteed.
(a) Two-dimensional
bisual-
ization result of T-SNE
(b) Heatmap of correlation matrix
Figure 7: Validity and relevance of features
Besides,we draw scatter matrix plot of individual feature,as can be seen from Figure 10.
Figure 8: Scatter matrix between[’return’, ’RSI-6’, ’MACD’]
~~~~

## 第 012 页

[查看原页版式](pages/page-012.jpg)

~~~~text
Team # 2208834
Page 11 of 24
There is some heterogeneity among the main technical indicators, so there is no need to exclude
any of them. However, among the averages, only those with longer periods have certain value.
Considering that the model has a strong learning ability, the model itself has a certain feature
screening ability after adding the attention mechanism, so I retained the majority of features.
5.1.2
Strategy under Stochastic Simulation Method
Assume that gold and Bitcoin’s prices follow a random walk:
St+1 = St ∗exp (µ∆t + σz)
(16)
St+1, St :are the asset prices of the day and the day before.
µ :the mean of changes in the logarithm of asset prices
∆t :the time interval, assumed here to be 1 day, has a value of 1/252
z :a random number that follows a standard normal distribution
Then the Monte Carlo simulation model is established according to the above equation, and
enough simulations are carried out to constantly adjust the holding proportion of the three assets
to obtain the ever-changing investment value.Based on this random walk, we construct a random
trading strategy as an baseline.
5.1.3
Machine Learning Approach——XGBoost
XGBoost, which stands for Extreme Gradient Boosting, is a scalable, distributed gradient-boosted
decision tree (GBDT) machine learning library. It provides parallel tree boosting and is the leading
machine learning library for regression, classiﬁcation, and ranking problems.
Lightgbm and
XGBoost are very competitive statistical learning models in competitions of quantitative trading.
While training the model, in order to avoid data leakage we only used part of the data from
the ﬁrst year for training and were very careful not to allow this part of the data to appear in the
subsequent backtesting.
5.1.4
Machine Learning Approach——LSTM
Long Short-Term Memory (LSTM) is a special kind of Recurrent Neural Network(RNN). LSTM
networks are explicitly designed to avoid the long-term dependency problem, and remembering
information for long periods of time is practically their default behavior. In this experiment, in order
to obtain better prediction eﬀect, we added attention mechanism into the model structure. We see
this attention-based LSTM as a strong competitor to our model, and it is probably one of the models
commonly used in quantitative trading these days. In practice, the LSTM network structure we use is
as follows. We take the price data and technical indicators of the 30 trading days before the forecast
date as features, and the feature dimension is [batchsize, timerange, features] = [64, 30, 20]. We
use a similar approach to the previous model to avoid data leakage.
5.2
Reiterate the Pairs Trading Strategy
The pairs trading model is based on the analysis that there is a lag co-integration relationship
between the gold and Bitcoin prices, namely the Bitcoin with gold on price trends exist obvious lag
correlation. Next according to gold price change trend, we can reasonably estimate price trend of
the Bitcoin, buy the asset whose price is forecasted to rise and sell the asset whose price is expected
to fall. If the current capital is suﬃcient, we will buy all the one asset; if the capital is insuﬃcient,
~~~~

## 第 013 页

[查看原页版式](pages/page-013.jpg)

~~~~text
Team # 2208834
Page 12 of 24
(a) Data split without data leakage
(b) Structure of attention based LSTM
Figure 9: Data split and Model structure
we will hold three diﬀerent assets appropriately. Finally, the investment value under this method is
obtained.
Figure 10: The net worth of four strategies
By observing the above investment value curve, it is found that the return under the pairs trading
strategy is signiﬁcantly improved compared with the other two methods. It can even be compared
with the price trend of Bitcoin, that after 2019, it has even exceeded the price growth of Bitcoin,
indicating that the strategy has worked well.
5.3
Horizontal Comparison of Indicators
5.3.1
Comparison of Basic Indicators
We can calculate the daily return rate of the above three methods according to the following formula,
and then calculate the arithmetic average return rate and return volatility through the average return
rate and standard deviation of return rate:
rt = Vt −Vt−1
Vt−1
(17)
Vt, Vt−1 :the position value of the current day and the previous day respectively.
~~~~

## 第 014 页

[查看原页版式](pages/page-014.jpg)

~~~~text
Team # 2208834
Page 13 of 24
The annualized arithmetic average return rate and annualized return volatility are obtained in
the following table:
Table 1: The basic indicators of four diﬀerent strategies
stochastic simulation method
XGBoost method
LSTM method
Pairs Trading method
Arithmetic
volatility of
Arithmetic
volatility of
Arithmetic
volatility of
Arithmetic
volatility of
return
return
return
return
return
return
return
return
26.64%
35.83%
53.42%
58.17%
53.31%
52.16%
76.96%
50.14%
The relationship among the size of annualized arithmetic average return rate is:
Pairs Trading method>XGBoost method>LSTM method>stochastic simulation method
The relationship between the volatility of annualized returns is as follows:
XGBoost method>LSTM method>Pairs Trading method>stochastic simulation method
5.3.2
Developing Indicators
Daily geometric time-weighted return(Rt):Since we analyze the size and change of the rate of
return, it is more meaningful to use daily geometric rate of return for analysis.
(1 + Rt)n =
n[
i=1
(1 + ri)
(18)
Jensen’s alpha: This index can measure the diﬀerence between expected return and average return.
The larger this index is, it means that our expected return exceeds the theoretical return and the
investment eﬀect is better. And because gold and Bitcoin are both safe-haven assets that have no
obvious relationship with the SSE 50 and other indexes, and we could hold cash, we assume that
rM = rf,that means Jensen’s alpha is the equivalent of excess return.
α = E (rp) −[rf + βp (rM −rf)] ⇒α = E (rp) −rf
(19)
Sharpe Ratio: This indicator is used to evaluate the advantages and disadvantages of investment
considering both return and risk. The higher the value, the greater the return will be obtained under
the same risk, and the lower the risk will be faced under the same return, which is in line with the
pursuit of investment strategy by risk-averse investors.
SR = E (rp) −rf
σ (rp)
(20)
Information Ratio: This indicator is used to evaluate the merits and demerits of active investment in
the portfolio, namely, the degree to which the investment strategy is superior to passive investment.
The higher the value, the more meaningful the investment strategy is.
IR =
α
σ (rp −rf)
(21)
Finally, the tracking error of the three methods is calculated on an annual basis. The smaller the
~~~~

## 第 015 页

[查看原页版式](pages/page-015.jpg)

~~~~text
Team # 2208834
Page 14 of 24
Table 2: The developing indicators of four diﬀerent strategies
stochastic simulation method
XGBoost method
LSTM method
Pairs Trading method
Indicators
Percent/Number
Percent/Number
Percent/Number
Percent/Number
Geometric time-weighted return
0.08%
0.14%
0.16%
0.26%
Jensen’s alpha
0.23
0.49
0.49
0.73
Sharpe Ratio
0.63
0.85
0.95
1.46
Information Ratio
0.05
0.06
0.06
0.10
index, the stronger the risk active avoidance ability corresponding to the strategy is, and the better
the strategy is.
TE = E (rp
′) −rf
(22)
E (rp′) :The average annual returns, not the average of all returns.
Figure 11: The (yearly) tracking error of four diﬀerent strategies
Observing the line chart of tracking error above, it can be found that: in the pairs trading
strategy, only the tracking error near 2017 is relatively large, but it is not diﬃcult to ﬁnd that this is
because the Bitcoin and gold prices in 2017 had unexpectedly huge ﬂuctuations. However, since
we assume a long-term investment of ﬁve years, the tracking error within a single period does not
represent anything. Moreover, when the price ﬂuctuates greatly near 2020, the model does not
have a large tracking error, indicating that the model can be adjusted independently after a huge
ﬂuctuation, which also shows the excellence of the strategy.
5.4
Vertical Comparison of Pairs Trading Strategy
Due to the co-integration relationship between Bitcoin and gold prices under the condition of lag
period, investment returns under diﬀerent lag periods are diﬀerent. However, there is no diﬀerence
in other aspects, because there are no signiﬁcant diﬀerences in the above indicators under the trade-
oﬀbetween risk and return. According to the graph of the ﬁnal value of diﬀerent lag periods, we
can know that the model performance is stable only when the lag period is in the range of [15, 60]
days. It is speculated that the too short time cycle is aﬀected by the short-term drastic ﬂuctuations
of assets, while the too long cycle is too lagged, resulting in information loss.
5.5
Conclusion
In terms of absolute position value, the initial $1,000 investment in our pairs trading strategy ended
up being worth a staggering $106,686.1 on October 9, 2021, far outperforming other existing
methods.
~~~~

## 第 016 页

[查看原页版式](pages/page-016.jpg)

~~~~text
Team # 2208834
Page 15 of 24
Figure 12: The ﬁnal value of diﬀerent lag period of pairs trading strategy
From the horizontal indicators analysis, the large geometric time-weighted return and Jensen’s
alpha value indicate that the absolute return rate of pairs trading strategy is higher than that
of existing methods.
And the large information ratio and sharpe ratio indicate that from the
perspective of balancing risks and returns, the pairs trading strategy still performs well and has
a good performance in active investment management. Tracking error trend indicates that the
strategy has good risk adaptability and can actively avoid unnecessary risks. To sum up, pairs
trading strategy is an innovative, low-risk, high-return strategy.
From the analysis of the longitudinal lag period, it is found that under diﬀerent lag periods, there
will be little diﬀerence in risk but deviation in returns. Therefore, we can obtain the best matching
trading strategy by adjusting the lag period, which is also the advanced point of this strategy.
Figure 13: The ﬁnal returns of the four strategies
6
The impact of Risk on Investment Strategy
Maximization of return is certainly one of the most important goals we pursue, but when we design
trading strategies, we have to consider the impact of the possible future uncertainty – risk. On the
one hand, risk will aﬀect the price trend of assets and thus aﬀect the improvement of our strategies
in reality. On the other hand, the risk aversion of diﬀerent investors will lead to diﬀerent trading
strategies of diﬀerent individuals.
6.1
Impact of Market Risk on Investment Strategy
Although gold and bitcoin’ s risk relative to stocks and other ﬁnancial products is low, their
investments are still faced with the profound inﬂuence of the market risk of price risk. And because
investors can also hold a certain amount of cash at the same time, as well as the existence of
~~~~

## 第 017 页

[查看原页版式](pages/page-017.jpg)

~~~~text
Team # 2208834
Page 16 of 24
Figure 14: Market risk eﬀects on trading strategy
transaction costs, it is greatly possible that reinvestment risk which is caused by the situation which
return of portfolio is less than the cash generated by the risk-free rate appears.
6.1.1
Price Risk
Gold as a safe-haven assets and its price sensitivity to interest rate is too low, but the price will be
also aﬀected by macroeconomic factors,such as economy, policy.For example, during the period of
the COVID-19, the world had a recession. People were afraid of risky assets, and began turning to
invest gold, bonds and other assets, leading to rising gold price. Therefore, when determining the
investment trading strategy, we should take the inﬂuence of macro factors into account, which is
also reﬂected in our own strategy decisions.
As a new hedge asset, bitcoin has similar price inﬂuencial factors to gold, so we won’t go into
too much detail. However, the biggest diﬀerence between the two is that the volatility of bitcoin is
higher, so when making strategies, the price volatility of bitcoin should be assumed to be higher
than that of gold.
6.1.2
Reinvestment Risk
Reinvestment risk mainly depends on the relationship between excess return rate and buying and
selling cost, and the following formula can be used to determine the non-trading interval:
−SCn ≤MCV An ≤PCn
(23)
non −trading interval:The expected excess rate of return falls within this range which means
you don’t buy or sell, holding cash instead ;
Where SCn stands for sell cost, PCn stands for purchase cost and MCVAn stands for marginal
contribution to value added. MCVAn in the above formula has the following relationship with
indicators such as excess return rate and information ratio:
MCV An = αn −IR∗MCARn
(24)
αn = Rn −Rf
(25)
Where αn stands for the excess rate of return over the risk-free rate,IR stands for information ratio
and MCARn stands for marginal contribution to active risk.
~~~~

## 第 018 页

[查看原页版式](pages/page-018.jpg)

~~~~text
Team # 2208834
Page 17 of 24
MCARn indicates the change of the overall risk brought by a 1 % change in the weight of asset
n,means:
MCARn = ∂σp
∂wn
(26)
Based on the above formula derivation,the non-trading interval related to the return rate of a single,
the cost of buying and selling asset is set:
IR ∗MCARn −SCn + Rf ≤Rn ≤IR∗MCARn + PCn + Rf
(27)
Therefore, based on the above analysis, once the predicted return of gold or bitcoin falls within the
above range, our trading strategy immediately changes to hold the corresponding cash.
6.2
The Inﬂuence of Individuals’ Risk Aversion on Trading Strategy
Although the Markowitz eﬃcient frontier model used in the calculation of portfolio holding ratio
assumes that all investors are completely risk-averse, in reality, diﬀerent investors have diﬀerent
degrees of risk aversion, namely, given risk aversion coeﬃcient (λ).
λA =
IR
2 ∗ϕp
(28)
Where ϕp stands for the optimal active risk(varies between individuals).
The reason why diﬀerent degrees of risk aversion have an impact on investment strategies is
that investment returns have the following utility function for investors:
U = αn −λA ∗ϕ2
p −TC
(29)
Where TC stands for transaction cost.
Then Max(U) can be calculated by using partial derivative of ϕp and operations research
method, and the corresponding asset holding ratio and cash holding ratio can be adjusted again.
7
Sensitivity Analysis
Next, we analyze the sensitivity of pairs transaction strategy to transaction cost.During the operation
of the strategy, each transaction will generate a handling fee, which will oﬀset the account value
downward in the transaction and generate an intercept. At point T1 in the ﬁgure, if all assets a0 are
invested, only relevant assets with value a1 can be obtained. For the convenience of analysis, we
assume that the trader invests all assets in each transaction, TC means transaction cost, there are:
a1 + TC = a0
(30)
We assume that there is a transaction cost of α% in each transaction, thus TC = αat. In the process
of a single transaction, the cost of each purchase is a1. Due to the limitation of transaction cost, the
actual value of the purchased ﬁnancial assets is a2. From this,we can get the relationship between
at and at+1 as follows:
at →at+1 = at(1 + α)−1
(31)
After considering one transaction process, we further consider n transaction processes.Assuming
that the ratio of ﬁnancial assets sold in each transaction is still α%, we can get that the relationship
~~~~

## 第 019 页

[查看原页版式](pages/page-019.jpg)

~~~~text
Team # 2208834
Page 18 of 24
between assets after n times of transaction cost an and undamaged assets a0 is as follows:
an = a0(1 + α)−n
(32)
Assuming that the proportion of ﬁnancial assets bought or sold in each transaction is the ﬁxed value
k%,then:
(1 −
αk
1 + α)na0 = an
(33)
Obviously, this formula has nothing to do with the ﬂuctuation of the asset itself.
We select diﬀerent transaction cost rates as the impact indicators, take time as the horizontal
axis and income as the vertical axis, we can see that the beneﬁts of the model under diﬀerent
transaction costs are shown in Figure 15.
Figure 15: The return of the model under diﬀernt transaction costs
(a) Relationship between transaction times and
transaction discount
(b) Fitting curve for brokerage and return
Figure 16: Sensitivity analysis of transaction costs
It can be seen from the ﬁgure that at the same time point, the lower the transaction cost, the higher
the return, which reﬂects the promotion eﬀect of transaction cost on return growth; Accordingly,
when the return is the same, the higher the transaction cost, the longer the time required to obtain
the same return, which shows the inhibitory eﬀect of high transaction cost on realizing the ideal
return. The trend of the model obtained by sensitivity test is consistent with the actual situation,
which also proves the rationality and robustness of the pairs trading strategy.
~~~~

## 第 020 页

[查看原页版式](pages/page-020.jpg)

~~~~text
Team # 2208834
Page 19 of 24
8
Conclusions
8.1
Summary of Results
8.1.1
Results of Problem 1
After the cointegration test, according to the results of the pairs transaction model,the initial $1,000
investment in our pairs trading strategy ended up being worth a staggering $106,686.1 on October
9, 2021.Given a transaction cost (e.g. αgold = 1% and αbitcoin = 2%), our model can get the
best transaction strategy up to the day and the ﬁnal income.
Figure 17: Changes in returns after adopting the pairs trading strategy
8.1.2
Results of Problem 2
According to the results of pairs trading strategy, we compare it with random trading strategy and
machine learning strategy (XGBoost), which shows that our strategy is the best(Figure 18). It
(a) The value of four diﬀerent strategies
(b) The absolute position value of four diﬀerent
strategies
Figure 18: Algorithm eﬀect comparison
can be seen from the ﬁgure that the ﬁnal return of paired trading far exceeds that of other trading
strategies. The ﬁnal return reaches 24.87 times that of random trading strategy and 8.03 times that
of XGBoost trading strategy.
~~~~

## 第 021 页

[查看原页版式](pages/page-021.jpg)

~~~~text
Team # 2208834
Page 20 of 24
8.1.3
Results of Problem 3
Through the sensitivity analysis of the model, it can be seen that there is a negative correlation
between transaction cost and return at the same time point, and vice versa.
(a) The return of the model under dif-
fernt transaction costs
(b) Fitting curve for brokerage and re-
turn
(c) Relationship between transaction
times and transaction discount
Figure 19: Sensitivity analysis of transaction cost
8.1.4
Results of Problem 4
The memorandum is attached at the end of the article.
8.2
Strength
• The model and strategy based on pairs trading are scientiﬁc and reasonable, which can
maximize the income. The results obtained have strong conﬁdence.
• Compared with other random strategies, LSTM strategies and machine learning strate-
gies(XGBoost), the model has stronger proﬁtability and better robustness.
• Considering the impact of various market risk factors on trading strategies, it provides
theoretical and data support for traders’ decision-making.
8.3
Possible Improvements
• Select highly relevant assets from richer assets for pairs trading model.
• At present, the formula is used to directly determine whether there is an abnormal ﬂuctuation
of assets. If the method of statistical learning is used to judge the ﬂuctuation, it may have
better accuracy.
• In the real world, traders can control risks by adding leverage and shorting. In order to
make the process clear and the results reliable, these more complex trading behaviors are not
included in the experiment.
~~~~

## 第 022 页

[查看原页版式](pages/page-022.jpg)

~~~~text
Memorandum
To: The Trader
From: Team# 2208834
Subject: Pairs trading strategy – higher return and lower risk
Date: February 22, 2022
Dear Sir or Madame,
Although quantitative trading based on machine learning has become very popular in recent
years (such as statistical learning, Markov Monte Carlo or recurrent neural networks(RNNs)).
However, they rely too much on data quality. Machine learning models are sometimes vulnerable
to noisy data in ﬁnancial markets. They don’t perform well, especially with limited data.
The data you provided is relatively simple and noisy. Out of caution, we do not choose the
black box of machine learning, but establish a math-based trading strategy: pairs-trading. It’s as
easy to understand as a transparent box, and risk is manageable.
According to your needs, we observe the processed gold price trend and bitcoin price trend,
and ﬁnd that there is a certain relationship between them through inspection. In this regard, we
conduct Johanson-test on the data after data cleaning and normalization, and the results show that
there is a cointegration relationship between them.On this basis, we use the pairs trading model to
backtest the data.
In order to backtest the policy, we build a backtest system using Python. This backtesting
system provides price information to the strategy accorording to trading days, getting a trading
order for the strategy, and then trading it. Therefore, if the strategy is separated from the price data,
the strategy can only obtain the past data and submit orders to the system.
The pairs trading is a trading strategy that involves matching a long position with a short position
in two stocks with a high correlation. The model treats bitcoin and gold as two stocks.Diﬀerent
from the traditional algorithm that needs to make prediction before decision-making, our pairs
~~~~

## 第 023 页

[查看原页版式](pages/page-023.jpg)

~~~~text
trading algorithm has the functions of prediction and decision-making. It can infer the subsequent
trend through the previous data trend and make the corresponding trading strategy.
For the purpose of proving that our strategy is the best, we compare random algorithm, machine
learning algorithm XGBoost and LSTM algorithm, and highlight the advantages of our model from
the following aspects:
• Sharpe Ratio could evaluate the trade-oﬀof return and risk of an investment. Our pairs
trading strategy’s Sharpe Ratio is 1.46. By contrast, other models’ indicators are only below
1. Usually, SR nearly 1.5 indicates investment will have high return with low risk. So our
strategy is relatively best.
• Information Ratio could indicate the ability of active investment. The indicator within our
own pairs trading strategy is approximately three times higher than other existing models.
This means our strategy has a great performance of actively intervene risk to obtain higher
return.
• Tracking error can trade oﬀwhether a strategy would avoid unnecessary risk. The TE of our
strategy is a little higher in 2017, but in any other period is always too low. This means the
strategy not only has a stronger risk avoidance, but also has a better ability of risk adaptation.
It is found that after using our trading strategy, through the diﬀerent conversion and multiple
buying and selling operations of two diﬀerent ﬁnancial assets-bitcoin and gold, the $1000 on
September 10, 2016 becomes $106986.1 on September 10, 2021.The net asset value has increased
by nearly 107 times year-on-year, realizing a great rate of return.
Using our model will not only have suﬃcient ﬂexibility and high anti risk ability, but also bring
you considerable beneﬁts. If you want to both at ease and earn money, choose our model!
~~~~

## 第 024 页

[查看原页版式](pages/page-024.jpg)

~~~~text
Team # 2208834
Page 23 of 24
References
[1] Charfeddine, L. , & Khediri, K. B. . (2016). Financial development and environmental quality
in uae: cointegration with structural breaks. Renewable & Sustainable Energy Reviews, 55,
1322-1335.
[2] Hodoshima, J. , Dempster, M. , & Gatheral, J. . (2019). Stock performance by utility indiﬀer-
ence pricing and the Sharpe ratio.
[3] Selvin, S. , Vinayakumar, R. , Gopalakrishnan, E. A. , Menon, V. K. , & Soman, K. P. . (2017).
Stock price prediction using LSTM, RNN and CNN-sliding window model. International
Conference on Advances in Computing. IEEE.
[4] Gashi, B. , & Date, P. . (2011). Two methods for optimal investment with trading strategies of
ﬁnite variation. Ima Journal of Management Mathematics, 23(2), 171-194.
[5] https://www.investopedia.com/terms/p/pairstrade.asp
[6] https://www.garp.org/white-paper/forecasting-bitcoin-risk-measures-a-robust-approach
[7] YE Wuyi, SUN Liping, & MIAO Baiqi(2020). A Study of Dynamic Cointegration of Gold
and Bitcoin Based on Semiparametric MIDAS Quantile Regression Model.(J. Sys. Sci. &
Math. Scis.)
[8] Wang, Y. , & Guo, Y. . (2020). Forecasting method of stock market volatility in time series
data based on mixed model of arima and xgboost. China Communications: English edition,
17(3), 17.
Appendices
Appendix A
Code Structure and Related Works
In this paper, the trading strategy and experimental codes are mainly implemented in Python,
and the risk control part is based on Excel, combined with statistical calculation. The speciﬁc
application environment is as follows:
~~~~

## 第 025 页

[查看原页版式](pages/page-025.jpg)

~~~~text
Team # 2208834
Page 24 of 24
A. Exploratory data analysis(EDA) This part contains: 1.
Data reading, basic analysis,
visualization; 2. Test related properties of data (such as normal distribution test, stationarity test
and cointegration test) according to policy requirements.
B. Backtesting system
This section constructs a trade environment class [Class TradeEnv(Object)], which contains
the relevant attributes needed by the test strategy: [data_dict], [Brokerage], [Account], [History].
Write and encapsulates the correlation function: [Getdata ()], [reset_Trade_data ()], [Record ()],
[the Trade ()], and so on.
C. Strategy part
The four strategies and implementation in this section are shown in the table below:
D. Experiment
a. Comparative experiment: ﬁnancial mathematical calculation using Excel.
b. Robustness and sensitivity test: After encapsulating the experimental environment and
strategy, program operation with diﬀerent experimental parameters (Time_range, Brokerage). Fi-
nally, collating experimental results.
~~~~
