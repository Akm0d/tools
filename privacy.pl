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
use Getopt::Long qw(:config ignore_case);
use Net::OpenSSH;#I want this to be optional
use Cwd;
use strict;
use warnings;

#Help Message
my $help_text =
"\nusage: po [options]\n
[options] are any of the following:
        -r,--remote             Allow discrete execution of commands on a remote host
        -a,--all                Hide ALL output
        -?,--help               Show this text\n";

#Handle command line options
my ( $remote,$all,$help ) = "";
GetOptions ( 'r|remote' => \$remote,
                         'a|all'        => \$all,
                         'help|?'       => \$help )
or die $help_text;

#Show help text
if ($help){
        print $help_text;
        exit (0);
}

#Require module to allow discrete remote command execution
#if($remote){
#       my $Open_SSH = `dpkg -l|grep -E '^ii' | grep libnet-openssh-perl`;
#       if (!$Open_SSH){
#          print "package \"libnet-openssh-perl\" must be installed\n";
#          exit (1);
#       } else {
#               require Net::OpenSSH;
#       }
#}

#Hide output and clear terminal
print ` stty -echo; clear`;

#Global variables
my $cmd = "hidden";
my $ssh_regex = "(.+\s+|\s*)ssh\s*.*";
my $aroba_regex = "(.+\s+|\s*)ssh\s*.+@.+";
my $ssh_en = "false";
my $user ||= getpwuid( $< );
my $host ||= ` hostname`;
my $password ||= "discrete";
my $pwd ||= cwd();
my $remote_pwd ||= "~/";

# No footprints in History
if ($all){#Hide ALL output
        while ($cmd ne "q\n"){
                if($remote && $ssh_en eq "false"){
                        if ($cmd =~ $ssh_regex){
                                if($cmd =~ $aroba_regex){
                                        my $temp = substr($cmd,0,index($cmd,'@'));
                                        $user = $temp =~ s/(.*)?\s//sr; 
                                        $host = substr($cmd,index($cmd,'@')+1);
                                } else {
                                        $user = getpwuid( $< );
                                        $host = $cmd =~ s/(.*ssh)?\s//sr;
                                }
                                chomp($host);
                #               print "$user\@$host\'s password:\n";
                                $password = <STDIN>;
                                my $login = Net::OpenSSH->new($host,
                                        master_opts => [-o => "StrictHostKeyChecking=no"],
                                        password => $password,
                                        user => "$user");
                                if ($login->error){
                                        $ssh_en = "false";
                                } else {
                                        $ssh_en = "true";
                                }
                                #Execute remote commands
                                if ($ssh_en eq "true"){
                                        my $remote_cmd = "discrete";
                                        while($remote_cmd ne "exit\n"){
                                                        print "successful";
                                                        $remote_cmd = <STDIN>;
                #                                       print "\n";
                                                        $login->capture(" $remote_cmd");
                                        }
                                }
                        }
                } else {
                        ` $cmd`;
                }
        }
} else {#Hide only typed output
        while ($cmd ne "q\n"){
                print "local: ";
                $cmd = <STDIN>;
                print "\n";
                if($remote && $ssh_en eq "false"){
                        if ($cmd =~ $ssh_regex){
                                if($cmd =~ $aroba_regex){
                                        my $temp = substr($cmd,0,index($cmd,'@'));
                                        $user = $temp =~ s/(.*)?\s//sr; 
                                        $host = substr($cmd,index($cmd,'@')+1);
                                } else {
                                        $user = getpwuid( $< );
                                        $host = $cmd =~ s/(.*ssh)?\s//sr;
                                }
                                chomp($host);
                                print "$user\@$host\'s password:\n";
                                $password = <STDIN>;
                                my $login = Net::OpenSSH->new($host,
                                        master_opts => [-o => "StrictHostKeyChecking=no"],
                                        password => $password,
                                        user => "$user");
                                if ($login->error){
                                        $ssh_en = "false";
                                } else {
                                        $ssh_en = "true";
                                }
                                #Execute remote commands
                                if ($ssh_en eq "true"){
                                        my $remote_cmd = "discrete";
                                        while($remote_cmd ne "exit\n"){
                                                        print "remote: ";
                                                        $remote_cmd = <STDIN>;
                                                        print "\n";
                                                        print $login->capture(" $remote_cmd");
                                        }
                                }
                        }
                } elsif($cmd eq "cd\n"){
                        chdir("/home/$user");
                } elsif($cmd =~ "^cd"){
                        my $dir = $cmd =~ s/(.*cd)?\s//sr;
                        chomp ($dir);
                        chdir ($dir);
                } else {
                        system (" $cmd");
                }
        }
}

#Reset terminal
` stty echo`;
print ` clear`;
