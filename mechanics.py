import random
import numpy as np
import pandas as pd
import datetime

# число игроков в команде
n = 6

# поправки на взятие вопроса
# мысленный прыжок
k_jump = 0.30
# докрут
k_help = 0.45
mods = 1

# в каком диапазоне генерируется навык
skill_rage1 = 40
skill_rage2 = 60

# в каком диапазоне генерируется эгоистичность
ego_rage1 = 40
ego_rage2 = 90

# в каком диапазоне генерируется случайная добавка
rnd_rage1 = 30
rnd_rage2 = 120

# в каком диапазоне генерируется сложность
dif_rage1 = 60
dif_rage2 = 60



# даёшь вероятность, а она выдаёт, вышло или нет
def get_rand(propability):
    base_random = random.randint(0, 9999)
    
    if float(base_random) < 10000 * propability:
        res = 1
    else:
        res = 0
    
    return res

# класс продукта      
class gamer:
    def __init__(
                self, 
                id=-1, 
                # skill=0, 
                # ego=60
                ):
        self.id = id
        self.skill = round(random.randint(skill_rage1, skill_rage2),2)
        self.ego = round(random.randint(ego_rage1, ego_rage2),2)
        
    # отображаем все параметры в виду dataframe
    def to_df(self):
        df=pd.DataFrame(data=[self.__dict__.values()], columns=self.__dict__.keys())
        return df
    

def create_team():
    gamers_lst = []
    for i in range(n):
        gamer_itm = gamer(i)
        gamers_lst.append(gamer_itm)
    return gamers_lst

def minute(gamers_lst, difficult):
    res = 0
    jump_lst = []
    help_lst = []

    # мысленный прыжок
    for i in range(n):
        # качество версии конкретного игрока на конкретном вопросе
        version_rage = round(
                                # в основе - навык игрока
                                gamers_lst[i].skill * \
                                # вероятность того, что версия родится, зависит от его эгоистичности
                                (get_rand(k_jump * (gamers_lst[i].ego) / 100)) * \
                                # и немного случайных блужданий
                                random.randint(rnd_rage1, rnd_rage2) / 100, 
                                2
                            )
        jump_lst.append(version_rage)
    jump_value = np.max(jump_lst)

    # докрут
    for i in range(n):
        # качество докрута конкретного игрока на конкретном вопросе
        help_rage = round(
                                # в основе - навык игрока
                                gamers_lst[i].skill * \
                                # вероятность того, что версия докрутится, зависит от его альтруистичности
                                (get_rand(k_help * (100 - gamers_lst[i].ego) / 100)) * \
                                # и немного случайных блужданий
                                random.randint(rnd_rage1, rnd_rage2) / 100, 
                                2
                            )
        help_lst.append(help_rage)
    help_value = np.max(help_lst)
    
    # определяем взятие
    team_value = round(jump_value + help_value,2)
    if team_value >= difficult:
        res = 1
    else:
        res = 0

    return res, jump_lst, help_lst, jump_value, help_value, team_value