import pandas as pd

data = {'fund_name': ['Alpha Quantum Fund 1', 'Alpha Quantum Fund 2', 'Alpha Quantum Fund 3', 'Alpha Quantum Fund 4', 'Alpha Quantum Fund 5', 'Alpha Quantum Fund 6', 'Alpha Quantum Fund 7', 'Alpha Quantum Fund 8', 'Alpha Quantum Fund 9', 'Alpha Quantum Fund 10', 'Alpha Quantum Fund 11', 'Alpha Quantum Fund 12', 'Alpha Quantum Fund 13', 'Alpha Quantum Fund 14', 'Alpha Quantum Fund 15', 'Beta Steady Growth 1', 'Beta Steady Growth 2', 'Beta Steady Growth 3', 'Beta Steady Growth 4', 'Beta Steady Growth 5', 'Beta Steady Growth 6', 'Beta Steady Growth 7', 'Beta Steady Growth 8', 'Beta Steady Growth 9', 'Beta Steady Growth 10', 'Beta Steady Growth 11', 'Beta Steady Growth 12', 'Beta Steady Growth 13', 'Beta Steady Growth 14', 'Beta Steady Growth 15', 'Gamma Defensive Allocation 1', 'Gamma Defensive Allocation 2', 'Gamma Defensive Allocation 3', 'Gamma Defensive Allocation 4', 'Gamma Defensive Allocation 5', 'Gamma Defensive Allocation 6', 'Gamma Defensive Allocation 7', 'Gamma Defensive Allocation 8', 'Gamma Defensive Allocation 9', 'Gamma Defensive Allocation 10'], 'risk_grade': ['High', 'High', 'High', 'High', 'High', 'High', 'High', 'High', 'High', 'High', 'High', 'High', 'High', 'High', 'High', 'Moderate', 'Moderate', 'Moderate', 'Moderate', 'Moderate', 'Moderate', 'Moderate', 'Moderate', 'Moderate', 'Moderate', 'Moderate', 'Moderate', 'Moderate', 'Moderate', 'Moderate', 'Low', 'Low', 'Low', 'Low', 'Low', 'Low', 'Low', 'Low', 'Low', 'Low'], 'latest_sharpe': [-1.2353277218237488, 2.728703521110678, 1.4259276504129073, -0.5126041364740223, 0.007923754547101867, 0.7863298963139138, 1.329415341229613, 1.2445299808312806, -0.0842036398383796, 1.1582087308253655, -3.0461640541224817, 0.7526032425393302, -0.18172087600364112, 1.6081421115260597, 0.456871053489776, 2.8725135694275257, -1.9690496133854885, 1.5346250651378304, 1.8127617223883312, 1.2861108312088354, 0.36366971149939537, 1.08089566017559, 0.39225093289840324, -2.7016303415939773, 5.709601424933037, -0.22965195209567116, -1.2616872690674614, 1.9262488702963627, -1.0569259651184117, -0.8663383683628101, 1.0511724545996395, 1.32371471097957, 3.8625150946711457, 0.7190796464842327, 1.5949281667641135, 2.951462373015161, 2.825066649488264, -0.5048358344320795, 0.5116048722981307, 1.0471906741187114]}
df_rec = pd.DataFrame(data)

def get_recommendation(risk_appetite):
    risk_appetite = risk_appetite.strip().capitalize()
    if risk_appetite not in ['Low', 'Moderate', 'High']:
        print("Invalid input. Select from: Low, Moderate, High")
        return None

    filtered = df_rec[df_rec['risk_grade'] == risk_appetite]
    top_3 = filtered.sort_values(by='latest_sharpe', ascending=False).head(3).copy()
    top_3.columns = ['Fund Name', 'Risk Profile', 'Latest Sharpe Ratio']

    print(f"\n=== TOP 3 RECOMMENDATIONS FOR {risk_appetite.upper()} RISK PROFILE ===")
    print(top_3.to_string(index=False))
    return top_3

if __name__ == '__main__':
    user_input = input("Enter your Risk Appetite (Low / Moderate / High): ")
    get_recommendation(user_input)