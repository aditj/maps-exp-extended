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
from otreeutils.admin_extensions import custom_export


author = 'Adit Jain'

doc = """
Map Experiment 2 D
"""
import numpy as np

class Constants(BaseConstants):
    name_in_url = 'map_grid'
    players_per_group = 2
    num_rounds = 1
    max_turns = 16
    grid_size = (7, 7)
    grid_dim = grid_size[0]
    grid_x = np.arange(grid_size[0],dtype=int)
    grid_y = np.arange(grid_size[1],dtype=int)
    grid_value = [
    [1,6,6,1,1,6,1],
    [1,6,6,1,1,6,1],
    [1,1,1,6,1,1,1],
    [1,1,10,1,1,6,1],
    [1,1,1,1,1,1,6],
    [10,1,1,1,6,1,6],
    [6,1,6,1,1,1,6],
]   
     
    map =[[29., 34., 24., 24., 19.],
       [28., 33., 28., 24., 19.],
       [18., 23., 23., 19., 19.],
       [27., 18., 23., 19., 29.],
       [28., 14., 19., 14., 29.]]
     
    map_dim = (len(map), len(map[0]))
    map_x = np.arange(map_dim[0],dtype=int)
    map_y = np.arange(map_dim[1],dtype=int)

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
    