#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import sys, os, codecs, xlrd, locale

def to_unicode(input_str):
	if sys.version < '3':
		return unicode(input_str)
	else:
		return str(input_str)

def write_workbook(workbook):
	worksheet = workbook.sheet_by_index(0)

	num_rows = worksheet.nrows - 1
	num_cells = worksheet.ncols - 1
	curr_row = -1
	while curr_row < num_rows:
		curr_row += 1
		row = worksheet.row(curr_row)
		line_values = []
		line_values.append(to_unicode(curr_row))
		curr_cell = -1
		while curr_cell < num_cells:
			curr_cell += 1
			# Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
			cell_type = worksheet.cell_type(curr_row, curr_cell)
			cell_value = worksheet.cell_value(curr_row, curr_cell)
			if cell_type == 2:
				value = to_unicode(cell_value).replace('.0', '')
			else:
				value = to_unicode(cell_value).replace('\n', ' ')

			line_values.append( value )
		line_str = u'\t'.join(line_values)

		try:
			print( line_str )
		except Exception:
			e = sys.exc_info()[1]
			print( Exception, e )



if __name__ == "__main__":
	# Wrap sys.stdout into a StreamWriter to allow writing unicode.
	if sys.version < '3':
		sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

	if len(sys.argv)>1:
		for input_file in sys.argv[1:]:
			if 'xls' in input_file.lower().split('.')[-1]:
				workbook = xlrd.open_workbook( input_file )
				write_workbook(workbook)
	else:
		workbook = xlrd.open_workbook( file_contents=sys.stdin.read() )
		write_workbook(workbook)