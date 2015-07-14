#!/usr/bin/perl
#Created By Tyler S Johnson
#July 10, 2015
#
#Comments:
#This script should be located in the ~/ folder
#
#For best performance, add an alias to your ~/.bashrc that runs this script
#For example, the following line makes it so the "po" command will run this script, 
#and then remove the history of having called it:
#alias po=' ~/.privacy.pl; history -d $((HISTCMD-1))'

#hide output and clear terminal
print ` stty -echo; clear`;

#global variables
my $cmd = "hidden";
my $option = shift;

# no footprints in History
if ($option){#Hide ALL output
        while ($cmd ne "q\n"){
                $cmd = <STDIN>;
                ` $cmd`;
        }
} else {#Hide only typed output
        while ($cmd ne "q\n"){
                $cmd = <STDIN>;
                system (" $cmd");
        }
}

#reset terminal
` stty echo`;
print ` clear`;
