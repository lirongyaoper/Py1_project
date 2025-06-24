#!/bin/bash
# 解密工具 v1.2 - 专用于 index.class.php

if [ ! -f "$1" ]; then
    echo "用法: ./deobfuscate.sh index.class.php"
    exit 1
fi

# 1. 创建临时工作目录
WORKDIR=$(mktemp -d)
cp "$1" "$WORKDIR/original.php"
cd "$WORKDIR" || exit

echo "正在分析文件: $1"

# 2. 提取所有加密字符串的数学表达式
echo "步骤1/3: 提取加密表达式..."
grep -oP 'pack\([^,]+,\s*\$GLOBALS\[[^]]+?\]\[([^]]+)\]\)' original.php |
  awk -F'[][]' '{print $3}' |
  sort -u > expressions.txt

# 3. 计算所有数学表达式的结果
echo "步骤2/3: 计算表达式值..."
while read -r expr; do
    # 安全计算表达式值
    value=$(php -r "echo @($expr);" 2>/dev/null)
    if [ -z "$value" ]; then
        value="NULL"
    fi
    echo "$expr=$value" >> mappings.txt
done < expressions.txt

# 4. 生成字符串映射表
echo "步骤3/3: 生成字符串映射..."
php -r '
$content = file_get_contents("original.php");
preg_match_all("/pack\([^,]+,\s*\\\$GLOBALS\[[^]]+?\]\[([^]]+)\]\)/", $content, $matches);
$indices = array_unique($matches[1]);
foreach($indices as $idx) {
    $val = eval("return $idx;");
    echo "$idx=".pack("H*", $val)."\n";
}' >> mappings.txt

# 5. 执行替换（保留原始文件备份）
echo "正在解密文件..."
while IFS='=' read -r expr value; do
    if [ "$value" != "NULL" ]; then
        # 替换数学表达式
        sed -i "s/\[$expr\]/\[$value\]/g" original.php
        # 替换pack调用
        sed -i "s/pack([^,]*,\s*\$GLOBALS\[[^]]*\]\[$expr\])/'$value'/g" original.php
    fi
done < mappings.txt

# 6. 输出结果
mv original.php "../${1%.*}_decrypted.php"
echo "解密完成！生成文件: ${1%.*}_decrypted.php"
echo "临时工作目录: $WORKDIR (分析完成后可手动删除)"