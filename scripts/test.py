import json
import os

from Vestivise import settings
from data.models import Benchmark, Holding, BenchmarkComposite


def run():
    benchmark_file_map = {}
    benchmark_names = []
    for i in range(2025, 2065, 5):
        name = "{} Vestivise Target Date Index".format(i)
        benchmark_names.append(name)
        benchmark_file_map[name] = "ms_targ_{}.json".format(str(i))

    group = 60
    for i in range(len(benchmark_names)):
        age_group = group - i * 5
        name = benchmark_names[i]
        Benchmark.objects.update_or_create(age_group=age_group, name=name)
    for benchmark_name, f in benchmark_file_map.iteritems():
        json_file = open(os.path.join(settings.BASE_DIR, 'data/fixtures/benchmark_data/{}'.format(f)))
        data = json.loads(json_file.read())
        for i in range(30):
            fund = data[i]
            fields = fund["fields"]
            secname = fields["secname"]
            ticker = fields["ticker"]
            category = fields["category"]
            benchmark = Benchmark.objects.get(name=benchmark_name)
            if not Holding.objects.filter(secname=secname):
                BenchmarkComposite.objects.update_or_create(secname=secname, ticker=ticker,
                                                            benchmark=benchmark, category=category)