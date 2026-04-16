from scripts.data_generators.locations import LocationGenerator
gen = LocationGenerator()
location_data = gen.generate_batch(10)
print(location_data)