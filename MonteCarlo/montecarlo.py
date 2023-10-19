import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


mc_sims = 5000
annual_inflation_rate = 0.02
endDate = dt.datetime(2022, 12, 31)
startDate = dt.datetime(1972, 1, 1)

# Questions should match what we already have on the website - these are just fillers and are not exactly word for word the same as what we have on the front page
def get_user_inputs():
    """
    Page 1: User Inputs
    """
    investment_amount = float(input("Enter your initial investment amount: "))
    purpose = input("Enter your investment purpose (buy a home, speculate, retirement, education, get started): ")
    duration = int(input("How many years do you plan to invest for? "))
    monthly_contribution = float(input("If you would like to try the simulator with a monthly investment contribution, enter it now. If not, enter 0: "))
    return investment_amount, monthly_contribution, purpose, duration

# Function to get stock data
def get_data(stocks, start, end, use_historical=True):
    stockData = {}
    for stock in stocks:
        try:
            data = yf.download(stock, start=start, end=end)
            stockData[stock] = data['Close']
        except Exception as e:
            print(f"Error fetching data for {stock}: {e}")
            continue

    combinedData = pd.DataFrame(stockData)
    returns = combinedData.pct_change()
    yearlyReturns = returns.resample('Y').apply(lambda x: (1 + x).prod() - 1)
    if use_historical:
        meanReturns = yearlyReturns.mean()
    else:
        default_annual_growth = 0.07
        meanReturns = np.full(len(stocks), default_annual_growth)

    meanReturns -= annual_inflation_rate
    covMatrix = yearlyReturns.cov()

    return meanReturns, covMatrix

# this is a place holder for the CIRCLE OF COMPETENCE PAGE
def stock_selection():
    """
    Page 2: Stock Selection
    """
    tickers_input = input("Enter stock tickers or cryptocurrency codes separated by commas (e.g., AAPL, MSFT, BTC-USD): ")
    chosen_stocks = [ticker.strip().upper() for ticker in tickers_input.split(',')]

    return chosen_stocks

def get_user_debt():
    """
    Page 3: User Debt
    """
    # Asking user for different types of debts
    student_debt = float(input("List your student debt amount or 0 if none: $"))
    auto_loan_debt = float(input("List your auto loan debt amount or 0 if none: $"))
    credit_card_debt = float(input("List your credit card debt amount or 0 if none: $"))
    margin_debt = float(input("List your margin debt amount or 0 if none: $"))
    
    # Summing up all the debts
    total_debt = student_debt + auto_loan_debt + credit_card_debt + margin_debt

    # Check for student loan or auto loan debt and show a popup
    if student_debt > 0 or auto_loan_debt > 0:
        response = input("Do you have a plan for paying down your debt? If not, would you like to connect with one of our financial counselors for a complimentary call? (Yes/No): ")
        
        if response.lower() == "yes":
            print("Connecting you with a financial counselor...")
        else:
            print("Okay, proceeding...")

    # Check for margin debt and show a popup
    if margin_debt > 0:
        print("Margin debt is generally not advised as a long-term sustainable way to grow wealth. In this current high rate environment, we recommend paying down margin debt before investing those funds. (In other words, if someone has $5000 to invest but has $2000 in margin debt, we recommend paying down the debt and investing $3000.)")
        input("Press enter to proceed...")  # Just a simple way to have the user acknowledge the message

    # Check for credit card debt and show a popup
    if credit_card_debt > 0:
        print("Credit card debt is perhaps the most crushing debt out there. We recommend users pay off their high-interest credit card debt with their discretionary investable cash before investing.")
        input("Press enter to proceed...")  # Again, this is to ensure the user sees and acknowledges the message

    return total_debt


