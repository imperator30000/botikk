from random import shuffle, choice


class Card:
    def __init__(self, num, mast, invis=False):
        self.mast = mast
        self.num = num
        self.invis = False

    def value(self):
        if self.num in "TJQK":
            return 10
        else:
            return " A23456789".index(self.num)

    def __str__(self):
        if self.invis:
            return 'XX'
        return self.num + self.mast

    def __gt__(self, other):
        alf = '23456789TJQKA'
        kard1 = alf.index(self.num)
        kard2 = alf.index(other.num)
        return kard1 > kard2

    def __lt__(self, other):
        alf = '23456789TJQKA'
        kard1 = alf.index(self.num)
        kard2 = alf.index(other.num)
        return kard1 < kard2

    def __eq__(self, other):
        alf = '23456789TJQKA'
        kard1 = alf.index(self.num)
        kard2 = alf.index(other.num)
        return kard1 == kard2


class Deck:
    def __init__(self):
        num = "23456789TJQKA"
        suits = "♧♤♡♢"
        self.cards = [Card(r, s) for r in num for s in suits]
        shuffle(self.cards)

    def give_away_card(self):
        return self.cards.pop()


class Player:
    def __init__(self):
        self.cards = []

    def give_card(self, card):
        self.cards.append(card)

    def get_value(self):
        result = 0
        aces = 0
        for card in self.cards:
            result += card.value()
            if card.num == "A":
                aces += 1
        if result + aces * 10 <= 21:
            result += aces * 10
        return result

    def __str__(self):
        output = ''
        for i in self.cards:
            output += str(i) + " "
        return output


class Game:
    def __init__(self, name):
        name = str(name)
        self.name = name
        self.deck = Deck()

        self.dealer = Player()
        self.player = Player()

        self.run = False

    def hod(self, hod, name):
        name = str(name)
        if self.name == name:
            if hod == 'взять':
                self.player.give_card(self.deck.give_away_card())
                output = f'{self.name}\n\n\nОчки дилера:\n' + str(self.dealer.cards[0].value()) + '\nКарты дилера: \n' + str(
                    self.dealer) + '\nВаши очки: \n' + str(self.player.get_value()) + '\nВаши карты: \n' + str(self.player)

                if self.player.get_value() < 21:
                    return output
                elif self.player.get_value() == 21:
                    return self.hod_diler()
                elif self.player.get_value() > 21:
                    self.run = False
                    for i in self.dealer.cards:
                        i.invis = False
                    output = f'{self.name}\n\n\nОчки дилера:\n' + str(self.dealer.get_value()) + '\nКарты дилера: \n' + str(
                        self.dealer) + '\nВаши очки: \n' + str(self.player.get_value()) + '\nВаши карты: \n' + str(
                        self.player)
                    return output + '\nДилер победил'

            elif hod == 'пас':
                return self.hod_diler()
            else:
                pass
        return name + ', ваша игра не запущена'

    def hod_diler(self):
        self.run = False
        while self.dealer.get_value() < 17:
            self.dealer.give_card(self.deck.give_away_card())
        for i in self.dealer.cards:
            i.invis = False
        output = f'{self.name}\n\n\nОчки дилера:\n' + str(self.dealer.get_value()) + '\nКарты дилера: \n' + str(
            self.dealer) + '\nВаши очки: \n' + str(self.player.get_value()) + '\nВаши карты: \n' + str(self.player)
        if self.dealer.get_value() > 21 or self.dealer.get_value() < self.player.get_value():
            return output + '\nВы победили'
        elif self.dealer.get_value() > self.player.get_value():
            return output + '\nДилер победил'
        elif self.dealer.get_value() == self.player.get_value():
            return output + '\nНичья'

    def start(self):
        self.run = True
        self.player.give_card(self.deck.give_away_card())
        self.player.give_card(self.deck.give_away_card())
        self.dealer.give_card(self.deck.give_away_card())
        self.dealer.give_card(self.deck.give_away_card())
        self.dealer.cards[1].invis = True

        output = f'{self.name}\n\n\nОчки дилера:\n' + str(self.dealer.cards[0].value()) + '\nКарты дилера: \n' + str(
            self.dealer) + '\nВаши очки: \n' + str(self.player.get_value()) + '\nВаши карты: \n' + str(self.player)
        return output


class bolshe_menshe:
    def __init__(self, name):
        name = str(name)
        self.name = name
        self.deck = Deck()
        self.run = False
        self.player = Player()
        self.conter = 0

    def start(self):
        self.run = True
        self.player.give_card(self.deck.give_away_card())
        output = f'{self.name}\n\n\nВы вытащили ' + str(self.player.cards[-1]) + '\nСледующая карта > или < ?'
        return output

    def hod(self, mes, name):
        name = str(name)
        if self.name == name:
            self.player.give_card(self.deck.give_away_card())
            if mes == '>' and self.player.cards[-1] > self.player.cards[-2]:
                self.conter += 1
                return f'{self.name}\n\n\nВы угадали!\nУ вас {self.conter} 🪙\n' + 'Вы вытащили ' + str(
                    self.player.cards[-1]) + '\nСледующая карта > или < ?'
            if mes == '<' and self.player.cards[-1] < self.player.cards[-2]:
                self.conter += 1
                return f'{self.name}\n\n\nВы угадали!\nУ вас {self.conter} 🪙\n' + 'Вы вытащили ' + str(
                    self.player.cards[-1]) + '\nСледующая карта > или < ?'
            if self.player.cards[-1] == self.player.cards[-2]:
                self.conter += 1
                return f'{self.name}\n\n\nЗначения карт равны!\nУ вас {self.conter}\n' + 'Вы вытащили ' + str(
                    self.player.cards[-1]) + '\nСледующая карта > или < ?'
            return f'{self.name}\n\n\nВы не угадали\nВы вытащили {str(self.player.cards[-1])} \nВы набрали {self.conter} 🪙'
        return name + ', ваша игра не запущена'


class russian_roulette:
    def __init__(self, name):
        name = str(name)
        self.name = name
        self.run = False
        self.mag = []
        self.patr = 0

    def start(self, patr):

        self.run = True
        self.patr = int(patr)
        self.mag = list(map(str, list(range(self.patr))))
        return f'{self.name}\n\n\nВыберите номер пули 🔫 \n' + ' '.join(self.mag)


    def hod(self, num, name):
        name = str(name)
        if self.name == name:
            a = choice(self.mag)
            if str(num) not in self.mag:
                return f'{self.name}\n\n\nНет такого числа!\nВыберите номер пули 🔫 \n' + ' '.join(self.mag)
            self.run = False
            if a == str(num):
                return f'{self.name}\n\n\nВы проиграли...'
            return f'{self.name}\n\n\nВы победили!'
        return name + ', ваша игра не запущена'
