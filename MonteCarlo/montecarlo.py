import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


mc_sims = 10000
annual_inflation_rate = 0.02
endDate = dt.datetime(2023, 11, 1)
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


# rename to suggest allocation ?
# The function assumes that stocks with higher historical mean returns are riskier
def suggest_portfolio(risk_level, chosen_stocks, meanReturns):
    print("Risk Level:", risk_level, "Type:", type(risk_level))
    num_stocks = len(chosen_stocks)
    sorted_indexes = meanReturns.argsort()[::-1]
    print("Sorted Indexes:", sorted_indexes)
    print("Sorted Stocks and Returns:")
    for index in sorted_indexes:
        print(f"Stock: {chosen_stocks[index]}, Return: {meanReturns[index]}")

    if risk_level == "Aggressive":
        # Higher allocation to stocks with highest returns
        top_indexes = sorted_indexes[:int(0.5 * num_stocks)]
        print("Top Indexes for Aggressive:", top_indexes)
        #
        weights = [0.8 / len(top_indexes) if i in top_indexes else 0.2 / (num_stocks - len(top_indexes)) for i in range(num_stocks)]
    elif risk_level == "Moderate Aggressive":
        # Balanced but slightly aggressive
        top_indexes = sorted_indexes[:int(0.7 * num_stocks)]
        print("Top Indexes for Moderate Aggressive:", top_indexes)
        #
        weights = [0.6 / len(top_indexes) if i in top_indexes else 0.4 / (num_stocks - len(top_indexes)) for i in range(num_stocks)]
    elif risk_level == "Moderate":
        # Evenly distributed weights
        weights = [1 / num_stocks] * num_stocks
        print("No specific top or bottom indexes for Moderate")
        #
    elif risk_level == "Moderate Conservative":
        # More conservative, lower allocation to higher return stocks
        bottom_indexes = sorted_indexes[int(0.6 * num_stocks):]
        print("Bottom Indexes for Moderate Conservative:", bottom_indexes)
        #
        weights = [0.4 / len(bottom_indexes) if i in bottom_indexes else 0.6 / (num_stocks - len(bottom_indexes)) for i in range(num_stocks)]
    else:  # "Conservative"
        # Highest allocation to less volatile stocks
        bottom_indexes = sorted_indexes[int(0.8 * num_stocks):]
        print("Bottom Indexes for Conservative:", bottom_indexes)
        #
        weights = [0.8 / len(bottom_indexes) if i in bottom_indexes else 0.2 / (num_stocks - len(bottom_indexes)) for i in range(num_stocks)]

    # Normalize weights to ensure they sum to 1
    weights = np.array(weights) / np.sum(weights)
    return weights ###


def custom_allocation(chosen_stocks):
    """
    Allows the user to specify a custom allocation for their chosen assets.
    """
    while True:  # Loop will keep running until the user gives a correct allocation summing up to 100%
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

        if math.isclose(sum(weights), 1, rel_tol=1e-5):  # Check if allocations sum up to 100%
            break  # Exit the loop if the allocations are correct
        else:
            print("Your allocations do not sum up to 100%. Please specify again.")
    return np.array(weights)