'''
This part will run on the RISK TOLERANCE PAGE and is meant to help define the user's
Risk Tolerance and correct it if it does not match up with the risk strategy they have defined via the 3 questions on PAGE 1
'''
def suggest_portfolio(risk_level, chosen_stocks, meanReturns):
    # For simplicity, let's just evenly distribute weights among chosen stocks
    num_stocks = len(chosen_stocks)

    if risk_level == "1":  # High risk
        weights = np.array([1/num_stocks] * num_stocks)
    elif risk_level == "2":  # Moderate risk
        # For the sake of this example, let's say 80% of investment is in stocks with the highest returns and 20% in others.
        sorted_indexes = meanReturns.argsort()[::-1]
        top_indexes = sorted_indexes[:int(0.8*num_stocks)]
        weights = np.array([0.8/len(top_indexes) if i in top_indexes else 0.2/(num_stocks-len(top_indexes)) for i in range(num_stocks)])
    else:  # Low risk
        # Inverse the logic: 80% in stocks with the lowest returns (assuming they're less volatile) and 20% in others.
        sorted_indexes = meanReturns.argsort()
        top_indexes = sorted_indexes[:int(0.8*num_stocks)]
        weights = np.array([0.8/len(top_indexes) if i in top_indexes else 0.2/(num_stocks-len(top_indexes)) for i in range(num_stocks)])

    # Normalize weights to ensure they sum to 1 due to potential rounding discrepancies.
    weights = weights / np.sum(weights)
    return weights

def custom_allocation(chosen_stocks):
    """
    Allows the user to specify a custom allocation for their chosen assets.
    """
    weights = []
    print("Specify your custom allocation (in %) for each asset. Ensure they sum up to 100%.")
    for stock in chosen_stocks:
        while True:
            try:
                weight = float(input(f"Allocation for {stock}: "))
                if 0 <= weight <= 100:
                    weights.append(weight / 100)  # Convert percentage to fraction
                    break
                else:
                    print("Please enter a value between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
    if not math.isclose(sum(weights), 1, rel_tol=1e-5):  # Check if allocations sum up to 100%
        print("Your allocations do not sum up to 100%. Please specify again.")
        return custom_allocation(chosen_stocks)
    return np.array(weights)

# RISK TOLERANCE PAGE
def risk_tolerance(investment_amount, purpose, duration, chosen_stocks, meanReturns):
    """
    Page 4: Risk Tolerance
    """
    # Provide options
    print("Choose your risk tolerance level:")
    risk_level = input("1. High risk\n2. Moderate risk\n3. Low risk\n4. Custom Allocation\n")

    if risk_level == "4":
        return custom_allocation(chosen_stocks)

    # Define potential portfolio allocations based on inputs and risk level
    if duration < 5 and purpose == "speculate":
        # Suggest aggressive portfolios
        portfolio_weights = suggest_portfolio("1", chosen_stocks, meanReturns)
    elif duration >= 20 and purpose == "retirement":
        # Suggest aggressive portfolios
        portfolio_weights = suggest_portfolio("1", chosen_stocks, meanReturns)
    elif purpose == "education":
        # Suggest conservative portfolios
        portfolio_weights = suggest_portfolio("3", chosen_stocks, meanReturns)
    elif purpose == "purchasing a home" and duration < 10:
        # Suggest moderate to conservative portfolios
        portfolio_weights = suggest_portfolio("2", chosen_stocks, meanReturns)
    elif purpose == "looking to get started":
        if duration >= 10:
            # Suggest moderate portfolios
            portfolio_weights = suggest_portfolio("2", chosen_stocks, meanReturns)
        else:
            # Suggest conservative portfolios
            portfolio_weights = suggest_portfolio("3", chosen_stocks, meanReturns)
    else:
        # If none of the conditions match, use the user's chosen risk level
        portfolio_weights = suggest_portfolio(risk_level, chosen_stocks, meanReturns)
    return portfolio_weights, chosen_stocks


# Monthly investments are added in the first year itself (12 * monthly_investment).
# For subsequent years, the portfolio's value at the end of the previous year is used along with adding monthly investments. This ensures the investments are being made right after the initial one.


# PAGE 5 - RESULTS PAGE - This monte carlo simulation will run on the results page
def monte_carlo_simulation(meanReturns, covMatrix, initial_weights, T, initialPortfolioValue, monthly_investment, mc_sims):
    """
    Page 5: Monte Carlo Simulation Results
    """
    def make_matrix_positive_definite(covMatrix):
        minEigenvalue = np.min(np.real(np.linalg.eigvals(covMatrix)))
        if minEigenvalue < 0:
            offset = -minEigenvalue
            covMatrix += offset * np.eye(*covMatrix.shape)
        return covMatrix

    meanM = np.full(shape=(T, len(initial_weights)), fill_value=meanReturns)
    meanM = meanM.T
    portfolio_sims = np.full(shape=(T, mc_sims), fill_value=0.0)

    covMatrix = make_matrix_positive_definite(covMatrix)
    L = np.linalg.cholesky(covMatrix)

    for m in range(0, mc_sims):
        Z = np.random.normal(size=(T, len(initial_weights)))
        yearlyReturns = meanM + np.inner(L, Z)

        for t in range(T):
            # Use the initial weights for all years (yearly rebalancing)
            current_weights = initial_weights

            if t == 0:
                # For the first year, just adjust with the initial investment
                portfolio_sims[t, m] = (np.inner(current_weights, yearlyReturns[:, t]) + 1) * initialPortfolioValue + 12 * monthly_investment
            else:
                # For subsequent years, adjust with the portfolio value at the end of the previous year and add monthly investments
                portfolio_sims[t, m] = (np.inner(current_weights, yearlyReturns[:, t]) + 1) * portfolio_sims[t - 1, m] + 12 * monthly_investment

    return portfolio_sims


# PLOTTING the monte carlo
def plot_results(T, portfolio_sims):
    p10 = np.percentile(portfolio_sims, 10, axis=1)
    p50 = np.percentile(portfolio_sims, 50, axis=1)
    p80 = np.percentile(portfolio_sims, 80, axis=1)

    plt.plot(p10, label='10th percentile', color='red', linestyle='dashed')
    plt.plot(p50, label='Median', color='blue')
    plt.plot(p80, label='80th percentile', color='green', linestyle='dashed')
    plt.fill_between(range(T), p10, p80, color='gray', alpha=0.5)
    plt.legend()
    plt.ylabel('Portfolio Value ($)')
    plt.xlabel('Years')
    plt.title('Monte Carlo Simulation of Portfolio with Confidence Intervals')
    plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: int(x)))
    plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
    plt.show()



