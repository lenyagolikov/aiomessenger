cache = {}


def mem_cache(handler):
    """Возвращает сообщения из кэша. Если данных нет - сохраняет их в кэш"""
    async def inner(async_session, chat_id, from_, cursor):
        if chat_id not in cache:
            messages = await handler(async_session, chat_id, from_, cursor)
            cache[chat_id] = {(from_, cursor): messages}
        else:
            for interval in cache[chat_id]:
                if interval[0] <= from_ <= interval[1] and interval[0] <= cursor <= interval[1]:
                    messages = cache[chat_id][interval][from_ - 1:cursor]
                    break
            else:
                messages = await handler(async_session, chat_id, from_, cursor)
                cache[chat_id].update({(from_, cursor): messages})
        return messages
    return inner


def invalidate_cache(handler):
    """Инвалидирует кэш, если новое сообщения попадает под интервал сохраненного кэша"""
    async def inner(*args, **kwargs):
        message_id = await handler(*args, **kwargs)
        _, chat_id, *_ = args

        prepare_for_removal = []

        if chat_id in cache:
            for interval in cache[chat_id]:
                if interval[0] <= message_id <= interval[1]:
                    prepare_for_removal.append(interval)

            for interval in prepare_for_removal:
                del cache[chat_id][interval]

            if not cache[chat_id]:
                del cache[chat_id]
        return message_id
    return inner
