#!/bin/sh

# Sometimes the stty command stucks so we have to check for that.
# In such a case we need to do a forced restart. After such a restart it normally works fine.
# It was never necessary before but we try up to 5 restarts.

sleep 5                                 # we check after 5 seconds
                                                                                                                    
psOut=$(ps | grep stty | wc -l)         # check if there is still a stty process
counterState=`cat restartCount.txt`     # this file stores the count of restarts that we needed
if [[ "$psOut" -ge 2  ]]                # if there is more than one process we know that the stty command stuck (2 processes because the command "ps | grep stty | wc -l" does count as well
then                                                                                                                
        echo "$(date): Probably need restart" >> restartlog.txt                                                     
        if [[ "$counterState" -ge 5  ]]
        then                                                                                                        
                echo "$(date): won't restart. Already tried 5 times" >> restartlog.txt                              
        else                                                                                                        
                counterState=$((counterState+1))                                                                    
                echo "New Counter: $counterState" >> restartlog.txt                                                 
                echo "$counterState" > restartCount.txt                                                             
                #for testing here is another sleep                                                                  
                sleep 10                                                                                            
                reboot -f                                                                                           
        fi                                                                                                          
else                                                                                                                
        echo "0" > restartCount.txt                                                                                 
fi  