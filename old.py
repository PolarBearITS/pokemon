def get_ATK(self, ATK_type, DMG_name=''):
	type_names = []
	for DEF_type, DMG_ratio in self.chart[ATK_type].items():
		if DMG_ratio == self.ratios[DMG_name]:
			type_names.append(DEF_type)
	return type_names

def get_DEF(self, DEF_type, DMG_name):
	type_names = []
	for ATK_type, DMG_ratios in self.chart.items():
		if DMG_ratios[DEF_type] == self.ratios[DMG_name]:
			type_names.append(ATK_type)
	return type_names

def get_double_ATK(self, ATK_type0, ATK_type1, DMG_name):
	type_names = []
	chart0 = self.chart[ATK_type0].values()
	chart1 = self.chart[ATK_type1].values()
	combined_chart = {k:a*b for k, (a, b) in zip(self.types, zip(chart0, chart1))}
	print(combined_chart)
	for DEF_type, (r0, r1) in zip(self.types, zip(chart0, chart1)):
		if r0 * r1 == self.ratios[DMG_name]:
			type_names.append(DEF_type)
	return type_names

def get_double_DEF(self, DEF_type0, DEF_type1, DMG_name):
	type_names = []
	for ATK_type, DMG_ratios in self.chart.items():
		if DMG_ratios[DEF_type0] * DMG_ratios[DEF_type1] == self.ratios[DMG_name]:
			type_names.append(ATK_type)
	return type_names