# RISK TOLERANCE QUESTIONAIRE
def risk_tolerance_questionnaire():
    total_points = 0
    questions = [
        {
            "prompt": "Let's determine your Risk Tolerance. First, the easy stuff: how would you describe your investment personality?",
            "options": [
                "Conservative: Capital preservation is very important for me right now.",
                "Moderately Conservative: Capital preservation is important but I’m willing to take on a little risk to grow principal and income.",
                "Moderate: I am willing to take a moderate amount of risk to grow my investment.",
                "Moderately Aggressive: I am looking for significant capital growth over time.",
                "Aggressive: I am seeking substantial capital growth and I am willing to take risks to do so."
            ],
            "scores": [1, 2, 3, 4, 5]
        },
        {
            "prompt": "How old are you?",
            "options": [
                "Below 18 – I’m just here to learn and get started.",
                "18 -25",
                "26 – 33",
                "34 – 40",
                "41-50",
                "51-59",
                "60- 69",
                "70+"
            ],
            "scores": [8, 7, 6, 5, 4, 3, 2, 1]
        },
        {
        "prompt": "What is your approximate yearly savings, after expenses?",
        "options": [
            "Zero savings: I’m a full-time student, not taking on debt.",
            "Zero savings: I’m a full-time student, taking on debt.",
            "I have negative yearly savings (I have net debt.)",
            "Zero savings: I am working but expenses eat up my income.",
            "Up to $5,000",
            "$5,000 - $12,000",
            "$12,000 - $25,000",
            "$25k - $50k",
            "Over $50k"
        ],
        "scores": [1, -1, -3, 0, 1, 2, 3, 4, 5]
        },
        {
            "prompt": "How important is politics and presidential elections in your investment decisions and your confidence in the economy?",
            "options": [
                "Political elections – and who’s in the White House - play a major role in how I feel about the economy and investing opportunities.",
                "Political policy (ie. tax policy) and elections play a minor tactical (short-term) role in how I invest.",
                "Politics has little to no influence on my LONG-TERM investing decisions."
            ],
            "scores": [-2, 0, 2]
        },
        {
            "prompt": "Let’s say you’ve invested $10,000 in a diversified portfolio of 4 stocks and after 6 months, you’ve already lost 20%, a loss of $2000, would you:",
            "options": [
                "Sell everything or almost everything.",
                "Sell about $1,000 to have some cash on the sideline?",
                "Do nothing",
                "Buy on the dip with $1,000 from your recent paycheck"
            ],
            "scores": [0, -1, 2, 3]
        },
        {
            "prompt": "News headlines report that another virus threatens to blow up into a full-blown pandemic and, as a result, stocks markets have already sold off 10% in 3 weeks. You invested $10,000 a month ago, and you’re already down $1,000. Would you:",
            "options": [
                "Sell everything or almost everything",
                "Sell about $1,000 to have some cash on the sideline?",
                "Do nothing",
                "Buy on the dip with a $1,000 from your paycheck?"
            ],
            "scores": [-2, 0, 1, 2]
        },
        {
            "prompt": "Just for fun: What’s the riskiest thing you’ve done – or want to do soon:",
            "options": [
                "Jumping from an airplane with Tom Cruise, riding your cycle off a mountain cliff, paragliding through a canyon or filming a video for Instagram in which you jump off a 10-story building into a narrow pool",
                "Off-road biking down a mountain path – with your helmet on. Skiing the double-black diamond trail at Vail, or rock climbing in an indoor gym.",
                "Night hiking all by yourself, travelling to a foreign country for the first time – without knowing anyone. Being the first on the dance floor – in front of the entire crowd",
                "None of the above"
            ],
            "scores": [3, 2, 1, 0]
        }
    ]

    total_score = 0

    for q in questions:
        print(q["prompt"])
        print("\n" + "="*50)  # separator for better readability
        for i, option in enumerate(q["options"], 1):
            print(f"{i}. {option}")

        while True:
            try:
                answer = int(input("Your choice (number): "))
                if 1 <= answer <= len(q["options"]):
                    total_score += q["scores"][answer - 1]
                    break
                else:
                    print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a number. Try again.")

    # Determine risk profile based on score
    if total_score <= 2:
        return "Conservative: You shouldn’t invest anything for under 2 years."
    elif 3 <= total_score <= 5:
        return "Moderate Conservative"
    elif 6 <= total_score <= 8:
        return "Moderate"
    elif 9 <= total_score <= 11:
        return "Moderate Aggressive"
    else:
        return "Aggressive: you’re good to go. No restrictions."


# DETERMINE RISK TOLERANCE FROM INPUTS
def determine_risk_tolerance_inputs(investment_amount, purpose, duration):
    """
    Adjusts the risk level based on investment amount, purpose, and duration.
    Returns a risk profile category.
    """

    # Determine risk level based on duration and purpose
    if duration < 5:
        if purpose == "speculate":
            return "Aggressive"
        elif purpose in ["education", "purchasing a home"]:
            return "Conservative"
        else:
            return "Moderate"
    elif duration >= 20 and purpose == "retirement":
        return "Aggressive"
    elif purpose == "education":
        return "Conservative"
    elif purpose == "purchasing a home" and duration < 10:
        return "Moderate Conservative"
    elif purpose == "looking to get started":
        return "Moderate" if duration >= 10 else "Conservative"
    else:
        return "Moderate"
