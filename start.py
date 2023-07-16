from src import User, Console, weather, solvers
from time import sleep
from config import TOKEN_VK


def status():
    '''
    Конструктор Статуса
    '''
    gorod = 'Ангарск'
    fl = vk.followers(255409704)
    bl = vk.get_black_list()
    msg = vk.get_count_msg('unread')['count']
    like = vk.get_like('photo', 457263374)
    gift = vk.gifts(255409704)
    stick = vk.stiker()
    wth = weather(8, 0, gorod)
    return f'пʏпсᴇнь 🐊\n{wth} \n[Followers: 🤓 {fl}]\n[BL: 😵 {bl}]\n[Not Read: ✉ {msg}]\n[Like Ava: ❤ {like}]\n[Gifts: 🎁 {gift}]\n[Sticker: 🎭 {stick}]'




if __name__ == '__main__':
    vk = User(TOKEN_VK)
    
    try:
        print(f'▶ Установка статуса')
        while True:
            st = status()
            print(st)
            vk.set_status(st, 0)
            print(f'✅ Успешно обновлен')
            print(f'💸 Баланс капчи: {solvers()}')
            sleep(5)
    except Exception as Error:
        Console.log(Error)
        