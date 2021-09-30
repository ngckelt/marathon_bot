from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

pagination_callback = CallbackData('paginator', 'key', 'page')


class Paginator:

    def __init__(self, prefix, key):
        self.btns_list = list()
        self.key = key
        self.callback_data = CallbackData(prefix, 'key', 'page')

    def add_btn(self, text: str, callback_data):
        self.btns_list.append(
            InlineKeyboardButton(
                text=text,
                callback_data=callback_data
            )
        )

    def create_markup(self, max_items: int, curr_page: int = 1, items_per_page: int = 1,
                      optional_btns: list = None):
        markup = InlineKeyboardMarkup()
        first_page = 1
        if items_per_page != 1:
            if max_items % 2 == 0:
                last_page = max_items // items_per_page
            else:
                last_page = max_items // items_per_page + 1
        else:
            last_page = max_items
        next_page = curr_page + 1
        prev_page = curr_page - 1

        if last_page == 1:
            if optional_btns:
                for btn in optional_btns:
                    markup.add(btn)
                return markup
            return None

        if curr_page > 1:
            if curr_page == 2:
                self.add_btn('< 1', self.callback_data.new(key=self.key, page=first_page))
                self.add_btn(f'{curr_page}', self.callback_data.new(key=self.key, page='curr_page'))
                if next_page < last_page:
                    self.add_btn(f'{next_page} >', self.callback_data.new(key=self.key, page=next_page))
                if next_page == last_page:
                    self.add_btn(f'{last_page} >', self.callback_data.new(key=self.key, page=last_page))
                if curr_page + 1 < last_page:
                    self.add_btn(f'{last_page} >>', self.callback_data.new(key=self.key, page=last_page))

            elif curr_page + 1 == last_page:
                self.add_btn('<< 1', self.callback_data.new(key=self.key, page=first_page))
                self.add_btn(f'< {prev_page}', self.callback_data.new(key=self.key, page=prev_page))
                self.add_btn(f'{curr_page}', self.callback_data.new(key=self.key, page='curr_page'))
                self.add_btn(f'{last_page} >', self.callback_data.new(key=self.key, page=last_page))

            elif curr_page == last_page:
                self.add_btn('<< 1', self.callback_data.new(key=self.key, page=first_page))
                self.add_btn(f'< {prev_page}', self.callback_data.new(key=self.key, page=prev_page))
                self.add_btn(f'{curr_page}', self.callback_data.new(key=self.key, page='curr_page'))
            else:
                self.add_btn('<< 1', self.callback_data.new(key=self.key, page=first_page))
                self.add_btn(f'< {prev_page}', self.callback_data.new(key=self.key, page=prev_page))
                self.add_btn(f'{curr_page}', self.callback_data.new(key=self.key, page='curr_page'))

                if next_page < last_page:
                    self.add_btn(f'{next_page} >', self.callback_data.new(key=self.key, page=next_page))
                self.add_btn(f'{last_page} >>', self.callback_data.new(key=self.key, page=last_page))
        else:
            self.add_btn('1', self.callback_data.new(key=self.key, page='curr_page'))
            if next_page < last_page:
                self.add_btn(f'{next_page} >', self.callback_data.new(key=self.key, page=next_page))
            if next_page == last_page:
                self.add_btn(f'{last_page} >', self.callback_data.new(key=self.key, page=last_page))
            else:
                self.add_btn(f'{last_page} >>', self.callback_data.new(key=self.key, page=last_page))

        if optional_btns:
            for btn in optional_btns:
                markup.add(btn)

        return markup.row(*self.btns_list)