def main():
    # 1. Collect all required inputs
    investment_amount, monthly_contribution, purpose, duration = get_user_inputs()
    chosen_stocks = stock_selection()
    debt = get_user_debt()

    # 2. Fetch the data and calculate mean returns and covariance matrix
    meanReturns, covMatrix = get_data(chosen_stocks, startDate, endDate)

    # Update the risk tolerance function call to include meanReturns
    portfolio_weights, chosen_stocks = risk_tolerance(investment_amount, purpose, duration, chosen_stocks, meanReturns)
    for stock, weight in zip(chosen_stocks, portfolio_weights): # Print the chosen stocks and their respective allocations
        print(f"{stock}: {weight*100:.2f}%")

    # 3. Calculate portfolio returns and portfolio risk based on the chosen weights
    port_return = np.dot(meanReturns, portfolio_weights)
    port_risk = np.sqrt(np.dot(portfolio_weights.T, np.dot(covMatrix, portfolio_weights)))

    # 4. Run the Monte Carlo simulation
    T = duration  # Number of years
    portfolio_sims = monte_carlo_simulation(meanReturns, covMatrix, portfolio_weights, T, investment_amount, monthly_contribution, mc_sims)

    # (Optional) Display final portfolio values
    final_portfolio_values = portfolio_sims[-1, :]  # final portfolio values
    final_median = np.median(final_portfolio_values)  # Median of the final portfolio values
    print('Final median portfolio value: $', '{:,.0f}'.format(final_median))

    # 5. Optionally, visualize the results
    plot_results(T, portfolio_sims)

if __name__ == "__main__":
    main()

'''
Sample stock symbols and weights:

# AAPL,MSFT,AMZN,GOOGL,META,JNJ,PG,V,JPM,BTC-USD
# .15,.15,.15,.1,.1,.1,.1,.05,.05,.05
# 15,15,15,10,10,10,10,5,5,5
'''