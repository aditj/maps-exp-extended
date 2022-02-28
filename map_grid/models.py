from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


author = 'Adit Jain'

doc = """
Your app description
"""
import numpy as np

class Constants(BaseConstants):
    name_in_url = 'map_grid'
    players_per_group = 2
    num_rounds = 1
    
    grid_size = (5, 5)
    grid_dim = grid_size[0]
    grid_x = np.arange(grid_size[0],dtype=int)
    grid_y = np.arange(grid_size[1],dtype=int)
    grid_value = [
        [1,2,4,1,3,5,2,1,3,4],
        [2,3,1,4,2,1,3,4,5,2],
        [4,1,3,2,5,3,1,2,4,5],
        [1,4,2,3,1,5,4,3,2,5],
        [3,2,5,1,4,2,5,1,3,4],
        [5,3,4,2,1,4,3,2,5,1],
        [2,1,3,5,3,2,4,1,5,3],
        [3,4,1,2,5,1,2,3,4,5],
        [1,2,5,4,2,3,1,5,3,4],
        [4,5,2,1,3,5,4,2,1,3]
    ]

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass



class Player(BasePlayer):
    name = models.StringField()
    chance = models.IntegerField(min=0, max=1)
    points = models.IntegerField()
    current_x = models.IntegerField()
    current_y = models.IntegerField()
    current_payoff = models.IntegerField(  default=0)
    current_chance = models.IntegerField(  default=0)

    

class Element(models.Model):
    value = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    player = models.Link(Player)
    class CustomModelConf:
            """
            Configuration for otreeutils admin extensions.
            """

            data_view = {  # define this attribute if you want to include this model in the live data view
                "link_with": "player"
            }
            export_data = {  # define this attribute if you want to include this model in the data export
                "link_with": "player"
            }

def update_element(self,data):
    x = int(data['current_x'])
    y = int(data['current_y'])
    value = int(Constants.grid_value[x][y])
    self.current_payoff += value
    for player in self.group.get_players():
        player.current_chance += 1
        if player!=self:
            opponent_id = player.id_in_group
            opponent_payoff = player.current_payoff


    e = Element(value = value, x=  x,y =  y,player = self)
    e.save()
    return {self.id_in_group:{
       "data":data,
        "was_opponent":0,
        "player_payoff":self.current_payoff,
        "current_chance":self.current_chance,
        "element_value":value,
    },
    opponent_id:{
        "data":data,
        "was_opponent":1,
        "opponent_payoff":self.current_payoff,
        "current_chance":self.current_chance,
        "element_value":value,
    }}


Player.update_element = update_element
    