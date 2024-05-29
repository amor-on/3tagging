class Navigation:
    def __init__(self, contents):
        self.contents = contents
        self.current_card_index = 0
        self.current_block_index = 0
        self.view = 'card'  # 'card' or 'block'
        self.card_titles = contents['card_title'].unique().tolist()
        self.blocks_per_card = {card: contents[contents['card_title'] == card].index.tolist() for card in self.card_titles}

    def get_card_titles(self):
        return self.card_titles

    def get_current_card(self):
        return self.card_titles[self.current_card_index]

    def get_current_block(self):
        current_card = self.get_current_card()
        return self.blocks_per_card[current_card][self.current_block_index]

    def previous_card(self):
        if self.current_card_index > 0:
            self.current_card_index -= 1
            self.current_block_index = 0
            self.view = 'card'
        return self.get_current_card()

    def next_card(self):
        if self.current_card_index < len(self.card_titles) - 1:
            self.current_card_index += 1
            self.current_block_index = 0
            self.view = 'card'
        return self.get_current_card()

    def previous_block(self):
        if self.current_block_index > 0:
            self.current_block_index -= 1
        return self.get_current_block()

    def next_block(self):
        if self.current_block_index < len(self.blocks_per_card[self.get_current_card()]) - 1:
            self.current_block_index += 1
        else:
            self.next_card()
        return self.get_current_block()

    def start_block_labeling(self):
        self.view = 'block'

    def is_labeling_blocks(self):
        return self.view == 'block'

    def save_progress(self, filepath):
        self.contents.to_csv(filepath, index=False)
