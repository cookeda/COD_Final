scrapy runspider results.py
python processing.py
python alg.py

if not exist "Results" mkdir Results
if not exist "Results\LinearRegression" mkdir Results\LinearRegression
if not exist "Results\MatPlotLib" mkdir Results\MatPlotLib

if not exist "Results\LinearRegression\CTRL" mkdir Results\LinearRegression\CTRL
if not exist "Results\LinearRegression\HP" mkdir Results\LinearRegression\HP
if not exist "Results\LinearRegression\S&D" mkdir "Results\LinearRegression\S&D"
if exist "Results\LinearRegression\results.csv" rm Results\LinearRegression\results.csv"


if not exist "Results\MatPlotLib\CTRL" mkdir Results\MatPlotLib\CTRL
if not exist "Results\MatPlotLib\HP" mkdir Results\MatPlotLib\HP
if not exist "Results\MatPlotLib\S&D" mkdir "Results\MatPlotLib\S&D"
if not exist "Results\MatPlotLib\Total" mkdir Results\MatPlotLib\Total

python Kills_Time_Series.py
python Linear_Regression.py
