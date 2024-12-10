lat = [50.8508, 51.0495, 51.0353, 50.93413, 51.03500, 50.9313, 50.8508]
long = [4.3488, 5.2261, 4.48322, 4.03926, 4.48421, 4.3278, 4.3488]

lat = [i for i in lat if i != max(lat) and i != min(lat)]
long = [i for i in long if i != max(long) and i != min(long)]

avglat = sum(lat)/len(lat)
avglong = sum(long)/len(long)

print(avglat, avglong)
