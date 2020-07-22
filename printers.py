import gdb.printing

class PODArrayPrinter:
    def __init__(self, val):
        self.val = val

    class _iterator:
        def __init__ (self, start, finish):
            self.item = start
            self.finish = finish
            self.count = 0

        def __iter__(self):
            return self

        def __next__(self):
            count = self.count
            self.count += 1

            if self.item == self.finish:
                raise StopIteration

            elt = self.item.dereference()
            self.item += 1

            return ('[%d]'.format(count), elt)

    def to_string(self) -> str:
        start = self.val['c_start']
        finish = self.val['c_end']
        end = self.val['c_end_of_storage']

        return ('{} of length {}, capacity {}'.format(
            self.val.type,
            int(finish - start),
            int(end - start)))

    def children(self):
        return self._iterator(
            self.val['c_start'],
            self.val['c_end'])

    def display_hint(self):
        return "array"


class IColumnPrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self) -> str:
        pass

def build_pretty_printers():
    pp = gdb.printing.RegexpCollectionPrettyPrinter("clickhouse")

    pp.add_printer('PODArray', '^DB::PODArray<.*>$', PODArrayPrinter)
    pp.add_printer('PaddedPODArray', '^DB::PaddedPODArray<.*>$', PODArrayPrinter)
    # pp.add_printer('IColumn', '^DB::IColumn<.*>$', IColumnPrinter)

    return pp

def register_ch_printers():
    gdb.printing.register_pretty_printer(
        gdb.current_objfile(),
        build_pretty_printers())
