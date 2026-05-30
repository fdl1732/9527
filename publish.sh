#!/bin/bash
# ================================================================
# 一键发布作品到 GitHub Pages
# 用法: bash publish.sh "作品标题" "作品描述" source.html  [标签]
# 示例: bash publish.sh "我的动画" "一个粒子特效" demo.html "visual interactive"
# ================================================================

if [ $# -lt 3 ]; then
    echo "用法: bash publish.sh \"标题\" \"描述\" 文件路径 [标签]"
    echo "示例: bash publish.sh \"黑洞动画\" \"粒子特效\" work.html \"visual html\""
    exit 1
fi

TITLE="$1"
DESC="$2"
FILE="$3"
TAGS="${4:-html}"
DATE=$(date +%Y-%m-%d)
ID=$(echo "$TITLE" | tr -cd 'a-zA-Z0-9' | head -c 20)
WORK_DIR="works"
ID="${ID:-work-$(date +%s)}"

# 复制文件到 works 目录
EXT="${FILE##*.}"
cp "$FILE" "$WORK_DIR/$ID.$EXT" 2>/dev/null && echo "✅ 文件已复制到 $WORK_DIR/$ID.$EXT" || { echo "❌ 文件 $FILE 不存在"; exit 1; }

# 生成 JS 数据条目
ENTRY=$(cat <<EOF
  {
    id: "$ID",
    title: "$TITLE",
    desc: "$DESC",
    tags: ["${TAGS// /\", \""}],
    date: "$DATE",
    href: "$WORK_DIR/$ID.$EXT"
  },
EOF
)

# 插入到 works.js
sed -i "/\/\/ ─────────────────────────────────────────────────────────────/i\\
$ENTRY" assets/works.js

echo "✅ 作品信息已添加到 assets/works.js"
echo ""
echo "现在提交并推送:"
echo "  git add ."
echo "  git commit -m \"发布: $TITLE\""
echo "  git push"
echo ""
echo "部署后访问: https://fdl1732.github.io/9527/"
