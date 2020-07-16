import ephesoftAutomation.helper.util as util
import ephesoftAutomation.helper.comparator as comparator


def compare_all_results(base_dir, config):
    print('Test')
    config = util.combine_path(base_dir, config)
    cfg = util.get_configurations(config)
    if not cfg:
        return

    doc_to_process = cfg['documents_to_process'].replace(' ', '').split(',')
    for doc in cfg['documents_list']:
        if doc['Name'] in doc_to_process:

            actual_values_file_path = util.combine_path(base_dir, doc['CSV'])
            extracted_values_file_path = util.combine_path(base_dir, doc['ExtractionResults'])

            comp_result = comparator.get_comparison_results(extracted_values_file_path, actual_values_file_path)

            if cfg['show_comparison_issues_in_output']:
                comp_result.print_extraction_errors()

            if cfg['show_comparison_results_in_output']:
                comp_result.print_results()

            if cfg['export_results_to_excel']:
                export_file_path = util.get_export_filename(cfg, base_dir, doc['Name'])
                if export_file_path:
                    comp_result.export_to_excel(export_file_path)


#compare_all_results()
