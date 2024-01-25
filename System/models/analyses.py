class Analyze():
    def __init__(self) -> None:
        self.data = []
        self.dates = []
        self.advices = {}

    def get_mean(self):
        return sum(self.data) / len(self.data)

    def get_max(self):
        return max(self.data)

    def get_min(self):
        return min(self.data)

    def generate_analyze(self):
        advices = {'has_day_without_production': [],
                   'has_day_with_negative_production': [],
                   'excepcional_production': [],  # production above mean

                   }

        if self.get_min() <= 0:

            for day in range(len(self.data)):
                if not self.data[day]:
                    advices['has_day_without_production'].append(
                        self.dates[day])

        if self.get_min() < 0:
            for day in range(len(self.data)):
                if self.data[day] < 0:
                    advices['has_day_with_negative_production'].append(
                        self.dates[day])

        if (self.get_max() - self.get_mean()) > (self.get_mean() * 2):
            for day in range(len(self.data)):
                if (self.get_max() - self.get_mean()) > (self.get_mean() * 2):
                    advices['excepcional_production'].append(self.dates[day])

        self.advices = advices
        return advices

    def genarate_insights(self):

        texts = {}

        result = self.generate_analyze()

        if self.advices:

            texts['resume'] = True
        else:
            texts['resume'] = False

        if texts['resume']:

            insights_to_show = []

            insights_resumes = {'has_day_without_production': [],
                                'has_day_with_negative_production': []}

            for insight in result.keys():
                insights_to_show.append(insight)

                if insight == 'has_day_without_production':
                    insights_resumes['has_day_without_production'] = result[insight]

                if insight == 'has_day_with_negative_production':
                    insights_resumes['has_day_with_negative_production'] = result[insight]

            return insights_resumes


if __name__ == '__main__':
    analise1 = Analyze()
    analise1.data = [-3, 3, 0, 300, -4]
    analise1.dates = ['2023', '2021', '2020', '1998', '2015']

    print(analise1.genarate_insights())
