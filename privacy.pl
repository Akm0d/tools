#!/usr/bin/perl
#Created By Tyler S Johnson
#July 10, 2015
#For best performance, add an alias to your ~/.bashrc that runs this script

#hide output
` stty -echo`;

#clear terminal
print ` clear`;
my $cmd = "hidden";
my $option = shift;

# No footprints in History
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
