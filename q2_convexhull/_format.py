import qiime2.plugin.model as model
from qiime2.plugin import ValidationError


class HullsFormat(model.TextFileFormat):
    def _validate(self, n_records=None):
        with self.open() as fh:
            # check the header column names
            header = fh.readline()
            comp_columns = [head.replace('\n', '')
                            for head in header.split('\t')][1:]
            # ensure there at least two components
            if len(comp_columns) != 3:
                raise ValidationError('There should only be three '
                                      'columns in the hull format')
            if comp_columns[1] != 'convexhull_volume':
                raise ValidationError('The second column '
                                      'should be the volume.')
            if comp_columns[2] != 'convexhull_area':
                raise ValidationError('The third column '
                                      'should be the volume.')
            # validate the body of the data
            for line_number, line in enumerate(fh):
                cells = line.split('\t')
                num_types = [is_float(v.strip()) for v in cells[2:]]
                num_types = [is_float(v.strip()) for v in cells[2:]]
                if not all(num_types):
                    raise ValidationError('Non float values '
                                          'in volume or area.')
                if not isinstance(cells[1], str):
                    raise ValidationError('Subject IDs '
                                          'should be strings.')

    def _validate_(self, level):
        record_count_map = {'min': 1, 'max': None}
        self._validate(record_count_map[level])


def is_float(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


HullsDirectoryFormat = model.SingleFileDirectoryFormat(
    'HullsDirectoryFormat', 'hulls.tsv',
    HullsFormat)
