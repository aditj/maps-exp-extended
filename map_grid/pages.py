from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants,Player,Element
import numpy as np
class Instructions(Page):
    def before_next_page(self):
        self.player.current_payoff = 0
class GridPlay(Page):
    form_model = "player"
    form_fields = ['current_x', 'current_y']
    live_method = 'update_element'
    def vars_for_template(self):
        grid = []
        for x in Constants.grid_x:
            for y in Constants.grid_y:
                grid.append(
                    {
                        'x': int(x),
                        'y': int(y),
                        'value': int(Constants.grid_value[x][y]),
                        'occupied': not Element.objects.filter(x=x, y=y,player__in =self.player.group.get_players()).exists()
                    }
                ) 
        other_players = self.player.group.get_players()
        opponent_payoff = [player.current_payoff for player in other_players if player != self.player][0]
        return {
            'grid': grid,
            'opponent_payoff': opponent_payoff,
        }
    def js_vars(self):
        grid = []
        
        for x in Constants.map_x:
            for y in Constants.map_y:
                grid.append(
                    {
                        'j': int(x),
                        'i': int(y),
                        'value': int(Constants.map[x][y]),
                    }
                )

        return {
            'current_chance': self.player.current_chance,
            'data': grid
        }
    def before_next_page(self):
       pass
class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    def js_vars(self):
        grid = []
        
        for x in Constants.map_x:
            for y in Constants.map_y:
                grid.append(
                    {
                        'j': int(x),
                        'i': int(y),
                        'value': int(Constants.map[x][y]),
                    }
                )


        return {
            'current_chance': self.player.current_chance,
            'data': grid
        }
    def vars_for_template(self):
        grid = []
        other_players = self.player.group.get_players()
        opponent = [player for player in other_players if player != self.player][0]
        for x in Constants.grid_x:
            for y in Constants.grid_y:
                player_occupied = False
                opponent_occupied = False
            
                if Element.objects.filter(x=x, y=y,player = self.player).exists():
                    player_occupied = True
                elif Element.objects.filter(x=x, y=y,player = opponent).exists():
                    opponent_occupied = True

                grid.append(
                        {
                            'x': int(x),
                            'y': int(y),
                            'value': int(Constants.grid_value[x][y]),
                            'player_occupied': player_occupied,
                            'opponent_occupied': opponent_occupied,
                        }
                    )
        opponent_payoff = [player.current_payoff for player in other_players if player != self.player][0]
        return {
            'opponent_payoff': opponent_payoff,
            'grid':grid
        }


page_sequence = [Instructions,WaitPage] + [GridPlay] +[ResultsWaitPage, Results]
