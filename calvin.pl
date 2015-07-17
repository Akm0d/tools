#!/usr/bin/perl

my $words = "talk";
my $num_args = $#ARGV;
my $mode ||= talk;#command,-c,talk,-t,spell,-s,quiet,-q
$mode = shift;
if ($mode eq "-c") {
        $mode = "command";
} elsif ($mode eq "-s"){ 
        $mode = "spell";
} elsif ($mode eq "-q"){ 
        $mode = "quiet";
} else {
        $mode = "talk";
}
while($num_args > 0){
        $param = $param . shift . " ";
        --$num_args;
}
$param ||= "^]NULL^]";
#command will run a command a speak the output raw
#talk will repeat everything you type
#spell will run a command, then literally repeat it
#quiet will skip the introduction and closing statement
#
#I considered a file option, but it is so similar to the
#command option which already includes this functionality
#and the implementation would be redundant which
#would be redundant. Simply type in your terminal:
#calvin command cat [file path]
#or make an alias in your bashrc such as:
#alias file='command cat'
#and then type:
#calvin file [file path]
my $user = getpwuid ($<);
my $random = int(rand(100));
if ($mode ne "quiet" && $mode ne "-q" && $param eq "^]NULL^]"){
        system("echo \"Hello $user, I am Calvin, You're digital assistant\" | espeak -s 120 2>/dev/null");
}
while ($words ne "q\n"){
        if ($param eq "^]NULL^]"){
                $words = <STDIN>;
        } else {
                $words = $param;
        }
        $random = int(rand(100));
        if ($words eq "command\n" ||$words eq "-c\n"){
                $mode = "command";
        } elsif ($words eq "talk\n" || $words eq "-t\n") {
                $mode = "talk";
        } elsif ($words eq "spell\n" || $words eq "-s\n") {
                $mode = "spell";#spell out the results of a command
        } elsif ($mode eq "spell") {
                chomp ($words);
                system ("touch spell.tmp");
                system ("$words > spell.tmp");
                system ("touch spell.bak");
                my $sed = "'s/\\(.\\)/\\1 /g;s/ \$//'";
                system ("sed $sed spell.tmp > spell.bak");
                $sed = "'s/\\./point/g'";
                system ("sed $sed spell.bak > spell.tmp");
                $sed = "'s/\\  / space /g'";
                system ("sed $sed spell.tmp > spell.bak");
                $sed = "':a;N;\$!ba;s/\\n/ new line /g'";
                system ("sed $sed spell.bak > spell.tmp");
                $sed = "'s/\\t/ tab /g'";
                system ("sed $sed spell.tmp > spell.bak");
                system ("cat spell.bak | espeak -p $random -s 80 2>/dev/null");
                system ("rm spell.tmp");
                system ("rm spell.bak");
        } elsif ($mode eq "command"){
                chomp($words);
                system("$words |espeak -p $random  -s 120 2>/dev/null");
        } elsif ($words ne "q\n" && $words ne "exit\n") {
                chomp($words);
                system("echo \"$words\" | espeak -p $random -s 120 2>/dev/null");
        } elsif ($mode ne "quiet" && $mode ne "-q" && $param eq "^]NULL^]") {
                system("echo \"Goodbye $user\" | espeak -s 120 2>/dev/null");
        }
        if ($param ne "^]NULL^]"){
                exit(0);
        }
}

#bashrc addition:
#alias calvin='/root/Documents/developement/espeak/calvin.pl'
#function alice {
#     espeak -ven-us+f4espeak -ven-us+f4espeak -ven-us+f2 -s100 -p 99 "$@" 2>/dev/null
#}
#function say {
#      /root/Documents/developement/espeak/calvin.pl -c cat /root/Documents/developement/espeak/preset/"$1"
#}
#preset files are NOT included, but I encourage you to write your own
