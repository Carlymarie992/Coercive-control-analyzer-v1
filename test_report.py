from report_generator import ReportGenerator

DOCUMENT_ANALYSIS_TYPE = 'document_analysis'

gen = ReportGenerator()
gen.generate_report(
    {'filepath': 'test.pdf', 'analysis_type': DOCUMENT_ANALYSIS_TYPE},
    output_filename='test.html'
)
