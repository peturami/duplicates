import pandas as pd


class Duplicates:
    def open_file(self, name, separator, encoding, header, chunksize, rows):
        self.dfObj = pd.read_csv(name, dtype=str, encoding=encoding, na_filter=False, sep=separator, header=header,chunksize=chunksize, nrows=rows)
        return self.dfObj

    def analyze(self, name, separator, encoding, header, column_analysis, column_list):
        self.stats = []

        Duplicates.open_file(self, name, separator, encoding, header, chunksize=None, rows=None)

        file_total = self.dfObj.shape
        file_unique = self.dfObj.describe().loc['unique']
        file_header = file_unique.index

        self.stats.append('Rows: {}'.format(file_total[0]))
        self.stats.append('Columns: {}'.format(file_total[1]))

        if column_analysis == 1 and len(column_list) != 0:
            Duplicates.find_duplicate_rows(self, subset=column_list, keep='first', with_header=0)
            self.stats.append('Column {} duplicates: {}'.format(column_list, len(self.duplicate_rows_DF)))

        dupl_cnt = Duplicates.find_duplicate_rows(self, with_header=0, keep='first')
        self.stats.append('Total row duplicates: {}'.format(len(dupl_cnt)))

        self.stats.append('\nCOLUMN ANALYSIS:')
        for i, j in zip(file_unique, file_header):
            self.stats.append(' • total unique values for column "{}": {}'.format(j, i))

        return self.stats

    # basic method for reading file and displaying several rows in output window
    def show_several_rows(self, name, encoding):
        with open(name, encoding=encoding) as file:
            read_rows = [next(file) for i in range(30)]
        return read_rows

    # method for finding duplicates - based on selected columns or whole row
    def find_duplicate_rows(self, subset=None, keep=False, with_header=1):
        self.duplicate_rows_DF = self.dfObj[self.dfObj.duplicated(subset=subset, keep=keep)]

        if with_header == 1:
            return [self.duplicate_rows_DF.columns.values.tolist()] + self.duplicate_rows_DF.values.tolist()
        else:
            return self.duplicate_rows_DF.values.tolist()

    # create output file with unique row
    def create_unique_output(self, name, separator, encoding, subset, keep):
        unique_rows = self.dfObj.drop_duplicates(subset=subset, keep=keep)
        unique_rows.to_csv(name, sep=separator, encoding=encoding, index=False)

    # create output file with duplicates - based on selected columns or whole row
    def create_dupl_output(self, name, separator, encoding, subset, keep):
        Duplicates.find_duplicate_rows(self, subset=subset, keep=keep)
        self.duplicate_rows_DF.to_csv(name, sep=separator, encoding=encoding)

    # method for splitting large files to smaller chunks
    def split_file(self, name, separator, encoding, header, chunksize):
        file_nbr = 0
        self.final_list = ["File split into:\n"]

        for chunk in Duplicates.open_file(self, name, separator, encoding, header, chunksize=chunksize, rows=None):
            file_nbr += 1
            output_name = name.split(".")[0] + "_" + str(file_nbr) + "." + name.split(".")[1]
            chunk.to_csv(output_name, sep=separator, encoding=encoding, index=False)
            self.final_list.append(output_name + "\n")
        return self.final_list
