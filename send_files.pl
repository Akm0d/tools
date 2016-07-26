#!/usr/bin/perl

system ("cat ./unlock.sh");

# TODO Add command line options -files x x x x x x and -servers x.x.x.x x.x.x.x and -list and -help

print "\n\nWhich files would you like to send?";
print "\n-----------------------------------\n";

# Print file names in this directory
my @ls = `ls`;
my $i = 0;
for my $file_name (@ls){
	print "$i. $file_name";
	$i++;
}

# Choose which files to send
# TODO Loop until correct input is given
print "Enter numbers separated by spaces:\n";
my $response = <STDIN>;
if ($response !~ /^\s*(\d+\s+)+$/){
	print "Invalid Input!\n";
	exit;
}
my @files = split / /,$response;
for my $file(@files){
	chomp($file);
	if ($file >= $i){
		print "\"$file\" is not in the list!\n";
		exit;
	}
}

# Choose servers that will receive file
# TODO Loop until correct input is given
print "Enter the FQDNs or IP Adresses of servers that will receive these files, separated by spaces:\n";
$response = <STDIN>;
if ($response !~ /^\s*([a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+\s+)+$/){
	print "Invalid Input!\n";
	exit;
}
my @servers;
my @unpinged = split / /,$response;
for my $server (@unpinged){
	chomp($server);
	#my $ping = system("ping -qc 1 $server > /dev/null 2> /dev/null");
	if ($ping){
		print "$server was unreachable\n"
	} else {
		push @servers,"$server";
	}
}
if (!@servers){
	print "No servers were reachable\n";
	exit;
}

# Choose the location for saving the files
# TODO Loop until valid input is given
print "Save file to [~]:\n";
chomp(my $location = <STDIN>);
$location ||= "~";
if ($location =~ /\s/){
	print "Invalid file location";
}

# Choose username to use
print "Username [root]:\n";
chomp(my $user = <STDIN>);
$user ||= "root";
if ($user =~ /\s/){
	print "Invalid user";
}

# Send the files to servers
for my $server (@servers){
	chomp($server);
	for my $number (@files){
		chomp($file_name = @ls[$number]);
		print "scp $file_name $user\@$server:$location\n";
		`scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $file_name $user\@$server:$location`;
	}	
}
