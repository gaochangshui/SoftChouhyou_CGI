#!/bin/bash -xv
#
# CHOUHYOU_PLANQTY_EXCEL_KENSAKU.CGI >>> 計画数設定
# Usage : CHOUHYOU_PLANQTY_EXCEL_KENSAKU.CGI
#
# Written by Gao.Changshui (TRE-CHINA) /Date : 11 Jan. 2019

#/////////////////////////////////////////////////////////////////////////
# 初期設定
#/////////////////////////////////////////////////////////////////////////

# 環境変数設定
export PATH=/home/SMART:/home/SMART_TRIAL:/usr/local/bin:${PATH}
export LANG=ja_JP.UTF-8

# ログディレクトリ設定
cgishld=/home/trial/AP/SOFT_CHOUHYOU
logd=${cgishld}/LOG

# 走行ログの記録
echo   "${logd}/LOG.$(basename $0).$(date +%Y%m%d)_$(date +%H%M%S)_$$" &>/dev/null
exec 2> ${logd}/LOG.$(basename $0).$(date +%Y%m%d)_$(date +%H%M%S)_$$

# ディレクトリ定義
dir=/home/trial
shld=${dir}/AP/SOFT_CHOUHYOU/CGI
cshld=${dir}/AP/SOFT_CHOUHYOU/CGI/COMMON_SHELL
sday=$(date +%Y%m%d)

tmp=/tmp/$$-$(basename $0)_$(date +%Y%m%d)_$(date +%H%M%S)

# 引数の確認
[ $# -ne 0 ] && exit 1
# 変数の定義

# エラー時の終了処理定義
ERROR_EXIT(){
 echo '{"error":"1"}'
 exit 1
}

#/////////////////////////////////////////////////////////////////////////
# 処理部分
#/////////////////////////////////////////////////////////////////////////

echo "Content-Type:text;charset=UTF-8"
echo ""

#画面から入力のデータ取得
dd count=$CONTENT_LENGTH bs=1 |
qsstr -l_ -i_                 > $tmp-param
[ $(errchk ${PIPESTATUS[@]}) -eq 0 ] || ERROR_EXIT

usercd=$(readvalue -uUSERID $tmp-param)
[ -z ${usercd} ] && ERROR_EXIT

# 操作履歴作成
shl=CHOUHYOU_OPTION_HISTORY_KENSAKU.SEARCH
${shld}/${shl} 0001 $(basename $0) ${usercd}
[ $? -eq 0 ] || ERROR_EXIT

kikanid=$(readvalue -uKIKANID $tmp-param)
[ -z ${kikanid} ] && ERROR_EXIT

kisetutype=$(readvalue -uKISETUTYPE $tmp-param)
[ -z ${kisetutype} ] && ERROR_EXIT

shl=CHOUHYOU_PLANQTY_EXCEL_FORMAT.SEARCH
${shld}/${shl} $tmp ${kikanid} ${kisetutype} ${usercd} > $tmp-urlfile
[ $? -eq 0 ] || ERROR_EXIT

error=0

url=$(cat $tmp-urlfile)
# 1.data 2.key 3.S:一つ値 F:ファイル 4.0:普通値 1:array _:無視
cat << FIN > $tmp-datafile
${error} error S 0
${url} excelurl S 0
FIN

shl=COMMON_TOJSON.SHELL
${cshld}/${shl} $tmp-datafile > $tmp-result
[ $? -eq 0 ] || ERROR_EXIT

cat $tmp-result


# 終了部分
#/////////////////////////////////////////////////////////////////////////
# 終了
#/////////////////////////////////////////////////////////////////////////
rm -rf $tmp-* &>/dev/null
exit 0
