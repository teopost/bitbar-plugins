#!/bin/bash
# <bitbar.title>Title goes here</bitbar.title>
export LANG=it_IT.UTF-8

warning_icon="iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAMAAADzapwJAAAA/FBMVEUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADzfFO9AAAAU3RSTlMAAQIDBAUGBwsNEhMZGhweICEiIyYnKSssLzEyNT9BQkNJTFZYXmFrcXN4e3x+g4WIiYyPkZKUmpuoqq+ywMXHztHT1dfa3N7g5ujp6/Hz9ff7/cfoDdwAAADRSURBVBgZBcEFQkIBAAWwAd9uDOzu7g4QE+x3/7u4AQAAAAAAgNL0yeNX42K+CwCMPSdJkr/tCgDLyfFgWdG39p63XoDxfI4yeVujspt2N1B6TRUf+YCN3ACzOYSXtMBNRsB5BuA6D2A4+6CZMuzlCpRTB18BqzkG8gnq6YDRrIAi9+AgVdAJTGQL1HIJS+0lcJd+oJEZtNKCnVwChvIzxWJ7keIob10Ac8nZYKHoW2/lqQeA4ackSfK7WQaA0vRp8/vxYqETAAAAAAAAAAAA/gFGJSLgdaa6SQAAAABJRU5ErkJggg=="
# Lo script deve funzionare solo se sono in WEDO.
# Per capire se lo sono controllo l'IP

sono_in_wedo=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | cut -d " " -f2 | grep '192.168.10' | wc -l)

if [ $sono_in_wedo -eq 0 ];then
   echo " | size=10 templateImage=${warning_icon}"
   exit
fi

# Conta processi oracle ci sono in Bocconi
# ------------------------------------------
num_procs=$(ssh bocconi_oracle 'ps -ef | grep oracle | wc -l')

# Imposto le soglie
procs_warning=1000
procs_alert=1400
procs_panic=1700

warning_msg="Attenzione. In Bocconi ci sono ${num_procs} processi oracle attivi"
alert_msg="Attenzione. In Bocconi ci sono ${num_procs} processi oracle attivi"
panic_msg="Attenzione, Attenzione. Sta succedendo qualcosa di grave in Bocconi!"

if [ $num_procs -lt $procs_warning ]; then
  echo "Oracle procs: $num_procs"

elif [ $num_procs -lt $procs_alert ]; then
  echo "Oracle procs: $num_procs | color=orange"
  osascript -e 'display notification "'"$warning_msg"'" with title "Processi Bocconi"'

else

  echo "Oracle procs: $num_procs | color=red"
  osascript -e 'display notification "'"$panic_msg"'" with title "Processi Bocconi"'

  say -v alice $panic_msg
fi

# Estrae il carico medio di cpu della macchina
# --------------------------------------------
cmd_cpu_average="sar -P ALL 1 2 | grep 'Media.*all' | awk -F\" \" '{print 100.0 -\$NF}'"

cmd_data=$(ssh bocconi_oracle $cmd_cpu_average)
cmd_data=${cmd_data%%,*}

if [ $cmd_data -lt 80 ]; then
  echo "Cpu average: $(ssh bocconi_oracle ${cmd_cpu_average})"
else
  echo "Cpu average: $(ssh bocconi_oracle ${cmd_cpu_average}) | color=red"
  osascript -e 'display notification "'"La CPU ha superato 80%"'" with title "Processi Bocconi"'
fi

# Sessioni oracle attive
# ------------------------------------------
active_sessions="
set heading off;
select count(*),sum(decode(status, 'ACTIVE',1,0)) from v\\\$session where type= 'USER';
"

cmd_data=$(ssh bocconi_oracle ". .profile_ESSE3; echo \"$active_sessions\" | sqlplus -s / as sysdba")

echo "Session count:" $(echo $cmd_data | awk '{print $1}')
echo "Active sessions:" $(echo $cmd_data | awk '{print $2}')

# menu
# ----
echo "---"
echo "Apri enterprise manager (sysman/mangoxx1)... | href=https://ks3-rcatem.sm.unibocconi.it:7802/em/faces/sdk/nonFacesWrapper?target=ESSE3&_em.coBM=/console/rac/racTopActivity%3FrefreshChoice%3DRT_15%26event%3DdoLoad%26target%3DESSE3%26type%3Drac_database%26waitClass%3DOverview&type=rac_database&_afrLoop=3974850672928603&_afrWindowMode=0&_afrWindowId=b0mk5uuz9_6#!%40%40%3Ftarget%3DESSE3%26_em.coBM%3D%252Fconsole%252Frac%252FracTopActivity%253Fevent%253DmoveSlider%2526target%253DESSE3%2526type%253Drac_database%2526waitClass%253DOverview%2526tabName%253Dundefined%2526selectedBand%253D1%2526leftEdge%253D1476706589531%2526rightEdge%253D1476706889531%2526refreshChoice%253DRT_15%2526aggregationChoice%253DWaits%2526selectedAction%253Dundefined%26type%3Drac_database%26_adf.ctrl-state%3Db0mk5uuz9_51"

echo "---"
# print compose_item_row('Mark all as read', 'mark_all_items_as_read', file_to_save)
echo "Refresh| refresh=true"
echo "---"
echo "Edit script...| terminal=false bash=/usr/local/bin/atom param1=$(dirname $0)/$(basename $0)"
