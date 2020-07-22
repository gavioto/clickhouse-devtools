## What does it do?

Adds some nice representation of ClickHouse's internal data structures in GDB. 

For example, when printing the `DB::PaddedPODArray`'s contents, instead of

```
$1 = (DB::PaddedPODArray<DB::ArrayIndexNumImpl<unsigned long, unsigned long, DB::Index
ToOne, false>::ResultType> &) @0x7ffff7847030: {<DB::PODArrayBase<1, 4096, Allocator<f711 alse, false>, 15, 16>> = {
<boost::noncopyable_::noncopyable> = {<boost::noncopyable_:: base_token> = {<No data fields>}, <No data fields>}, 
<Allocator<false, false>> = {stat713 ic clear_memory = false, static mmap_flags = 34}, static pad_right = 15, 
static pad_left = 16, static null = <optimized out>, c_start = 0x7ffff78a5c10 "", 
c_end = 0x7ffff78a5c42 '\245' <repeats 62 times>, 'Z' <repeats 128 times>, "\202\031", 
c_end_of_storage= 0x7ffff78a5c71 '\245' <repeats 15 times>, 'Z' <repeats 128 times>, "\202\031", 
mprotected = false}, <No data fields>}    
```
you would see this:

```
$1 = DB::PaddedPODArray<DB::ArrayIndexNumImpl<unsigned
long, unsigned long, DB::IndexToOne, false> of length 50, capacity 97 = 
{0 '\000', 0 '\000', 0
'\000', 0 '\000', 0 '\000', 0 '\000', 0 '\000', 0 '\000
', 0 '\000', 0 '\000', 0 '\000', 0 '\000', 0 '\000', 0
'\000', 0 '\000', 0 '\000', 0 '\000', 0 '\000', 0 '\000
', 0 '\000', 0 '\000', 0 '\000', 0 '\000', 0 '\000', 0
'\000', 0 '\000', 0 '\000', 0 '\000', 0 '\000', 0 '\000
', 0 '\000', 0 '\000', 0 '\000', 0 '\000', 0 '\000', 0
'\000', 0 '\000', 0 '\000', 0 '\000', 0 '\000', 0 '\000
', 0 '\000', 0 '\000', 0 '\000', 0 '\000', 0 '\000', 0
'\000', 0 '\000', 0 '\000', 0 '\000'}
```

## How to use it?

1. Install gdb and verify that it supports Python scripting (invoke `gdb --version` and check for `--with-python=...` lines).
2. Create a `~/.gdbinit` file and put these lines in it:

```
python
import sys
sys.path.insert(0, '/full/path/to/repo')

from printers import register_ch_printers

register_ch_printers()
end
```

3. Run gdb and type `info pretty-printer`. You should see something like that:

```
(gdb) info pretty-printer 
global pretty-printers:
  ...
  clickhouse
    PODArray
    ...
  libstdc++-v6
    ...
```

## FAQ

1. Ok, I see the containers' capacity and size, but not the contents (other variant: I see not all of the children).

Open gdb and type `set print elements xx` to show first `xx` array's elements.


