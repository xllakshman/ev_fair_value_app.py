
import yfinance as yf
import pandas as pd
from datetime import datetime

def backtest_fair_value(ticker, fair_value_current, years=3):
    try:
        stock = yf.Ticker(ticker)
        end_date = datetime.now()
        start_date = end_date.replace(year=end_date.year - years)
        hist = stock.history(start=start_date, end=end_date)

        if hist.empty or "Close" not in hist:
            return pd.DataFrame()

        result_rows = []
        for year in range(end_date.year - years, end_date.year):
            year_data = hist[hist.index.year == year]
            if year_data.empty:
                continue

            avg_price = year_data["Close"].mean()
            high_price = year_data["High"].max()
            low_price = year_data["Low"].min()

            # simulate fair value for past using current fair value adjusted by 10% CAGR reverse
            reverse_years = end_date.year - year
            simulated_fv = fair_value_current / ((1.10) ** reverse_years)
            deviation_pct = ((simulated_fv - avg_price) / avg_price) * 100
            converged = (low_price <= simulated_fv <= high_price)

            result_rows.append({
                "Year": year,
                "Simulated Fair Value": round(simulated_fv, 2),
                "Avg Market Price": round(avg_price, 2),
                "Price High": round(high_price, 2),
                "Price Low": round(low_price, 2),
                "Deviation (%)": round(deviation_pct, 2),
                "Converged": "Yes" if converged else "No"
            })

        return pd.DataFrame(result_rows)

    except Exception as e:
        return pd.DataFrame()
