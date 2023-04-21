from otree.api import *
import random

class C(BaseConstants):
    NAME_IN_URL = 'asset_experiment_with_distribution'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    #CREDIT = 80 # This is sufficient to cover the maximum bidding price of 20 in each of the 4 bidding decisions per round.
    MAX = 20 # Maximum bid.
    NAMES = {
        1: ['K', '', 'K', ''],
    }

    PAYOFFS = {
        1: {'K': 20, 'C': 10, 'H': 20},
    }

    PROJ_PAYOFF_3 = { # Projected payoffs in period 3.
        1: {'K': 13},
    }

    PROJ_PAYOFF_6 = { # Projected payoffs in period 6.
        1: {'K': 13},
    }


class Subsession(BaseSubsession):
    cummulative_earnings = models.IntegerField(initial = 0)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    prob_3 = models.IntegerField(label='',min=0,max=100)
#    prob_3_2= models.IntegerField(label='',min=0,max=100)
    bid_3 = models.IntegerField(label='', min=0, max=20)
#    bid_3_2 = models.IntegerField(label='', min=0, max=20)
    price_3 = models.IntegerField(initial = 0)
#    price_3_2 = models.IntegerField(initial = 0)
    curr_payoff_3 = models.IntegerField(initial = 0) # Projected payoff after period 3 of first asset.
#    curr_payoff_3_2 = models.IntegerField(initial = 0)
    shares_acquired_3 = models.IntegerField(initial=0)  # Shares acquired in the first purchase after period 3.
#    shares_acquired_3_2 = models.IntegerField(initial=0)  # Shares acquired in the second purchase after period 3.
    acquired_3 = models.StringField(initial = 'No') # Yes if shares_aquired_3 is 1, otherwise No.
#    acquired_3_2 = models.StringField(initial = 'No') # Yes if shares_aquired_3_2 is 1, otherwise No.
    payoff_3 = models.IntegerField(initial=0) # Payoff for the first asset purchased after round 3.
#    payoff_3_2 = models.IntegerField(initial=0)  # Payoff for the second asset purchased after round 3.
    earnings_3 = models.IntegerField(initial=0)  # payoff_3 * shares_acquired_3 - price_3
#    earnings_3_2 = models.IntegerField(initial=0)  # payoff_3_2 * shares_acquired_3_2 - price_3_2
    guess_3 = models.IntegerField(label='')  # Subject's guess for the final payout of the first asset they bid on in the first market.
#    guess_3_2 = models.IntegerField(label='')

    prob_6 = models.IntegerField(label='',min=0,max=100)
#    prob_6_2= models.IntegerField(label='',min=0,max=100)
    bid_6 = models.IntegerField(label='', min=0, max=20)
#    bid_6_2 = models.IntegerField(label='', min=0, max=20)
    price_6 = models.IntegerField(initial = 0)
#    price_6_2 = models.IntegerField(initial = 0)
    curr_payoff_6 = models.IntegerField(initial = 0) # Projected payoff after period 3 of first asset.
#    curr_payoff_6_2 = models.IntegerField(initial = 0)
    shares_acquired_6 = models.IntegerField(initial=0)  # Shares acquired in the first purchase after period 6.
#    shares_acquired_6_2 = models.IntegerField(initial=0)  # Shares acquired in the second purchase after period 6.
    acquired_6 = models.StringField(initial = 'No') # Yes if shares_aquired_6 is 1, otherwise No.
#    acquired_6_2 = models.StringField(initial = 'No') # Yes if shares_aquired_6_2 is 1, otherwise No.
    payoff_6 = models.IntegerField(initial=0) # Payoff for the first asset purchased after round 6.
#    payoff_6_2 = models.IntegerField(initial=0) # Payoff for the second asset purchased after round 6.
    earnings_6 = models.IntegerField(initial=0)
#    earnings_6_2 = models.IntegerField(initial=0)
    guess_6 = models.IntegerField(label='')  # Subject's guess for the final payout of the first asset they bid on in the second market.
#    guess_6_2 = models.IntegerField(label='')

    earnings = models.IntegerField(initial=0) # Earnings for the round from asset payoffs.
    earnings_1 = models.IntegerField(initial=0) # Total earnings from the first market.
    earnings_2 = models.IntegerField(initial=0) # Total earnings from the second market.
    earnings_from_guess_1 = models.IntegerField(initial=0)  # Earnings from correct payoff guesses in the first round. +/- 1 is okay.
    earnings_from_guess_2 = models.IntegerField(initial=0)  # Earnings from correct payoff guesses in the first round. +/- 1 is okay.

    asset_3 = models.StringField(initial='') # Name of tne first asset that could be picked at the end of round 3.
#    asset_3_2 = models.StringField(initial='') # Name of the second asset that could be picked at the end of round 3.
    asset_6 = models.StringField(initial='') # Name of asset that could be picked at the end of round 6.
#    asset_6_2 = models.StringField(initial='') # Name of asset that could be picked at the end of round 6.

    final_earnings = models.IntegerField(initial=0)



# FUNCTIONS
# PAGES
class Intro(Page):
    def vars_for_template(player: Player):
        current_round = player.round_number + 10
        return{
            'current_round': current_round
        }



class Bid1(Page):

    def vars_for_template(player: Player):
       player.asset_3 = C.NAMES[player.round_number][0]  # The name of the first asset that can be purchased after period 3.
