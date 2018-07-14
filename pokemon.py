import pickle
import itertools
import bisect

class type_analysis:
	def __init__(self):
		self.chart = pickle.load(open('chart', 'rb'))
		self.type_names = list(self.chart.keys())

		# Generate unique versions of listed functions according to ATK or DEF.
		# After the functions are made, bind them to self.
		# e.g. with the string 'get', two functions, get_ATK and get_DEF are now
		# binded to self, meaning the expression "self.get_ATK(params)" works properly
		func_names = ['get_ratios', 'get', 'print', 'rank']
		for AD in ['ATK', 'DEF']:
			for name in func_names:
				setattr(self.__class__, f'{name}_{AD}', self.factory(name, AD))

	def get_damage(self, ATK, DEF):
		print(self.chart[ATK][DEF])

	def get_ratio_ATK(self, ATK_type):
		return self.chart[ATK_type]

	def get_ratio_DEF(self, DEF_type):
		return {ATK_type:self.chart[ATK_type][DEF_type] for ATK_type in self.chart}
	
	def prod(self, a, b):
		return {k:a[k]*b[k] for k in a}

	def ratio_test(self, ratios, target_ratio):
		return [p for p, r in ratios.items() if r == target_ratio]

	def total_len(self, dictionary):
		return sum(len(v) for v in dictionary.values())

	def get_ratios(self, AD, types):
		ratios = dict(zip(self.type_names, [1]*len(self.type_names)))
		for t in types:
			ratios = self.prod(ratios, getattr(self, f'get_ratio_{AD}')(t))
		return ratios

	def get(self, AD, types, DMG_ratio):
		return self.ratio_test(getattr(self, f'get_ratios_{AD}')(types), DMG_ratio)

	def print(self, AD, types):
		print(types)
		DMG_range = range(1, len(types)+1)
		ratios = [2**x for x in reversed(DMG_range)] + [1] + [1/2**x for x in DMG_range] + [0]
		for r in ratios:
			print(r, getattr(self, f'get_{AD}')(types, r))

	def rank(self, AD, DMG_ratios, combo=1):
		types = [x for n in range(1, combo+1) for x in itertools.combinations(self.type_names, n)]
		ranks = []
		for t in types:
			DMG_dict = dict(zip(DMG_ratios, (getattr(self, f'get_{AD}')(t , r) for r in DMG_ratios)))
			# DMG_lists = [getattr(self, f'get_{AD}')(t , r) for r in DMG_ratios]
			for i, (_t, l) in enumerate(ranks):
				if self.total_len(l) < self.total_len(DMG_dict):
					ranks.insert(i, (t, DMG_dict))
					break
			else:
				ranks.append((t, DMG_dict))
		return ranks

	def factory(self, name, AD):
		def func(self, *args, **kwargs):
			return getattr(self, name)(AD, *args, **kwargs)
		return func

t = type_analysis()
# names = ('ghost', 'ground')
# print(t.get_DEF(names, 0.5))
ranks = t.rank_ATK((2, 4), combo=2)
for t, lst in ranks:
	print(t, lst)
# names = ranks[0][0]
# t.print_ATK(names)