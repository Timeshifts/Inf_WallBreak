import wall, status, time, shop

SAVE_LOC = 'save/save.txt'

def save():
    f = open(SAVE_LOC, 'w')
    data = dict()
    data['Version'] = 1
    data['Timestamp'] = int(time.time())
    data['Money'] = status.Money.money
    for key, value in status.Stat.stat.items():
        data[f'Stat_{key}'] = value
    data['Level'] = status.Stat.level
    data['Exp'] = status.Stat.exp
    data['SP'] = status.Stat.SP
    data['WallCount'] = wall.Wall.count
    for key, value in shop.shop_item.items():
        data[f'Shop_{key}'] = shop.Shop.items[key - 1].buy
    for key, value in data.items():
        f.write(f'{key}:{value}\n')
    f.close()

def load():
    data = dict()
    try:
        f = open(SAVE_LOC, 'r')
        while True:
            line = f.readline()[:-1]
            if not line: break
            try:
                data[line.split(':')[0]] = int(line.split(':')[1])
            except ValueError:
                try:
                    data[line.split(':')[0]] = float(line.split(':')[1])
                except ValueError:
                    data[line.split(':')[0]] = line.split(':')[1]
        f.close()
    except FileNotFoundError:
        print('[경고] 세이브 파일을 찾지 못했습니다.')
    # print(data)
    if data:
        login_elapsed = int(time.time())-data['Timestamp']
        print(f'{login_elapsed}초만에 다시 오셨네요! 환영합니다!')
        status.Money.money = data['Money']
        for key, value in data.items():
            if key[0:5] == 'Stat_':
                status.Stat.stat[key[5:]] = value
            elif key[0:5] == 'Shop_':
                shop.Shop.items[int(key[5:]) - 1].buy = data[f'Shop_{key[5:]}']
        status.Stat.level = data['Level']
        status.Stat.exp = data['Exp']
        status.Stat.SP = data['SP']
        status.Stat.max = data['Level'] ** 2 + 7 * data['Level'] + 15
        wall.Wall.count = data['WallCount']
        wall.wall_obj.set_difficulty()
        wall.wall_obj.scale_wall(False)
        status.obj.renew_text()
        status.obj.render_self()
        status.money_obj.render_self()