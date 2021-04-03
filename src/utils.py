def prefilter_items(data,
                    low_price=60,
                    high_price=1000):
    # Уберем самые популярные товары (их и так купят)
    popularity = data.groupby('item_id')['user_id'].nunique().reset_index() / data['user_id'].nunique()
    popularity.rename(columns={'user_id': 'share_unique_users'}, inplace=True)

    top_popular = popularity[popularity['share_unique_users'] > 0.5].item_id.tolist()
    data = data[~data['item_id'].isin(top_popular)]

    # Уберем самые НЕ популярные товары (их и так НЕ купят)
    top_notpopular = popularity[popularity['share_unique_users'] < 0.01].item_id.tolist()
    data = data[~data['item_id'].isin(top_notpopular)]

    # Уберем товары, которые не продавались за последние 12 месяцев
    not_sold_52 = data[data['week_no'] > (max(data['week_no']) - 52)].item_id.tolist()
    data = data[~data['item_id'].isin(not_sold_52)]

    # Уберем не интересные для рекоммендаций категории (department)
    # data = data.merge(product[['department', 'item_id']], how='left', on='item_id')

    # Уберем слишком дешевые товары (на них не заработаем). 1 покупка из рассылок стоит 60 руб.
    too_cheap = data[data['price'] < low_price].item_id.tolist()
    data = data[~data['item_id'].isin(too_cheap)]

    # Уберем слишком дорогие товары
    too_expensive = data[data['price'] > high_price].item_id.tolist()
    data = data[~data['item_id'].isin(too_expensive)]

    # ...


def postfilter_items(user_id, recommednations):
    pass