#       player.asset_3_2 = C.NAMES[player.round_number][1] # The name of the second asset that can be purchased after period 3.

       player.payoff_3 = C.PAYOFFS[player.round_number][player.asset_3]  # The payoff of the frist asset that can be purchased after period 3.
#       player.payoff_3_2 = C.PAYOFFS[player.round_number][player.asset_3_2]  # The payoff of the second asset that can be purchased after period 3.

       player.curr_payoff_3 = C.PROJ_PAYOFF_3[player.round_number][player.asset_3]
#       player.curr_payoff_3_2 = C.PROJ_PAYOFF_3[player.round_number][player.asset_3_2]

       return dict(
          image_path1 = 'asset_experiment_cliff_nelson/asset_movements_with_distribution_1_part1.jpg',
          image_path2 = 'asset_experiment_cliff_nelson/asset_movements_with_distribution_part1_graph.jpg',
          image_path3 = 'asset_experiment_cliff_nelson/10000_simulation_results.jpg'

       )
    form_model = 'player'
    form_fields = ['prob_3','guess_3','bid_3']

class Bid2(Page):
    def vars_for_template(player: Player):
        player.asset_6 = C.NAMES[player.round_number][2]  # The name of the first asset that can be purchased after period 6.
#        player.asset_6_2 = C.NAMES[player.round_number][3]  # The name of the second asset that can be purchased after period 6.

        player.payoff_6 = C.PAYOFFS[player.round_number][player.asset_6]  # The payoff of the frist asset that can be purchased after period 3.
#        player.payoff_6_2 = C.PAYOFFS[player.round_number][player.asset_6_2]  # The payoff of the second asset that can be purchased after period 3.

        player.curr_payoff_6 = C.PROJ_PAYOFF_6[player.round_number][player.asset_6]
#        player.curr_payoff_6_2 = C.PROJ_PAYOFF_6[player.round_number][player.asset_6_2]

        return dict(
            image_path1 = 'asset_experiment_cliff_nelson/asset_movements_with_distribution_1_part2.jpg',
            image_path2 = 'asset_experiment_cliff_nelson/asset_movements_with_distribution_part2_graph.jpg',
            image_path3 = 'asset_experiment_cliff_nelson/10000_simulation_results_6.jpg'

        )
    form_model = 'player'
    form_fields = ['prob_6','guess_6','bid_6',]

class Results1(Page):
    @staticmethod
    def vars_for_template(player: Player):
        ran_int = random.randint(1,C.MAX)
        purchase_3 = (ran_int<=player.bid_3)

        if purchase_3:
            player.price_3 = ran_int
            player.shares_acquired_3 = 1
            player.acquired_3 = "Yes"
            statement = "Since " + str(ran_int) +" is less than or equal to your bid, you puchased 1 unit of asset " + player.asset_3 + " at the price of " + str(player.price_3) +"."
        else:
            player.shares_acquired_3 = 0
            statement = "Since " + str(ran_int) + " is greater than your bid, you did not purchase any units of asset " + player.asset_3 + "."


        return{
            "ran_int":ran_int,
            "statement":statement,
        }



class Results2(Page):
    @staticmethod
    def vars_for_template(player: Player):
        ran_int = random.randint(1,C.MAX)
        purchase_6 = (ran_int <= player.bid_6)

        if purchase_6:
            player.price_6 = ran_int
            player.shares_acquired_6 = 1
            player.acquired_6 = "Yes"
            statement = "Since " + str(ran_int) +" is less than or equal to your bid, you puchased 1 unit of asset " + player.asset_6 + " at the price of " + str(player.price_6) +"."
        else:
            player.shares_acquired_6 = 0
            statement = "Since " + str(ran_int) + " is greater than your bid, you did not purchase any units of asset " + player.asset_6 + "."


        return{
            "ran_int":ran_int,
            "statement":statement,
        }



class CombinedResults(Page):
    @staticmethod
    def vars_for_template(player: Player):

        player.earnings_3 = player.payoff_3 * player.shares_acquired_3 - player.price_3
        #player.earnings_3_2 = player.payoff_3_2 * player.shares_acquired_3_2 - player.price_3_2
        player.earnings_6 = player.payoff_6 * player.shares_acquired_6 - player.price_6
        #player.earnings_6_2 = player.payoff_6_2 * player.shares_acquired_6_2  - player.price_6_2


        player.earnings = player.earnings_3 + player.earnings_6

        player.earnings_from_guess_1 = 0
        player.earnings_from_guess_2 = 0

        if abs(player.guess_3 - player.payoff_3) < 2:
            player.earnings_from_guess_1 += 1
        #if abs(player.guess_3_2 - player.payoff_3_2) < 2:
        #    player.earnings_from_guess_1 += 1
        if player.guess_6 == player.payoff_6:
            player.earnings_from_guess_2 += 1
        #if player.guess_6_2 == player.payoff_6_2:
        #    player.earnings_from_guess_2 += 1

        player.earnings_1 = player.earnings_3 + player.earnings_from_guess_1
        player.earnings_2 = player.earnings_6 + player.earnings_from_guess_2

        player.earnings = player.earnings_1 + player.earnings_2

        player.final_earnings = player.participant.vars['final_earnings'] + player.participant.vars['final_earnings_app2'] + player.earnings

        player.participant.vars['final_earnings_bonus'] = player.earnings

        return dict(
            image_path= 'asset_experiment_cliff_nelson/asset_movements_with_distribution_1_part3.jpg'
        )

page_sequence = [Intro, Bid1 , Results1, Bid2, Results2, CombinedResults]
