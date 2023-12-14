class Analyze():
    def __init__(self) -> None:
        self.data = []
        self.dates = []
        self.advices = {}

    def get_median(self):
        return sum(self.data) / len(self.data)
    
    def get_max(self):
        return max(self.data)
    
    def get_min(self):
        return min(self.data)
    
    def generate_analyze(self):
        advices = {'has_day_without_production' : [],
                   'has_day_with_negative_production' : []
                   }

        if self.get_min() == 0:
            for day in range(len(self.data)):
                if not self.data[day]:
                    advices['has_day_without_production'].append(self.dates[day])

        
            self.advices = advices

        else:
            del(advices['has_day_without_production'])    


        return advices

    def genarate_insigths(self):

        texts = {}

        result = self.generate_analyze()

        if self.advices:

            texts['resume'] = True
        else:
            texts['resume'] = False


        if texts['resume']:

            insights_to_show = []

            insights_resumes = []

            for insight in result.keys():
                insights_to_show.append(insight)

                if insight == 'has_day_without_production':
                    insights_resumes.append(f'These days has none production: {result[insight]}')
        
            return insights_resumes


if __name__ == '__main__':
    analise1 = Analyze()
    analise1.data = [0, 3, 2, 12]
    analise1.dates = ['2023', '2021', '2020', '1998']

    print(analise1.genarate_insigths())