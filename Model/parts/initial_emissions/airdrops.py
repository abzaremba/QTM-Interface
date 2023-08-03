import pandas as pd

# POLICIY FUNCTIONS
def airdrops(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to incentivise the ecosystem
    """
    # get parameters
    total_token_supply = params['initial_total_supply']
    airdrop_allocation = params['airdrop_allocation']
    airdrop_date1 = pd.to_datetime(params['airdrop_date1'], format='%d.%m.%y')
    airdrop_date2 = pd.to_datetime(params['airdrop_date2'], format='%d.%m.%y')
    airdrop_date3 = pd.to_datetime(params['airdrop_date3'], format='%d.%m.%y')
    airdrop_amount1 = params['airdrop_amount1']
    airdrop_amount2 = params['airdrop_amount2']
    airdrop_amount3 = params['airdrop_amount3']

    # get state variables
    current_date = pd.to_datetime(prev_state['date'])

    # policy logic
    # calculate airdrop amounts
    airdrop_tokens = 0
    # check if current month is airdrop month
    if current_date <= airdrop_date1 and current_date+pd.DateOffset(months=1) > airdrop_date1:
        airdrop_tokens += total_token_supply * airdrop_allocation/100 * airdrop_amount1/100
    if current_date <= airdrop_date2 and current_date+pd.DateOffset(months=1) > airdrop_date2:
        airdrop_tokens += total_token_supply * airdrop_allocation/100 * airdrop_amount2/100
    if current_date <= airdrop_date3 and current_date+pd.DateOffset(months=1) > airdrop_date3:
        airdrop_tokens += total_token_supply * airdrop_allocation/100 * airdrop_amount3/100

    return {'airdrop_tokens': airdrop_tokens}

# STATE UPDATE FUNCTIONS
def update_agents_after_airdrops(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the vested tokens for each investor based on some criteria
    """
    # get parameters

    # get state variables
    updated_agents = prev_state['agents']

    # get policy input
    airdrop_tokens = policy_input['airdrop_tokens']

    # update logic
    # add airdropped tokens to airdrop receivers stakeholder group
    investors = sum([1 for agent in updated_agents if (updated_agents[agent]['type'] == 'airdrop_receivers')])
    for agent in updated_agents:
        if updated_agents[agent]['type'] == 'airdrop_receivers':
            updated_agents[agent]['tokens'] = updated_agents[agent]['tokens'] + airdrop_tokens / investors

    return ('agents', updated_agents)

def update_token_economy_after_airdrops(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the token economy after incentivisation
    """
    # get parameters

    # get state variables
    updated_token_economy = prev_state['token_economy'].copy()
    liquidity_pool = prev_state['liquidity_pool']

    # get policy input
    airdrop_tokens = policy_input['airdrop_tokens']

    # update logic
    updated_token_economy['airdrop_tokens'] = airdrop_tokens
    updated_token_economy['airdrop_tokens_cum'] += airdrop_tokens
    updated_token_economy['airdrop_tokens_usd'] = airdrop_tokens * liquidity_pool['token_price']

    return ('token_economy', updated_token_economy)