from vk_api import VkApi

from traceback import format_exc

from time import sleep

from datetime import datetime, timedelta, timezone

from python3_anticaptcha import ImageToTextTask, AntiCaptchaControl

from config import TOKEN_CAPT, TOKEN_OWM

from pyowm import OWM

from pyowm.utils.config import get_default_config




acc = AntiCaptchaControl.AntiCaptchaControl(TOKEN_CAPT)

class Console:
    @staticmethod
    def log(message, sender="SYSTEM"):
        """
        Вывод даты, времени и сообщения в консоль. Запись в файл logs.txt
        """
        time = datetime.now().strftime("%H:%M:%S")
        date = datetime.now().strftime("%d.%m.%y")
        if sender == "ERROR":
            line = format_exc().split(", line ")[1].split(",")[0]
            msg = f"{date} | ({time}) [ERROR] >> {message} (line {line})"
        else:
            msg = f"{date} | ({time}) [{sender}] >> {message}"
        print(msg)
        with open("logs.txt", "a", encoding="utf-8") as file:
            file.write(f"{msg}\n")

class User:
    def __init__(self, token) -> None:
        """
        Авторизация пользователя
        """
        try:
            self.session = VkApi(
                token=token,
                captcha_handler=self.solver
            )
        except Exception as AuthError:
            Console.log(f"Ошибка вторизации: {AuthError}")
        else:
            Console.log("Авторизация прошла успешно")

    def solver(self, captcha):
        """
        Решение капчи Вконтакте
        """
        answer = ImageToTextTask(TOKEN_CAPT).captcha_handler(captcha.get_url())
        Console.log("Капча Вконтакте решена")
        return captcha.try_again(answer['solution']['text'])

    def set_status(self, status: str, group_id: None):
        '''
        params: status - Ваш статус
        params: group_id - Указывайте если необходимо менять в сообществе, если на страницу то указываем 0
                    Пример group_id  -1111111111
        '''
        status = self.session.method(
            'status.set', {
                'text' : status,
                'group_id' : group_id

            }
        )

        return status

    def stiker(self):
        '''
        Возвращает количество купленных стикеров
        '''
        get_stik = self.session.method(
            'store.getProducts', {
                'type' : 'stickers',
                'filters' : 'purchased'
            }
        )
        
        return get_stik['count']
    

    def followers(self, user_id: int):
        '''
        params user_id: указываем айди своей страницы
        показывает количество подписчиков MAX 1000 подписчиков
        '''
        folower = self.session.method(
            'users.getFollowers', {
                'user_id' : user_id
            }
        )

        return folower['count']
    
    def get_count_msg(self, filters : str):
        '''
        params filters: all - получить все сообщения
                        unread - только не прочитаные
        '''
        count = self.session.method(
            'messages.getConversations', {
                #'count': count,
                'filter': filters
            }
        )

        return count

    def get_like(self, types: str, item_id: int):
        
        '''
        type:
            string

            Тип объекта. Возможные типы:



            •
            post — запись на стене пользователя или сообщества.

            •
            post_ads — рекламная запись.

            •
            comment — комментарий к записи на стене.

            •
            photo — фотография.

            •
            video — видеозапись.

            •
            note — заметка.

            •
            market — товар.

            •
            photo_comment — комментарий к фотографии.

            •
            video_comment — комментарий к видеозаписи.

            •
            topic_comment — комментарий в обсуждении.

            •
            market_comment — комментарий к товару.

            item_id: 
                int
                Указываем ID того от куда считать лайки
        '''

        like = self.session.method(
            'likes.getList', {
                'type' : types,
                'item_id' : item_id
            }
        )

        return like['count']

    def gifts(self, user_id):
        '''
        Возвращает количество подарков
        '''
        gift = self.session.method(
            'gifts.get', {
                'user_id' : user_id
            }
        )
        
        return gift['count']
    
    def get_black_list(self):
        '''
        
        '''
        blacklist = self.session.method(
            'account.getBanned'
        )

        return blacklist['count']


pic = [
    "0⃣","1⃣","2⃣","3⃣","4⃣","5⃣","6⃣","7⃣","8⃣","9⃣"
    ]

def times(hours, minutes):
    while True:
        timezn = timedelta(hours=hours, minutes=minutes)
        times = (datetime.now(timezone.utc) + timezn)
        timeset = times.strftime('%H:%M')
        time_nower = ""
        time_nower += pic[int(timeset[0])]
        time_nower += pic[int(timeset[1])]
        time_nower += ":"
        time_nower += pic[int(timeset[3])]
        time_nower += pic[int(timeset[4])]
        sleep(1)
        return time_nower

def weather(hours: float, minutes:float, gorod:str):
    '''
    params hours
    params minutes
    Укаывается часовой пояс

    params gorod:
        Указываем город
    '''
    timers = times(hours, minutes)
    config_dict = get_default_config()
    config_dict['language'] = 'ru'
    owm = OWM(TOKEN_OWM, config_dict)   
    mgr = owm.weather_manager()
    gorod = gorod
    search = mgr.weather_at_place(gorod).weather
    temp = search.temperature("celsius")['temp']
    return f'{gorod} \n🌡: {temp}°C \n🕐: {timers}'

def solvers():
    '''
    Возвращает баланс антикапчи
    '''
    money_balance = acc.get_balance()['balance']

    return money_balance

print(solvers())