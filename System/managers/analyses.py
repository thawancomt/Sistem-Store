class Analyse():
    def __init__(self) -> None:
        self.data = []

    def get_median(self):
        return sum(self.data) / len(self.data)
    

if __name__ == '__main__':
    analise1 = Analyse()
    analise1.data = [15, 15, 40, 15]
    print(analise1.get_median())