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
        for x in Constants.grid_x:
            for y in Constants.grid_y:
                grid.append(
                    {
                        'j': int(x),
                        'i': int(y),
                        'value': int(Constants.grid_value[x][y]),
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
    def vars_for_template(self):
        other_players = self.player.group.get_players()

        opponent_payoff = [player.current_payoff for player in other_players if player != self.player][0]
        return {
            'opponent_payoff': opponent_payoff,
        }


page_sequence = [Instructions] + [GridPlay] +[ResultsWaitPage, Results]