'''
def risk_tolerance(investment_amount, purpose, duration, chosen_stocks, meanReturns, risk_profile):
    """
    Page 4: Risk Tolerance
    First assign a default risk level based on the risk profile, then adjust the risk level for specific scenarios - finally suggest a portfolio
    """

    # Map the risk_profile to a numerical risk level for portfolio suggestion
    profile_to_risk = {
        "Conservative": "0",
        "ModCON": "1",
        "Moderate": "2",
        "MOD AGG": "3",
        "AGGRESSIVE": "4"
    }

    # Get the risk level from the profile or default to "2"
    risk_level = profile_to_risk.get(risk_profile, "2")

    # Ask user if they want a custom allocation
    custom_choice = input("Do you want a custom allocation? (yes/no): ").strip().lower()
    if custom_choice == "yes":
        portfolio_weights = custom_allocation(chosen_stocks)
        return portfolio_weights, chosen_stocks

    # Adjust risk level based on duration and purpose
    if duration < 5 and purpose == "speculate":
        risk_level = "4"
    elif duration >= 20 and purpose == "retirement":
        risk_level = "4"
    elif purpose == "education":
        risk_level = "0"
    elif purpose == "purchasing a home" and duration < 10:
        risk_level = "1"
    elif purpose == "looking to get started":
        if duration >= 10:
            risk_level = "2"
        else:
            risk_level = "0"

    # Suggest a portfolio based on the final risk level
    portfolio_weights = suggest_portfolio(risk_level, chosen_stocks, meanReturns)
    return portfolio_weights, chosen_stocks
'''

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
    investment_amount, monthly_contribution, purpose, duration = get_user_inputs()
    chosen_stocks = stock_selection()
    debt = get_user_debt()

    # Fetch the data and calculate mean returns and covariance matrix
    meanReturns, covMatrix = get_data(chosen_stocks, startDate, endDate)

    # Debugging: Print portfolio weights for each risk level
    for risk_level in ["Aggressive", "Moderate Aggressive", "Moderate", "Moderate Conservative", "Conservative"]:
        weights = suggest_portfolio(risk_level, chosen_stocks, meanReturns)
        print(f"Risk Level: {risk_level}, Weights: {weights}")

    # Determine user's risk profile using the questionnaire
    risk_profile_questionnaire = risk_tolerance_questionnaire()
    print(f"Based on your answers, your risk profile is: {risk_profile_questionnaire}")

    # Determine risk profile using the inputs (3 questions)
    risk_profile_inputs = determine_risk_tolerance_inputs(investment_amount, purpose, duration) ##### should output a risk level
    print(f"Based on your answers to the 3 questions at the beginning (age, investment duration, and purspose), your risk profile is: {risk_profile_inputs}")
    # Show Monte Carlo scenarios for both risk profiles
    if risk_profile_inputs != risk_profile_questionnaire:
        print("\nThere seems to be a mismatch between your initial inputs and your questionnaire results.")

        # Portfolio weights for inputs-based risk profile
        weights_inputs = suggest_portfolio(risk_profile_inputs, chosen_stocks, meanReturns)

        # Show Monte Carlo scenario for inputs-based risk profile
        print("\nMonte Carlo scenario for your initial inputs-based risk profile:")
        portfolio_sims1 = monte_carlo_simulation(meanReturns, covMatrix, weights_inputs, duration, investment_amount, monthly_contribution, mc_sims)
        final_portfolio_values1 = portfolio_sims1[-1, :]  # final portfolio values
        final_median1 = np.median(final_portfolio_values1)  # Median of the final portfolio values
        print('Final median portfolio value: $', '{:,.0f}'.format(final_median1))
        plot_results(duration, portfolio_sims1)

        # Portfolio weights for questionnaire-based risk profile
        weights_questionnaire = suggest_portfolio(risk_profile_questionnaire, chosen_stocks, meanReturns)

        # Show Monte Carlo scenario for questionnaire-based risk profile
        print("\nMonte Carlo scenario for your questionnaire-based risk profile:")
        portfolio_sims2 = monte_carlo_simulation(meanReturns, covMatrix, weights_questionnaire, duration, investment_amount, monthly_contribution, mc_sims)
        final_portfolio_values2 = portfolio_sims1[-1, :]  # final portfolio values
        final_median2 = np.median(final_portfolio_values2)  # Median of the final portfolio values
        print('Final median portfolio value: $', '{:,.0f}'.format(final_median2))
        plot_results(duration, portfolio_sims2)

         # User chooses which risk profile to proceed with
        chosen_risk_profile = input("\nChoose which risk profile to proceed with (inputs/questionnaire): ").strip().lower()
        risk_profile_to_use = weights_questionnaire if chosen_risk_profile == 'questionnaire' else weights_inputs
        # portfolio_weights = weights_questionnaire if chosen_risk_profile == 'questionnaire' else weights_inputs
    else:
      # IF THERE IS NO MISMATCH BETWEEN THE QUESTIONNAIRE AND THE INPUTS
        risk_profile_to_use = suggest_portfolio(risk_profile_questionnaire, chosen_stocks, meanReturns)

    # Suggest initial allocation based on risk profile
    suggested_weights = suggest_portfolio(risk_profile_to_use, chosen_stocks, meanReturns) ###1
    print("\nSuggested allocation based on your risk profile:")
    for stock, weight in zip(chosen_stocks, suggested_weights):
        print(f"{stock}: {weight * 100:.2f}%")

   # Ask if the user wants to customize the allocation
    customize = input("\nWould you like to customize the suggested allocation? (yes/no): ").strip().lower()
    if customize == 'yes':
        portfolio_weights = custom_allocation(chosen_stocks)
    else:
        portfolio_weights = suggested_weights

    # Calculate portfolio returns and portfolio risk based on the chosen weights
    port_return = np.dot(meanReturns, portfolio_weights)
    port_risk = np.sqrt(np.dot(portfolio_weights.T, np.dot(covMatrix, portfolio_weights)))

    # Run the Monte Carlo simulation
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


# Example usage:
# profile = risk_tolerance_questionnaire()
# print(f"Your risk profile is: {profile}")

'''
Sample stock symbols and weights:

# AAPL,MSFT,AMZN,0,JPM,BTC-USD
# .15,.15,.15,.1,.1,.1,.1,.05,.05,.05
# 15,15,15,10,10,10,10,5,5,5
'''