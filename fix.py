#!/usr/bin/env python
with open('DailyHitman.py', 'rb') as file:
	data = file.read()
	data = data.replace(b'\r\n', b'\n')
with open('DailyHitman.py', 'wb') as file:
	file.write(data)
