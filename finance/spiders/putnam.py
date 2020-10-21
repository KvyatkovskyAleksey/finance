import scrapy
import io
import PyPDF2
import re
import tabula
import pandas as pd

from finance.items import FinanceItem



class PutnamSpider(scrapy.Spider):
    name = 'putnam'
    allowed_domains = ['www.putnam.com']
    start_urls = ['https://www.putnam.com/literature/pdf/TX001-6a6398e1779dd03e057b2f6f9972ee58.pdf']

    def parse(self, response):
        pdf = PyPDF2.PdfFileReader(io.BytesIO(response.body))
        pages = pdf.getNumPages()
        # start = end = 0
        # output = []
        date_created = None
        for page in range(pages):
            text = pdf.getPage(page).extractText()
            if not date_created:
                if re.search('\(as of (\d+/\d+/\d+)[ ]*\)', text):
                    date_created = re.search('\(as of (\d+/\d+/\d+)[ ]*\)', text).group(1)
            else:
                break
        #     for n, string in enumerate(text.split('\n')):
        #         if '$ total' in string or 'No estimated extra taxable distribution required' in string:
        #             start = n + 1
        #         if '   ' in string or '(over)' in string:
        #             end = n
        #             break
        #     text = text.split('\n')[start:end]
        #     cleaned_text = []
        #     for string in text:
        #         if '%' in string:
        #             cleaned_text.extend([s.strip('$') for s in string.split('%')])
        #         else:
        #             cleaned_text.append(string.strip('$'))
        #
        #     for n in range(0, len(cleaned_text), 11):
        #         output.append(cleaned_text[n:n+11])
        output = []
        tables = tabula.read_pdf(io.BytesIO(response.body), pages="all", multiple_tables=True, stream=True)
        for table in tables:
            if len(table) < 1:
                continue
            for ix in table.index:
                output_row = []
                row = table.loc[ix]
                for n, cell in enumerate(row):
                    if n == 0:
                        if (pd.isna(cell) or cell == 'Putnam fund name'):
                            break
                        else:
                            output_row.append(cell)
                    else:
                        for s in cell.split():
                            output_row.append(s.strip('$%'))
                if output_row:
                    output.append(output_row)
        for row in output:
            if row[0].startswith(':'):
                row[0] = row[0][1:]
            item = FinanceItem()
            item['firm_name'] = 'Putnam'
            item['fund_name'] = row[0]
            item['ex_date'] = row[1]
            item['pay_date'] = row[2]
            per_share_total = float(row[-1])
            item['short_term_gain'] = float(row[-4])
            try:
                item['short_term_gain_pct'] = item['short_term_gain'] / per_share_total
            except ZeroDivisionError:
                item['short_term_gain_pct'] = 0
            item['long_term_gain'] = float(row[-3])
            try:
                item['long_term_gain_pct'] = item['long_term_gain'] / per_share_total
            except:
                item['long_term_gain_pct'] = 0
            item['record_date'] = date_created
            item['source_url'] = response.url
            yield item