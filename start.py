from src import User, Console, weather, solvers
from time import sleep
from config import TOKEN_VK


def status():
    '''
    Конструктор Статуса
    '''

    gorod = 'Ангарск'
    fl = vk.followers(YOUR_ID)
    bl = vk.get_black_list()
    msg = vk.get_count_msg('unread')['count']
    like = vk.get_like('photo', YOU_ID_PHOTO)
    gift = vk.gifts(YOUR_ID)
    stick = vk.stiker()
    wth = weather(8, 0, gorod)
    text = f'пʏпсᴇнь 🐊\n{wth} \n[Followers: 🤓 {fl}]\n[BL: 😵 {bl}]\n[Not Read: ✉ {msg}]\n[Like Ava: ❤ {like}]\n[Gifts: 🎁 {gift}]\n[Sticker: 🎭 {stick}]'
    return text




if __name__ == '__main__':
    vk = User(TOKEN_VK)
    
    try:
        while True:
            st = status()
            vk.set_status(st, 0)
            sleep(5)
    except Exception as Error:
        Console.log(Error)
        