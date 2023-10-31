import pandas as pd

#This is the test csv I used but should work with any pnow csv files.
df = pd.read_csv('ledger.csv')

df = df.drop(columns=['session_start_at', 'session_end_at', 'stack', 'buy_out'])
df['net'] = df['net']/100
df['buy_in'] = df['buy_in']/100

df = df.rename(columns={
    'player_nickname': 'name',
    'player_id': 'id'
})
df = df.groupby('id', as_index=False).agg({
    'name': 'first',
    'buy_in': 'sum',
    'net': 'sum'
})
df= df.sort_values(by='net', ascending=False)
df = df.drop(columns=['buy_in'])
print("Full graph:")
print(df)
winners_df = df[df['net'] > 0]
losers_df = df[df['net'] < 0]
print("Winners:")
print(winners_df)
print("\nLosers:")
print(losers_df)

winners_df = winners_df.sort_values(by='net', ascending=False).reset_index(drop=True)
losers_df = losers_df.sort_values(by='net').reset_index(drop=True) # Smallest (most negative) first

transactions = []

for loser_index, loser_row in losers_df.iterrows():
    loser_amount = abs(loser_row['net'])
    
    winner_index = 0
    while loser_amount > 0 and winner_index < len(winners_df):
        winner_row = winners_df.loc[winner_index]
        
        transfer_amount = min(winner_row['net'], loser_amount)
        
        transactions.append({
            'from': loser_row['name'],
            'to': winner_row['name'],
            'amount': transfer_amount
        })
        
        loser_amount -= transfer_amount
        winners_df.at[winner_index, 'net'] -= transfer_amount
        
        if winners_df.at[winner_index, 'net'] == 0:
            winner_index += 1
            
for transaction in transactions:
    if transaction['amount'] > 0:
        print(f"{transaction['from']} pays {transaction['to']} ${transaction['amount']:.2f}")
