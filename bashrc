function highstate() {
        salt ''$1'' state.highstate | grep -v "Result: Clean" |{
                count=0
                while IFS= read -r line
                do
                        if echo $line|grep -Eq '^Total states run:*'
                        then
                                ((count+=1))
                                echo -e "\e[1;34m$line"
                        else
                                if echo $line|grep -Eq '^Failed:\s*[1-9]+0?'
                                then
                                        echo -e "\e[1;31m$line"
                                else
                                        if [[ "$line" == "" ]]
                                        then 
                                                ignore="yes"
                                        else
                                                echo -ne "\e[1;32m"
                                                echo "$line"
                                        fi
                                fi
                        fi
                done
                echo -ne "\e[0m"
                echo "$count minions returned"
        }
}

function state(){
        salt ''$1'' state.sls services/$2 |grep -v "Result: Clean" | {
                count=0
                while IFS= read -r line
                do
                        if echo $line|grep -Eq '^Total states run:*'
                        then
                                ((count+=1))
                                echo -e "\e[1;34m$line"
                        else
                                if echo $line|grep -Eq '^Failed:\s*[1-9]+0?'
                                then
                                        echo -e "\e[1;31m$line"
                                else
                                        if [[ "$line" == "" ]]
                                        then 
                                                ignore="yes"
                                        else
                                                echo -ne "\e[1;32m"
                                                echo "$line"
                                        fi
                                fi
                        fi
                done
                echo -ne "\e[0m"
                echo "$count minions returned"
        }
}
