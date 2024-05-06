scrapy runspider results.py
python processing.py
python alg.py
mkdir Results/LinearRegression/CTRL
mkdir Results/LinearRegression/HP
mkdir Results/LinearRegression/S&D
mkdir Results/MatPlotLib/CTRL
mkdir Results/MatPlotLib/HP
mkdir Results/MatPlotLib/S&D
mkdir Results/MatPlotLib/Total
rm Results/LinearRegression/results.csv
python Kills_Time_Series.py
python Linear_Regression.py
