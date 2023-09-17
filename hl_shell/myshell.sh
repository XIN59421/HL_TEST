#!/bin/bash

# 要搜索的文件
search_file="aa.txt"

# 要搜索的内容
search_text="a"

# 结果文件
rest_file="new_file.txt"

# 使用grep查找指定内容
grep -n "$search_file" "$search_text" > "$rest_file"

# 输出结果到控制台
cat "$search_file" | while read t; do echo "$t"; done